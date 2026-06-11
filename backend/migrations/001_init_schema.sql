CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE accounts (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_name  TEXT NOT NULL,
    balance     NUMERIC(20, 2) NOT NULL DEFAULT 0,
    created_at  TIMESTAMPTZ DEFAULT now(),
    CONSTRAINT  balance_non_negative CHECK (balance >= 0)
);

CREATE TABLE ledger_entries (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id  UUID NOT NULL REFERENCES accounts(id),
    amount      NUMERIC(20, 2) NOT NULL CHECK (amount > 0),
    entry_type  TEXT NOT NULL CHECK (entry_type IN ('DEBIT', 'CREDIT')),
    transfer_id UUID NOT NULL,
    created_at  TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_ledger_transfer_id ON ledger_entries(transfer_id);
CREATE INDEX idx_ledger_account_id  ON ledger_entries(account_id);
CREATE INDEX idx_ledger_created_at  ON ledger_entries(created_at DESC);

CREATE TABLE idempotency_keys (
    key         TEXT PRIMARY KEY,
    response    JSONB NOT NULL,
    status_code INT NOT NULL DEFAULT 200,
    created_at  TIMESTAMPTZ DEFAULT now()
);
