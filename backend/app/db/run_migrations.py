import asyncio
import asyncpg
import os
from pathlib import Path

MIGRATIONS_DIR = Path(__file__).parent.parent.parent / "migrations"

async def run():
    db_url = os.getenv(
        "DATABASE_URL",
        "postgresql://ledger_user:ledger_pass@localhost:5432/ledger"
    )
    conn = await asyncpg.connect(dsn=db_url)
    try:
        for migration_file in sorted(MIGRATIONS_DIR.glob("*.sql")):
            print(f"Running {migration_file.name}...")
            sql = migration_file.read_text()
            await conn.execute(sql)
            print(f"Done: {migration_file.name}")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(run())
