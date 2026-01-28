import joblib
import numpy as np
import pandas as pd

model = joblib.load("resources/Disease_pred.pkl")
encoder = joblib.load("resources/label_encoder.pkl")

# The exact order used in your training
SELECTED_FEATURES = [
    'Insulin', 'BMI', 'Cholesterol', 'Glucose', 'Hematocrit', 'Red Blood Cells', 
    'White Blood Cells', 'Platelets', 'Mean Corpuscular Volume', 
    'Mean Corpuscular Hemoglobin', 'Mean Corpuscular Hemoglobin Concentration', 'Hemoglobin'
]

def predict_disease(test_data: list):
    # Ensure exactly 12 features are received
    if len(test_data) != 12:
        raise ValueError(f"Expected 12 features, but received {len(test_data)}")

    # Convert to DataFrame to match training format and avoid warnings
    input_df = pd.DataFrame([test_data], columns=SELECTED_FEATURES)
    
    prediction = model.predict(input_df)
    predicted_disease = encoder.inverse_transform(prediction)[0]

    probabilities = model.predict_proba(input_df)[0]
    risk_scores = {encoder.classes_[i]: round(probabilities[i]*100, 2) for i in range(len(encoder.classes_))}
    
    return predicted_disease, risk_scores