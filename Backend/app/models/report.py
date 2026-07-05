from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, nullable=True)

    file_name = Column(String(255))   # ✅ FIXED
    file_path = Column(String(255))   # ✅ FIXED

    prediction = Column(String(100), default="Processing")
    risk = Column(String(50), default="Unknown")

    created_at = Column(DateTime, default=datetime.utcnow)