import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")


def send_qr_email(to_email: str, student_name: str, qr_path: str):
    msg = EmailMessage()
    msg["From"] = SMTP_USER
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

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)

    print("Email sent successfully ✅")
