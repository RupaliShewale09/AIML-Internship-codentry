from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session

from backend.database import get_db, Base, engine
from backend.models import User, Patient, Technician, Appointment, TestReport
from backend.schemas import *
from backend.utils import hash_password, verify_password, get_disease_prediction
from datetime import datetime

# Create all tables
Base.metadata.create_all(bind=engine)

router = APIRouter()

# -------------------------
# AUTH
# -------------------------

@router.post("/login")
def login(
    username: str = Form(...), 
    password: str = Form(...), 
    db: Session = Depends(get_db)
):
    # 1. Check for Admin (static check)
    if username == "admin" and password == "admin123":
        return {"id": 0, "username": "admin", "role": "admin"}
    
    # 2. Check Database for User
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # 3. Logic Fix: Return the specific Role ID (Patient ID or Tech ID)
    # This ensures the frontend 'user.id' matches the foreign keys in Appointment/Report tables
    profile_id = user.id
    if user.role == "patient":
        patient = db.query(Patient).filter(Patient.user_id == user.id).first()
        if patient: profile_id = patient.id
    elif user.role == "technician":
        tech = db.query(Technician).filter(Technician.user_id == user.id).first()
        if tech: profile_id = tech.id
    
    return {"id": profile_id, "username": user.username, "role": user.role}


@router.post("/admin/technician", response_model=TechnicianOut)
def add_technician(username: str = Form(...),
    password: str = Form(...),
    name: str = Form(...),
    db: Session = Depends(get_db)
):
    # create user
    user = User(username=username, password_hash=hash_password(password), role="technician")
    db.add(user)
    db.commit()
    db.refresh(user)

    technician = Technician(user_id=user.id, name=name)
    db.add(technician)
    db.commit()
    db.refresh(technician)
    return technician

@router.get("/admin/technicians", response_model=List[TechnicianOut])
def list_technicians(db: Session = Depends(get_db)):
    return db.query(Technician).all()

@router.get("/admin/appointments", response_model=List[AppointmentOut])
def list_all_appointments(db: Session = Depends(get_db)):
    return db.query(Appointment).all()

@router.get("/admin/appointments/today", response_model=List[AppointmentOut])
def list_today_appointments(db: Session = Depends(get_db)):
    today = datetime.now().date()
    return db.query(Appointment).filter(Appointment.schedule_time.between(datetime.combine(today, datetime.min.time()), datetime.combine(today, datetime.max.time()))).all()

# -------------------------
# PATIENT
# -------------------------
@router.post("/register/patient", response_model=PatientOut)
def register_patient(username: str = Form(...),
    password: str = Form(...),
    name: str = Form(...),
    dob: str = Form(...),
    gender: str = Form(...),
    db: Session = Depends(get_db)
):
    user = User(username=username, password_hash=hash_password(password), role="patient")
    db.add(user)
    db.commit()
    db.refresh(user)

    pat = Patient(user_id=user.id, name=name, dob=dob, gender=gender)
    db.add(pat)
    db.commit()
    db.refresh(pat)
    return pat

@router.post("/patient/appointment", response_model=AppointmentOut)
def book_appointment(patient_id: int = Form(...),
    technician_id: int = Form(...),
    schedule_time: datetime = Form(...),
    db: Session = Depends(get_db)
):
    appointment = Appointment(patient_id=patient_id, technician_id=technician_id, schedule_time=schedule_time)
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment

@router.get("/patient/appointments", response_model=List[AppointmentOut])
def get_patient_appointments(patient_id: int, db: Session = Depends(get_db)):
    return db.query(Appointment).filter(Appointment.patient_id == patient_id).all()

@router.get("/patient/reports", response_model=List[TestReportOut])
def get_patient_reports(patient_id: int, db: Session = Depends(get_db)):
    apps = db.query(Appointment).filter(Appointment.patient_id == patient_id).all()
    reports = []
    for app in apps:
        report = db.query(TestReport).filter(TestReport.appointment_id == app.id).first()
        if report:
            reports.append(report)
    return reports

# -------------------------
# TECHNICIAN
# -------------------------
@router.get("/technician/appointments", response_model=List[AppointmentOut])
def get_technician_appointments(technician_id: int, db: Session = Depends(get_db)):
    return db.query(Appointment).filter(Appointment.technician_id == technician_id).all()

@router.post("/technician/report", response_model=TestReportOut)
def add_test_report(appointment_id: int = Form(...),
    Insulin: float = Form(...),
    BMI: float = Form(...),
    Cholesterol: float = Form(...),
    Glucose: float = Form(...),
    Hematocrit: float = Form(...),
    Red_Blood_Cells: float = Form(...),
    White_Blood_Cells: float = Form(...),
    Platelets: float = Form(...),
    Mean_Corpuscular_Volume: float = Form(...),
    Mean_Corpuscular_Hemoglobin: float = Form(...),
    Mean_Corpuscular_Hemoglobin_Concentration: float = Form(...),
    Hemoglobin: float = Form(...),
    db: Session = Depends(get_db)
):
    test_data_list = [
        Insulin, BMI, Cholesterol, Glucose, Hematocrit, Red_Blood_Cells, 
        White_Blood_Cells, Platelets, Mean_Corpuscular_Volume, 
        Mean_Corpuscular_Hemoglobin, Mean_Corpuscular_Hemoglobin_Concentration, Hemoglobin
    ]

    predicted_disease, risk_scores = get_disease_prediction(test_data_list)
    test_report = TestReport(
        appointment_id=appointment_id,
        test_data=test_data_list,
        predicted_disease=predicted_disease,
        risk_scores=risk_scores
    )
    db.add(test_report)
    # mark appointment as done
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if appointment:
        appointment.status = "done"
    db.commit()
    db.refresh(test_report)
    return test_report
