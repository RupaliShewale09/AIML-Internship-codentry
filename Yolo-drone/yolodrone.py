import cv2
from ultralytics import YOLO

# Load your trained model
model = YOLO("Yolo-drone\\best.pt")   # <-- path to your trained model

# Open webcam (0 = default camera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Webcam not accessible")
    exit()

print("✅ Webcam started. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLOv8 inference
    results = model(
        frame,
        conf=0.4,        # confidence threshold
        iou=0.5,
        imgsz=640,
        device="cpu"     # use "0" for GPU if available
    )

    # Plot results on frame
    annotated_frame = results[0].plot()

    # Show output
    cv2.imshow("YOLOv8 Drone Detection", annotated_frame)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()