<div align="center">

![Project Banner](assets/banner.png)

# 🌬️ Air Quality Index (AQI) Analysis 📊

[![GitHub stars](https://img.shields.io/github/stars/neeraj214/Air-Quality-Index-Analysis?style=for-the-badge)](https://github.com/neeraj214/Air-Quality-Index-Analysis/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/neeraj214/Air-Quality-Index-Analysis?style=for-the-badge)](https://github.com/neeraj214/Air-Quality-Index-Analysis/network/members)
[![GitHub issues](https://img.shields.io/github/issues/neeraj214/Air-Quality-Index-Analysis?style=for-the-badge)](https://github.com/neeraj214/Air-Quality-Index-Analysis/issues)
[![GitHub repo size](https://img.shields.io/github/repo-size/neeraj214/Air-Quality-Index-Analysis?style=for-the-badge)](https://github.com/neeraj214/Air-Quality-Index-Analysis)
[![GitHub top language](https://img.shields.io/github/languages/top/neeraj214/Air-Quality-Index-Analysis?style=for-the-badge)](https://github.com/neeraj214/Air-Quality-Index-Analysis)

**A sophisticated Machine Learning system to predict AQI levels across major Indian cities using real-time pollutant data.**

[Exploration](#-exploration) • [Tech Stack](#-tech-stack) • [Installation](#-installation) • [Usage](#-usage) • [Contributing](#-contributing)

</div>

---

## 🚀 Overview

This project provides an end-to-end pipeline for analyzing and predicting Air Quality Index (AQI) levels. It specifically targets major Indian hubs including **Delhi, Bangalore, Kolkata, and Hyderabad**. By leveraging advanced ML algorithms, it predicts pollutant levels and provides a user-friendly dashboard for visualization.

## 🛠️ Tech Stack

<div align="center">

| Area | Technologies |
| :--- | :--- |
| **Frontend** | ![React](https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB) ![Tailwind](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat-square&logo=tailwind-css&logoColor=white) ![Framer](https://img.shields.io/badge/Framer_Motion-0055FF?style=flat-square&logo=framer&logoColor=white) |
| **Backend** | ![FastAPI](https://img.shields.io/badge/fastapi-109989?style=flat-square&logo=fastapi&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white) |
| **Machine Learning** | ![Scikit-learn](https://img.shields.io/badge/scikit_learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white) ![XGBoost](https://img.shields.io/badge/XGBoost-black?style=flat-square) ![LightGBM](https://img.shields.io/badge/LightGBM-blue?style=flat-square) |
| **Data** | ![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white) ![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white) |

</div>

## ✨ Key Features

- 📈 **Real-time Visualization**: Interactive charts and gauges for pollutant levels.
- 🔮 **Predictive Analytics**: High-accuracy AQI predictions using SMOTE-enhanced datasets.
- 🏙️ **City-wise Analysis**: Tailored insights for specific Indian metropolises.
- 📱 **Responsive Design**: Seamless experience across mobile and desktop.
- ⚡ **Fast API**: High-performance backend for model serving.

## 📅 Project Phases

- [x] **Phase 1: EDA** - Exploratory Data Analysis of pollutant trends.
- [x] **Phase 2: Preprocessing** - Handling missing values and SMOTE for class balance.
- [x] **Phase 3: Model Training** - Comparing XGBoost, LightGBM, and Random Forest.
- [x] **Phase 4: Model Evaluation** - R2 Score, RMSE, and MAE metrics.
- [/] **Phase 5: FastAPI Backend** - Building the REST API.
- [/] **Phase 6: React Frontend** - Developing the dashboard.
- [ ] **Phase 7: Deployment** - Pushing to Vercel and Hugging Face.

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/neeraj214/Air-Quality-Index-Analysis.git
   cd Air-Quality-Index-Analysis
   ```

2. **Setup Backend**
   ```bash
   python -m venv venv
   source venv/bin/activate # or venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Setup Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

<div align="center">

Made with ❤️ for a Cleaner Environment 🌍

</div>