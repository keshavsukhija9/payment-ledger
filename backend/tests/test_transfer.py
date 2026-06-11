import pytest
import uuid

SENDER   = "a0000000-0000-0000-0000-000000000001"
RECEIVER = "a0000000-0000-0000-0000-000000000002"

async def make_transfer(client, sender, receiver, amount, idem_key=None):
    return await client.post("/api/v1/payments/", json={
        "sender_id": sender,
        "receiver_id": receiver,
        "amount": amount
    }, headers={"Idempotency-Key": idem_key or str(uuid.uuid4())})

@pytest.mark.asyncio
async def test_happy_path(client):
    res = await make_transfer(client, SENDER, RECEIVER, 1000)
    assert res.status_code == 200
    data = res.json()
    assert data['status'] == 'success'
    assert float(data['amount']) == 1000

@pytest.mark.asyncio
async def test_insufficient_funds(client):
    res = await make_transfer(client, SENDER, RECEIVER, 999999)
    assert res.status_code == 422
    assert "Insufficient funds" in res.json()['detail']

@pytest.mark.asyncio
async def test_same_account_rejected(client):
    res = await make_transfer(client, SENDER, SENDER, 100)
    assert res.status_code == 422

@pytest.mark.asyncio
async def test_account_not_found(client):
    fake_id = str(uuid.uuid4())
    res = await make_transfer(client, fake_id, RECEIVER, 100)
    assert res.status_code == 422

@pytest.mark.asyncio
async def test_ledger_entries_created(client):
    await make_transfer(client, SENDER, RECEIVER, 500)
    res = await client.get("/api/v1/ledger/entries")
    entries = res.json()
    assert len(entries) == 2
    types = {e['entry_type'] for e in entries}
    assert types == {'DEBIT', 'CREDIT'}
    amounts = {float(e['amount']) for e in entries}
    assert amounts == {500.0}
