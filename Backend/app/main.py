from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.api.appointments import router as appointment_router
from app.api.reports import router as reports_router
from app.api.chatbot import router as chatbot_router
from app.database import init_db

from groq import Groq
from dotenv import load_dotenv

from datetime import datetime
import random
import os

# ==========================
# ENVIRONMENT
# ==========================

load_dotenv()
init_db()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ==========================
# FASTAPI
# ==========================

app = FastAPI()

# ✅ ONLY ROUTERS (KEEP THIS)
app.include_router(appointment_router)
app.include_router(reports_router)
app.include_router(chatbot_router)

# ==========================
# CORS
# ==========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================
# MODELS
# ==========================

class UserRegister(BaseModel):
    name: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


# ❌ REMOVED Appointment model (NOT needed here anymore)

class ChatRequest(BaseModel):
    message: str


# ==========================
# DATABASES
# ==========================

users_db = {
    "admin@gmail.com": {
        "name": "Admin",
        "email": "admin@gmail.com",
        "password": "admin123",
        "role": "admin"
    }
}

appointments_db = []
reports_db = []

# ==========================
# HOME
# ==========================

@app.get("/")
def home():
    return {
        "message": "DiagnoAI Backend Running"
    }


# ==========================
# REGISTER
# ==========================

@app.post("/auth/register")
def register(user: UserRegister):

    if user.email in users_db:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    users_db[user.email] = {
        "name": user.name,
        "email": user.email,
        "password": user.password,
        "role": "user"
    }

    return {
        "message": "User registered successfully"
    }


# ==========================
# LOGIN
# ==========================

@app.post("/auth/login")
def login(user: UserLogin):

    db_user = users_db.get(user.email)

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if db_user["password"] != user.password:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    return {
        "message": "Login successful",
        "token": "fake-jwt-token",
        "role": db_user["role"],
        "user": {
            "name": db_user["name"],
            "email": db_user["email"]
        }
    }


# ==========================
# CURRENT USER
# ==========================

@app.get("/auth/me")
def get_me():
    return {
        "name": "Demo User",
        "email": "demo@gmail.com",
        "role": "user"
    }


# ==========================
# DASHBOARD
# ==========================

@app.get("/dashboard")
def dashboard():
    return {
        "total_users": len(users_db),
        "total_reports": len(reports_db),
        "total_appointments": len(appointments_db)
    }


# ==========================
# REPORTS
# ==========================

@app.get("/reports")
def get_reports():
    return reports_db


@app.post("/reports/upload")
async def upload_report(file: UploadFile = File(...)):

    diseases = [
        "Normal",
        "Diabetes Risk",
        "Anaemia Risk",
        "High Cholesterol"
    ]

    risks = [
        "Low",
        "Moderate",
        "High"
    ]

    report = {
        "id": len(reports_db) + 1,
        "file_name": file.filename,
        "prediction": random.choice(diseases),
        "risk": random.choice(risks),
        "created_at": datetime.now().strftime("%d %B %Y")
    }

    reports_db.append(report)

    return {
        "message": "Report uploaded successfully",
        "report": report
    }


# ==========================
# CHATBOT
# ==========================

@app.post("/chatbot")
def chatbot(data: ChatRequest):

    try:

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are DiagnoAI, a medical assistant. Provide simple health explanations."
                },
                {
                    "role": "user",
                    "content": data.message
                }
            ]
        )

        reply = completion.choices[0].message.content

        return {
            "reply": reply
        }

    except Exception as e:
        return {
            "reply": str(e)
        }


# ==========================
# ADMIN USERS
# ==========================

@app.get("/users")
def users():
    return list(users_db.values())


# ==========================
# ANALYTICS
# ==========================

@app.get("/analytics")
def analytics():
    return {
        "users": len(users_db),
        "reports": len(reports_db),
        "appointments": len(appointments_db)
    }