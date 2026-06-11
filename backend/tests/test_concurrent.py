import pytest
import asyncio
import uuid

HOTSPOT  = "a0000000-0000-0000-0000-000000000004"
RECEIVER = "a0000000-0000-0000-0000-000000000002"

@pytest.mark.asyncio
async def test_concurrent_transfers_no_corruption(client):
    async def one_transfer():
        return await client.post("/api/v1/payments/", json={
            "sender_id": HOTSPOT,
            "receiver_id": RECEIVER,
            "amount": 1
        }, headers={"Idempotency-Key": str(uuid.uuid4())})

    responses = await asyncio.gather(*[one_transfer() for _ in range(50)])

    assert all(r.status_code in (200, 503) for r in responses)
    assert sum(1 for r in responses if r.status_code == 200) > 0

    integrity = (await client.get("/api/v1/ledger/integrity")).json()
    assert integrity['balanced'] is True

    from app.services.account_service import get_account
    account = await get_account(HOTSPOT)
    assert account['balance'] >= 0
