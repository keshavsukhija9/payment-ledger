import asyncio
import pytest
import pytest_asyncio
import asyncpg
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import create_pool, close_pool, get_connection

TEST_DB_URL = "postgresql://ledger_user:ledger_pass@localhost:5432/ledger"

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_db():
    await create_pool()
    yield
    await close_pool()

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as c:
        yield c

@pytest_asyncio.fixture(autouse=True)
async def clean_db():
    yield
    async with get_connection() as conn:
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
