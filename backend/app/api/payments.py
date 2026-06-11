import uuid
from fastapi import APIRouter, HTTPException, Request
from app.services.payment_service import transfer
from app.models.schemas import TransferRequest, TransferResponse, MetricsResponse
from app.database import get_connection
from app.redis_client import get_redis
from app.db import queries as q

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/", response_model=TransferResponse)
async def create_transfer(body: TransferRequest, request: Request):
    transfer_id = str(uuid.uuid4())
    try:
        result = await transfer(
            sender_id=str(body.sender_id),
            receiver_id=str(body.receiver_id),
            amount=body.amount,
            transfer_id=transfer_id
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        if "LockNotAvailable" in type(e).__name__:
            raise HTTPException(
                status_code=503,
                detail="Account temporarily locked, retry shortly",
                headers={"Retry-After": "1"}
            )
        raise HTTPException(status_code=500, detail="Internal error")

@router.get("/metrics", response_model=MetricsResponse)
async def get_metrics():
    async with get_connection() as conn:
        total = await conn.fetchval(q.COUNT_TRANSFERS)
        rows = await conn.fetch(q.GET_LEDGER_INTEGRITY)

    debit_sum  = next((r['total_amount'] for r in rows if r['entry_type'] == 'DEBIT'),  0)
    credit_sum = next((r['total_amount'] for r in rows if r['entry_type'] == 'CREDIT'), 0)
    balanced = abs(float(debit_sum) - float(credit_sum)) < 0.01

    redis = await get_redis()
    deduped = await redis.get("metrics:deduped_count")

    return {
        "total_transfers": total or 0,
        "total_volume": debit_sum,
        "deduped_requests": int(deduped or 0),
        "ledger_balanced": balanced,
        "debit_sum": debit_sum,
        "credit_sum": credit_sum
    }
