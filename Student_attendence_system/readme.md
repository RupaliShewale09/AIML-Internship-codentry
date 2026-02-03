# 🎓 QR-Based Student Attendance System

A modern, automated attendance tracking system built with **FastAPI** and **SQLite**. This system allows administrators to register students, generate unique QR codes, and manage attendance sessions, while students can mark their attendance simply by scanning their QR codes.

---

## 🚀 How to Start the System

### 1. Prerequisites

Ensure you have **Python 3.8+** installed.

Install the required dependencies:

```bash
pip install fastapi uvicorn sqlalchemy qrcode[pil] jinja2 python-multipart pydantic-settings
```

---

### 2. Run the Application

Navigate to the root directory (**Student_attendence_system**) and run:

```bash
python -m backend.main
```

The server will start at:

```
http://127.0.0.1:8000
```

---

## ✨ Features

### 🔐 Admin Management

* **Secure Login**
  Access the admin dashboard using default credentials:

  * Username: `admin`
  * Password: `admin123`

* **Student Registration**
  Register students with unique roll numbers and email IDs.

* **Automated QR Generation**
  A unique QR code is generated automatically for every student during registration.
  QR images are stored in:

  ```
  static/qr_codes/
  ```

* **Session Scheduling**
  Create single or recurring attendance sessions (for example, daily sessions for a week, with an option to exclude weekends).

* **Real-time Monitoring**
  View **Today's Sessions** and track how many students are currently marked **IN**.

---

### 📸 Attendance Scanner

* **QR Scanner**
  Built-in web-based QR scanner using **html5-qrcode**.

* **Smart Logging (IN / OUT)**
  Automatically toggles attendance status between **IN** and **OUT** based on the student’s last scan.

* **Anti-Spam Protection**
  Prevents accidental multiple scans by enforcing a **30-second cooldown** between consecutive scans.

---

### 📊 Attendance Tracking

* **Session-Wise Reports**
  View detailed attendance reports for each session, including:

  * Student name
  * Attendance status
  * Timestamp of scan

* **Database Persistence**
  All data is stored securely in a local **SQLite database**:

  ```
  attendance.db
  ```

---

## 🛠 Project Structure

```
Student_attendence_system/
│
├── backend/
│   ├── main.py          # Application entry point
│   ├── models.py        # Database models
│   ├── routes.py        # API routes and logic
│   ├── qr_utils.py      # QR code generation utilities
│   ├── schemas.py
│   ├── attendance_logic.py
│   ├── database.py
│
├── templates/
│   ├── login.html       # Admin login page
│   ├── admin.html   # Admin dashboard
│   ├── scanner.html    # QR scanner interface
│   └── base.html
│
├── static/
│   └── qr_codes/        # Generated student QR images
│
├── attendance.db        # SQLite database (auto-generated)
└── README.md
```

---

## ✅ Summary

This QR-Based Student Attendance System provides:

* Paperless attendance tracking
* Secure admin controls
* Real-time monitoring
* Reliable database-backed persistence

Designed to be **simple**, **efficient**, and **scalable** for educational institutions.
