# 🩺 DiagnoAI

DiagnoAI is an AI-powered healthcare platform that enables users to upload medical reports, book diagnostic appointments, and interact with an AI medical chatbot for basic health guidance.

Built using **React.js**, **FastAPI**, **MySQL**, and **Groq Llama 3.3-70B**.

---

# ✨ Features

## 📄 Medical Report Upload
- Upload medical reports
- Store reports securely in MySQL
- View uploaded reports

## 📅 Appointment Booking
- Book appointments online
- Store appointment details in MySQL
- Automatic confirmation email to the patient
- Automatic notification email to the admin

## 🤖 AI Medical Chatbot
- Powered by Groq API
- Uses Llama-3.3-70B-Versatile
- Provides AI-based health guidance
- Answers general medical queries

## 👤 User Profile
- Displays user information
- Shows total uploaded reports
- Shows total booked appointments

## 📊 Dashboard
- Overview of reports
- Appointment statistics
- Basic analytics

---

# 🛠 Tech Stack

## Frontend
- React.js
- Vite
- Axios
- React Router
- Framer Motion
- React Icons

## Backend
- FastAPI
- SQLAlchemy
- Pydantic
- FastAPI-Mail
- Uvicorn

## Database
- MySQL

## AI
- Groq API
- Llama-3.3-70B-Versatile

---

# 📁 Project Structure

```
DiagnoAI/
│
├── Backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── database.py
│   │   └── main.py
│   │
│   ├── uploads/
│   ├── utils/
│   └── requirements.txt
│
├── Frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   └── App.jsx
│   └── package.json
│
├── .env.example
├── .gitignore
└── README.md
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/zeeya0103/DiagnoAI.git
cd DiagnoAI
```

---

## Backend Setup

```bash
cd Backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file:

```env
DATABASE_URL=mysql+pymysql://username:password@localhost/database_name

GROQ_API_KEY=your_groq_api_key

MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_FROM=your_email@gmail.com
ADMIN_EMAIL=your_admin_email@gmail.com
```

Run the backend:

```bash
python -m uvicorn app.main:app --reload
```

---

## Frontend Setup

```bash
cd Frontend

npm install

npm run dev
```

---

# 📧 Email Notifications

When an appointment is booked:

- ✅ Confirmation email is sent to the patient.
- ✅ Notification email is sent to the administrator.

---

# 🤖 AI Chatbot

Powered by:

- Groq API
- Llama-3.3-70B-Versatile

Capabilities:

- General health guidance
- Symptom explanations
- Medical information assistance

---

# 📸 Screenshots

Add screenshots for:

- Home Page
- Dashboard
- Upload Report
- Appointment Booking
- AI Chatbot
- Profile

---

# 🚀 Future Enhancements

- Secure User Authentication (JWT)
- Medical Report Parsing
- AI Disease Prediction
- OCR-based Report Analysis
- Doctor Dashboard
- Appointment Rescheduling
- PDF Report Generation
- Cloud Deployment
- Docker Support

---

# 👨‍💻 Author

**Zeeya Sinha**

GitHub: https://github.com/zeeya0103

---

⭐ If you found this project useful, please consider starring the repository.# DiagnoAI
