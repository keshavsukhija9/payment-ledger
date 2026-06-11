import uuid
from app.database import get_connection
from app.db import queries

async def get_account(account_id: str) -> dict | None:
    async with get_connection() as conn:
        row = await conn.fetchrow(queries.GET_ACCOUNT, uuid.UUID(account_id))
        return dict(row) if row else None

async def list_accounts() -> list[dict]:
    async with get_connection() as conn:
        rows = await conn.fetch(queries.LIST_ACCOUNTS)
        return [dict(r) for r in rows]

async def create_account(owner_name: str, initial_balance: float = 0) -> dict:
    async with get_connection() as conn:
        row = await conn.fetchrow(
            "INSERT INTO accounts (owner_name, balance) VALUES ($1, $2) RETURNING *",
            owner_name, initial_balance
        )
        return dict(row)
