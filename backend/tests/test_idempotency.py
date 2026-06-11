import pytest
import uuid

SENDER   = "a0000000-0000-0000-0000-000000000001"
RECEIVER = "a0000000-0000-0000-0000-000000000002"

@pytest.mark.asyncio
async def test_same_key_sequential_deduplicated(client):
    idem_key = str(uuid.uuid4())
    payload = {"sender_id": SENDER, "receiver_id": RECEIVER, "amount": 100}
    headers = {"Idempotency-Key": idem_key}

    r1 = await client.post("/api/v1/payments/", json=payload, headers=headers)
    r2 = await client.post("/api/v1/payments/", json=payload, headers=headers)

    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r1.json()['transfer_id'] == r2.json()['transfer_id']

    entries = (await client.get("/api/v1/ledger/entries")).json()
    assert len(entries) == 2

@pytest.mark.asyncio
async def test_missing_key_rejected(client):
    res = await client.post("/api/v1/payments/", json={
        "sender_id": SENDER, "receiver_id": RECEIVER, "amount": 100
    })
    assert res.status_code == 400
    assert "Idempotency-Key" in res.json()['error']
