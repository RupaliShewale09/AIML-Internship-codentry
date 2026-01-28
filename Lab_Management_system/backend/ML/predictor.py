import joblib
import numpy as np

model = joblib.load("resources/Disease_pred.pkl")
encoder = joblib.load("resources/label_encoder.pkl")

def predict_disease(test_data: list):
    input_array = np.array([test_data])
    prediction = model.predict(input_array)
    predicted_disease = encoder.inverse_transform(prediction)[0]

    probabilities = model.predict_proba(input_array)[0]
    risk_scores = {encoder.classes_[i]: round(probabilities[i]*100,2) for i in range(len(encoder.classes_))}
    
    return predicted_disease, risk_scores
