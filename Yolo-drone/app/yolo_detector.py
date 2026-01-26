from ultralytics import YOLO

class DroneDetector:
    def __init__(self):
        self.model = YOLO("yolo-drone/best.pt")

    def detect(self, frame):

        results = self.model(
            frame,
            conf=0.4,
            iou=0.5,
            imgsz=640,
            device="cpu"
        )

        drone_count = len(results[0].boxes)
        annotated_frame = results[0].plot()

        return annotated_frame, drone_count
