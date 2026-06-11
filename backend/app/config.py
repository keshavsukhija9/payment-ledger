from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://ledger_user:ledger_pass@localhost:5432/ledger"
    redis_url: str = "redis://localhost:6379"
    pool_min_size: int = 5
    pool_max_size: int = 20
    idempotency_ttl: int = 86400
    debug: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
