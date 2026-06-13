# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List
import os
import jwt
from datetime import datetime, timedelta
from openai import OpenAI

# 1. Importing your exact custom data organs
from app.database import get_db, engine, Base
from app.models import User, LabReport, ExtractedValue, AIAnalysis, Booking, ChatHistory, AdminLog
from app.schemas import UserCreate, UserResponse, Token, BookingCreate, BookingResponse, ChatMessageSchema, ChatResponseSchema
from app.auth import get_password_hash, verify_password, create_access_token, get_current_user, RoleChecker
from app.engine.ocr_processor import parse_pdf_document_stream
from app.engine.ai_analyzer import generate_health_analysis
from app.services.email_service import send_booking_alert_email

# Build schemas out dynamically using your unified engine structure
Base.metadata.create_all(bind=engine)

app = FastAPI(title="diagnoAI Enterprise Production Backend System Engine", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- INLINED PRODUCTION CUSTOMER HUB ---
@app.get("/", response_class=HTMLResponse)
async def serve_customer_portal():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>diagnoAI Enterprise Portal</title>
        <style>
            * { box-sizing: border-box; font-family: 'Segoe UI', system-ui, sans-serif; }
            body { background: #f0f2f5; color: #333; margin: 0; padding: 20px; }
            .wrapper { max-width: 900px; margin: 0 auto; }
            header { background: #0052cc; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; text-align: center; }
            .card { background: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 20px; }
            .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
            @media(max-width: 768px) { .grid { grid-template-columns: 1fr; } }
            input, textarea, select { width: 100%; padding: 10px; margin: 8px 0 16px; border: 1px solid #ccc; border-radius: 6px; }
            button { background: #0052cc; color: white; border: none; padding: 12px 20px; border-radius: 6px; font-weight: bold; cursor: pointer; width: 100%; }
            button:hover { background: #003d99; }
            .hidden { display: none; }
            .status-box { padding: 12px; background: #e6f0ff; border-left: 4px solid #0052cc; margin-top: 10px; border-radius: 4px; font-family: monospace; font-size: 13px; max-height: 200px; overflow-y: auto; white-space: pre-wrap; }
        </style>
    </head>
    <body>
    <div class="wrapper">
        <header>
            <h1>🏥 diagnoAI Customer Hub</h1>
            <p>Enterprise Production Portal Engine</p>
        </header>

        <div id="authSection" class="card">
            <h3>🔐 Secure Identity Gate</h3>
            <div class="grid">
                <div>
                    <h4>Sign In</h4>
                    <input type="email" id="loginEmail" placeholder="email@example.com">
                    <input type="password" id="loginPass" placeholder="Password">
                    <button onclick="handleAuth('login')">Authenticate Account</button>
                </div>
                <div>
                    <h4>Register Account</h4>
                    <input type="email" id="regEmail" placeholder="email@example.com">
                    <input type="password" id="regPass" placeholder="Password">
                    <select id="regRole">
                        <option value="patient">Patient Client Profile</option>
                        <option value="admin">System Administration Operator</option>
                    </select>
                    <button onclick="handleAuth('register')">Provision Identity</button>
                </div>
            </div>
            <div id="authStatus" class="status-box hidden"></div>
        </div>

        <div id="mainDashboard" class="hidden">
            <div class="card">
                <h3>📄 Diagnostic Data Extraction (OCR)</h3>
                <p>Upload your lab result PDF report to parse structural telemetry metrics into the engine layer.</p>
                <input type="file" id="reportFile" accept=".pdf">
                <button onclick="uploadReport()">Upload & Execute Clinical OCR</button>
                <div id="ocrStatus" class="status-box hidden"></div>
            </div>

            <div class="grid">
                <div class="card">
                    <h3>💬 Context-Aware AI Chat</h3>
                    <textarea id="chatMsg" placeholder="Ask diagnoAI about your results..."></textarea>
                    <button onclick="sendChatMessage()">Execute Context Inquiry</button>
                    <div id="chatStatus" class="status-box hidden"></div>
                </div>
                <div class="card">
                    <h3>📅 Home Sample Collection Scheduler</h3>
                    <input type="text" id="bookAddress" placeholder="Physical Logistics Delivery Address">
                    <input type="datetime-local" id="bookSlot">
                    <button onclick="bookCollection()">Schedule Home Collection</button>
                    <div id="bookStatus" class="status-box hidden"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let TOKEN = "";

        function logStatus(elementId, text, isRaw = false) {
            const el = document.getElementById(elementId);
            el.classList.remove('hidden');
            el.innerText = isRaw ? text : `[SYSTEM LOG]: ${text}`;
        }

        async function handleAuth(type) {
            const email = document.getElementById(type === 'login' ? 'loginEmail' : 'regEmail').value;
            const password = document.getElementById(type === 'login' ? 'loginPass' : 'regPass').value;
            const role = type === 'register' ? document.getElementById('regRole').value : "patient";
            const url = type === 'login' ? '/api/auth/login' : '/api/auth/register';
            
            try {
                const res = await fetch(url, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password, role })
                });
                const data = await res.json();
                
                if (!res.ok) throw new Error(data.detail || "Authentication processing exception.");

                if (type === 'login') {
                    TOKEN = data.access_token;
                    logStatus('authStatus', "Access token issued successfully. System panel unlocked.");
                    document.getElementById('authSection').classList.add('hidden');
                    document.getElementById('mainDashboard').classList.remove('hidden');
                } else {
                    logStatus('authStatus', "Identity matrix registered to system database. Proceed to login.");
                }
            } catch (err) {
                logStatus('authStatus', `Error: ${err.message}`);
            }
        }

        async function uploadReport() {
            const fileInput = document.getElementById('reportFile');
            if (!fileInput.files[0]) return alert("Please select a file.");
            const formData = new FormData();
            formData.append("file", fileInput.files[0]);

            logStatus('ocrStatus', "Uploading PDF binary payload to parsing array...");
            try {
                const res = await fetch('/api/patient/reports/upload', {
                    method: 'POST',
                    headers: { 'Authorization': `Bearer ${TOKEN}` },
                    body: formData
                });
                const data = await res.json();
                logStatus('ocrStatus', JSON.stringify(data, null, 2), true);
            } catch (err) { logStatus('ocrStatus', `Execution Fail: ${err.message}`); }
        }

        async function sendChatMessage() {
            const msg = document.getElementById('chatMsg').value;
            try {
                const res = await fetch('/api/patient/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${TOKEN}` },
                    body: JSON.stringify({ message: msg })
                });
                const data = await res.json();
                logStatus('chatStatus', `Response:\\n${data.reply}`, true);
            } catch (err) { logStatus('chatStatus', `Execution Fail: ${err.message}`); }
        }

        async function bookCollection() {
            const address = document.getElementById('bookAddress').value;
            const preferred_slot = document.getElementById('bookSlot').value;
            try {
                const res = await fetch('/api/patient/book-collection', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${TOKEN}` },
                    body: JSON.stringify({ address, preferred_slot })
                });
                const data = await res.json();
                logStatus('bookStatus', `Booking complete. ID: ${data.id}`, true);
            } catch (err) { logStatus('bookStatus', `Execution Fail: ${err.message}`); }
        }
    </script>
    </body>
    </html>
    """

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
    current_user: User = Depends(RoleChecker(["patient"])), 
    db: Session = Depends(get_db)
):
    contents = await file.read()
    metrics = parse_pdf_document_stream(contents)
    insights = generate_health_analysis(metrics)

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
    recent_logs = db.query(ChatHistory).filter(ChatHistory.user_id == current_user.id).order_by(ChatHistory.timestamp.desc()).limit(10).all()
    recent_logs.reverse()

    latest_report = db.query(LabReport).filter(LabReport.user_id == current_user.id).order_by(LabReport.uploaded_at.desc()).first()
    
    context_string = "You are an on-premise medical diagnostic assistant. Translate medical jargon simply."
    if latest_report and latest_report.ai_analysis:
        context_string += f" Patient's latest test status: {latest_report.ai_analysis.status}. Risk Profile: {latest_report.ai_analysis.risk_level}."

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        q = payload.message.lower()
        reply = "Local Engine Response: Please bring anomalous parameter arrays directly to your doctor."
        if "glucose" in q or "sugar" in q: reply = "Fasting glucose markers indicate glycemic saturation thresholds. Limit simple sugar intake."
    else:
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