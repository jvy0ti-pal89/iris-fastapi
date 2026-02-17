FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files (including models)
COPY . .
COPY models/ ./models/

# Use the PORT environment variable provided by Render
ENV PORT 8000
EXPOSE ${PORT}

# Start Uvicorn binding to 0.0.0.0 and the provided $PORT
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1"]
FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY models/ ./models/
COPY train.py .
COPY streamlit_app.py .

# Expose ports
EXPOSE 8000 8501

# Default command: start FastAPI
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
