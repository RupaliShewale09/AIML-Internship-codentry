from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from datetime import timedelta, datetime, time


from backend.database import get_db
from backend import models, schemas
from backend.qr_utils import generate_qr
from backend.attendance_logic import get_next_scan_type
from backend.email_utils import send_qr_email

router = APIRouter()

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
# ------------------ LOGIN ROUTE ------------------
@router.post("/admin/login")
def admin_login(
    response: Response,
    credentials: schemas.AdminLogin = Depends(schemas.AdminLogin.as_form)
):
    if credentials.username != ADMIN_USERNAME or credentials.password != ADMIN_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin credentials"
        )
    response.set_cookie(key="admin_logged_in", value="true", httponly=False, path="/")
    return {"message": "Login successful", "admin": credentials.username}


# ---------------- STUDENT REGISTER ----------------
@router.post("/admin/student/register", response_model=schemas.StudentResponse)
def register_student(
    data: schemas.StudentCreate = Depends(schemas.StudentCreate.as_form),
    db: Session = Depends(get_db)
):
    student = models.Student(
        name=data.name,
        email=data.email,
        roll_no=data.roll_no
    )

    db.add(student)
    db.commit()
    db.refresh(student)

    qr_code, qr_path = generate_qr(student.id)
    student.qr_code = qr_code
    db.commit()
    db.refresh(student)

    try:
        send_qr_email(
            to_email=student.email,
            student_name=student.name,
            qr_path=qr_path
        )
    except Exception as e:
        print("Email error:", e)

    return student


# ---------------- SESSION REGISTER ----------------
@router.post("/admin/session/create")
def create_session(
    data: schemas.SessionCreate = Depends(schemas.SessionCreate.as_form),
    db: Session = Depends(get_db)
):
    sessions_created = []

    for day in range(data.repeat_days):
        start = data.start_time + timedelta(days=day)
        end = data.end_time + timedelta(days=day)

        if not data.include_weekends and start.weekday() >= 5:
            continue

        session = models.Session(
            subject=data.subject,
            start_time=start,
            end_time=end
        )

        db.add(session)
        sessions_created.append(session)

    db.commit()
    return {"sessions_created": len(sessions_created)}


# ---------------- GET ALL SESSIONS ----------------
@router.get("/admin/session/all", response_model=list[schemas.SessionResponse])
def get_all_sessions(db: Session = Depends(get_db)):
    now = datetime.now()
    
    # Aaj ki saari sessions uthayein
    today_start = datetime.combine(now.date(), time.min)
    today_end = datetime.combine(now.date(), time.max)
    
    sessions = db.query(models.Session).filter(
        models.Session.start_time >= today_start,
        models.Session.start_time <= today_end
    ).all()

    for session in sessions:
        if now > session.end_time and session.status == models.SessionStatus.pending:
            session.status = models.SessionStatus.completed
            db.add(session)

        if now < session.start_time:
            session.attended_count = 0 
            count = 0
            all_students = db.query(models.Student).all()
            
            for student in all_students:
                last_log = db.query(models.AttendanceLog).filter(
                    models.AttendanceLog.student_id == student.id,
                    models.AttendanceLog.scan_time <= session.end_time
                ).order_by(models.AttendanceLog.scan_time.desc()).first()

                if last_log and last_log.scan_type == "IN":
                    count += 1
            
            session.attended_count = count

    db.commit()
    return sessions


@router.get("/admin/session/{session_id}/attendance", response_model=list[dict])
def get_session_attendance(session_id: int, db: Session = Depends(get_db)):
    session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    present_students = []
    all_students = db.query(models.Student).all()

    for student in all_students:
        last_log = db.query(models.AttendanceLog).filter(
            models.AttendanceLog.student_id == student.id,
            models.AttendanceLog.scan_time <= session.end_time
        ).order_by(models.AttendanceLog.scan_time.desc()).first()

        if last_log and last_log.scan_type == "IN":
            present_students.append({
                "name": student.name,
                "roll_no": student.roll_no,
                "scan_time": last_log.scan_time.strftime("%H:%M:%S")
            })

    return present_students


# ---------------- ATTENDANCE SCAN ----------------
@router.post("/attendance/scan", response_model=schemas.AttendanceResponse)
def scan_qr(
    data: schemas.QRScanRequest = Depends(schemas.QRScanRequest.as_form),
    db: Session = Depends(get_db)
):
    student = db.query(models.Student).filter(
        models.Student.qr_code == data.qr_code
    ).first()

    if not student:
        raise HTTPException(status_code=404, detail="Invalid QR")

    scan_type = get_next_scan_type(db, student.id)
    now = datetime.now()

    last_log = db.query(models.AttendanceLog).filter(
        models.AttendanceLog.student_id == student.id
    ).order_by(models.AttendanceLog.scan_time.desc()).first()

    if last_log and (now - last_log.scan_time).total_seconds() < 30:
        raise HTTPException(400, "Scan too fast. Wait 30 seconds.")

    log = models.AttendanceLog(
        student_id=student.id,
        scan_type=scan_type,
        scan_time=now
    )
    db.add(log)
    db.commit()

    return {
        "student_name": student.name,
        "scan_type": scan_type,
        "scan_time": now,
        "message": f"Successfully marked {scan_type}"
    }