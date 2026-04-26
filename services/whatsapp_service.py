import time
import random
import requests
from loguru import logger
from config import settings

def send_whatsapp_message(phone_number: str, message: str, is_business: bool = False, instance_id: str = None):
    """
    إرسال رسالة حقيقية أو محاكاة الإرسال لوضع العرض التقدمي (Presentation Mode)
    """
    if settings.WHATSAPP_MOCK_MODE:
        logger.warning(f"🚀 [PRESENTATION MODE] محاكاة إرسال رسالة إلى {phone_number}...")
        logger.info(f"نص الرسالة المحاكاة: {message}")
        time.sleep(1.5) # محاكاة وقت المعالجة لتبدو واقعية أمام اللجنة
        logger.success(f"✅ [MOCK SUCCESS] تم الإرسال بنجاح (المحاكاة نشطة)")
        return True

    # Use provided instance_id or fallback to default from settings
    target_instance = instance_id or settings.EVOLUTION_INSTANCE_ID
    
    if settings.WHATSAPP_PROVIDER.lower() == "meta":
        logger.info(f"إعداد السيرفر لإرسال رسالة واتساب إلى {phone_number} باستخدام Meta Cloud API")
        clean_phone = phone_number.replace("+", "").strip()
        url = f"https://graph.facebook.com/{settings.META_API_VERSION}/{settings.META_PHONE_NUMBER_ID}/messages"
        headers = {
            "Authorization": f"Bearer {settings.META_API_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": clean_phone,
            "type": "text",
            "text": {
                "body": message
            }
        }
    else:
        logger.info(f"إعداد السيرفر لإرسال رسالة واتساب إلى {phone_number} باستخدام النسخة {target_instance} (Evolution API)")
        
        # تنظيف رقم الهاتف ليتوافق مع مكتبات الواتساب
        clean_phone = phone_number.replace("+", "").strip()
        if "@" not in clean_phone:
            clean_phone = f"{clean_phone}@s.whatsapp.net"
        
        url = f"{settings.EVOLUTION_API_URL}/message/sendText/{target_instance}"
        headers = {
            "apikey": settings.EVOLUTION_API_TOKEN,
            "Content-Type": "application/json"
        }
        payload = {
            "number": clean_phone,
            "text": message
        }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=20)
        response.raise_for_status()
        logger.success(f"تم إرسال الرسالة بنجاح إلى الرقم {phone_number}!")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"فشل إرسال الرسالة إلى {phone_number}. الخطأ: {str(e)}")
        if e.response is not None:
            logger.error(f"تفاصيل الاستجابة من السيرفر: {e.response.text}")
        raise e

def generate_otp() -> str:
    """Generate a random 6-digit OTP code"""
    return str(random.randint(100000, 999999))
