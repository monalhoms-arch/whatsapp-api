from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import otp, notifications, accounts

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
    allow_methods=["*"],
    allow_headers=["*"],
)

# تضمين مسارات التطبيق
app.include_router(otp.router, prefix="/api/v1/otp", tags=["Security & OTP"])
app.include_router(notifications.router, prefix="/api/v1/notifications", tags=["Notifications"])
app.include_router(accounts.router, prefix="/api/v1/accounts", tags=["Account Management"])

@app.get("/")
def root():
    return {"message": "خدمة الواتساب الخارجية تعمل بنجاح (موصولة بقاعدة بيانات تجريبية)"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
