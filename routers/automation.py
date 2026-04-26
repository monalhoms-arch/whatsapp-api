from fastapi import APIRouter, HTTPException, Depends, Query
import requests
from config import settings
from security import get_api_key
from loguru import logger
from typing import Optional

router = APIRouter(dependencies=[Depends(get_api_key)])

@router.get("/status")
def get_automation_status():
    """التحقق من حالة النظام الإجمالية ومزود الخدمة النشط"""
    provider = settings.WHATSAPP_PROVIDER.lower()
    response = {
        "status": "online",
        "provider": provider,
    }
    if provider == "meta":
        response["meta_api_version"] = settings.META_API_VERSION
        response["meta_phone_number_id"] = settings.META_PHONE_NUMBER_ID
        response["meta_api_configured"] = bool(settings.META_API_TOKEN and settings.META_API_TOKEN != "change_me_in_env")
    else:
        response["evolution_api_url"] = settings.EVOLUTION_API_URL
        response["default_instance"] = settings.EVOLUTION_INSTANCE_NAME
    return response

@router.get("/instances")
def list_instances():
    """جلب جميع النسخ (Instances) من Evolution API"""
    url = f"{settings.EVOLUTION_API_URL}/instance/fetchInstances"
    headers = {"apikey": settings.EVOLUTION_API_TOKEN}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error fetching instances: {e}")
        raise HTTPException(status_code=500, detail="فشل جلب قائمة النسخ من السيرفر")

@router.post("/instances")
def create_instance(name: str):
    """إنشاء نسخة جديدة (Instance) في Evolution API"""
    url = f"{settings.EVOLUTION_API_URL}/instance/create"
    headers = {
        "apikey": settings.EVOLUTION_API_TOKEN,
        "Content-Type": "application/json"
    }
    payload = {
        "instanceName": name,
        "integration": "WHATSAPP-BAILEYS",
        "qrcode": True
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        if response.status_code != 201 and response.status_code != 200:
            logger.error(f"Evolution API Error: {response.status_code} - {response.text}")
            raise HTTPException(status_code=response.status_code, detail=f"Evolution API Error: {response.text}")
        return response.json()
    except Exception as e:
        logger.error(f"Error creating instance: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/instances/{instance_id}/connect")
def connect_instance(instance_id: str):
    """طلب رمز QR للارتباط بالواتساب لنسخة معينة"""
    url = f"{settings.EVOLUTION_API_URL}/instance/connect/{instance_id}"
    headers = {"apikey": settings.EVOLUTION_API_TOKEN}
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error getting QR for {instance_id}: {e}")
        raise HTTPException(status_code=500, detail="فشل طلب رمز QR")

@router.post("/instances/{instance_id}/logout")
def logout_instance(instance_id: str):
    """تسجيل الخروج وقطع الارتباط لنسخة معينة"""
    url = f"{settings.EVOLUTION_API_URL}/instance/logout/{instance_id}"
    headers = {"apikey": settings.EVOLUTION_API_TOKEN}
    
    try:
        response = requests.post(url, headers=headers, timeout=15)
        response.raise_for_status()
        return {"status": "success", "message": f"تم تسجيل الخروج من {instance_id}"}
    except Exception as e:
        logger.error(f"Error logging out {instance_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/instances/{instance_id}")
def delete_instance(instance_id: str):
    """حذف نسخة بالكامل من السيرفر"""
    url = f"{settings.EVOLUTION_API_URL}/instance/delete/{instance_id}"
    headers = {"apikey": settings.EVOLUTION_API_TOKEN}
    
    try:
        response = requests.delete(url, headers=headers, timeout=15)
        response.raise_for_status()
        return {"status": "success", "message": f"تم حذف النسخة {instance_id} بنجاح"}
    except Exception as e:
        logger.error(f"Error deleting instance {instance_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test-message")
def test_automated_message(phone: str, message: str, instance_id: Optional[str] = Query(None)):
    """إرسال رسالة اختبار سريعة من نسخة معينة"""
    from services.whatsapp_service import send_whatsapp_message
    try:
        send_whatsapp_message(phone, message, instance_id=instance_id)
        return {"success": True, "message": f"تم إرسال الرسالة إلى {phone} من النسخة {instance_id or settings.EVOLUTION_INSTANCE_NAME}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
