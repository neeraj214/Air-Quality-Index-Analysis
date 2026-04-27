import pandas as pd
import numpy as np
import os
import joblib
import warnings

from sklearn.preprocessing     import LabelEncoder, StandardScaler
from sklearn.model_selection   import train_test_split
from imblearn.over_sampling    import SMOTE

warnings.filterwarnings('ignore')

# -----------------------------------------------------------------------
# CONFIG
# -----------------------------------------------------------------------
CLEANED_PATH      = 'data/processed/cleaned.csv'
FEATURED_PATH     = 'data/processed/featured.csv'
PROCESSED_DIR     = 'data/processed/'
MODELS_DIR        = 'models/'

FEATURE_COLS = [
    'PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3',
    'CO', 'SO2', 'O3', 'Benzene', 'Toluene', 'Xylene',
    'Month', 'Season', 'Is_Winter', 'City_Encoded'
]

TARGET_REG   = 'AQI'
TARGET_CLF   = 'AQI_Bucket_Encoded'

# -----------------------------------------------------------------------
# STEP 1 -- Load Cleaned Data
# -----------------------------------------------------------------------
def load_cleaned(path):
    print("\n[1] Loading cleaned dataset...")
    df = pd.read_csv(path, parse_dates=['Date'])
    print(f"    Shape: {df.shape}")
    return df

# -----------------------------------------------------------------------
# STEP 2 -- DateTime Feature Engineering
# -----------------------------------------------------------------------
def add_datetime_features(df):
    print("\n[2] Adding datetime features...")
    df['Month']     = df['Date'].dt.month
    df['Year']      = df['Date'].dt.year
    df['DayOfWeek'] = df['Date'].dt.dayofweek

    season_map = {
        12: 0, 1: 0, 2: 0,   # Winter = 0
        3:  1, 4: 1, 5: 1,   # Spring = 1
        6:  2, 7: 2, 8: 2,   # Summer = 2
        9:  3, 10: 3, 11: 3  # Monsoon = 3
    }
    df['Season']    = df['Month'].map(season_map)
    df['Is_Winter'] = (df['Season'] == 0).astype(int)

    print(f"    Season distribution:\n{df['Season'].value_counts()}")
    return df

# -----------------------------------------------------------------------
# STEP 3 -- Encode Categorical Columns
# -----------------------------------------------------------------------
def encode_categoricals(df):
    print("\n[3] Encoding categorical columns...")
    os.makedirs(MODELS_DIR, exist_ok=True)

    # City encoding
    city_encoder = LabelEncoder()
    df['City_Encoded'] = city_encoder.fit_transform(df['City'])
    joblib.dump(city_encoder, f'{MODELS_DIR}city_encoder.joblib')
    city_mapping = dict(zip(city_encoder.classes_, city_encoder.transform(city_encoder.classes_)))
    print(f"    City mapping: {city_mapping}")

    # AQI_Bucket encoding (ordered)
    bucket_order   = ['Good', 'Satisfactory', 'Moderate',
                      'Poor', 'Very Poor', 'Severe']
    bucket_map     = {b: i for i, b in enumerate(bucket_order)}
    df['AQI_Bucket_Encoded'] = df['AQI_Bucket'].map(bucket_map)
    joblib.dump(bucket_map, f'{MODELS_DIR}bucket_map.joblib')
    print(f"    Bucket mapping: {bucket_map}")

    return df

# -----------------------------------------------------------------------
# STEP 4 -- Save Featured Dataset
# -----------------------------------------------------------------------
def save_featured(df, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"\n[4] Featured dataset saved to: {path}")

# -----------------------------------------------------------------------
# STEP 5 -- Train / Test Split
# -----------------------------------------------------------------------
def split_data(df):
    print("\n[5] Splitting into train/test sets (80/20 stratified)...")
    X = df[FEATURE_COLS]
    y_clf = df[TARGET_CLF]
    y_reg  = df[TARGET_REG]

    X_train, X_test, y_clf_train, y_clf_test, y_reg_train, y_reg_test = \
        train_test_split(
            X, y_clf, y_reg,
            test_size=0.2,
            random_state=42,
            stratify=y_clf
        )

    print(f"    Train size : {X_train.shape[0]}")
    print(f"    Test size  : {X_test.shape[0]}")
    print(f"    Train class distribution:\n{y_clf_train.value_counts()}")

    return X_train, X_test, y_clf_train, y_clf_test, y_reg_train, y_reg_test

# -----------------------------------------------------------------------
# STEP 6 -- Scale Features
# -----------------------------------------------------------------------
def scale_features(X_train, X_test):
    print("\n[6] Scaling features with StandardScaler...")
    scaler = StandardScaler()
    X_train_scaled = pd.DataFrame(
        scaler.fit_transform(X_train),
        columns=FEATURE_COLS
    )
    X_test_scaled = pd.DataFrame(
        scaler.transform(X_test),
        columns=FEATURE_COLS
    )
    joblib.dump(scaler, f'{MODELS_DIR}scaler.joblib')
    print(f"    Scaler saved to: {MODELS_DIR}scaler.joblib")
    return X_train_scaled, X_test_scaled

# -----------------------------------------------------------------------
# STEP 7 -- Apply SMOTE
# -----------------------------------------------------------------------
def apply_smote(X_train, y_train):
    print("\n[7] Applying SMOTE to balance AQI_Bucket classes...")
    print(f"    Before SMOTE:\n{y_train.value_counts()}")

    smote = SMOTE(random_state=42, k_neighbors=5)
    X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

    X_resampled = pd.DataFrame(X_resampled, columns=FEATURE_COLS)
    y_resampled = pd.Series(y_resampled, name=TARGET_CLF)

    print(f"\n    After SMOTE:\n{y_resampled.value_counts()}")
    print(f"    Resampled shape : {X_resampled.shape}")
    return X_resampled, y_resampled

# -----------------------------------------------------------------------
# STEP 8 -- Save All Splits
# -----------------------------------------------------------------------
def save_splits(X_train, X_test, y_clf_train, y_clf_test,
                y_reg_train, y_reg_test, X_res, y_res):
    print("\n[8] Saving all splits to data/processed/...")
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    X_train.to_csv(f'{PROCESSED_DIR}X_train.csv',               index=False)
    X_test.to_csv( f'{PROCESSED_DIR}X_test.csv',                index=False)
    y_clf_train.to_csv(f'{PROCESSED_DIR}y_clf_train.csv',       index=False)
    y_clf_test.to_csv( f'{PROCESSED_DIR}y_clf_test.csv',        index=False)
    y_reg_train.to_csv(f'{PROCESSED_DIR}y_reg_train.csv',       index=False)
    y_reg_test.to_csv( f'{PROCESSED_DIR}y_reg_test.csv',        index=False)
    X_res.to_csv(      f'{PROCESSED_DIR}X_train_resampled.csv', index=False)
    y_res.to_csv(      f'{PROCESSED_DIR}y_train_resampled.csv', index=False)

    print("    All splits saved successfully.")

# -----------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("PHASE 2 -- Feature Engineering + SMOTE")
    print("=" * 60)

    df = load_cleaned(CLEANED_PATH)
    df = add_datetime_features(df)
    df = encode_categoricals(df)
    save_featured(df, FEATURED_PATH)

    X_train, X_test, y_clf_train, y_clf_test, \
    y_reg_train, y_reg_test = split_data(df)

    X_train_scaled, X_test_scaled = scale_features(X_train, X_test)
    X_res, y_res = apply_smote(X_train_scaled, y_clf_train)

    save_splits(
        X_train_scaled, X_test_scaled,
        y_clf_train, y_clf_test,
        y_reg_train, y_reg_test,
        X_res, y_res
    )

    print("\n" + "=" * 60)
    print("Feature Engineering + SMOTE complete.")
    print("Next: Run src/model_training.py")
    print("=" * 60)
