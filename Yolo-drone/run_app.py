import subprocess
import sys
import time

print("🚀 Starting Drone Detection System...")

processes = []
try:
    print("\nStarting FastAPI backend...")
    backend = subprocess.Popen([
        sys.executable, "app/main.py"
    ])
    processes.append(backend)

    time.sleep(2)  # wait for backend

    print("Starting Streamlit dashboard...")
    frontend = subprocess.Popen([
        sys.executable, "-m", "streamlit", "run", "ui_app.py"
    ])
    processes.append(frontend)

    print("\n✅ System started successfully 🚀")
    print("Press CTRL+C to stop the system.")

    # Keep launcher alive
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\n🛑 Shutdown signal received...")

    for p in processes:
        p.terminate()   # graceful stop

    time.sleep(1)

    for p in processes:
        if p.poll() is None:
            p.kill()    # force kill if still running

    print("✅ System shut down cleanly.")
