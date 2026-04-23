from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from loguru import logger
from config import settings

Base = declarative_base()

# ── اتصال قاعدة البيانات ──────────────────────────────────────────────────────
def _build_engine(url: str):
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    return create_engine(url, connect_args=connect_args, pool_pre_ping=True)

try:
    engine = _build_engine(settings.DATABASE_URL)
    # اختبار الاتصال الفعلي
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    logger.success(f"✅ قاعدة البيانات متصلة: {settings.DATABASE_URL.split('@')[-1]}")
except Exception as e:
    _fallback_url = "sqlite:///./whatsapp_fallback.db"
    logger.warning(
        f"⚠️  فشل الاتصال بقاعدة البيانات الرئيسية: {e}\n"
        f"    ← التحويل تلقائياً إلى SQLite المحلية: {_fallback_url}"
    )
    engine = _build_engine(_fallback_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
