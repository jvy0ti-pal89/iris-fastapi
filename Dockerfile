FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (don't COPY a non-existent models/ path)
COPY app/ ./app/
COPY train.py ./
COPY streamlit_app.py ./
COPY README.md ./

# Create models dir and train at build time if model is missing
RUN mkdir -p ./models && \
	if [ ! -f ./models/iris_model.joblib ]; then python train.py; fi

# Use Render's PORT env var
ENV PORT 8000
EXPOSE ${PORT}

# Start Uvicorn binding to 0.0.0.0 and the provided $PORT
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1"]
