from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, ForeignKey, DECIMAL, TIMESTAMP, text
from database import Base
import enum

class AppointmentStatus(enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"

class AccountDB(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), unique=True, index=True)
    account_type = Column(String(50))  # 'customer', 'provider', 'admin'
    is_business_whatsapp = Column(Boolean, default=False)
    name = Column(String(100), nullable=True)

class Provider(Base):
    __tablename__ = "provider"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    job = Column(String(100))

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey("provider.id"), nullable=False)
    customer_name = Column(String(100), nullable=False)
    appointment_datetime = Column(DateTime, nullable=False)
    status = Column(String(20), default="pending")
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
