import pytest
import uuid

@pytest.mark.asyncio
async def test_double_entry_invariant(client):
    accounts = [
        "a0000000-0000-0000-0000-000000000001",
        "a0000000-0000-0000-0000-000000000002",
        "a0000000-0000-0000-0000-000000000003",
    ]
    pairs = [
        (accounts[0], accounts[1], 100),
        (accounts[1], accounts[2], 50),
        (accounts[0], accounts[2], 200),
        (accounts[2], accounts[0], 75),
        (accounts[1], accounts[0], 300),
    ]
    for sender, receiver, amount in pairs:
        res = await client.post("/api/v1/payments/", json={
            "sender_id": sender,
            "receiver_id": receiver,
            "amount": amount
        }, headers={"Idempotency-Key": str(uuid.uuid4())})
        assert res.status_code == 200

    integrity = (await client.get("/api/v1/ledger/integrity")).json()
    assert integrity['balanced'] is True
    assert float(integrity['delta']) == 0.0
    assert integrity['entry_count'] == len(pairs) * 2
