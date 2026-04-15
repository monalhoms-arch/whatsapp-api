from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from loguru import logger
from schemas import NotificationRequest, NotificationResponse
from services.whatsapp_service import send_whatsapp_message
from database import get_db
from security import get_api_key
import models

router = APIRouter(dependencies=[Depends(get_api_key)])

@router.post("/send", response_model=NotificationResponse)
def send_notification(request: NotificationRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """إرسال تنبيه أو إشعار لحساب بشكل متزامن وغير معطل لعمليات الخادم (Backgrounding)"""
    logger.info(f"Notification System: Preparing notification for {request.phone_number} (Type: {request.account_type})")
    
    is_business = False
    db_account = db.query(models.AccountDB).filter(models.AccountDB.phone_number == request.phone_number).first()
    if db_account:
        is_business = db_account.is_business_whatsapp

    prefix = ""
    if request.account_type == "customer":
        prefix = "👤 تنبيه للزبون: "
    elif request.account_type == "provider":
        prefix = "👷 تنبيه لمقدم الخدمة: "
    elif request.account_type == "admin":
        prefix = "⚙️ إشعار للمسؤول: "
        
    final_message = f"{prefix}\n{request.message}"
    
    # Send via Background Task
    background_tasks.add_task(send_whatsapp_message, request.phone_number, final_message, is_business)
    logger.info(f"Notification queued for background execution: {request.phone_number}")
    
    return NotificationResponse(
        success=True,
        message_id="queued_in_background",
        status="queued"
    )
