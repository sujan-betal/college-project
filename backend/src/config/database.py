from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from dotenv import load_dotenv
import os

from src.config.base import Base

load_dotenv()

COLLEGE_DATABASE_URL = os.getenv("DATABASE_URL", "")

college_engine = create_async_engine(
    COLLEGE_DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,  # default
    max_overflow=5,  # default
    pool_timeout=30,
)

SessionLocal = async_sessionmaker(
    bind=college_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()