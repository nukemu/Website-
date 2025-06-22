import asyncio
import uvicorn


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import delete
from datetime import datetime
from contextlib import asynccontextmanager

from orm import create_tables
from database import engine, session_factory
from routers import users, admins, auth, services
from models import ResetTokenOrm


scheduler = AsyncIOScheduler()


async def cleanup_expired_tokens():
    async with session_factory() as session:
        try:
            await session.execute(
                delete(ResetTokenOrm)
                .where(
                    (ResetTokenOrm.expires_at < datetime.now()) | 
                    (ResetTokenOrm.used == True)
                )
            )
            await session.commit()
            print("Expired and used tokens removed")
            
        except Exception as e:
            print(f"Except error on tokens removed: {e}")
            await session.rollback()


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()
    

scheduler.add_job(
    cleanup_expired_tokens,
    'interval',
    hours=1,
    next_run_time=datetime.now()
)


app = FastAPI(lifespan=lifespan)


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