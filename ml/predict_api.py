# predict_api.py

from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

# Create FastAPI app
app = FastAPI(title="PEC ML Prediction API")

# Load trained artifacts
model = joblib.load("multi_model.pkl")
scaler = joblib.load("multi_scaler.pkl")
feature_cols = joblib.load("multi_features.pkl")

# Input schema
class PredictionInput(BaseModel):
    heart_rate: int
    bp_sys: int
    bp_dia: int
    spo2: int
    temperature_c: float
    age: int

# Prediction endpoint
@app.post("/predict")
def predict(data: PredictionInput):
    # Arrange input in correct order
    X = np.array([[
        data.heart_rate,
        data.bp_sys,
        data.bp_dia,
        data.spo2,
        data.temperature_c,
        data.age
    ]])

    # Scale and predict
    X_scaled = scaler.transform(X)
    pred_blood, pred_resp = model.predict(X_scaled)[0]

    # Return predictions
    return {
        "predicted_blood_sugar": round(float(pred_blood), 2),
        "predicted_resp_rate": round(float(pred_resp), 2)
    }
