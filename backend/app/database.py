import asyncpg
from contextlib import asynccontextmanager
from app.config import settings

_pool: asyncpg.Pool | None = None

async def create_pool():
    global _pool
    _pool = await asyncpg.create_pool(
        dsn=settings.database_url,
        min_size=settings.pool_min_size,
        max_size=settings.pool_max_size,
        command_timeout=30,
    )

async def close_pool():
    if _pool:
        await _pool.close()

@asynccontextmanager
async def get_connection():
    if _pool is None:
        raise RuntimeError("Pool not initialised. Was create_pool() called?")
    async with _pool.acquire() as conn:
        yield conn
