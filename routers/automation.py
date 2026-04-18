from fastapi import APIRouter, HTTPException, Depends
import requests
from config import settings
from security import get_api_key
from loguru import logger

router = APIRouter(dependencies=[Depends(get_api_key)])

@router.get("/status")
def get_automation_status():
    """التحقق من حالة الاتصال بسيرفر Evolution API"""
    url = f"{settings.EVOLUTION_API_URL}/instance/connectionState/{settings.EVOLUTION_INSTANCE_ID}"
    headers = {"apikey": settings.EVOLUTION_API_TOKEN}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        return {
            "status": "online",
            "evolution_api": "connected",
            "instance": settings.EVOLUTION_INSTANCE_NAME,
            "details": data.get("instance", {})
        }
    except Exception as e:
        logger.error(f"Automation Status Error: {e}")
        return {
            "status": "offline",
            "evolution_api": "disconnected",
            "instance": settings.EVOLUTION_INSTANCE_NAME,
            "error": str(e)
        }

@router.post("/test-message")
def test_automated_message(phone: str, message: str):
    """إرسال رسالة اختبار سريعة للتحقق من الأتمتة"""
    from services.whatsapp_service import send_whatsapp_message
    try:
        # We don't use background tasks here for the test to give immediate feedback
        send_whatsapp_message(phone, message)
        return {"success": True, "message": f"تم إرسال رسالة الاختبار إلى {phone}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
