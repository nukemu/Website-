# FROM python:3.11-alpine
# WORKDIR /project-app

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .
# COPY .env .env

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# CMD ["python", "backend/main.py"]

FROM python:3.11-alpine
WORKDIR /app

# Установка зависимостей для postgres
RUN apk add --no-cache libpq

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект (кроме того, что в .dockerignore)
COPY . .

# Устанавливаем PYTHONPATH
ENV PYTHONPATH=/app

# Устанавливаем переменные окружения напрямую
ENV DB_URL=postgresql+asyncpg://db
ENV DB_PORT=5432
ENV DB_USER=postgres
ENV DB_PASS=password
ENV DB_NAME=mydatabase

WORKDIR /app/backend
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]