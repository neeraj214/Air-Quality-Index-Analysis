---
title: AQI Analysis Backend
emoji: 🌫️
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# AQI Analysis Backend API

FastAPI backend for Air Quality Index prediction across Indian cities.

## Endpoints
- `GET  /`             — API status
- `GET  /health`       — Health check
- `GET  /cities`       — Supported cities
- `GET  /models/info`  — Loaded model info
- `POST /predict`      — Single AQI prediction
- `POST /predict/batch`— Batch predictions

## Docs
Visit `/docs` for full Swagger UI documentation.
