from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class AccountDB(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    account_type = Column(String)  # 'customer', 'provider', 'admin'
    is_business_whatsapp = Column(Boolean, default=False)
    name = Column(String, nullable=True)

# OtpDB has been removed as we are migrating it directly to Redis
