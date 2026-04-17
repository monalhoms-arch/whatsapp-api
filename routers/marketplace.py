from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
import urllib.parse

router = APIRouter()

@router.get("/providers", response_model=list[schemas.ProviderResponse])
def list_providers(db: Session = Depends(get_db)):
    """جلب قائمة المزودين من قاعدة البيانات abc"""
    providers = db.query(models.Provider).all()
    return providers

@router.post("/send-to-provider")
def send_to_provider(request: schemas.MarketplaceRequest, db: Session = Depends(get_db)):
    """تجهيز رابط واتساب وتسجيل موعد في قاعدة البيانات"""
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
    
    return {"status": "processing", "redirect": whatsapp_url}
