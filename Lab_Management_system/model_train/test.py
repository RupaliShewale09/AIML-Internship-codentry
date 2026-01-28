import joblib
import numpy as np
import pandas as pd

model = joblib.load("resources/Disease_pred.pkl")
encoder = joblib.load("resources/label_encoder.pkl")

print("✅ Model and Label Encoder loaded successfully\n")

# The 12 features identified (MUST be in the same order as your training X columns)
# 1. Insulin, 2. BMI, 3. Cholesterol, 4. Glucose, 5. Hematocrit, 6. Red Blood Cells, 
# 7. White Blood Cells, 8. Platelets, 9. Mean Corpuscular Volume, 
# 10. Mean Corpuscular Hemoglobin, 11. Mean Corpuscular Hemoglobin Concentration, 12. Hemoglobin

# Test Case: Diabetes
sample_input1 = np.array([[0.3539, 0.6815, 0.9726, 0.4367, 0.7984, 0.5639, 0.6757, 0.1809, 0.6704, 0.3761, 0.1849, 0.0850]])

# Test Case: Anemia
sample_input2 = np.array([[0.0178, 0.5600, 0.0694, 0.4295, 0.1040, 0.1239, 0.4869, 0.3749, 0.6896, 0.7776, 0.3967, 0.5536]])

# Test Case: Heart Disease
sample_input3 = np.array([[0.3104, 0.4544, 0.3248, 0.5457, 0.9341, 0.6610, 0.5586, 0.4757, 0.3818, 0.5003, 0.5318, 0.5845]])

# Test Case: Thalassemia
sample_input4 = np.array([[0.6457, 0.0709, 0.0337, 0.0018, 0.5780, 0.8665, 0.5626, 0.9979, 0.9146, 0.0269, 0.0386, 0.1147]])

# Test Case: Healthy
sample_input5 = np.array([[0.6588, 0.6787, 0.4681, 0.3495, 0.7916, 0.8799, 0.6052, 0.2531, 0.4120, 0.7533, 0.2667, 0.7872]])


input = sample_input5

prediction = model.predict(input)
predicted_disease = encoder.inverse_transform(prediction)

print("\n🔹 PHASE 1: Disease Prediction")
print("Predicted Disease:", predicted_disease[0])
print("-" * 50)



probabilities = model.predict_proba(input)[0]

risk_scores = {
    encoder.classes_[i]: round(probabilities[i] * 100, 2)
    for i in range(len(encoder.classes_))
}

print("🔹 PHASE 2: Disease Risk Scores (%)")

for disease, risk in risk_scores.items():
    print(f"{disease}: {risk}%")

print("-" * 50)


risk_df = pd.DataFrame({
    "Disease": list(risk_scores.keys()),
    "Risk (%)": list(risk_scores.values())
}).sort_values(by="Risk (%)", ascending=False)

print("📊 Risk Score Table:")
print(risk_df)