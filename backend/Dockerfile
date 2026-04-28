FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy backend files
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/ ./backend/

# Copy models folder (needed at runtime)
COPY models/ ./models/

# Set PYTHONPATH so imports resolve correctly
ENV PYTHONPATH=/app/backend

# Expose port
EXPOSE 8000

# Run app
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
