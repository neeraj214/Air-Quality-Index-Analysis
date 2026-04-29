<div align="center">

![Project Banner](assets/banner.png)

# 🌬️ Air Quality Index (AQI) Analysis 📊

[![GitHub stars](https://img.shields.io/github/stars/neeraj214/Air-Quality-Index-Analysis?style=for-the-badge)](https://github.com/neeraj214/Air-Quality-Index-Analysis/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/neeraj214/Air-Quality-Index-Analysis?style=for-the-badge)](https://github.com/neeraj214/Air-Quality-Index-Analysis/network/members)
[![GitHub issues](https://img.shields.io/github/issues/neeraj214/Air-Quality-Index-Analysis?style=for-the-badge)](https://github.com/neeraj214/Air-Quality-Index-Analysis/issues)
[![GitHub repo size](https://img.shields.io/github/repo-size/neeraj214/Air-Quality-Index-Analysis?style=for-the-badge)](https://github.com/neeraj214/Air-Quality-Index-Analysis)
[![GitHub top language](https://img.shields.io/github/languages/top/neeraj214/Air-Quality-Index-Analysis?style=for-the-badge)](https://github.com/neeraj214/Air-Quality-Index-Analysis)

**A comprehensive Machine Learning system for predicting and analyzing Air Quality Index (AQI) levels across major Indian cities.**

[Exploration](#-exploration) • [Features](#-key-features) • [Tech Stack](#-tech-stack) • [Installation](#-installation) • [Usage](#-usage) • [Evaluation](#-model-evaluation)

</div>

---

## 🚀 Overview

This project provides an end-to-end data science and engineering pipeline for AQI analysis. It encompasses everything from Exploratory Data Analysis (EDA) and feature engineering to model training, evaluation, and deployment via a FastAPI backend and a React-based frontend dashboard. 

The system specifically targets major Indian metropolitan areas: **Delhi, Bengaluru, Kolkata, and Hyderabad**.

## 🔗 Live Demo
| Component | URL                                                          |
|-----------|--------------------------------------------------------------|
| Frontend  | https://air-quality-index-analysis.vercel.app                |
| Backend   | https://neeraj214-aqi-analysis-backend.hf.space/docs         |
| Models    | https://huggingface.co/Neeraj214/aqi-analysis-models         |

## ✨ Key Features

- 📉 **Advanced Analytics**: Detailed EDA of pollutant trends across different seasons and cities.
- 🔮 **Dual-Mode Prediction**:
  - **Regression**: Predict exact AQI values (R² Score: ~0.94).
  - **Classification**: Categorize air quality into buckets (Good, Satisfactory, Moderate, etc.) with ~82% accuracy.
- ⚖️ **Class Balancing**: Utilizes SMOTE to handle class imbalance in air quality categories.
- ⚡ **High-Performance API**: FastAPI-based REST backend for real-time inference.
- 📊 **Interactive Dashboard**: React frontend featuring gauges, charts, and health advisories.
- 🔍 **Model Explainability**: SHAP (SHapley Additive exPlanations) values used to interpret model decisions.
- 🐳 **Dockerized**: Containerized backend for seamless deployment.

## 🛠️ Tech Stack

| Area | Technologies |
| :--- | :--- |
| **Frontend** | React, Tailwind CSS, Framer Motion, Axios |
| **Backend** | FastAPI, Uvicorn, Docker |
| **Machine Learning** | Scikit-learn, XGBoost, LightGBM, SHAP, SMOTE |
| **Data Processing**| Pandas, NumPy |
| **Deployment** | HF Spaces (backend), Vercel (frontend), Hugging Face Hub (Models) |

## 📅 Project Status

- [x] **Phase 1: EDA** - Exploratory Data Analysis and visualization.
- [x] **Phase 2: Preprocessing** - Missing value imputation, feature engineering, and SMOTE resampling.
- [x] **Phase 3: Model Training** - Training Regressors (XGBoost, Random Forest) and Classifiers.
- [x] **Phase 4: Model Evaluation** - Detailed metrics (R², MAE, RMSE) and SHAP analysis.
- [x] **Phase 5: FastAPI Backend** - Building the production-ready REST API.
- [x] **Phase 6: React Frontend** - Developing the interactive dashboard.
- [x] **Phase 7: Deployment** - Final deployment to Hugging Face Spaces and Vercel.

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/neeraj214/Air-Quality-Index-Analysis.git
cd Air-Quality-Index-Analysis
```

### 2. Backend Setup
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r backend/requirements.txt
```

### 3. Frontend Setup
```bash
cd frontend
npm install
```

## 🖥️ Usage

### Running the API (Backend)
```bash
cd backend
uvicorn main:app --reload --port 8000
```
- **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

### Running the Dashboard (Frontend)
```bash
cd frontend
npm run dev
```
- **URL**: [http://localhost:5173](http://localhost:5173)

### Running with Docker
```bash
docker build -t aqi-backend -f backend/Dockerfile .
docker run -p 8000:8000 aqi-backend
```

## 📊 Model Evaluation

Our models were evaluated on a comprehensive test set.

| Model Type | Best Algorithm | Metric | Value |
| :--- | :--- | :--- | :--- |
| **Regression** | XGBoost | R² Score | **0.9425** |
| **Classification** | Random Forest | Accuracy | **82.22%** |

Refer to `reports/evaluation_summary.txt` and `reports/figures/` for detailed metrics and plots including Confusion Matrices and SHAP Summary plots.

## 🤝 Contributing

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

<div align="center">

Made with ❤️ for a Cleaner Environment 🌍

</div>