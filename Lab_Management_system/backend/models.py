from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password_hash = Column(String)
    role = Column(String)  # admin, patient, technician
    created_at = Column(DateTime, default=datetime.utcnow)

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    dob = Column(String)
    gender = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User")

class Technician(Base):
    __tablename__ = "technicians"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    specialty = Column(String, default="Blood Test")
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User")

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    technician_id = Column(Integer, ForeignKey("technicians.id"))
    schedule_time = Column(DateTime)
    status = Column(String, default="booked")
    created_at = Column(DateTime, default=datetime.utcnow)

class TestReport(Base):
    __tablename__ = "test_reports"
    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"))
    test_data = Column(JSON)
    predicted_disease = Column(String)
    risk_scores = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
