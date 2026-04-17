from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from database import get_db
from services.whatsapp_service import send_whatsapp_message
from security import get_api_key
import models, schemas
import urllib.parse
from loguru import logger

router = APIRouter()
print("DEBUG: Marketplace Router Loaded", flush=True)

@router.get("/providers", response_model=list[schemas.ProviderResponse])
def list_providers(db: Session = Depends(get_db)):
    """جلب قائمة المزودين من قاعدة البيانات abc"""
    try:
        from sqlalchemy import text
        
        # 🟢 التشخيص الجوهري
        print("--- DATABASE DIAGNOSTICS ---", flush=True)
        db_name = db.execute(text("SELECT DATABASE()")).scalar()
        db_version = db.execute(text("SELECT VERSION()")).scalar()
        tables = db.execute(text("SHOW TABLES")).fetchall()
        
        print(f"DEBUG: Connected to DB [{db_name}] | Version: {db_version}", flush=True)
        print(f"DEBUG: Tables found: {[t[0] for t in tables]}", flush=True)

        count = db.execute(text("SELECT COUNT(*) FROM provider")).scalar()
        print(f"DEBUG: RAW SQL COUNT in 'provider' = {count}", flush=True)

        providers = db.query(models.Provider).all()
        print(f"DEBUG: SQLAlchemy found {len(providers)} providers.", flush=True)
        return providers
    except Exception as e:
        print(f"DEBUG ERROR: {e}", flush=True)
        return []

@router.post("/providers", response_model=schemas.ProviderResponse, dependencies=[Depends(get_api_key)])
def create_provider(provider: schemas.ProviderCreate, db: Session = Depends(get_db)):
    """إضافة عامل جديد لقاعدة البيانات (Admin Only)"""
    logger.info(f"Admin: Adding new provider {provider.full_name}")
    new_worker = models.Provider(**provider.model_dump())
    db.add(new_worker)
    db.commit()
    db.refresh(new_worker)
    return new_worker

@router.put("/providers/{provider_id}", response_model=schemas.ProviderResponse, dependencies=[Depends(get_api_key)])
def update_provider(provider_id: int, provider_data: schemas.ProviderCreate, db: Session = Depends(get_db)):
    """تعديل بيانات عامل موجود (Admin Only)"""
    logger.info(f"Admin: Updating provider {provider_id}")
    db_worker = db.query(models.Provider).filter(models.Provider.id == provider_id).first()
    if not db_worker:
        raise HTTPException(status_code=404, detail="العامل غير موجود")
    
    for key, value in provider_data.model_dump().items():
        setattr(db_worker, key, value)
    
    db.commit()
    db.refresh(db_worker)
    return db_worker

@router.delete("/providers/{provider_id}", dependencies=[Depends(get_api_key)])
def delete_provider(provider_id: int, db: Session = Depends(get_db)):
    """حذف عامل نهائياً من قاعدة البيانات (Admin Only)"""
    logger.info(f"Admin: Deleting provider {provider_id}")
    db_worker = db.query(models.Provider).filter(models.Provider.id == provider_id).first()
    if not db_worker:
        raise HTTPException(status_code=404, detail="العامل غير موجود")
    
    db.delete(db_worker)
    db.commit()
    return {"success": True, "message": "تم حذف العامل بنجاح"}

@router.post("/send-to-provider")
def send_to_provider(request: schemas.MarketplaceRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """تجهيز رابط واتساب وتسجيل موعد، مع خيار الإرسال المباشر آلياً"""
    provider = db.query(models.Provider).filter(models.Provider.id == request.provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="المزود غير موجود في قاعدة البيانات")

    # إنشاء رسالة الواتساب
    msg = f"مرحباً {provider.full_name}، أنا الزبون {request.customer_name} أطلب خدمتك كـ {provider.job}."
    
    if request.appointment_datetime:
        msg += f"\n📅 الموعد المقترح: {request.appointment_datetime}"
        # تسجيل الموعد في جدول appointments
        try:
            new_appt = models.Appointment(
                provider_id=provider.id,
                customer_name=request.customer_name,
                appointment_datetime=request.appointment_datetime,
                status="pending"
            )
            db.add(new_appt)
            db.commit()
        except Exception as e:
            print(f"Failed to log appointment: {e}")

    if request.latitude and request.longitude:
        msg += f"\n📍 موقعي الجغرافي: https://maps.google.com/?q={request.latitude},{request.longitude}"

    encoded_msg = urllib.parse.quote(msg)
    whatsapp_url = f"https://wa.me/{provider.phone}?text={encoded_msg}"
    
    # خيار الإرسال الآلي من السيرفر
    if request.auto_send:
        # التحقق إذا كان الرقم هو حساب أعمال (Business) من جدول الحسابات
        is_business = False
        db_account = db.query(models.AccountDB).filter(models.AccountDB.phone_number == provider.phone).first()
        if db_account:
            is_business = db_account.is_business_whatsapp
        
        # وضع أمر الإرسال في الخلفية
        background_tasks.add_task(send_whatsapp_message, provider.phone, msg, is_business)
        return {"status": "sent", "message": "تم إرسال الطلب آلياً إلى المزود بنجاح.", "redirect": whatsapp_url}
    
    return {"status": "processing", "redirect": whatsapp_url}
