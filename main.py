from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from database import engine, Base
from routers import otp, notifications, accounts, marketplace, automation


# ── بدء التطبيق وإيقافه بشكل آمن ────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ─── عند الإقلاع ───
    logger.info("🚀 بدء تشغيل خدمة الواتساب...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.success("✅ جداول قاعدة البيانات جاهزة.")
    except Exception as e:
        logger.error(f"❌ فشل إنشاء الجداول: {e}")
    yield
    # ─── عند الإيقاف ───
    logger.info("🛑 إيقاف خدمة الواتساب.")


app = FastAPI(
    title="WhatsApp Microservice API — منصة خدمتي",
    description="خدمة OTP والإشعارات عبر الواتساب لنظام إدارة العمال.",
    version="2.0.0",
    lifespan=lifespan,
)

# ── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(otp.router,          prefix="/api/v1/otp",          tags=["Security & OTP"])
app.include_router(notifications.router,prefix="/api/v1/notifications", tags=["Notifications"])
app.include_router(accounts.router,     prefix="/api/v1/accounts",      tags=["Account Management"])
app.include_router(marketplace.router,  prefix="/api/v1/marketplace",   tags=["Marketplace"])
app.include_router(automation.router,   prefix="/api/v1/automation",    tags=["Automation"])

# ── Endpoints الأساسية ────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {"status": "online", "service": "whatsapp-microservice", "version": "2.0.0"}

@app.get("/api/v1/health", tags=["Health"])
def health_check():
    from redis_client import redis_client
    from config import settings
    redis_ok = redis_client.ping() if hasattr(redis_client, 'ping') else False
    return {
        "status": "online",
        "service": "whatsapp",
        "redis": "connected" if redis_ok else "unavailable (fallback active)",
        "mock_mode": settings.WHATSAPP_MOCK_MODE,
        "evolution_api": settings.EVOLUTION_API_URL,
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
