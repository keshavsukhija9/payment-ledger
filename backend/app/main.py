from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import create_pool, close_pool
from app.redis_client import close_redis
from app.middleware.idempotency import IdempotencyMiddleware
from app.api.router import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_pool()
    yield
    await close_pool()
    await close_redis()

app = FastAPI(
    title="Payment Ledger API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(IdempotencyMiddleware)

app.include_router(router)
