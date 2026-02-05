import os
import smtplib
from email.message import EmailMessage
from backend.config import settings


def send_qr_email(to_email: str, student_name: str, qr_path: str):
    msg = EmailMessage()
    msg["From"] = settings.SMTP_USER
    msg["To"] = to_email
    msg["Subject"] = "Your Attendance QR Code"
    
    body = f"""
        Hello {student_name},

        Your registration is successful.
        Please find your QR code attached.

        Use this QR for attendance scanning.

        Regards,
        Admin
        """
    msg.set_content(body)

    with open(qr_path, "rb") as f:
        qr_data = f.read()

    msg.add_attachment(
        qr_data,
        maintype="image",
        subtype="png",
        filename="attendance_qr.png"
    )

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg)

    print("Email sent successfully ✅")
