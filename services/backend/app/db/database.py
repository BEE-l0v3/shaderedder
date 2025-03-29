from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

URL_DATABASE = (settings.SQLALCHEMY_DATABASE_URI.unicode_string())

engine = create_async_engine(
    url=URL_DATABASE,
    echo=True
)

session_factory = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def close_db():
    await engine.dispose()
