"""
predict.py
Prediction logic using the loaded AQI model.
"""
import joblib
import os


def load_model(model_path: str):
    """Load a saved model from disk."""
    return joblib.load(model_path)


def predict_aqi(features: list, model_path: str, scaler_path: str):
    """Run prediction on input features and return AQI category."""
    model = load_model(model_path)
    scaler = load_model(scaler_path)
    scaled = scaler.transform([features])
    prediction = model.predict(scaled)
    return prediction[0]
