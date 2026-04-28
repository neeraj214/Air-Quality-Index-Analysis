import numpy as np
import pandas as pd
import joblib
from datetime import datetime

from config import (
    BEST_REGRESSOR_PATH, BEST_CLASSIFIER_PATH,
    SCALER_PATH, CITY_ENCODER_PATH, BUCKET_MAP_PATH,
    FEATURE_COLS, BUCKET_LABELS, SEASON_MAP, HEALTH_ADVISORY
)
from schemas import PredictRequest, PredictResponse

# -----------------------------------------------------------------------
# Load models once at startup
# -----------------------------------------------------------------------
regressor   = joblib.load(BEST_REGRESSOR_PATH)
classifier  = joblib.load(BEST_CLASSIFIER_PATH)
scaler      = joblib.load(SCALER_PATH)
city_encoder = joblib.load(CITY_ENCODER_PATH)
bucket_map  = joblib.load(BUCKET_MAP_PATH)

# Reverse bucket map: encoded int → label string
reverse_bucket = {v: k for k, v in bucket_map.items()}

RISK_LEVELS = {
    'Good'        : 'Minimal',
    'Satisfactory': 'Low',
    'Moderate'    : 'Moderate',
    'Poor'        : 'High',
    'Very Poor'   : 'Very High',
    'Severe'      : 'Hazardous',
}

# -----------------------------------------------------------------------
# Feature Builder
# -----------------------------------------------------------------------
def build_feature_row(req: PredictRequest) -> np.ndarray:
    season    = SEASON_MAP.get(req.month, 0)
    is_winter = int(season == 0)

    try:
        city_encoded = city_encoder.transform([req.city])[0]
    except Exception:
        city_encoded = 0

    row = {
        'PM2.5'       : req.PM2_5,
        'PM10'        : req.PM10,
        'NO'          : req.NO,
        'NO2'         : req.NO2,
        'NOx'         : req.NOx,
        'NH3'         : req.NH3,
        'CO'          : req.CO,
        'SO2'         : req.SO2,
        'O3'          : req.O3,
        'Benzene'     : req.Benzene,
        'Toluene'     : req.Toluene,
        'Xylene'      : req.Xylene,
        'Month'       : req.month,
        'Season'      : season,
        'Is_Winter'   : is_winter,
        'City_Encoded': city_encoded,
    }

    df  = pd.DataFrame([row], columns=FEATURE_COLS)
    arr = scaler.transform(df)
    return arr

# -----------------------------------------------------------------------
# Single Prediction
# -----------------------------------------------------------------------
def run_prediction(req: PredictRequest) -> PredictResponse:
    features = build_feature_row(req)

    # Regression — AQI value
    aqi_raw       = float(regressor.predict(features)[0])
    aqi_predicted = round(max(0.0, min(500.0, aqi_raw)), 2)

    # Classification — AQI Bucket
    bucket_encoded = int(classifier.predict(features)[0])
    aqi_bucket     = reverse_bucket.get(bucket_encoded, 'Moderate')

    advisory   = HEALTH_ADVISORY.get(aqi_bucket, '')
    risk_level = RISK_LEVELS.get(aqi_bucket, 'Unknown')

    return PredictResponse(
        city            = req.city,
        month           = req.month,
        aqi_predicted   = aqi_predicted,
        aqi_bucket      = aqi_bucket,
        health_advisory = advisory,
        risk_level      = risk_level,
        timestamp       = datetime.utcnow().isoformat() + 'Z',
    )
