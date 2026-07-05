from pydantic import BaseModel
from datetime import datetime


class AppointmentCreate(BaseModel):
    patient_name: str
    email: str
    phone: str
    address: str
    date: str
    time: str