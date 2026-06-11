from fastapi import APIRouter
from app.api import payments, accounts, ledger

router = APIRouter(prefix="/api/v1")
router.include_router(payments.router)
router.include_router(accounts.router)
router.include_router(ledger.router)
