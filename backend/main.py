import asyncio
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from orm import create_tables
from database import engine
from routers import users, admins, auth, services


app = FastAPI()

app.include_router(users.router)
app.include_router(admins.router)
app.include_router(auth.router)
app.include_router(services.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    asyncio.run(create_tables(engine))
    uvicorn.run("main:app", reload=True)