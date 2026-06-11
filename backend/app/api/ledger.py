from fastapi import APIRouter, Query
from app.database import get_connection
from app.models.schemas import LedgerEntryResponse, IntegrityResponse
from app.db import queries as q
from decimal import Decimal

router = APIRouter(prefix="/ledger", tags=["ledger"])

@router.get("/entries", response_model=list[LedgerEntryResponse])
async def get_ledger_entries(
    limit: int = Query(default=50, le=200),
    offset: int = Query(default=0, ge=0)
):
    async with get_connection() as conn:
        rows = await conn.fetch(q.GET_LEDGER_ENTRIES, limit, offset)
    return [dict(r) for r in rows]

@router.get("/integrity", response_model=IntegrityResponse)
async def check_integrity():
    async with get_connection() as conn:
        rows = await conn.fetch(q.GET_LEDGER_INTEGRITY)
        count = await conn.fetchval("SELECT COUNT(*) FROM ledger_entries")

    debit_sum  = next((r['total_amount'] for r in rows if r['entry_type'] == 'DEBIT'),  Decimal('0'))
    credit_sum = next((r['total_amount'] for r in rows if r['entry_type'] == 'CREDIT'), Decimal('0'))
    delta = abs(debit_sum - credit_sum)

    return {
        "balanced": delta < Decimal('0.01'),
        "debit_sum": debit_sum,
        "credit_sum": credit_sum,
        "delta": delta,
        "entry_count": count or 0
    }
