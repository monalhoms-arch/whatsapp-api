from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from loguru import logger
from schemas import OTPRequest, OTPVerify, OTPResponse
from services.whatsapp_service import send_whatsapp_message, generate_otp
from database import get_db
from redis_client import redis_client
from config import settings
from security import get_api_key
import models

router = APIRouter(dependencies=[Depends(get_api_key)])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/send", response_model=OTPResponse)
def send_otp(request: OTPRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    phone = request.phone_number
    logger.info(f"OTP System: Request to generate OTP for {phone}")
    
    block_key = f"block:{phone}"
    if redis_client.exists(block_key):
        ttl = redis_client.ttl(block_key)
        logger.warning(f"OTP Blocked: {phone} is currently blocked for {ttl // 60} minutes.")
        raise HTTPException(
            status_code=429, 
            detail=f"تم حظر الرقم مؤقتاً لتجاوز المحاولات. الرجاء المحاولة بعد {ttl // 60} دقيقة."
        )

    otp_key = f"otp:{phone}"
    plain_code = generate_otp()
    hashed_code = get_password_hash(plain_code)
    
    redis_client.setex(
        name=otp_key,
        time=settings.OTP_EXPIRATION_MINUTES * 60,
        value=hashed_code
    )
    
    attempts_key = f"attempts:{phone}"
    redis_client.delete(attempts_key)

    is_business = False
    db_account = db.query(models.AccountDB).filter(models.AccountDB.phone_number == phone).first()
    if db_account:
        is_business = db_account.is_business_whatsapp

    if request.account_type == "customer":
        msg = f"رمز التحقق الخاص بك لطلب العمال هو: {plain_code}\nلا تشاركه مع أحد. صالح لمدة {settings.OTP_EXPIRATION_MINUTES} دقائق."
    elif request.account_type == "provider":
        msg = f"مقدم الخدمة العزيز، يرجى تأكيد العملية بالرمز: {plain_code}\nصالح لمدة {settings.OTP_EXPIRATION_MINUTES} دقائق."
    elif request.account_type == "admin":
        msg = f"تنبيه أمان (مدير): رمز التحقق للوصول للنظام: {plain_code}\nصالح لـ {settings.OTP_EXPIRATION_MINUTES} دقائق."
    else:
        msg = f"رمز التحقق (OTP) الخاص بك: {plain_code}"

    background_tasks.add_task(send_whatsapp_message, phone, msg, is_business)
    logger.info(f"OTP generated successfully for {phone} and queued for background dispatch.")

    return OTPResponse(success=True, message=f"تم وضع أمر الإرسال في الخلفية بنجاح.")

@router.post("/verify", response_model=OTPResponse)
def verify_otp(request: OTPVerify):
    phone = request.phone_number
    logger.info(f"OTP System: Attempting verification for {phone}")
    block_key = f"block:{phone}"
    
    if redis_client.exists(block_key):
        logger.warning(f"OTP Verification Failed: {phone} is blocked.")
        raise HTTPException(status_code=429, detail="الحساب محظور مؤقتاً لتجاوز المحاولات المسموحة.")
        
    otp_key = f"otp:{phone}"
    hashed_otp = redis_client.get(otp_key)
    
    if not hashed_otp:
        logger.warning(f"OTP Verification Failed: No active OTP for {phone}.")
        raise HTTPException(status_code=400, detail="لا يوجد رمز فعّال لهذا الرقم أو انتهت صلاحيته.")
        
    is_valid = verify_password(request.code, hashed_otp)
    
    if is_valid:
        redis_client.delete(otp_key)
        redis_client.delete(f"attempts:{phone}")
        logger.success(f"OTP verified successfully for {phone}.")
        return OTPResponse(success=True, message="تم التحقق من الكود بنجاح")
    else:
        attempts_key = f"attempts:{phone}"
        current_attempts = redis_client.incr(attempts_key)
        
        if current_attempts >= settings.MAX_FAILED_ATTEMPTS:
            redis_client.setex(
                name=block_key,
                time=settings.BLOCK_DURATION_MINUTES * 60,
                value="blocked"
            )
            redis_client.delete(otp_key)
            redis_client.delete(attempts_key)
            logger.error(f"OTP Verification Failed: Max attempts exceeded for {phone}. Account blocked.")
            raise HTTPException(
                status_code=429, 
                detail=f"تم تجاوز الحد المسموح {settings.MAX_FAILED_ATTEMPTS} مرات. الحساب محظور لمدة {settings.BLOCK_DURATION_MINUTES} دقيقة."
            )
            
        remaining = settings.MAX_FAILED_ATTEMPTS - current_attempts
        logger.warning(f"OTP Verification Failed: Incorrect code for {phone}. Remaining attempts: {remaining}")
        raise HTTPException(status_code=400, detail=f"الرمز غير صحيح، يتبقى لك {remaining} محاولات.")
