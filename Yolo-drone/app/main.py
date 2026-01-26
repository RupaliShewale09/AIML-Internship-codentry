from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import cv2
import uvicorn
from camera import VideoCamera
from yolo_detector import DroneDetector
import time

app = FastAPI(title="Drone Detection System")

camera = VideoCamera()
detector = DroneDetector()

# Shared stats
drone_count = 0
fps = 0.0

def generate_frames():
    global drone_count, fps
    prev_time = time.time()
    while True:
        frame = camera.get_frame()
        if frame is None:
            break

        annotated, count = detector.detect(frame)
        drone_count = count

        # Calculate FPS
        curr_time = time.time()
        fps = round(1 / (curr_time - prev_time), 2)
        prev_time = curr_time

        _, buffer = cv2.imencode(".jpg", annotated)
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + buffer.tobytes()
            + b"\r\n"
        )

@app.get("/video")
def video_feed():
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

@app.get("/stats")
def get_stats():
    return {"drone_count": drone_count, "fps": fps}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
