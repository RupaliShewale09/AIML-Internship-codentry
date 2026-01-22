# House Price Prediction

Simple machine learning project to predict house prices. The project includes **model training**, **testing**, and a **web app** for prediction.

---

## Project Structure

```
house_price_ml/
│
├── templates/              # HTML/CSS files for web UI
├── app.py                  # Main application file
├── price_ml.ipynb          # Model training notebook
├── house_test.py           # Model testing (not used in project)
├── house_price_dataset.csv # Dataset
└── house_price_pred.pkl    # Trained ML model
```

---

## Requirements

Install required libraries:

```bash
pip install pandas numpy scikit-learn flask
```

---

## Training the Model

1. Open `price_ml.ipynb`
2. Run all cells
3. The trained model will be saved as `house_price_pred.pkl`

---

## Run the Application

`app.py` is the **main file**.

```bash
python app.py
```

Then open browser and go to:

```
http://127.0.0.1:5000/
```

---

## Notes

* Model is trained using regression
* HTML/CSS files are inside the `templates` folder
* Dataset is included for reference

---

## Summary

* Training → `price_ml.ipynb`
* Model → `house_price_pred.pkl`
* Web App → `app.py`

This project is part of an **AI/ML Internship** and is intended for learning and demonstration purposes.
