FROM python:3.11-slim

WORKDIR /app

# Copy requirements first (from Space repo root)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install huggingface_hub

# Copy all source files from Space repo root
COPY . .

# Create models directory (downloaded at runtime or copied via COPY . .)
RUN mkdir -p models/

# Set PYTHONPATH to /app so imports resolve correctly
ENV PYTHONPATH=/app

# HF Spaces requires port 7860
EXPOSE 7860

# Start FastAPI on port 7860
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
