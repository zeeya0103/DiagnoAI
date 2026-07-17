from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_mail import MessageSchema
import os

from app.database import get_db
from app.models.appointment import Appointment as AppointmentModel
from app.schemas.appointment import AppointmentCreate
from utils.email import fm

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)


# ==========================
# TEMP USER (NO AUTH)
# ==========================
class FakeUser:
    id = 1
    email = "demo@gmail.com"


def get_fake_user():
    return FakeUser()


# ==========================
# GET ALL APPOINTMENTS
# ==========================
@router.get("/")
def get_appointments(db: Session = Depends(get_db)):
    return db.query(AppointmentModel).all()


# ==========================
# BOOK APPOINTMENT
# ==========================
@router.post("/")
async def book_appointment(
    data: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: FakeUser = Depends(get_fake_user)
):
    try:
        # Save appointment in database
        appointment = AppointmentModel(
            user_id=current_user.id,
            patient_name=data.patient_name,
            email=data.email,
            phone=data.phone,
            address=data.address,
            date=data.date,
            time=data.time
        )

        db.add(appointment)
        db.commit()
        db.refresh(appointment)

        admin_email = os.getenv(
            "ADMIN_EMAIL",
            "diagnocare19@gmail.com"
        )

        # ==========================
        # USER EMAIL
        # ==========================
        user_msg = MessageSchema(
            subject="Appointment Confirmed",
            recipients=[data.email],
            body=f"""
            <h2>Appointment Confirmed</h2>

            <p>Hi <b>{data.patient_name}</b>,</p>

            <p>Your appointment has been booked successfully.</p>

            <p>
            <b>Date:</b> {data.date}<br>
            <b>Time:</b> {data.time}
            </p>

            <p>Thank you for choosing <b>DIAGNOAI</b> 💙.</p>
            """,
            subtype="html"
        )

        # ==========================
        # ADMIN EMAIL
        # ==========================
        admin_msg = MessageSchema(
            subject="New Appointment",
            recipients=[admin_email],
            body=f"""
            <h2>New Appointment Received</h2>

            <p><b>Patient:</b> {data.patient_name}</p>

            <p><b>Email:</b> {data.email}</p>

            <p><b>Phone:</b> {data.phone}</p>

            <p><b>Address:</b> {data.address}</p>

            <p><b>Date:</b> {data.date}</p>

            <p><b>Time:</b> {data.time}</p>
            """,
            subtype="html"
        )

        # ==========================
        # SEND EMAIL (OPTIONAL)
        # ==========================
        try:
            await fm.send_message(user_msg)
            await fm.send_message(admin_msg)
            print("✅ Emails sent successfully")

        except Exception as email_error:
            print("❌ Email sending failed:", email_error)
            # Do not stop appointment booking

        return {
            "message": "Appointment booked successfully",
            "appointment_id": appointment.id,
            "email_status": "sent_or_skipped"
        }

    except Exception as e:
        db.rollback()
        print("❌ Appointment Error:", e)
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )