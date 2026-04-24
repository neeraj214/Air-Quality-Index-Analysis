"""
main.py
FastAPI application entry point for AQI prediction backend.
"""
from fastapi import FastAPI

app = FastAPI(title="AQI Prediction API", version="1.0.0")


@app.get("/")
def root():
    return {"message": "AQI Prediction API is running"}
