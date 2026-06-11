GET_ACCOUNT_FOR_UPDATE = """
    SELECT id, owner_name, balance
    FROM accounts
    WHERE id = $1
    FOR UPDATE NOWAIT
"""

GET_ACCOUNT = """
    SELECT id, owner_name, balance, created_at
    FROM accounts
    WHERE id = $1
"""

LIST_ACCOUNTS = """
    SELECT id, owner_name, balance, created_at
    FROM accounts
    ORDER BY owner_name
"""

DEBIT_ACCOUNT = """
    UPDATE accounts
    SET balance = balance - $1
    WHERE id = $2
"""

CREDIT_ACCOUNT = """
    UPDATE accounts
    SET balance = balance + $1
    WHERE id = $2
"""

INSERT_LEDGER_ENTRY = """
    INSERT INTO ledger_entries (account_id, amount, entry_type, transfer_id)
    VALUES ($1, $2, $3, $4)
    RETURNING id, created_at
"""

GET_LEDGER_ENTRIES = """
    SELECT le.id, le.account_id, a.owner_name, le.amount,
           le.entry_type, le.transfer_id, le.created_at
    FROM ledger_entries le
    JOIN accounts a ON a.id = le.account_id
    ORDER BY le.created_at DESC
    LIMIT $1 OFFSET $2
"""

GET_LEDGER_INTEGRITY = """
    SELECT
        entry_type,
        COUNT(*) as entry_count,
        COALESCE(SUM(amount), 0) as total_amount
    FROM ledger_entries
    GROUP BY entry_type
"""

COUNT_TRANSFERS = """
    SELECT COUNT(DISTINCT transfer_id) FROM ledger_entries
"""

INSERT_AUDIT = """
    INSERT INTO ledger_audit (transfer_id, event_type, actor_id, metadata)
    VALUES ($1, $2, $3, $4)
"""
