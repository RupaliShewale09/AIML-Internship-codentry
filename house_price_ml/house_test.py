import joblib
import pandas as pd

model = joblib.load("MachineLearning\\house_price\\house_price_pred.pkl")

input_data = {
    "area_sqft" : 1300,
    "bedrooms" : 2,
    "bathrooms" : 2,
    "floors" : 3,
    "parking" : 1,
    "age_of_house" : 0
}

input_df = pd.DataFrame([input_data])
print(input_df)

predicted_price = model.predict(input_df)
print(predicted_price)