CREATE TABLE ledger_audit (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transfer_id  UUID,
    event_type   TEXT NOT NULL,
    actor_id     UUID,
    metadata     JSONB,
    created_at   TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_audit_transfer_id ON ledger_audit(transfer_id);
CREATE INDEX idx_audit_event_type  ON ledger_audit(event_type);
CREATE INDEX idx_audit_created_at  ON ledger_audit(created_at DESC);
