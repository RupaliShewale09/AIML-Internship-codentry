from sqlalchemy import (
    Column, Integer, String, DateTime,
    ForeignKey, Enum
)
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base
import enum


class SessionStatus(enum.Enum):
    pending = "pending"
    completed = "completed"

# ---------------- STUDENT ----------------
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    roll_no = Column(String, unique=True, index=True, nullable=False)

    qr_code = Column(String, unique=True, nullable=True)

    attendance_logs = relationship("AttendanceLog", back_populates="student")


# ---------------- SESSION ----------------
class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    status = Column(
        Enum(SessionStatus),
        default=SessionStatus.pending
    )

    attended_count = Column(Integer, default=0)

    attendance_logs = relationship("AttendanceLog", back_populates="session")


# ---------------- ATTENDANCE LOG ----------------
class AttendanceLog(Base):
    __tablename__ = "attendance_logs"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("students.id"))
    session_id = Column(Integer, ForeignKey("sessions.id"))

    scan_type = Column(String)   # IN / OUT
    scan_time = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="attendance_logs")
    session = relationship("Session", back_populates="attendance_logs")
