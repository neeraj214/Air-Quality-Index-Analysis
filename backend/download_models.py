import os
from huggingface_hub import hf_hub_download
from pathlib import Path

HF_USERNAME = os.getenv('HF_USERNAME', 'Neeraj214')
REPO_ID     = f'{HF_USERNAME}/aqi-analysis-models'
MODELS_DIR  = Path('models')

MODEL_FILES = [
    'best_regressor.joblib',
    'best_classifier.joblib',
    'scaler.joblib',
    'city_encoder.joblib',
    'bucket_map.joblib',
]

def download_models():
    MODELS_DIR.mkdir(exist_ok=True)
    print(f"Downloading models from: {REPO_ID}")
    for filename in MODEL_FILES:
        dest = MODELS_DIR / filename
        if dest.exists():
            print(f"  ✅ Already exists: {filename}")
            continue
        print(f"  Downloading {filename}...")
        hf_hub_download(
            repo_id   = REPO_ID,
            filename  = filename,
            repo_type = 'model',
            local_dir = str(MODELS_DIR),
        )
        print(f"  ✅ Downloaded: {filename}")
    print("All models ready.")

if __name__ == "__main__":
    download_models()
