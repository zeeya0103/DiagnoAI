# app/services/email_service.py
import smtplib
from email.mime.text import MIMEText
import os
from fastapi import BackgroundTasks
from dotenv import load_dotenv

load_dotenv()

def send_booking_alert_email(booking_id: int, user_email: str, slot: str, address: str):
    """Sends immediate outbound laboratory dispatch emails via background thread tasks."""
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASSWORD")

    if not all([smtp_host, smtp_user, smtp_pass]):
        print(f"SMTP variables unconfigured. Console Alert: Booking #{booking_id} submitted for {user_email}.")
        return

    msg = MIMEText(f"CRITICAL OP LOG: New Home Sample Collection Booking Received.\n\nBooking ID: {booking_id}\nPatient: {user_email}\nPreferred Time Window: {slot}\nAddress: {address}")
    msg['Subject'] = f"[LAB ALERT] Sample Request #{booking_id} Placed"
    msg['From'] = smtp_user
    msg['To'] = smtp_user  # Alerts operations management desk directly

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, [smtp_user], msg.as_string())
    except Exception as e:
        print(f"SMTP execution encountered error states: {str(e)}")