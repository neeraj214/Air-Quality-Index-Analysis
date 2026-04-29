import os
from pathlib import Path

# Model paths
MODELS_DIR           = '/app/models'
BEST_REGRESSOR_PATH  = f'{MODELS_DIR}/best_regressor.joblib'
BEST_CLASSIFIER_PATH = f'{MODELS_DIR}/best_classifier.joblib'
SCALER_PATH          = f'{MODELS_DIR}/scaler.joblib'
CITY_ENCODER_PATH    = f'{MODELS_DIR}/city_encoder.joblib'
BUCKET_MAP_PATH      = f'{MODELS_DIR}/bucket_map.joblib'

# App config
APP_TITLE       = 'AQI Analysis API'
APP_DESCRIPTION = 'Air Quality Index prediction API for Indian cities'
APP_VERSION     = '1.0.0'

# CORS origins (add Vercel URL here after deployment)
ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://localhost:3000',
    'https://*.vercel.app',
    'https://neeraj214-aqi-analysis-backend.hf.space',
]

# Feature columns (must match Phase 2 exactly)
FEATURE_COLS = [
    'PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3',
    'CO', 'SO2', 'O3', 'Benzene', 'Toluene', 'Xylene',
    'Month', 'Season', 'Is_Winter', 'City_Encoded'
]

# AQI bucket labels in encoded order
BUCKET_LABELS = ['Good', 'Satisfactory', 'Moderate',
                 'Poor', 'Very Poor', 'Severe']

# City list
CITIES = ['Delhi', 'Bengaluru', 'Kolkata', 'Hyderabad']

# Season mapping
SEASON_MAP = {
    12: 0, 1: 0, 2: 0,
    3:  1, 4: 1, 5: 1,
    6:  2, 7: 2, 8: 2,
    9:  3, 10: 3, 11: 3
}

# Health advisories
HEALTH_ADVISORY = {
    'Good'        : 'Air quality is satisfactory. Enjoy outdoor activities.',
    'Satisfactory': 'Acceptable air quality. Sensitive groups limit exertion.',
    'Moderate'    : 'Sensitive groups may experience health effects.',
    'Poor'        : 'Everyone may experience health effects. Limit outdoor activity.',
    'Very Poor'   : 'Health alert. Everyone may experience serious effects.',
    'Severe'      : 'Emergency conditions. Avoid all outdoor activity.',
}
