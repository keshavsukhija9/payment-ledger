import json
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from app.redis_client import get_redis
from app.config import settings
from app.utils.audit import write_audit_simple

LOCK_TTL = 30
CACHE_TTL = settings.idempotency_ttl

class IdempotencyMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        if request.method != "POST":
            return await call_next(request)

        if not request.url.path.endswith("/payments/") and \
           not request.url.path.endswith("/payments"):
            return await call_next(request)

        key = request.headers.get("Idempotency-Key")
        if not key:
            return JSONResponse(
                status_code=400,
                content={"error": "Idempotency-Key header is required for payment requests"}
            )

        redis = await get_redis()
        cache_key = f"idem:response:{key}"
        lock_key  = f"idem:lock:{key}"

        acquired = await redis.set(lock_key, "1", nx=True, ex=LOCK_TTL)
        if not acquired:
            return JSONResponse(
                status_code=409,
                content={"error": "A request with this Idempotency-Key is already being processed"}
            )

        try:
            cached = await redis.get(cache_key)
            if cached:
                await write_audit_simple(key, 'DEDUP_BLOCKED')
                await redis.incr("metrics:deduped_count")
                return Response(
                    content=cached,
                    status_code=200,
                    media_type="application/json"
                )

            body = await request.body()

            async def receive():
                return {"type": "http.request", "body": body, "more_body": False}

            request._receive = receive

            response = await call_next(request)

            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk

            if response.status_code == 200:
                await redis.setex(cache_key, CACHE_TTL, response_body)

            return Response(
                content=response_body,
                status_code=response.status_code,
                media_type="application/json",
                headers=dict(response.headers)
            )

        finally:
            await redis.delete(lock_key)
