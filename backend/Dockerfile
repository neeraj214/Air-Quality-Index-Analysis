FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install huggingface_hub

# Copy backend source
COPY backend/ ./backend/

# Create models directory
RUN mkdir -p models/

# Set PYTHONPATH so imports resolve from backend/
ENV PYTHONPATH=/app/backend

# HF Spaces requires port 7860
EXPOSE 7860

# Start FastAPI on port 7860
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"]
