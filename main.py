from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import otp, notifications, accounts, marketplace, automation

# Create database tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="WhatsApp Microservice API",
    description="خدمة مستقلة للتعامل مع الواتساب، وإرسال الـ OTP والإشعارات لنظام التأجير.",
    version="1.0.0"
)

# تفعيل سياسة CORS للسماح للوحة التحكم بالاتصال بالسيرفر
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# تضمين مسارات التطبيق
app.include_router(otp.router, prefix="/api/v1/otp", tags=["Security & OTP"])
app.include_router(notifications.router, prefix="/api/v1/notifications", tags=["Notifications"])
app.include_router(accounts.router, prefix="/api/v1/accounts", tags=["Account Management"])
app.include_router(marketplace.router, prefix="/api/v1/marketplace", tags=["Marketplace"])
app.include_router(automation.router, prefix="/api/v1/automation", tags=["Automation"])

@app.get("/")
def root():
    return {"message": "خدمة الواتساب تعمل بنجاح (موصولة بقاعدة بيانات PostgreSQL المركزة)"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
