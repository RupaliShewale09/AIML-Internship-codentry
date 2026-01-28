from passlib.context import CryptContext
from backend.ML.predictor import predict_disease

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# ML Prediction wrapper
def get_disease_prediction(test_data: list):
    predicted_disease, risk_scores = predict_disease(test_data)
    return predicted_disease, risk_scores
