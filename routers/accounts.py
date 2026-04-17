from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from loguru import logger
from schemas import AccountCreate, AccountResponse
from database import get_db
from security import get_api_key
import models

router = APIRouter(dependencies=[Depends(get_api_key)])

@router.post("/", response_model=AccountResponse)
def add_account(account: AccountCreate, db: Session = Depends(get_db)):
    """
    إضافة حساب (إذا وجد) لتمكين إرسال الرسائل بشكل مخصص بناءً على الإعدادات.
    """
    logger.info(f"Account DB: Request to add account {account.phone_number}")
    db_account = db.query(models.AccountDB).filter(models.AccountDB.phone_number == account.phone_number).first()
    if db_account:
        logger.warning(f"Account Add Failed: {account.phone_number} already exists.")
        raise HTTPException(
            status_code=400, 
            detail="هذا الرقم مسجل مسبقاً في النظام. يرجى استخدام رقم آخر أو تسجيل الدخول."
        )
    
    new_account = models.AccountDB(**account.model_dump())
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    
    logger.success(f"Account added successfully for {account.phone_number}")
    return new_account

@router.get("/{phone_number}", response_model=AccountResponse)
def get_account(phone_number: str, db: Session = Depends(get_db)):
    """جلب بيانات حساب محلي إن وجد"""
    logger.info(f"Account DB: Looking up account {phone_number}")
    db_account = db.query(models.AccountDB).filter(models.AccountDB.phone_number == phone_number).first()
    if not db_account:
        logger.warning(f"Account Lookup Failed: {phone_number} not found.")
        raise HTTPException(status_code=404, detail="الحساب غير موجود في قاعدة البيانات المحلية.")
    
    return db_account

@router.put("/{phone_number}", response_model=AccountResponse)
def update_account(phone_number: str, account_data: AccountCreate, db: Session = Depends(get_db)):
    """تعديل بيانات حساب موجود"""
    logger.info(f"Account DB: Request to update account {phone_number}")
    db_account = db.query(models.AccountDB).filter(models.AccountDB.phone_number == phone_number).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="لا يمكن التعديل، الحساب غير موجود.")
    
    for key, value in account_data.model_dump().items():
        setattr(db_account, key, value)
    
    db.commit()
    db.refresh(db_account)
    logger.success(f"Account {phone_number} updated successfully.")
    return db_account

@router.delete("/{phone_number}")
def delete_account(phone_number: str, db: Session = Depends(get_db)):
    """حذف حساب نهائياً من قاعدة البيانات"""
    logger.info(f"Account DB: Request to delete account {phone_number}")
    db_account = db.query(models.AccountDB).filter(models.AccountDB.phone_number == phone_number).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="لا يمكن الحذف، الحساب غير موجود.")
    
    db.delete(db_account)
    db.commit()
    logger.success(f"Account {phone_number} deleted successfully.")
    return {"success": True, "message": f"تم حذف الحساب {phone_number} بنجاح."}
