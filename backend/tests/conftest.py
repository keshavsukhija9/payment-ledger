import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
import app.database as db_module
import app.redis_client as redis_module

@pytest_asyncio.fixture
async def client():
    # Fresh pool and redis for every test
    await db_module.create_pool()
    redis_module._client = None

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as c:
        yield c

    # Cleanup DB state
    async with db_module.get_connection() as conn:
        await conn.execute("TRUNCATE ledger_entries, ledger_audit, idempotency_keys CASCADE")
        await conn.execute("""
            UPDATE accounts SET balance = CASE
                WHEN id = 'a0000000-0000-0000-0000-000000000001' THEN 50000
                WHEN id = 'a0000000-0000-0000-0000-000000000002' THEN 20000
                WHEN id = 'a0000000-0000-0000-0000-000000000003' THEN 15000
                WHEN id = 'a0000000-0000-0000-0000-000000000004' THEN 100000
                ELSE balance
            END
        """)

    # Teardown connections
    if redis_module._client:
        try:
            await redis_module._client.aclose()
        except Exception:
            pass
        redis_module._client = None
    await db_module.close_pool()
    db_module._pool = None
