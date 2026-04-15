from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal

# مسارات الحسابات
class AccountBase(BaseModel):
    phone_number: str
    account_type: Literal["customer", "provider", "admin"]
    is_business_whatsapp: bool = False
    name: Optional[str] = None

class AccountCreate(AccountBase):
    pass

class AccountResponse(AccountBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# مسارات الأمان OTP
class OTPRequest(BaseModel):
    phone_number: str
    account_type: Literal["customer", "provider", "admin"]

class OTPVerify(BaseModel):
    phone_number: str
    code: str

class OTPResponse(BaseModel):
    success: bool
    message: str

# مسارات التنبيهات
class NotificationRequest(BaseModel):
    phone_number: str
    message: str
    account_type: Literal["customer", "provider", "admin"]
    
class NotificationResponse(BaseModel):
    success: bool
    message_id: Optional[str] = None
    status: str
