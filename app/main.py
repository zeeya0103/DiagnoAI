# app/main.py
import os
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import List
from openai import OpenAI

# Assuming your imports are structured as before
from app.models import User, LabReport, ExtractedValue, AIAnalysis, Booking, ChatHistory, AdminLog
from app.schemas import UserCreate, UserResponse, Token, BookingCreate, BookingResponse, ChatMessageSchema, ChatResponseSchema
from app.auth import get_password_hash, verify_password, create_access_token, get_current_user, RoleChecker
from app.engine.ocr_processor import parse_pdf_document_stream
from app.engine.ai_analyzer import generate_health_analysis
from app.services.email_service import send_booking_alert_email

# --- DATABASE CONFIGURATION ---
# Using the persistent /code/data path to prevent Render "Internal Server Error"
DATABASE_URL = "sqlite:////code/data/diagnoai.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="diagnoAI Production Engine", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- PORTAL INTERFACE (INLINED) ---
@app.get("/", response_class=HTMLResponse)
async def serve_customer_portal():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>diagnoAI Portal</title>
        <style>
            body { font-family: sans-serif; background: #f4f7f6; padding: 40px; }
            .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); max-width: 600px; margin: auto; }
            button { background: #0052cc; color: white; border: none; padding: 10px; width: 100%; cursor: pointer; border-radius: 4px; }
            .status-box { background: #eee; padding: 10px; margin-top: 10px; white-space: pre-wrap; font-size: 12px; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🏥 diagnoAI Portal</h1>
            <p>Welcome. Please use the API endpoints or the admin dashboard.</p>
            <button onclick="window.location.href='/docs'">View API Documentation</button>
        </div>
    </body>
    </html>
    """

# --- AUTHENTICATION ---
@app.post("/api/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_account(user_in: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(status_code=400, detail="Account already exists.")
    new_user = User(email=user_in.email, hashed_password=get_password_hash(user_in.password), role=user_in.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/api/auth/login", response_model=Token)
def authenticate_user(user_in: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email).first()
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Auth failed.")
    return {"access_token": create_access_token({"sub": user.email}), "token_type": "bearer"}

# --- PATIENT OPERATIONS ---
@app.post("/api/patient/reports/upload", status_code=status.HTTP_201_CREATED)
async def upload_and_process_report(file: UploadFile = File(...), current_user: User = Depends(RoleChecker(["patient"])), db: Session = Depends(get_db)):
    contents = await file.read()
    metrics = parse_pdf_document_stream(contents)
    insights = generate_health_analysis(metrics)
    report = LabReport(user_id=current_user.id, file_name=file.filename)
    db.add(report)
    db.commit()
    db.add(ExtractedValue(report_id=report.id, **metrics))
    db.add(AIAnalysis(report_id=report.id, **insights))
    db.commit()
    return {"report_id": report.id, "metrics": metrics, "analysis": insights}

@app.post("/api/patient/chat", response_model=ChatResponseSchema)
def engage_ai_chat(payload: ChatMessageSchema, current_user: User = Depends(RoleChecker(["patient"])), db: Session = Depends(get_db)):
    # Simple Chat Logic
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key) if api_key else None
    
    reply = "AI is currently unavailable."
    if client:
        res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": payload.message}])
        reply = res.choices[0].message.content
        
    db.add(ChatHistory(user_id=current_user.id, role="user", message=payload.message))
    db.add(ChatHistory(user_id=current_user.id, role="assistant", message=reply))
    db.commit()
    return {"reply": reply}

@app.post("/api/patient/book-collection", response_model=BookingResponse)
def place_collection_request(booking_in: BookingCreate, bg_tasks: BackgroundTasks, current_user: User = Depends(RoleChecker(["patient"])), db: Session = Depends(get_db)):
    new_booking = Booking(user_id=current_user.id, address=booking_in.address, preferred_slot=booking_in.preferred_slot)
    db.add(new_booking)
    db.commit()
    bg_tasks.add_task(send_booking_alert_email, new_booking.id, current_user.email, str(new_booking.preferred_slot), new_booking.address)
    return new_booking

# --- ADMIN ---
@app.get("/api/admin/dashboard-telemetry", dependencies=[Depends(RoleChecker(["admin"]))])
def fetch_admin_system_metrics(db: Session = Depends(get_db)):
    return {"status": "operational", "patients": db.query(User).count()}