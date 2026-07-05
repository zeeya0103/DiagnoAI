from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer)

    patient_name = Column(String(100))

    email = Column(String(100))

    phone = Column(String(20))

    address = Column(String(255))

    date = Column(String(20))

    time = Column(String(20))

    status = Column(String(30), default="Pending")

    created_at = Column(DateTime(timezone=True), server_default=func.now())