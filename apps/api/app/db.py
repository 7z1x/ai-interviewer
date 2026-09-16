from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings
from app.models import Base  # noqa: F401 — ensure models imported for metadata

# NullPool avoids asyncpg "attached to different loop" when TestClient creates new loops
engine = create_async_engine(
    settings.database_url,
    echo=False,
    future=True,
    poolclass=pool.NullPool,
)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
