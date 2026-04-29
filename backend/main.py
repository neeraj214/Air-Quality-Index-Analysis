from fastapi             import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses   import JSONResponse
from datetime            import datetime
import traceback

from config  import (
    APP_TITLE, APP_DESCRIPTION, APP_VERSION,
    ALLOWED_ORIGINS, CITIES, BUCKET_LABELS, FEATURE_COLS
)
from schemas import (
    PredictRequest, PredictResponse,
    BatchPredictRequest, BatchPredictResponse,
    HealthResponse, ModelInfoResponse
)
from predict import run_prediction, load_models
from contextlib import asynccontextmanager
from download_models import download_models

# -----------------------------------------------------------------------
# App Init & Lifespan
# -----------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    download_models()   # Step 1: download from HF Hub
    load_models()       # Step 2: load into memory
    yield

app = FastAPI(
    title       = APP_TITLE,
    description = APP_DESCRIPTION,
    version     = APP_VERSION,
    docs_url    = '/docs',
    redoc_url   = '/redoc',
    lifespan    = lifespan,
)

# -----------------------------------------------------------------------
# CORS
# -----------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins     = ALLOWED_ORIGINS,
    allow_credentials = True,
    allow_methods     = ['*'],
    allow_headers     = ['*'],
)

# -----------------------------------------------------------------------
# Global Exception Handler
# -----------------------------------------------------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            'error'  : 'Internal server error',
            'detail' : str(exc),
            'path'   : str(request.url),
        }
    )

# -----------------------------------------------------------------------
# GET /health
# -----------------------------------------------------------------------
@app.get('/health', response_model=HealthResponse, tags=['System'])
def health_check():
    return HealthResponse(
        status    = 'ok',
        version   = APP_VERSION,
        timestamp = datetime.utcnow().isoformat() + 'Z',
    )

# -----------------------------------------------------------------------
# GET /cities
# -----------------------------------------------------------------------
@app.get('/cities', tags=['Info'])
def get_cities():
    return {
        'cities' : CITIES,
        'count'  : len(CITIES),
    }

# -----------------------------------------------------------------------
# GET /models/info
# -----------------------------------------------------------------------
@app.get('/models/info', response_model=ModelInfoResponse, tags=['Info'])
def model_info():
    import predict as pred
    return ModelInfoResponse(
        regressor_type   = type(pred.regressor).__name__ if pred.regressor else 'Not Loaded',
        classifier_type  = type(pred.classifier).__name__ if pred.classifier else 'Not Loaded',
        feature_count    = len(FEATURE_COLS),
        supported_cities = CITIES,
        bucket_labels    = BUCKET_LABELS,
        model_version    = APP_VERSION,
    )

# -----------------------------------------------------------------------
# POST /predict
# -----------------------------------------------------------------------
@app.post('/predict', response_model=PredictResponse, tags=['Prediction'])
def predict(req: PredictRequest):
    try:
        result = run_prediction(req)
        return result
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f'Prediction failed: {str(e)}')

# -----------------------------------------------------------------------
# POST /predict/batch
# -----------------------------------------------------------------------
@app.post('/predict/batch', response_model=BatchPredictResponse,
          tags=['Prediction'])
def predict_batch(req: BatchPredictRequest):
    if len(req.predictions) > 20:
        raise HTTPException(
            status_code=400,
            detail='Batch size cannot exceed 20 predictions.'
        )
    try:
        results = [run_prediction(r) for r in req.predictions]
        return BatchPredictResponse(results=results, count=len(results))
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f'Batch prediction failed: {str(e)}')

# -----------------------------------------------------------------------
# GET / (root)
# -----------------------------------------------------------------------
@app.get('/', tags=['System'])
def root():
    return {
        'message'  : 'AQI Analysis API is running',
        'docs'     : '/docs',
        'health'   : '/health',
        'version'  : APP_VERSION,
    }
