from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    username: str
    role: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    class Config:
        from_attributes = True

# Patient Schemas
class PatientCreate(BaseModel):
    username: str
    password: str
    name: str
    dob: str
    gender: str

class PatientOut(BaseModel):
    id: int
    name: str
    dob: str
    gender: str
    user: UserOut
    class Config:
        from_attributes = True

# Technician Schemas
class TechnicianCreate(BaseModel):
    username: str
    password: str
    name: str

class TechnicianOut(BaseModel):
    id: int
    name: str
    specialty: str
    user: UserOut
    class Config:
        from_attributes = True

# Appointment Schemas
class AppointmentCreate(BaseModel):
    patient_id: int
    technician_id: int
    schedule_time: datetime

class AppointmentOut(BaseModel):
    id: int
    patient_id: int
    technician_id: int
    schedule_time: datetime
    status: str
    class Config:
        from_attributes = True

# Test Report Schemas
class TestReportCreate(BaseModel):
    appointment_id: int
    test_data: List[float]

class TestReportOut(BaseModel):
    id: int
    appointment_id: int
    test_data: List[float]
    predicted_disease: str
    risk_scores: dict
    class Config:
        from_attributes = True
