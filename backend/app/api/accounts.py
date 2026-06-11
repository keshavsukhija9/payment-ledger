from fastapi import APIRouter, HTTPException
from app.services.account_service import get_account, list_accounts, create_account
from app.models.schemas import AccountResponse
from pydantic import BaseModel

router = APIRouter(prefix="/accounts", tags=["accounts"])

class CreateAccountRequest(BaseModel):
    owner_name: str
    initial_balance: float = 0

@router.get("/", response_model=list[AccountResponse])
async def get_accounts():
    return await list_accounts()

@router.get("/{account_id}", response_model=AccountResponse)
async def get_account_by_id(account_id: str):
    account = await get_account(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@router.post("/", response_model=AccountResponse, status_code=201)
async def create_new_account(body: CreateAccountRequest):
    return await create_account(body.owner_name, body.initial_balance)
