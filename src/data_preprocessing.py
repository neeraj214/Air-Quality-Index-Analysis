import pandas as pd
import numpy as np
import os
import warnings

warnings.filterwarnings('ignore')

# -----------------------------------------------------------------------
# CONFIG
# -----------------------------------------------------------------------
RAW_PATH       = 'data/raw/city_day.csv'
PROCESSED_PATH = 'data/processed/cleaned.csv'
TARGET_CITIES  = ['Delhi', 'Bengaluru', 'Kolkata', 'Hyderabad']

POLLUTANT_COLS = [
    'PM2.5', 'PM10', 'NO', 'NO2', 'NOx',
    'NH3', 'CO', 'SO2', 'O3', 'Benzene', 'Toluene', 'Xylene'
]

# -----------------------------------------------------------------------
# STEP 1 -- Load Data
# -----------------------------------------------------------------------
def load_data(path):
    print("\n[1] Loading dataset...")
    df = pd.read_csv(path, parse_dates=['Date'])
    print(f"    Raw shape       : {df.shape}")
    print(f"    Columns         : {list(df.columns)}")
    return df

# -----------------------------------------------------------------------
# STEP 2 -- Filter Target Cities
# -----------------------------------------------------------------------
def filter_cities(df, cities):
    print("\n[2] Filtering target cities...")
    df = df[df['City'].isin(cities)].copy()
    print(f"    Filtered shape  : {df.shape}")
    print(f"    Cities retained : {df['City'].unique()}")
    return df

# -----------------------------------------------------------------------
# STEP 3 -- Drop Rows With No AQI Target
# -----------------------------------------------------------------------
def drop_missing_target(df):
    print("\n[3] Dropping rows with missing AQI or AQI_Bucket...")
    before = len(df)
    df = df.dropna(subset=['AQI', 'AQI_Bucket'])
    after  = len(df)
    print(f"    Dropped         : {before - after} rows")
    print(f"    Remaining       : {after} rows")
    return df

# -----------------------------------------------------------------------
# STEP 4 -- Impute Missing Pollutant Values
# -----------------------------------------------------------------------
def impute_pollutants(df):
    print("\n[4] Imputing missing pollutant values (city-wise median)...")
    for col in POLLUTANT_COLS:
        if col in df.columns:
            missing_before = df[col].isnull().sum()
            df[col] = df.groupby('City')[col].transform(
                lambda x: x.fillna(x.median())
            )
            # fallback: global median if city median is also NaN
            df[col] = df[col].fillna(df[col].median())
            missing_after = df[col].isnull().sum()
            if missing_before > 0:
                print(f"    {col:<12}: {missing_before} -> {missing_after} missing")
    return df

# -----------------------------------------------------------------------
# STEP 5 -- Remove Outliers (IQR Method on AQI)
# -----------------------------------------------------------------------
def remove_outliers(df):
    print("\n[5] Removing AQI outliers using IQR method...")
    before = len(df)
    Q1  = df['AQI'].quantile(0.25)
    Q3  = df['AQI'].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 3.0 * IQR
    upper = Q3 + 3.0 * IQR
    df = df[(df['AQI'] >= lower) & (df['AQI'] <= upper)]
    print(f"    IQR bounds      : [{lower:.1f}, {upper:.1f}]")
    print(f"    Removed         : {before - len(df)} rows")
    print(f"    Remaining       : {len(df)} rows")
    return df

# -----------------------------------------------------------------------
# STEP 6 -- Clean AQI_Bucket Labels
# -----------------------------------------------------------------------
def clean_bucket_labels(df):
    print("\n[6] Cleaning AQI_Bucket labels...")
    df['AQI_Bucket'] = df['AQI_Bucket'].str.strip()
    valid_buckets = ['Good', 'Satisfactory', 'Moderate',
                     'Poor', 'Very Poor', 'Severe']
    before = len(df)
    df = df[df['AQI_Bucket'].isin(valid_buckets)]
    print(f"    Dropped invalid : {before - len(df)} rows")
    print(f"    Class counts    :\n{df['AQI_Bucket'].value_counts()}")
    return df

# -----------------------------------------------------------------------
# STEP 7 -- Save Cleaned Data
# -----------------------------------------------------------------------
def save_cleaned(df, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"\n[7] Cleaned data saved to: {path}")
    print(f"    Final shape     : {df.shape}")

# -----------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("PHASE 2 -- Data Preprocessing")
    print("=" * 60)

    df = load_data(RAW_PATH)
    df = filter_cities(df, TARGET_CITIES)
    df = drop_missing_target(df)
    df = impute_pollutants(df)
    df = remove_outliers(df)
    df = clean_bucket_labels(df)
    save_cleaned(df, PROCESSED_PATH)

    print("\n" + "=" * 60)
    print("Preprocessing complete. Run feature_engineering.py next.")
    print("=" * 60)
