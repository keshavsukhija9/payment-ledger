import uuid
import json
from typing import Optional
from app.db.queries import INSERT_AUDIT

async def write_audit(
    conn,
    transfer_id: str,
    event_type: str,
    actor_id: Optional[str] = None,
    metadata: Optional[dict] = None
):
    await conn.execute(
        INSERT_AUDIT,
        uuid.UUID(transfer_id) if transfer_id else None,
        event_type,
        uuid.UUID(actor_id) if actor_id else None,
        json.dumps(metadata) if metadata else None
    )

async def write_audit_simple(idem_key: str, event_type: str):
    from app.database import get_connection
    async with get_connection() as conn:
        await conn.execute(
            INSERT_AUDIT,
            None,
            event_type,
            None,
            json.dumps({"idempotency_key": idem_key})
        )
