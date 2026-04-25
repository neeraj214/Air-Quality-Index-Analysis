"""
Phase 1 — Exploratory Data Analysis (EDA)
==========================================
Project : Air Quality Index Analysis
Script  : src/eda.py
Dataset : data/raw/city_day.csv
Output  : reports/figures/
"""

# =============================================================================
# SECTION 1 — Imports & Setup
# =============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import os

warnings.filterwarnings('ignore')

# Plot style
sns.set_theme(style="darkgrid", palette="muted")
plt.rcParams['figure.figsize'] = (12, 5)
plt.rcParams['figure.dpi'] = 120

# Output directory
os.makedirs('reports/figures', exist_ok=True)

# Load dataset
df = pd.read_csv('data/raw/city_day.csv', parse_dates=['Date'])

print("=" * 60)
print("Dataset Loaded Successfully")
print(f"Shape: {df.shape}")
print("=" * 60)


# =============================================================================
# SECTION 2 — Basic Dataset Overview
# =============================================================================

def dataset_overview(df):
    print("\n--- Data Types & Non-Null Counts ---")
    print(df.info())

    print("\n--- Summary Statistics ---")
    print(df.describe().T.to_string())

    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    missing_df = pd.DataFrame({
        'Missing Count': missing,
        'Missing %': missing_pct
    }).sort_values('Missing %', ascending=False)

    print("\n--- Missing Values ---")
    print(missing_df[missing_df['Missing Count'] > 0].to_string())

    print(f"\nUnique Cities : {df['City'].unique()}")
    print(f"Date Range    : {df['Date'].min()} to {df['Date'].max()}")
    print(f"Total Rows    : {len(df)}")


dataset_overview(df)


# =============================================================================
# SECTION 3 — AQI Distribution (Overall)
# =============================================================================

def plot_aqi_distribution(df):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Histogram
    axes[0].hist(df['AQI'].dropna(), bins=50,
                 color='steelblue', edgecolor='white')
    axes[0].set_title('Overall AQI Distribution')
    axes[0].set_xlabel('AQI Value')
    axes[0].set_ylabel('Frequency')
    axes[0].axvline(df['AQI'].mean(), color='red', linestyle='--',
                    label=f"Mean: {df['AQI'].mean():.1f}")
    axes[0].legend()

    # AQI Bucket bar chart
    bucket_order = ['Good', 'Satisfactory', 'Moderate',
                    'Poor', 'Very Poor', 'Severe']
    bucket_counts = df['AQI_Bucket'].value_counts().reindex(bucket_order)
    colors = ['#2ecc71', '#a8d08d', '#f9c74f',
              '#f77f00', '#d62828', '#6a040f']

    axes[1].bar(bucket_counts.index, bucket_counts.values,
                color=colors, edgecolor='white')
    axes[1].set_title('AQI Bucket Class Distribution')
    axes[1].set_xlabel('AQI Bucket')
    axes[1].set_ylabel('Count')
    axes[1].tick_params(axis='x', rotation=30)

    plt.tight_layout()
    plt.savefig('reports/figures/01_aqi_distribution.png', bbox_inches='tight')
    plt.close()
    print("Saved: 01_aqi_distribution.png")

    print("\nClass Distribution (%):")
    print((df['AQI_Bucket'].value_counts(normalize=True) * 100).round(2))


plot_aqi_distribution(df)


# =============================================================================
# SECTION 4 — City-wise AQI Analysis
# =============================================================================

def plot_city_aqi(df):
    target_cities = ['Delhi', 'Bengaluru', 'Kolkata', 'Hyderabad']
    city_df = df[df['City'].isin(target_cities)]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Boxplot
    sns.boxplot(data=city_df, x='City', y='AQI',
                palette='Set2', ax=axes[0])
    axes[0].set_title('AQI Distribution by City')
    axes[0].set_xlabel('City')
    axes[0].set_ylabel('AQI Value')

    # Mean AQI bar chart
    city_mean = city_df.groupby('City')['AQI'].mean().sort_values(ascending=False)
    axes[1].bar(city_mean.index, city_mean.values,
                color=sns.color_palette('Set2', 4))
    axes[1].set_title('Mean AQI by City')
    axes[1].set_xlabel('City')
    axes[1].set_ylabel('Mean AQI')
    for i, v in enumerate(city_mean.values):
        axes[1].text(i, v + 2, f'{v:.1f}', ha='center', fontsize=10)

    plt.tight_layout()
    plt.savefig('reports/figures/02_city_aqi.png', bbox_inches='tight')
    plt.close()
    print("Saved: 02_city_aqi.png")


plot_city_aqi(df)


# =============================================================================
# SECTION 5 — Time-Series AQI Trends
# =============================================================================

def plot_time_series(df):
    target_cities = ['Delhi', 'Bengaluru', 'Kolkata', 'Hyderabad']
    city_df = df[df['City'].isin(target_cities)].copy()
    city_df['YearMonth'] = city_df['Date'].dt.to_period('M').dt.to_timestamp()

    # Monthly trend
    monthly_avg = city_df.groupby(
        ['YearMonth', 'City'])['AQI'].mean().reset_index()

    plt.figure(figsize=(16, 5))
    for city in target_cities:
        subset = monthly_avg[monthly_avg['City'] == city]
        plt.plot(subset['YearMonth'], subset['AQI'],
                 label=city, linewidth=1.8)
    plt.title('Monthly Average AQI Trend by City')
    plt.xlabel('Date')
    plt.ylabel('Average AQI')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('reports/figures/03_monthly_aqi_trend.png', bbox_inches='tight')
    plt.close()
    print("Saved: 03_monthly_aqi_trend.png")

    # Season-wise AQI
    city_df['Month'] = city_df['Date'].dt.month
    city_df['Season'] = city_df['Month'].map({
        12: 'Winter', 1: 'Winter',  2: 'Winter',
        3:  'Spring', 4: 'Spring',  5: 'Spring',
        6:  'Summer', 7: 'Summer',  8: 'Summer',
        9:  'Monsoon', 10: 'Monsoon', 11: 'Monsoon'
    })

    plt.figure(figsize=(12, 5))
    season_order = ['Winter', 'Spring', 'Summer', 'Monsoon']
    sns.boxplot(data=city_df, x='Season', y='AQI',
                order=season_order, hue='City', palette='Set2')
    plt.title('Season-wise AQI by City')
    plt.xlabel('Season')
    plt.ylabel('AQI')
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig('reports/figures/04_season_aqi.png', bbox_inches='tight')
    plt.close()
    print("Saved: 04_season_aqi.png")


plot_time_series(df)


# =============================================================================
# SECTION 6 — Pollutant Correlation Heatmap
# =============================================================================

def plot_correlation_heatmap(df):
    pollutants = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3',
                  'CO', 'SO2', 'O3', 'Benzene', 'Toluene', 'Xylene', 'AQI']

    corr_matrix = df[pollutants].dropna().corr()

    plt.figure(figsize=(13, 9))
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    sns.heatmap(
        corr_matrix, mask=mask, annot=True, fmt='.2f',
        cmap='coolwarm', center=0, square=True,
        linewidths=0.5, cbar_kws={"shrink": 0.8}
    )
    plt.title('Pollutant Correlation Heatmap')
    plt.tight_layout()
    plt.savefig('reports/figures/05_correlation_heatmap.png', bbox_inches='tight')
    plt.close()
    print("Saved: 05_correlation_heatmap.png")

    print("\nTop Correlations with AQI:")
    print(corr_matrix['AQI'].drop('AQI').sort_values(ascending=False))


plot_correlation_heatmap(df)


# =============================================================================
# SECTION 7 — Pollutant Distributions (Delhi Only)
# =============================================================================

def plot_delhi_pollutants(df):
    delhi_df = df[df['City'] == 'Delhi'].copy()
    pollutant_cols = ['PM2.5', 'PM10', 'NO2', 'CO', 'SO2', 'O3']

    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    axes = axes.flatten()

    for i, col in enumerate(pollutant_cols):
        axes[i].hist(delhi_df[col].dropna(), bins=40,
                     color='steelblue', edgecolor='white', alpha=0.8)
        axes[i].set_title(f'{col} Distribution (Delhi)')
        axes[i].set_xlabel(col)
        axes[i].set_ylabel('Frequency')
        axes[i].axvline(delhi_df[col].mean(), color='red',
                        linestyle='--', linewidth=1.2,
                        label=f"Mean: {delhi_df[col].mean():.2f}")
        axes[i].legend(fontsize=8)

    plt.suptitle('Key Pollutant Distributions — Delhi', fontsize=14, y=1.01)
    plt.tight_layout()
    plt.savefig('reports/figures/06_delhi_pollutant_dist.png', bbox_inches='tight')
    plt.close()
    print("Saved: 06_delhi_pollutant_dist.png")


plot_delhi_pollutants(df)


# =============================================================================
# SECTION 8 — Main Runner
# =============================================================================

if __name__ == "__main__":
    print("\n========== EDA COMPLETE ==========")
    print("All figures saved to: reports/figures/")
    print("Figures generated:")
    for f in sorted(os.listdir('reports/figures')):
        if f.endswith('.png'):
            print(f"  - {f}")
