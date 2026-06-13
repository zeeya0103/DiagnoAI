# app/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Boolean, Index
from sqlalchemy.orm import relationship
from app.database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="patient") # patient, admin
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    reports = relationship("LabReport", back_populates="patient")
    bookings = relationship("Booking", back_populates="patient")

class LabReport(Base):
    __tablename__ = "lab_reports"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_name = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)

    patient = relationship("User", back_populates="reports")
    extracted_values = relationship("ExtractedValue", back_populates="report", uselist=False, cascade="all, delete-orphan")
    ai_analysis = relationship("AIAnalysis", back_populates="report", uselist=False, cascade="all, delete-orphan")

class ExtractedValue(Base):
    __tablename__ = "extracted_values"
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("lab_reports.id"), nullable=False, unique=True)
    hemoglobin = Column(Float, nullable=True)
    glucose = Column(Float, nullable=True)
    cholesterol = Column(Float, nullable=True)
    wbc = Column(Float, nullable=True)
    rbc = Column(Float, nullable=True)
    platelets = Column(Float, nullable=True)

    report = relationship("LabReport", back_populates="extracted_values")

class AIAnalysis(Base):
    __tablename__ = "ai_analysis"
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("lab_reports.id"), nullable=False, unique=True)
    status = Column(String, nullable=False)
    risk_level = Column(String, nullable=False) # Low, Moderate, High
    explanation = Column(Text, nullable=False)
    precautions = Column(Text, nullable=False)
    suggestions = Column(Text, nullable=False)

    report = relationship("LabReport", back_populates="ai_analysis")

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    address = Column(Text, nullable=False)
    preferred_slot = Column(DateTime, nullable=False)
    status = Column(String, default="pending") # pending, confirmed, collected, completed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    patient = relationship("User", back_populates="bookings")

class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String, nullable=False) # user, assistant
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class AdminLog(Base):
    __tablename__ = "admin_logs"
    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# High-Performance Query Optimization Indexes
Index('idx_user_email', User.email)
Index('idx_report_user', LabReport.user_id)
Index('idx_booking_user', Booking.user_id)