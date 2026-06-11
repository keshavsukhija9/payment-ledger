import uuid
from decimal import Decimal
from app.database import get_connection
from app.db import queries
from app.utils.audit import write_audit

async def transfer(
    sender_id: str,
    receiver_id: str,
    amount: Decimal,
    transfer_id: str
) -> dict:

    async with get_connection() as conn:
        async with conn.transaction():

            await write_audit(conn, transfer_id, 'TRANSFER_INITIATED', sender_id, {
                'amount': str(amount),
                'receiver_id': receiver_id
            })

            # Always lock in sorted UUID order to prevent deadlocks
            # If A->B and B->A happen concurrently without this,
            # both transactions wait on each other forever
            lock_order = sorted([sender_id, receiver_id])

            locked = {}
            for acc_id in lock_order:
                row = await conn.fetchrow(queries.GET_ACCOUNT_FOR_UPDATE, uuid.UUID(acc_id))
                if row is None:
                    raise ValueError(f"Account not found: {acc_id}")
                locked[acc_id] = row

            sender = locked[sender_id]

            if sender['balance'] < amount:
                await write_audit(conn, transfer_id, 'INSUFFICIENT_FUNDS', sender_id, {
                    'requested': str(amount),
                    'available': str(sender['balance'])
                })
                raise ValueError("Insufficient funds")

            await conn.execute(queries.DEBIT_ACCOUNT, amount, uuid.UUID(sender_id))
            await conn.execute(queries.CREDIT_ACCOUNT, amount, uuid.UUID(receiver_id))

            tid = uuid.UUID(transfer_id)
            await conn.execute(
                queries.INSERT_LEDGER_ENTRY,
                uuid.UUID(sender_id), amount, 'DEBIT', tid
            )
            await conn.execute(
                queries.INSERT_LEDGER_ENTRY,
                uuid.UUID(receiver_id), amount, 'CREDIT', tid
            )

            await write_audit(conn, transfer_id, 'TRANSFER_SUCCESS', sender_id, {
                'amount': str(amount)
            })

            return {
                'transfer_id': transfer_id,
                'status': 'success',
                'amount': amount,
                'sender_id': sender_id,
                'receiver_id': receiver_id
            }
