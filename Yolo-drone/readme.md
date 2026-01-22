# YOLO Drone Detection

Simple steps to **train** and **run prediction**.

---

## Requirements

```bash
pip install ultralytics opencv-python
```

---

## Training (Google Colab)

1. Open **`yolo_drone_train.ipynb`** in Google Colab
2. Upload / mount your dataset as mentioned in the notebook
3. Run all cells
4. After training, download the generated **`best.pt`** file

> Training is done on Colab because GPU is available there.

---

## Prediction (VS Code / Local System)

1. Place **`best.pt`** inside the project folder
2. Make sure webcam is connected
3. Run:

```bash
python yolodrone.py
```

4. Press **`q`** to stop the webcam

---

## Notes

* If you don’t have GPU, the code will run on **CPU**
* Update the model path in code if folder name changes

---

## Files

* `yolo_drone_train.ipynb` → Training (Colab)
* `yolodrone.py` → Real-time prediction using webcam
* `best.pt` → Trained YOLOv8 model 
