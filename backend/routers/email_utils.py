from email.mime.text import MIMEText
import smtplib
from routers.email_config import settings


async def send_password_reset_email(email_to: str, token: str):
    subject = "Восстановление пароля"
    reset_link = f"https://yourdomain.com/reset-password?token={token}"
    message = f"""
    <html>
        <body>
            <p>Вы запросили восстановление пароля.</p>
            <p>Для установки нового пароля перейдите по ссылке:</p>
            <p><a href="{reset_link}">{reset_link}</a></p>
            <p>Если вы не запрашивали восстановление, проигнорируйте это письмо.</p>
        </body>
    </html>
    """
    
    msg = MIMEText(message, "html")
    msg["Subject"] = subject
    msg["From"] = settings.EMAIL_FROM
    msg["To"] = email_to
    
    with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.send_message(msg)