from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

# Load trained model
model = joblib.load("house_price_ml\\house_price_pred.pkl")

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")

@app.route("/predict", methods=["GET", "POST"])
def index():
    predicted_price = None

    if request.method == "POST":
        input_data = {
            "area_sqft": float(request.form["area_sqft"]),
            "bedrooms": int(request.form["bedrooms"]),
            "bathrooms": int(request.form["bathrooms"]),
            "floors": int(request.form["floors"]),
            "parking": int(request.form["parking"]),
            "age_of_house": int(request.form["age_of_house"])
        }

        input_df = pd.DataFrame([input_data])
        predicted_price = model.predict(input_df)[0]

        predicted_price = round(predicted_price, 2)

    return render_template("index.html", predicted_price=predicted_price)


if __name__ == "__main__":
    app.run(debug=True)
