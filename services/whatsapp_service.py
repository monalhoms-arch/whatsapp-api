import random
import requests
from loguru import logger
from config import settings

def send_whatsapp_message(phone_number: str, message: str, is_business: bool = False):
    """
    إرسال رسالة حقيقية عبر Evolution API مع استخدام Loguru لتسجيل الأحداث
    """
    logger.info(f"إعداد السيرفر لإرسال رسالة واتساب إلى {phone_number} (حساب أعمال: {is_business})")
    
    # تنظيف رقم الهاتف (حذف علامة الزائد) ليتوافق مع مكتبات الواتساب
    clean_phone = phone_number.replace("+", "").strip()
    
    url = f"{settings.EVOLUTION_API_URL}/message/sendText/{settings.EVOLUTION_INSTANCE_NAME}"
    headers = {
        "apikey": settings.EVOLUTION_API_TOKEN,
        "Content-Type": "application/json"
    }
    
    payload = {
        "number": clean_phone,
        "options": {
            "delay": 1200,              # محاكاة الكتابة لثانية ليظهر بشكل بشري
            "presence": "composing" 
        },
        "textMessage": {"text": message}
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        logger.success(f"تم إرسال الرسالة بنجاح إلى الرقم {phone_number}!")
    except requests.exceptions.RequestException as e:
        logger.error(f"فشل إرسال الرسالة إلى {phone_number}. الخطأ: {str(e)}")
        if e.response is not None:
            logger.error(f"تفاصيل الاستجابة من السيرفر: {e.response.text}")

def generate_otp() -> str:
    """Generate a random 6-digit OTP code"""
    return str(random.randint(100000, 999999))
