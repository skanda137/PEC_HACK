import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor

# Load dataset
df = pd.read_csv(r"C:\SKANDA\Dataset_PEC.csv")

# Features and targets
feature_cols = ["heart_rate", "bp_sys", "bp_dia", "spo2", "temperature_C", "age"]
target_cols = ["blood_sugar_mg_dL", "resp_rate"]

X = df[feature_cols]
Y = df[target_cols]

# Train-test split
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.2, random_state=42
)

# Scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Model
base_model = RandomForestRegressor(
    n_estimators=300,
    random_state=42,
    n_jobs=-1
)

model = MultiOutputRegressor(base_model)
model.fit(X_train_scaled, Y_train)

# Save artifacts
joblib.dump(model, "multi_model.pkl")
joblib.dump(scaler, "multi_scaler.pkl")
joblib.dump(feature_cols, "multi_features.pkl")

import joblib

# Save trained model and scaler
joblib.dump(model, "multi_model.pkl")
joblib.dump(scaler, "multi_scaler.pkl")
joblib.dump(feature_cols, "multi_features.pkl")

print("Model, scaler, and features saved successfully")

from sklearn.metrics import mean_squared_error
import numpy as np

# Predict
preds = model.predict(X_test_scaled)

# Separate targets
y_test_blood = Y_test["blood_sugar_mg_dL"]
y_test_resp = Y_test["resp_rate"]

pred_blood = preds[:, 0]
pred_resp = preds[:, 1]

# MSE
mse_blood = mean_squared_error(y_test_blood, pred_blood)
mse_resp = mean_squared_error(y_test_resp, pred_resp)

# RMSE
rmse_blood = np.sqrt(mse_blood)
rmse_resp = np.sqrt(mse_resp)

print(f"Blood Sugar MSE: {mse_blood:.2f}")
print(f"Blood Sugar RMSE: {rmse_blood:.2f} mg/dL")

print(f"Resp Rate MSE: {mse_resp:.2f}")
print(f"Resp Rate RMSE: {rmse_resp:.2f} breaths/min")

