from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App API Security
    API_SECRET_KEY: str = "my_super_secret_key_123"

    # Database (MySQL for abc.sql)
    DATABASE_URL: str = "mysql+pymysql://root@127.0.0.1:3306/abc"
    
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
    EVOLUTION_API_TOKEN: str = "global_token_from_evolution"
    EVOLUTION_INSTANCE_NAME: str = "main_instance"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
