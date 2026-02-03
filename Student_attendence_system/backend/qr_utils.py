import qrcode
import os
import uuid

QR_DIR = "static/qr_codes" 

def generate_qr(student_id: int):
    os.makedirs(QR_DIR, exist_ok=True)

    unique_code = f"STD-{student_id}-{uuid.uuid4().hex[:8]}"
    path = os.path.join(QR_DIR, f"student_{student_id}.png")

    img = qrcode.make(unique_code)
    img.save(path)

    return unique_code, path