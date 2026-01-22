from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

CONF_THRESHOLD = 0.87

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, stream=True)

    for r in results:
        frame = r.plot()

    cv2.imshow("YOLO Webcam", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()