from pydantic import BaseModel, field_validator
from decimal import Decimal
from datetime import datetime
from typing import Optional
from uuid import UUID

class TransferRequest(BaseModel):
    sender_id: UUID
    receiver_id: UUID
    amount: Decimal

    @field_validator('amount')
    @classmethod
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Amount must be greater than 0')
        return v

    @field_validator('receiver_id')
    @classmethod
    def sender_receiver_different(cls, v, info):
        if 'sender_id' in info.data and v == info.data['sender_id']:
            raise ValueError('Sender and receiver must be different accounts')
        return v

class TransferResponse(BaseModel):
    transfer_id: str
    status: str
    amount: Decimal
    sender_id: str
    receiver_id: str

class AccountResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: str
    owner_name: str
    balance: Decimal
    created_at: datetime

    @field_validator('id', mode='before')
    @classmethod
    def coerce_uuid(cls, v):
        return str(v)

class LedgerEntryResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: str
    account_id: str
    amount: Decimal
    entry_type: str
    transfer_id: str
    created_at: datetime

    @field_validator('id', 'account_id', 'transfer_id', mode='before')
    @classmethod
    def coerce_uuid(cls, v):
        return str(v)

class MetricsResponse(BaseModel):
    total_transfers: int
    total_volume: Decimal
    deduped_requests: int
    ledger_balanced: bool
    debit_sum: Decimal
    credit_sum: Decimal

class IntegrityResponse(BaseModel):
    balanced: bool
    debit_sum: Decimal
    credit_sum: Decimal
    delta: Decimal
    entry_count: int
