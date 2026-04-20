from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App API Security
    API_SECRET_KEY: str = "my_super_secret_key_123"

# Database (PostgreSQL - matches docker-compose)
    DATABASE_URL: str = "postgresql+psycopg2://postgres:598624713@localhost:5432/whatsapp_data"
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    
    # Security Rules
    OTP_EXPIRATION_MINUTES: int = 5
    MAX_FAILED_ATTEMPTS: int = 3
    BLOCK_DURATION_MINUTES: int = 15

    # WhatsApp Evolution API Integration
    EVOLUTION_API_URL: str = "http://localhost:8080"
    EVOLUTION_API_TOKEN: str = "56A5801CBC7B-404D-9D1A-9E9823778D3B"
    EVOLUTION_INSTANCE_NAME: str = "moha"
    EVOLUTION_INSTANCE_ID: str = "moha"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
