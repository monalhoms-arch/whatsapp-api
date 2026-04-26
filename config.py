from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # ───────── App API Security ─────────
    API_SECRET_KEY: str = "change_me_in_env"

    # ───────── Database ─────────
    # يجب تعريف DATABASE_URL في ملف .env
    DATABASE_URL: str = "sqlite:///./whatsapp_fallback.db"

    # ───────── Redis ─────────
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None

    # ───────── Security Rules ─────────
    OTP_EXPIRATION_MINUTES: int = 5
    MAX_FAILED_ATTEMPTS: int = 3
    BLOCK_DURATION_MINUTES: int = 15

    # ───────── WhatsApp Provider Config ─────────
    # Options: 'evolution' or 'meta'
    WHATSAPP_PROVIDER: str = "evolution"

    # ───────── WhatsApp Evolution API ─────────
    EVOLUTION_API_URL: str = "http://127.0.0.1:8080"
    EVOLUTION_API_TOKEN: str = "change_me_in_env"
    EVOLUTION_INSTANCE_NAME: str = "default"
    EVOLUTION_INSTANCE_ID: str = "default"

    # ───────── WhatsApp Meta Cloud API ─────────
    META_API_TOKEN: str = "change_me_in_env"
    META_PHONE_NUMBER_ID: str = "change_me_in_env"
    META_API_VERSION: str = "v19.0"

    # ───────── Presentation Mode ─────────
    # True  = محاكاة ناجحة للعرض (لا ترسل رسائل حقيقية)
    # False = إرسال حقيقي
    WHATSAPP_MOCK_MODE: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()

