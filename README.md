# Iris Classifier - REST API + Web UI

A machine learning project for iris flower classification with FastAPI REST API, Streamlit web UI, Docker containerization, and comprehensive logging.

## Features

 **FastAPI REST API** — Fast, modern Python web framework with auto-documentation
 **Streamlit Web UI** — Interactive dashboard for predictions
 **Docker & Docker Compose** — Containerized deployment
 **Input Validation** — Pydantic schemas with bounds checking
 **Logging** — File and console logging for debugging
 **Model Training** — Scikit-learn RandomForest (100% accuracy)

---

## Quick Start (Local)

### 1. Setup

```powershell
cd C:\Users\hp\iris-fastapi

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Train Model (optional)

```powershell
python train.py
# Output: Saved model to models/iris_model.joblib
```

### 3. Run API Server

```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

**Server running:** http://127.0.0.1:8000

### 4. Run Web UI (separate terminal)

```powershell
.\.venv\Scripts\Activate.ps1
streamlit run streamlit_app.py
```

**Web UI running:** http://127.0.0.1:8501

---

## Docker Deployment

### Option 1: Docker Compose (Recommended)

```bash
# Build and start both API + UI
docker-compose up

# API: http://localhost:8000
# UI: http://localhost:8501
```

### Option 2: Docker Build & Run

```bash
# Build image
docker build -t iris-classifier .

# Run API
docker run -p 8000:8000 iris-classifier

# Run UI
docker run -p 8501:8501 iris-classifier streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port 8501
```

---

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | API info & endpoints |
| `/health` | GET | Server & model status |
| `/predict` | POST | Classify iris (JSON input) |
| `/docs` | GET | Swagger UI (interactive) |
| `/redoc` | GET | ReDoc documentation |

### Example Request

```powershell
$body = @{
    sepal_length = 5.1
    sepal_width = 3.5
    petal_length = 1.4
    petal_width = 0.2
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/predict" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

### Example Response

```json
{
  "prediction": "setosa",
  "prediction_index": 0,
  "probabilities": [1.0, 0.0, 0.0],
  "confidence": 1.0,
  "timestamp": "2026-02-16T16:45:30.123456"
}
```

---

## Project Structure

```
iris-fastapi/
 app/
    main.py                (FastAPI app with logging & validation)
 streamlit_app.py           (Web UI)
 models/
    iris_model.joblib      (Trained RandomForest model)
 .venv/                     (Virtual environment)
 train.py                   (Training script)
 requirements.txt           (Python dependencies)
 Dockerfile                 (Container definition)
 docker-compose.yml         (Multi-container orchestration)
 .dockerignore              (Docker build exclusions)
 .gitignore                 (Git exclusions)
 README.md                  (This file)
 api.log                    (API logs)
 .git/                      (Git repository)
```

---

## Logging

Logs are written to both console and file (`api.log`):

```
2026-02-16 16:45:30 - __main__ - INFO - Loading model from: ...
2026-02-16 16:45:31 - __main__ - INFO - Model loaded. Classes: [...]
2026-02-16 16:45:32 - __main__ - INFO - Prediction request: sepal_length=5.1, ...
2026-02-16 16:45:32 - __main__ - INFO - Prediction result: setosa (confidence: 1.0000)
```

---

## Input Validation

All inputs are validated with bounds:

- **sepal_length**: 0.1 - 10.0 cm
- **sepal_width**: 0.1 - 10.0 cm
- **petal_length**: 0.1 - 10.0 cm
- **petal_width**: 0.0 - 5.0 cm

Invalid inputs return a 422 Validation Error with details.

---

## Model Details

- **Algorithm:** RandomForest (100 estimators)
- **Dataset:** UCI Iris (150 samples, 4 features, 3 classes)
- **Classes:** setosa, versicolor, virginica
- **Test Accuracy:** 100%
- **File Size:** ~187 KB

---

## Dependencies

| Package | Purpose |
|---------|---------|
| fastapi | Web framework |
| uvicorn | ASGI server |
| scikit-learn | ML algorithms |
| joblib | Model serialization |
| pandas | Data handling |
| numpy | Numerical computing |
| streamlit | Web UI |
| pydantic | Input validation |

---

## Common Commands

```powershell
# Activate venv
.\.venv\Scripts\Activate.ps1

# Install packages
pip install -r requirements.txt

# Train model
python train.py

# Run API
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Run Streamlit UI
streamlit run streamlit_app.py

# View logs
Get-Content api.log -Tail 50

# Docker compose up
docker-compose up

# Docker compose down
docker-compose down

# Git status
git status

# Git commit
git add -A
git commit -m "Your message"
```

---

## Troubleshooting

**Q: "Cannot connect to API"**  
A: Ensure the API server is running on the correct host/port. Check firewall settings.

**Q: "Model not found"**  
A: Run `python train.py` to create `models/iris_model.joblib`.

**Q: "Streamlit app won't load"**  
A: Ensure the API is running first, then start Streamlit.

**Q: "Docker build fails"**  
A: Run `docker-compose down` and retry. Check Docker is installed and running.

---

## Next Steps

- Deploy to cloud (AWS ECS, Azure Container Instances, Heroku)
- Add unit tests & CI/CD pipeline
- Add database for prediction history
- Implement authentication & rate limiting
- Add data preprocessing UI
- Create mobile app wrapper

---

## License

MIT License - Feel free to use this project!

---

**Author:** ML Project Demo  
**Created:** Feb 2026  
**Status:**  Production Ready
