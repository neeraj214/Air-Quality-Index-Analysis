import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import joblib
import shap
import warnings
import os

from sklearn.metrics import (
    confusion_matrix, classification_report,
    mean_absolute_error, mean_squared_error, r2_score,
    accuracy_score, f1_score
)

warnings.filterwarnings('ignore')
sns.set_theme(style='darkgrid', palette='muted')
plt.rcParams['figure.dpi'] = 120

# -----------------------------------------------------------------------
# CONFIG
# -----------------------------------------------------------------------
MODELS_DIR    = 'models/'
REPORTS_DIR   = 'reports/'
FIGURES_DIR   = 'reports/figures/'
PROCESSED_DIR = 'data/processed/'

FEATURE_COLS  = [
    'PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3',
    'CO', 'SO2', 'O3', 'Benzene', 'Toluene', 'Xylene',
    'Month', 'Season', 'Is_Winter', 'City_Encoded'
]

BUCKET_LABELS = ['Good', 'Satisfactory', 'Moderate',
                 'Poor', 'Very Poor', 'Severe']
BUCKET_COLORS = ['#2ecc71', '#a8d08d', '#f9c74f',
                 '#f77f00', '#d62828', '#6a040f']

os.makedirs(FIGURES_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

# -----------------------------------------------------------------------
# STEP 1 — Load Data & Models
# -----------------------------------------------------------------------
def load_all():
    print("\n[1] Loading data and models...")

    X_train     = pd.read_csv(f'{PROCESSED_DIR}X_train.csv')
    X_test      = pd.read_csv(f'{PROCESSED_DIR}X_test.csv')
    y_clf_test  = pd.read_csv(f'{PROCESSED_DIR}y_clf_test.csv').squeeze()
    y_reg_test  = pd.read_csv(f'{PROCESSED_DIR}y_reg_test.csv').squeeze()
    X_resampled = pd.read_csv(f'{PROCESSED_DIR}X_train_resampled.csv')
    y_resampled = pd.read_csv(f'{PROCESSED_DIR}y_train_resampled.csv').squeeze()
    comparison  = pd.read_csv(f'{REPORTS_DIR}model_comparison.csv')

    best_reg    = joblib.load(f'{MODELS_DIR}best_regressor.joblib')
    best_clf    = joblib.load(f'{MODELS_DIR}best_classifier.joblib')

    all_regressors = {
        'Linear Regression' : joblib.load(f'{MODELS_DIR}lr_regressor.joblib'),
        'Random Forest'     : joblib.load(f'{MODELS_DIR}rf_regressor.joblib'),
        'XGBoost'           : joblib.load(f'{MODELS_DIR}xgb_regressor.joblib'),
        'LightGBM'          : joblib.load(f'{MODELS_DIR}lgbm_regressor.joblib'),
    }
    all_classifiers = {
        'Logistic Regression': joblib.load(f'{MODELS_DIR}lr_classifier.joblib'),
        'Random Forest'      : joblib.load(f'{MODELS_DIR}rf_classifier.joblib'),
        'XGBoost'            : joblib.load(f'{MODELS_DIR}xgb_classifier.joblib'),
        'LightGBM'           : joblib.load(f'{MODELS_DIR}lgbm_classifier.joblib'),
    }

    print("    All models and data loaded successfully.")
    return (X_train, X_test, y_clf_test, y_reg_test,
            X_resampled, y_resampled, comparison,
            best_reg, best_clf,
            all_regressors, all_classifiers)

# -----------------------------------------------------------------------
# STEP 2 — Regression Metrics Comparison Plot
# -----------------------------------------------------------------------
def plot_regression_metrics(all_regressors, X_test, y_test):
    print("\n[2] Plotting regression metrics comparison...")

    names, maes, rmses, r2s = [], [], [], []

    for name, model in all_regressors.items():
        y_pred = model.predict(X_test)
        names.append(name)
        maes.append(mean_absolute_error(y_test, y_pred))
        rmses.append(np.sqrt(mean_squared_error(y_test, y_pred)))
        r2s.append(r2_score(y_test, y_pred))

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    colors = ['#60a5fa', '#34d399', '#f9c74f', '#f87171']

    for ax, values, label, fmt in zip(
        axes,
        [maes, rmses, r2s],
        ['MAE (lower is better)',
         'RMSE (lower is better)',
         'R² Score (higher is better)'],
        ['.1f', '.1f', '.4f']
    ):
        bars = ax.bar(names, values, color=colors, edgecolor='white',
                      width=0.5)
        ax.set_title(label, fontsize=11, pad=10)
        ax.set_xticklabels(names, rotation=20, ha='right', fontsize=9)
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + max(values) * 0.01,
                    f'{val:{fmt}}', ha='center', fontsize=9)

    plt.suptitle('Regression Model Comparison', fontsize=14,
                 fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}07_regression_metrics.png', bbox_inches='tight')
    plt.close()
    print("    Saved: 07_regression_metrics.png")

# -----------------------------------------------------------------------
# STEP 3 — Classification Metrics Comparison Plot
# -----------------------------------------------------------------------
def plot_classification_metrics(all_classifiers, X_test, y_test):
    print("\n[3] Plotting classification metrics comparison...")

    names, accs, f1_macros, f1_weights = [], [], [], []

    for name, model in all_classifiers.items():
        y_pred = model.predict(X_test)
        names.append(name)
        accs.append(accuracy_score(y_test, y_pred))
        f1_macros.append(f1_score(y_test, y_pred, average='macro',
                                  zero_division=0))
        f1_weights.append(f1_score(y_test, y_pred, average='weighted',
                                   zero_division=0))

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    colors = ['#60a5fa', '#34d399', '#f9c74f', '#f87171']

    for ax, values, label in zip(
        axes,
        [accs, f1_macros, f1_weights],
        ['Accuracy', 'F1 Score (Macro)', 'F1 Score (Weighted)']
    ):
        bars = ax.bar(names, values, color=colors, edgecolor='white',
                      width=0.5)
        ax.set_title(label, fontsize=11, pad=10)
        ax.set_ylim(0, 1.1)
        ax.set_xticklabels(names, rotation=20, ha='right', fontsize=9)
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.01,
                    f'{val:.4f}', ha='center', fontsize=9)

    plt.suptitle('Classification Model Comparison', fontsize=14,
                 fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}08_classification_metrics.png',
                bbox_inches='tight')
    plt.close()
    print("    Saved: 08_classification_metrics.png")

# -----------------------------------------------------------------------
# STEP 4 — Confusion Matrix (Best Classifier)
# -----------------------------------------------------------------------
def plot_confusion_matrix(best_clf, X_test, y_test):
    print("\n[4] Plotting confusion matrix for best classifier...")

    y_pred = best_clf.predict(X_test)
    cm     = confusion_matrix(y_test, y_pred)
    cm_pct = cm.astype(float) / cm.sum(axis=1, keepdims=True) * 100

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Raw counts
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=BUCKET_LABELS,
                yticklabels=BUCKET_LABELS,
                ax=axes[0], linewidths=0.5)
    axes[0].set_title('Confusion Matrix — Raw Counts', fontsize=12)
    axes[0].set_xlabel('Predicted', fontsize=10)
    axes[0].set_ylabel('Actual',    fontsize=10)
    axes[0].tick_params(axis='x', rotation=30)

    # Percentage
    sns.heatmap(cm_pct, annot=True, fmt='.1f', cmap='Oranges',
                xticklabels=BUCKET_LABELS,
                yticklabels=BUCKET_LABELS,
                ax=axes[1], linewidths=0.5)
    axes[1].set_title('Confusion Matrix — Row % (Recall)', fontsize=12)
    axes[1].set_xlabel('Predicted', fontsize=10)
    axes[1].set_ylabel('Actual',    fontsize=10)
    axes[1].tick_params(axis='x', rotation=30)

    plt.suptitle('Best Classifier — Confusion Matrix', fontsize=14,
                 fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}09_confusion_matrix.png', bbox_inches='tight')
    plt.close()
    print("    Saved: 09_confusion_matrix.png")

    # Print text report
    print("\n    Classification Report:")
    print(classification_report(y_test, y_pred,
                                target_names=BUCKET_LABELS,
                                zero_division=0))

# -----------------------------------------------------------------------
# STEP 5 — Feature Importance (Best Classifier)
# -----------------------------------------------------------------------
def plot_feature_importance(best_clf, best_reg):
    print("\n[5] Plotting feature importance...")

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))

    for ax, model, title in zip(
        axes,
        [best_clf, best_reg],
        ['Best Classifier — Feature Importance',
         'Best Regressor  — Feature Importance']
    ):
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
        else:
            # Logistic Regression fallback
            importances = np.abs(model.coef_).mean(axis=0) \
                if hasattr(model, 'coef_') else np.zeros(len(FEATURE_COLS))

        indices = np.argsort(importances)[::-1]
        sorted_features = [FEATURE_COLS[i] for i in indices]
        sorted_values   = importances[indices]

        bars = ax.barh(sorted_features[::-1], sorted_values[::-1],
                       color='#60a5fa', edgecolor='white')
        ax.set_title(title, fontsize=11, pad=10)
        ax.set_xlabel('Importance Score')
        for bar, val in zip(bars, sorted_values[::-1]):
            ax.text(val + 0.001, bar.get_y() + bar.get_height() / 2,
                    f'{val:.4f}', va='center', fontsize=8)

    plt.suptitle('Feature Importance Comparison', fontsize=14,
                 fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}10_feature_importance.png', bbox_inches='tight')
    plt.close()
    print("    Saved: 10_feature_importance.png")

# -----------------------------------------------------------------------
# STEP 6 — SHAP Summary Plot (Best Classifier)
# -----------------------------------------------------------------------
def plot_shap_summary(best_clf, X_test):
    print("\n[6] Generating SHAP summary plot (may take ~1 min)...")

    try:
        X_sample = X_test.sample(min(300, len(X_test)),
                                 random_state=42)
        explainer   = shap.TreeExplainer(best_clf)
        shap_values = explainer.shap_values(X_sample)

        plt.figure(figsize=(12, 7))

        # Handle multi-class shap_values (list of arrays)
        if isinstance(shap_values, list):
            # Use class with highest average absolute impact
            mean_impacts = [np.abs(sv).mean() for sv in shap_values]
            best_class   = int(np.argmax(mean_impacts))
            shap.summary_plot(
                shap_values[best_class],
                X_sample,
                feature_names=FEATURE_COLS,
                show=False,
                plot_size=None
            )
            plt.title(
                f'SHAP Summary — Class: {BUCKET_LABELS[best_class]}',
                fontsize=13
            )
        else:
            shap.summary_plot(
                shap_values, X_sample,
                feature_names=FEATURE_COLS,
                show=False,
                plot_size=None
            )
            plt.title('SHAP Feature Summary', fontsize=13)

        plt.tight_layout()
        plt.savefig(f'{FIGURES_DIR}11_shap_summary.png', bbox_inches='tight')
        plt.close()
        print("    Saved: 11_shap_summary.png")

    except Exception as e:
        print(f"    SHAP skipped: {e}")

# -----------------------------------------------------------------------
# STEP 7 — Actual vs Predicted (Best Regressor)
# -----------------------------------------------------------------------
def plot_actual_vs_predicted(best_reg, X_test, y_test):
    print("\n[7] Plotting actual vs predicted AQI...")

    y_pred    = best_reg.predict(X_test)
    residuals = y_test.values - y_pred

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Scatter: Actual vs Predicted
    axes[0].scatter(y_test, y_pred, alpha=0.4, color='#60a5fa',
                    edgecolors='none', s=18)
    lims = [min(y_test.min(), y_pred.min()) - 10,
            max(y_test.max(), y_pred.max()) + 10]
    axes[0].plot(lims, lims, 'r--', linewidth=1.5, label='Perfect Fit')
    axes[0].set_xlabel('Actual AQI')
    axes[0].set_ylabel('Predicted AQI')
    axes[0].set_title('Actual vs Predicted AQI')
    axes[0].legend()

    # Residual Distribution
    axes[1].hist(residuals, bins=50, color='#34d399',
                 edgecolor='white', alpha=0.85)
    axes[1].axvline(0, color='red', linestyle='--', linewidth=1.5)
    axes[1].set_xlabel('Residual (Actual − Predicted)')
    axes[1].set_ylabel('Frequency')
    axes[1].set_title('Residual Distribution')
    axes[1].text(0.97, 0.95,
                 f'MAE  : {mean_absolute_error(y_test, y_pred):.2f}\n'
                 f'RMSE : {np.sqrt(mean_squared_error(y_test, y_pred)):.2f}\n'
                 f'R²   : {r2_score(y_test, y_pred):.4f}',
                 transform=axes[1].transAxes,
                 va='top', ha='right', fontsize=9,
                 bbox=dict(boxstyle='round', facecolor='#1e293b',
                           alpha=0.8, edgecolor='gray'))

    plt.suptitle('Best Regressor — Prediction Quality', fontsize=14,
                 fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}12_actual_vs_predicted.png',
                bbox_inches='tight')
    plt.close()
    print("    Saved: 12_actual_vs_predicted.png")

# -----------------------------------------------------------------------
# STEP 8 — SMOTE Impact Visualization
# -----------------------------------------------------------------------
def plot_smote_impact(y_clf_train_original, y_resampled):
    print("\n[8] Plotting SMOTE class balance impact...")

    bucket_order = list(range(6))

    before_counts = pd.Series(y_clf_train_original).value_counts().reindex(
        bucket_order, fill_value=0)
    after_counts  = pd.Series(y_resampled).value_counts().reindex(
        bucket_order, fill_value=0)

    x      = np.arange(len(BUCKET_LABELS))
    width  = 0.35

    fig, ax = plt.subplots(figsize=(12, 5))
    bars1 = ax.bar(x - width/2, before_counts.values, width,
                   label='Before SMOTE', color='#f87171', edgecolor='white')
    bars2 = ax.bar(x + width/2, after_counts.values,  width,
                   label='After SMOTE',  color='#34d399', edgecolor='white')

    ax.set_xticks(x)
    ax.set_xticklabels(BUCKET_LABELS, rotation=20, ha='right')
    ax.set_xlabel('AQI Bucket')
    ax.set_ylabel('Sample Count')
    ax.set_title('SMOTE Impact — Class Distribution Before vs After',
                 fontsize=13)
    ax.legend()

    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + 5,
                str(bar.get_height()), ha='center', fontsize=8)
    for bar in bars2:
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + 5,
                str(bar.get_height()), ha='center', fontsize=8)

    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}13_smote_impact.png', bbox_inches='tight')
    plt.close()
    print("    Saved: 13_smote_impact.png")

# -----------------------------------------------------------------------
# STEP 9 — Save Evaluation Summary Text
# -----------------------------------------------------------------------
def save_evaluation_summary(best_reg, best_clf,
                             X_test, y_reg_test, y_clf_test):
    print("\n[9] Saving evaluation summary...")

    y_reg_pred  = best_reg.predict(X_test)
    y_clf_pred  = best_clf.predict(X_test)

    mae   = mean_absolute_error(y_reg_test, y_reg_pred)
    rmse  = np.sqrt(mean_squared_error(y_reg_test, y_reg_pred))
    r2    = r2_score(y_reg_test, y_reg_pred)
    acc   = accuracy_score(y_clf_test, y_clf_pred)
    f1_m  = f1_score(y_clf_test, y_clf_pred,
                     average='macro', zero_division=0)
    f1_w  = f1_score(y_clf_test, y_clf_pred,
                     average='weighted', zero_division=0)

    summary = f"""
============================================================
PHASE 4 — MODEL EVALUATION SUMMARY
Air Quality Index Analysis
============================================================

BEST REGRESSOR
----------------------------------------
MAE          : {mae:.3f}
RMSE         : {rmse:.3f}
R² Score     : {r2:.4f}

BEST CLASSIFIER
----------------------------------------
Accuracy     : {acc:.4f}
F1 (Macro)   : {f1_m:.4f}
F1 (Weighted): {f1_w:.4f}

CLASSIFICATION REPORT
----------------------------------------
{classification_report(y_clf_test, y_clf_pred,
                       target_names=BUCKET_LABELS,
                       zero_division=0)}

PLOTS GENERATED
----------------------------------------
07_regression_metrics.png
08_classification_metrics.png
09_confusion_matrix.png
10_feature_importance.png
11_shap_summary.png
12_actual_vs_predicted.png
13_smote_impact.png
============================================================
"""
    with open(f'{REPORTS_DIR}evaluation_summary.txt', 'w', encoding='utf-8') as f:
        f.write(summary)
    # Replaced print(summary) to avoid unicode errors in console
    print(f"    Saved: reports/evaluation_summary.txt")

# -----------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("PHASE 4 — Model Evaluation")
    print("=" * 60)

    (X_train, X_test, y_clf_test, y_reg_test,
     X_resampled, y_resampled, comparison,
     best_reg, best_clf,
     all_regressors, all_classifiers) = load_all()

    plot_regression_metrics(all_regressors, X_test, y_reg_test)
    plot_classification_metrics(all_classifiers, X_test, y_clf_test)
    plot_confusion_matrix(best_clf, X_test, y_clf_test)
    plot_feature_importance(best_clf, best_reg)
    plot_shap_summary(best_clf, X_test)
    plot_actual_vs_predicted(best_reg, X_test, y_reg_test)
    plot_smote_impact(y_clf_test, y_resampled)
    save_evaluation_summary(best_reg, best_clf,
                             X_test, y_reg_test, y_clf_test)

    print("\n" + "=" * 60)
    print("Phase 4 Evaluation complete.")
    print("All plots saved to: reports/figures/")
    print("Next: Phase 5 — FastAPI Backend (backend/main.py)")
    print("=" * 60)
