from pydantic import BaseModel, EmailStr, Field, ValidationError
from datetime import datetime
from fastapi import Form
from fastapi.exceptions import RequestValidationError


# ---------------- ADMIN ----------------
class AdminLogin(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=5)

    @classmethod
    def as_form(
        cls,
        username: str = Form(...),
        password: str = Form(...)
    ):
        try:
            return cls(username=username, password=password)
        except ValidationError as e:
            raise RequestValidationError(e.errors())

# ---------------- STUDENT ----------------
class StudentCreate(BaseModel):
    name: str = Field(min_length=2)
    email: EmailStr
    roll_no: str = Field(min_length=1)

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        email: str = Form(...),
        roll_no: str = Form(...)
    ):
        try:
            return cls(name=name, email=email, roll_no=roll_no)
        except ValidationError as e:
            raise RequestValidationError(e.errors())


class StudentResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    roll_no: str
    qr_code: str

    class Config:
        from_attributes = True


# ---------------- SESSION ----------------
class SessionCreate(BaseModel):
    subject: str
    start_time: datetime
    end_time: datetime

    repeat_days: int = 1           # today only OR n days
    include_weekends: bool = True  # sat/sun on or off

    @classmethod
    def as_form(
        cls,
        subject: str = Form(...),
        start_time: datetime = Form(...),
        end_time: datetime = Form(...),
        repeat_days: int = Form(1),
        include_weekends: bool = Form(True)
    ):
        try:
            return cls(
                subject=subject, 
                start_time=start_time, 
                end_time=end_time, 
                repeat_days=repeat_days, 
                include_weekends=include_weekends
            )
        except ValidationError as e:
            raise RequestValidationError(e.errors())


class SessionResponse(BaseModel):
    id: int
    subject: str
    start_time: datetime
    end_time: datetime
    status: str
    attended_count: int

    class Config:
        from_attributes = True


# ---------------- ATTENDANCE ----------------
class QRScanRequest(BaseModel):
    qr_code: str

    @classmethod
    def as_form(
        cls,
        qr_code: str = Form(...)
    ):
        try:
            return cls(qr_code=qr_code)
        except ValidationError as e:
            raise RequestValidationError(e.errors())


class AttendanceResponse(BaseModel):
    student_name: str
    scan_type: str
    scan_time: datetime
    message: str
