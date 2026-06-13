# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os
from openai import OpenAI

from app.database import get_db, engine, Base
from app.models import User, LabReport, ExtractedValue, AIAnalysis, Booking, ChatHistory, AdminLog
from app.schemas import UserCreate, UserResponse, Token, BookingCreate, BookingResponse, ChatMessageSchema, ChatResponseSchema
from app.auth import get_password_hash, verify_password, create_access_token, get_current_user, RoleChecker
from app.engine.ocr_processor import parse_pdf_document_stream
from app.engine.ai_analyzer import generate_health_analysis
from app.services.email_service import send_booking_alert_email

# Build schemas out dynamically
Base.metadata.create_all(bind=engine)

app = FastAPI(title="diagnoAI Enterprise Production Backend System Engine", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODULE 1: AUTHENTICATION ROUTING CONTROLLER ---
@app.post("/api/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_account(user_in: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(status_code=400, detail="Target identity account already registered.")
    new_user = User(email=user_in.email, hashed_password=get_password_hash(user_in.password), role=user_in.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/api/auth/login", response_model=Token)
def authenticate_user(user_in: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email).first()
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Authentication verification failed.")
    return {"access_token": create_access_token({"sub": user.email}), "token_type": "bearer"}

# --- MODULE 2: PATIENT ENDPOINT ROUTERS & PROCESSING ---
@app.post("/api/patient/reports/upload", status_code=status.HTTP_201_CREATED)
async def upload_and_process_report(
    file: UploadFile = File(...), 
    current_user: User = Depends(RoleChecker(["patient"])), # FIXED: Removed nested Depends statement
    db: Session = Depends(get_db)
):
    contents = await file.read()
    # 1. Parse metrics out via local structural OCR script
    metrics = parse_pdf_document_stream(contents)
    
    # 2. Feed parsed metrics to Analysis Engine
    insights = generate_health_analysis(metrics)

    # 3. Store the records securely in the database using the unified session manager
    report = LabReport(user_id=current_user.id, file_name=file.filename)
    db.add(report)
    db.commit()

    extracted = ExtractedValue(report_id=report.id, **metrics)
    analysis = AIAnalysis(report_id=report.id, **insights)
    db.add(extracted)
    db.add(analysis)
    db.commit()

    return {"report_id": report.id, "extracted_metrics": metrics, "clinical_analysis": insights}

@app.get("/api/patient/reports", status_code=status.HTTP_200_OK)
def fetch_personal_reports(current_user: User = Depends(RoleChecker(["patient"])), db: Session = Depends(get_db)):
    reports = db.query(LabReport).filter(LabReport.user_id == current_user.id).all()
    return [{
        "report_id": r.id, "file_name": r.file_name, "uploaded_at": r.uploaded_at,
        "metrics": r.extracted_values, "analysis": r.ai_analysis
    } for r in reports]

# --- MODULE 6: CONTEXT-AWARE CONVERSATIONAL MEMORY CHAT ---
@app.post("/api/patient/chat", response_model=ChatResponseSchema)
def engage_ai_chat(payload: ChatMessageSchema, current_user: User = Depends(RoleChecker(["patient"])), db: Session = Depends(get_db)):
    # Pull conversation history across sessions to establish memory context
    recent_logs = db.query(ChatHistory).filter(ChatHistory.user_id == current_user.id).order_by(ChatHistory.timestamp.desc()).limit(10).all()
    recent_logs.reverse()

    # Pull the latest lab metrics to provide tailored, context-aware answers
    latest_report = db.query(LabReport).filter(LabReport.user_id == current_user.id).order_by(LabReport.uploaded_at.desc()).first()
    
    context_string = "You are an on-premise medical diagnostic assistant. Translate medical jargon simply."
    if latest_report and latest_report.ai_analysis:
        context_string += f" Patient's latest test status: {latest_report.ai_analysis.status}. Risk Profile: {latest_report.ai_analysis.risk_level}."

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        # Offline rule-based chatbot fallback response matrix
        q = payload.message.lower()
        reply = "Local Engine Response: Please bring anomalous parameter arrays directly to your doctor."
        if "glucose" in q or "sugar" in q: reply = "Fasting glucose markers indicate glycemic saturation thresholds. Limit simple sugar intake."
    else:
        # Build out a conversational message payload including historical context
        client = OpenAI(api_key=api_key)
        messages = [{"role": "system", "content": context_string}]
        for log in recent_logs:
            messages.append({"role": log.role, "content": log.message})
        messages.append({"role": "user", "content": payload.message})

        try:
            res = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
            reply = res.choices[0].message.content
        except Exception:
            reply = "Network execution failure. Please ensure data parameters are reviewed by human clinicians."

    # Commit conversational histories to support future analytical cycles
    db.add(ChatHistory(user_id=current_user.id, role="user", message=payload.message))
    db.add(ChatHistory(user_id=current_user.id, role="assistant", message=reply))
    db.commit()
    return {"reply": reply}

# --- MODULE 7: HOME SAMPLE COLLECTION SCHEDULING ---
@app.post("/api/patient/book-collection", response_model=BookingResponse)
def place_collection_request(booking_in: BookingCreate, bg_tasks: BackgroundTasks, current_user: User = Depends(RoleChecker(["patient"])), db: Session = Depends(get_db)):
    new_booking = Booking(user_id=current_user.id, address=booking_in.address, preferred_slot=booking_in.preferred_slot)
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    
    # Push notification alerts out asynchronously using background task workers
    bg_tasks.add_task(send_booking_alert_email, new_booking.id, current_user.email, str(new_booking.preferred_slot), new_booking.address)
    return new_booking

# --- MODULE 3: SECURE LAB OPERATIONS DASHBOARD (ADMIN PRIVILEGES SCOPE) ---
@app.get("/api/admin/dashboard-telemetry", dependencies=[Depends(RoleChecker(["admin"]))])
def fetch_admin_system_metrics(db: Session = Depends(get_db)):
    return {
        "total_registered_patients": db.query(User).filter(User.role == "patient").count(),
        "total_documents_processed": db.query(LabReport).count(),
        "total_active_bookings": db.query(Booking).count()
    }

@app.get("/api/admin/bookings", response_model=List[BookingResponse], dependencies=[Depends(RoleChecker(["admin"]))])
def manage_all_bookings(db: Session = Depends(get_db)):
    return db.query(Booking).order_by(Booking.created_at.desc()).all()

@app.patch("/api/admin/bookings/{booking_id}/status", dependencies=[Depends(RoleChecker(["admin"]))])
def update_booking_status(booking_id: int, target_status: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking record not found.")
    booking.status = target_status
    db.add(AdminLog(admin_id=current_user.id, action=f"Modified status of booking #{booking_id} to {target_status}"))
    db.commit()
    return {"message": "System logs modified and processing status updated."}