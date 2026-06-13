# app/schemas.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Optional[str] = "patient"

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: str
    created_at: datetime
    class Config: from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class BookingCreate(BaseModel):
    address: str
    preferred_slot: datetime

class BookingResponse(BaseModel):
    id: int
    user_id: int
    address: str
    preferred_slot: datetime
    status: str
    created_at: datetime
    class Config: from_attributes = True

class ChatMessageSchema(BaseModel):
    message: str

class ChatResponseSchema(BaseModel):
    reply: str