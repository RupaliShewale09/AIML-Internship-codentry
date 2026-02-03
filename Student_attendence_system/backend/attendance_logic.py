from datetime import datetime
from sqlalchemy.orm import Session
from backend.models import AttendanceLog

def get_next_scan_type(db: Session, student_id: int):
    last = (
        db.query(AttendanceLog)
        .filter(AttendanceLog.student_id == student_id)
        .order_by(AttendanceLog.scan_time.desc())
        .first()
    )

    if not last or last.scan_type == "OUT":
        return "IN"
    return "OUT"


def mark_attendance_for_active_sessions(db: Session, student_id: int, scan_type: str, scan_time: datetime):
    from backend.models import Session as SessionModel
    
    active_sessions = db.query(SessionModel).filter(
        SessionModel.start_time <= scan_time,
        SessionModel.end_time >= scan_time
    ).all()
    
    for session in active_sessions:
        log = AttendanceLog(
            student_id=student_id,
            session_id=session.id,
            scan_type=scan_type,
            scan_time=scan_time
        )
        db.add(log)