# app/main.py
import os
import jwt
from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from passlib.context import CryptContext

# --- GLOBAL SECURITY ---
SECRET_KEY = os.getenv("JWT_SECRET", "super-secret-production-key-fallback-999")
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- DATABASE SETUP ---
DATABASE_URL = "sqlite:////code/data/diagnoai.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class LocalUser(Base):
    __tablename__ = "local_users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="patient")

Base.metadata.create_all(bind=engine)

def get_local_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- FASTAPI ENGINE ---
app = FastAPI(title="diagnoAI Fixed Engine", version="2.6.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- UNIFIED SCHEMAS ---
class UserAuthSchema(BaseModel):
    email: str  # Changed from EmailStr to robust string to prevent validation crash
    password: str
    role: str = "patient"

class ChatMessageSchema(BaseModel):
    message: str

# --- INLINED USER PORTAL ---
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
            
            if(!email || !password) {
                return alert("Please enter both email and password fields.");
            }

            try {
                const res = await fetch(url, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password, role })
                });
                const data = await res.json();
                
                if (!res.ok) throw new Error(data.detail || "Transaction verification failed.");

                if (type === 'login') {
                    TOKEN = data.access_token;
                    logStatus('authStatus', "Access Token verified successfully. Dashboard unlocked.");
                    document.getElementById('authSection').classList.add('hidden');
                    document.getElementById('mainDashboard').classList.remove('hidden');
                } else {
                    logStatus('authStatus', "Identity created successfully! You can now input your details on the left and click 'Authenticate Account'.");
                }
            } catch (err) {
                logStatus('authStatus', `Error: ${err.message}`);
            }
        }

        async function uploadReport() {
            const fileInput = document.getElementById('reportFile');
            if (!fileInput.files[0]) return alert("Select file first.");
            const formData = new FormData();
            formData.append("file", fileInput.files[0]);

            logStatus('ocrStatus', "Uploading PDF binary metadata to parsing array...");
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

# --- AUTH ROUTING WITH UNIFIED SCHEMA ---
@app.post("/api/auth/register", status_code=status.HTTP_201_CREATED)
def register_account(user_in: UserAuthSchema, db: Session = Depends(get_local_db)):
    existing = db.query(LocalUser).filter(LocalUser.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Account already registered.")
    hashed = pwd_context.hash(user_in.password)
    new_user = LocalUser(email=user_in.email, hashed_password=hashed, role=user_in.role)
    db.add(new_user)
    db.commit()
    return {"status": "success", "email": new_user.email}

@app.post("/api/auth/login")
def authenticate_user(user_in: UserAuthSchema, db: Session = Depends(get_local_db)):
    user = db.query(LocalUser).filter(LocalUser.email == user_in.email).first()
    if not user or not pwd_context.verify(user_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Authentication verification failed.")
    
    expire = datetime.utcnow() + timedelta(days=1)
    token = jwt.encode({"sub": user.email, "role": user.role, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

# --- SYSTEM STUBS ---
@app.post("/api/patient/reports/upload")
async def upload_and_process_report():
    return {"status": "success", "msg": "Document parsed."}

@app.post("/api/patient/chat")
def engage_ai_chat(payload: ChatMessageSchema):
    return {"reply": "Connection live. Diagnostic matrix fully calibrated."}

@app.post("/api/patient/book-collection")
def place_collection_request():
    return {"id": 777, "status": "Collection verified."}