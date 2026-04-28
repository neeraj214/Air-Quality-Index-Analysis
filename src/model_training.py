import pandas as pd
import numpy as np
import os
import joblib
import warnings
import time

from sklearn.linear_model    import LinearRegression, LogisticRegression
from sklearn.ensemble        import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics         import (
    mean_absolute_error, mean_squared_error, r2_score,
    accuracy_score, f1_score, classification_report
)
from xgboost                 import XGBRegressor, XGBClassifier
from lightgbm                import LGBMRegressor, LGBMClassifier

warnings.filterwarnings('ignore')

# -----------------------------------------------------------------------
# CONFIG
# -----------------------------------------------------------------------
PROCESSED_DIR = 'data/processed/'
MODELS_DIR    = 'models/'
REPORTS_DIR   = 'reports/'
RANDOM_STATE  = 42

os.makedirs(MODELS_DIR,  exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

# -----------------------------------------------------------------------
# STEP 1 — Load All Splits
# -----------------------------------------------------------------------
def load_splits():
    print("\n[1] Loading train/test splits...")

    X_train     = pd.read_csv(f'{PROCESSED_DIR}X_train.csv')
    X_test      = pd.read_csv(f'{PROCESSED_DIR}X_test.csv')
    y_clf_train = pd.read_csv(f'{PROCESSED_DIR}y_clf_train.csv').squeeze()
    y_clf_test  = pd.read_csv(f'{PROCESSED_DIR}y_clf_test.csv').squeeze()
    y_reg_train = pd.read_csv(f'{PROCESSED_DIR}y_reg_train.csv').squeeze()
    y_reg_test  = pd.read_csv(f'{PROCESSED_DIR}y_reg_test.csv').squeeze()
    X_resampled = pd.read_csv(f'{PROCESSED_DIR}X_train_resampled.csv')
    y_resampled = pd.read_csv(f'{PROCESSED_DIR}y_train_resampled.csv').squeeze()

    print(f"    X_train shape         : {X_train.shape}")
    print(f"    X_test shape          : {X_test.shape}")
    print(f"    X_resampled shape     : {X_resampled.shape}")
    print(f"    y_resampled classes   : {y_resampled.value_counts().to_dict()}")

    return (X_train, X_test,
            y_clf_train, y_clf_test,
            y_reg_train, y_reg_test,
            X_resampled, y_resampled)

# -----------------------------------------------------------------------
# STEP 2 — Regression Models
# -----------------------------------------------------------------------
def train_regression_models(X_train, X_test, y_train, y_test):
    print("\n[2] Training Regression Models...")
    print("-" * 50)

    models = {
        'LinearRegression' : LinearRegression(),
        'RandomForest'     : RandomForestRegressor(
                                n_estimators=200,
                                max_depth=15,
                                min_samples_split=5,
                                random_state=RANDOM_STATE,
                                n_jobs=-1
                            ),
        'XGBoost'          : XGBRegressor(
                                n_estimators=300,
                                learning_rate=0.05,
                                max_depth=6,
                                subsample=0.8,
                                colsample_bytree=0.8,
                                random_state=RANDOM_STATE,
                                verbosity=0
                            ),
        'LightGBM'         : LGBMRegressor(
                                n_estimators=300,
                                learning_rate=0.05,
                                max_depth=6,
                                num_leaves=63,
                                random_state=RANDOM_STATE,
                                verbosity=-1,
                                n_jobs=-1
                            ),
    }

    results = []
    trained = {}

    for name, model in models.items():
        print(f"\n    Training {name}...")
        start = time.time()
        model.fit(X_train, y_train)
        elapsed = time.time() - start

        y_pred = model.predict(X_test)
        mae    = mean_absolute_error(y_test, y_pred)
        rmse   = np.sqrt(mean_squared_error(y_test, y_pred))
        r2     = r2_score(y_test, y_pred)

        print(f"    MAE  : {mae:.3f}")
        print(f"    RMSE : {rmse:.3f}")
        print(f"    R²   : {r2:.4f}")
        print(f"    Time : {elapsed:.1f}s")

        filename = name.lower().replace(' ', '_') + '_regressor'
        joblib.dump(model, f'{MODELS_DIR}{filename}.joblib')
        print(f"    Saved: models/{filename}.joblib")

        results.append({
            'Model'    : name,
            'Type'     : 'Regression',
            'MAE'      : round(mae,  3),
            'RMSE'     : round(rmse, 3),
            'R2'       : round(r2,   4),
            'Time(s)'  : round(elapsed, 1),
        })
        trained[name] = (model, r2)

    # Save best regressor
    best_name  = max(trained, key=lambda k: trained[k][1])
    best_model = trained[best_name][0]
    joblib.dump(best_model, f'{MODELS_DIR}best_regressor.joblib')
    print(f"\n    [BEST] Best Regressor : {best_name} (R²={trained[best_name][1]:.4f})")
    print(f"    Saved: models/best_regressor.joblib")

    return results, best_name

# -----------------------------------------------------------------------
# STEP 3 — Classification Models (trained on SMOTE resampled data)
# -----------------------------------------------------------------------
def train_classification_models(X_train, X_test, y_train, y_test):
    print("\n[3] Training Classification Models (on SMOTE data)...")
    print("-" * 50)

    models = {
        'LogisticRegression' : LogisticRegression(
                                   max_iter=1000,
                                   random_state=RANDOM_STATE,
                                   n_jobs=-1
                               ),
        'RandomForest'       : RandomForestClassifier(
                                   n_estimators=200,
                                   max_depth=15,
                                   min_samples_split=5,
                                   random_state=RANDOM_STATE,
                                   n_jobs=-1
                               ),
        'XGBoost'            : XGBClassifier(
                                   n_estimators=300,
                                   learning_rate=0.05,
                                   max_depth=6,
                                   subsample=0.8,
                                   colsample_bytree=0.8,
                                   use_label_encoder=False,
                                   eval_metric='mlogloss',
                                   random_state=RANDOM_STATE,
                                   verbosity=0
                               ),
        'LightGBM'           : LGBMClassifier(
                                   n_estimators=300,
                                   learning_rate=0.05,
                                   max_depth=6,
                                   num_leaves=63,
                                   random_state=RANDOM_STATE,
                                   verbosity=-1,
                                   n_jobs=-1
                               ),
    }

    results  = []
    trained  = {}

    for name, model in models.items():
        print(f"\n    Training {name}...")
        start = time.time()
        model.fit(X_train, y_train)
        elapsed = time.time() - start

        y_pred   = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        f1_macro = f1_score(y_test, y_pred, average='macro')
        f1_weighted = f1_score(y_test, y_pred, average='weighted')

        print(f"    Accuracy    : {accuracy:.4f}")
        print(f"    F1 (macro)  : {f1_macro:.4f}")
        print(f"    F1 (weighted): {f1_weighted:.4f}")
        print(f"    Time        : {elapsed:.1f}s")

        filename = name.lower().replace(' ', '_') + '_classifier'
        joblib.dump(model, f'{MODELS_DIR}{filename}.joblib')
        print(f"    Saved: models/{filename}.joblib")

        results.append({
            'Model'        : name,
            'Type'         : 'Classification',
            'Accuracy'     : round(accuracy,    4),
            'F1_Macro'     : round(f1_macro,    4),
            'F1_Weighted'  : round(f1_weighted, 4),
            'Time(s)'      : round(elapsed, 1),
        })
        trained[name] = (model, f1_macro)

    # Save best classifier
    best_name  = max(trained, key=lambda k: trained[k][1])
    best_model = trained[best_name][0]
    joblib.dump(best_model, f'{MODELS_DIR}best_classifier.joblib')
    print(f"\n    [BEST] Best Classifier : {best_name} (F1={trained[best_name][1]:.4f})")
    print(f"    Saved: models/best_classifier.joblib")

    return results, best_name

# -----------------------------------------------------------------------
# STEP 4 — Print Classification Report for Best Model
# -----------------------------------------------------------------------
def print_best_clf_report(X_train, X_test, y_train, y_test, best_name):
    print(f"\n[4] Detailed Classification Report — {best_name}")
    print("-" * 50)
    model = joblib.load(f'{MODELS_DIR}best_classifier.joblib')
    y_pred = model.predict(X_test)
    bucket_labels = ['Good', 'Satisfactory', 'Moderate',
                     'Poor', 'Very Poor', 'Severe']
    print(classification_report(
        y_test, y_pred,
        target_names=bucket_labels,
        zero_division=0
    ))

# -----------------------------------------------------------------------
# STEP 5 — Save Comparison Table
# -----------------------------------------------------------------------
def save_comparison_table(reg_results, clf_results):
    print("\n[5] Saving model comparison table...")

    reg_df = pd.DataFrame(reg_results)
    clf_df = pd.DataFrame(clf_results)

    # Merge into one table (fill missing cols with NaN)
    comparison = pd.concat([reg_df, clf_df], ignore_index=True)
    comparison.to_csv(f'{REPORTS_DIR}model_comparison.csv', index=False)
    print(f"    Saved: reports/model_comparison.csv")

    print("\n--- Regression Results ---")
    print(reg_df[['Model', 'MAE', 'RMSE', 'R2', 'Time(s)']].to_string(index=False))

    print("\n--- Classification Results ---")
    print(clf_df[['Model', 'Accuracy', 'F1_Macro',
                  'F1_Weighted', 'Time(s)']].to_string(index=False))

# -----------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("PHASE 3 — Model Training")
    print("=" * 60)

    (X_train, X_test,
     y_clf_train, y_clf_test,
     y_reg_train, y_reg_test,
     X_resampled, y_resampled) = load_splits()

    reg_results, best_reg  = train_regression_models(
        X_train, X_test, y_reg_train, y_reg_test
    )

    clf_results, best_clf  = train_classification_models(
        X_resampled, X_test, y_resampled, y_clf_test
    )

    print_best_clf_report(
        X_resampled, X_test, y_resampled, y_clf_test, best_clf
    )

    save_comparison_table(reg_results, clf_results)

    print("\n" + "=" * 60)
    print(f"Training complete.")
    print(f"Best Regressor  : {best_reg}")
    print(f"Best Classifier : {best_clf}")
    print("Next: Run src/model_evaluation.py")
    print("=" * 60)
