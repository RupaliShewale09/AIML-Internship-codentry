from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from backend.database import init_db
from backend.routes import router
import os
import uvicorn

# Initialize database (create tables)
init_db()

app = FastAPI(
    title="QR Attendance System",
    description="QR-based student attendance with session-wise tracking"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include all routes
app.include_router(router)

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):        
    return templates.TemplateResponse("admin.html", {"request": request})

@app.get("/scanner", response_class=HTMLResponse)
async def scanner_page(request: Request):
    return templates.TemplateResponse("scanner.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run( "backend.main:app", host="127.0.0.1", port=8000, reload=True)
