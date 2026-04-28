from pydantic import BaseModel, Field, validator
from typing   import Optional, List
from datetime import datetime

# -----------------------------------------------------------------------
# INPUT SCHEMA
# -----------------------------------------------------------------------
class PredictRequest(BaseModel):
    city  : str   = Field(..., example='Delhi',
                          description='City name')
    month : int   = Field(..., ge=1, le=12,
                          description='Month (1-12)')
    PM2_5 : float = Field(..., ge=0, le=999,  alias='PM2.5',
                          description='PM2.5 in µg/m³')
    PM10  : float = Field(..., ge=0, le=999,
                          description='PM10 in µg/m³')
    NO    : float = Field(0.0, ge=0, le=500,
                          description='Nitric Oxide µg/m³')
    NO2   : float = Field(..., ge=0, le=500,
                          description='Nitrogen Dioxide µg/m³')
    NOx   : float = Field(0.0, ge=0, le=500,
                          description='Nitrogen Oxides µg/m³')
    NH3   : float = Field(0.0, ge=0, le=500,
                          description='Ammonia µg/m³')
    CO    : float = Field(..., ge=0, le=100,
                          description='Carbon Monoxide mg/m³')
    SO2   : float = Field(..., ge=0, le=500,
                          description='Sulphur Dioxide µg/m³')
    O3    : float = Field(..., ge=0, le=500,
                          description='Ozone µg/m³')
    Benzene : float = Field(0.0, ge=0, le=100,
                            description='Benzene µg/m³')
    Toluene : float = Field(0.0, ge=0, le=100,
                            description='Toluene µg/m³')
    Xylene  : float = Field(0.0, ge=0, le=100,
                            description='Xylene µg/m³')

    @validator('city')
    def validate_city(cls, v):
        allowed = ['Delhi', 'Bengaluru', 'Kolkata', 'Hyderabad']
        if v not in allowed:
            raise ValueError(f'City must be one of {allowed}')
        return v

    class Config:
        populate_by_name = True

# -----------------------------------------------------------------------
# OUTPUT SCHEMA
# -----------------------------------------------------------------------
class PredictResponse(BaseModel):
    city            : str
    month           : int
    aqi_predicted   : float
    aqi_bucket      : str
    health_advisory : str
    risk_level      : str
    timestamp       : str

# -----------------------------------------------------------------------
# BATCH SCHEMAS
# -----------------------------------------------------------------------
class BatchPredictRequest(BaseModel):
    predictions: List[PredictRequest]

class BatchPredictResponse(BaseModel):
    results : List[PredictResponse]
    count   : int

# -----------------------------------------------------------------------
# HEALTH & INFO SCHEMAS
# -----------------------------------------------------------------------
class HealthResponse(BaseModel):
    status    : str
    version   : str
    timestamp : str

class ModelInfoResponse(BaseModel):
    regressor_type   : str
    classifier_type  : str
    feature_count    : int
    supported_cities : List[str]
    bucket_labels    : List[str]
    model_version    : str
