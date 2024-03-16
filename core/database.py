from sqlalchemy.ext.asyncio import create_async_engine,AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker

from core.configs import settings

engine: AsyncEngine = create_async_engine(settings.DB_URL)

Session: AsyncSession = sessionmaker (
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=AsyncEngine,
    bind=engine
)