from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

image_path = "Deep Learning\\image.png"
img = cv2.imread(image_path)

results = model(img)

annotated_frame = results[0].plot()

cv2.imshow("YOLO detection", annotated_frame )
cv2.waitKey(0)
cv2.destroyAllWindows()