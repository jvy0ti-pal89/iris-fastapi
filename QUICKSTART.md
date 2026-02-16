#  QUICK START GUIDE

## Option 1: Local Development (Recommended for Testing)

### Terminal 1 - Start API
```powershell
cd C:\Users\hp\iris-fastapi
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```
 API running: http://127.0.0.1:8000

### Terminal 2 - Start Web UI
```powershell
cd C:\Users\hp\iris-fastapi
.\.venv\Scripts\Activate.ps1
streamlit run streamlit_app.py
```
 UI running: http://127.0.0.1:8501

### Terminal 3 - Test API (optional)
```powershell
$body = @{sepal_length=5.1; sepal_width=3.5; petal_length=1.4; petal_width=0.2} | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:8000/predict" -Method Post -ContentType "application/json" -Body $body | ConvertTo-Json
```

---

## Option 2: Docker Compose (Production-Ready)

### Build & Run Both Containers
```bash
cd C:\Users\hp\iris-fastapi
docker-compose up --build
```

 API: http://localhost:8000  
 UI: http://localhost:8501

### Stop Containers
```bash
docker-compose down
```

---

## What''s New in This Update

 **Streamlit Web UI** (`streamlit_app.py`)
   - Interactive sliders for flower measurements
   - Real-time predictions with confidence scores
   - Probability visualization charts
   - API health status indicator

 **Enhanced Logging** (`app/main.py`)
   - File logging to `api.log`
   - Console output with timestamps
   - Request/response tracking

 **Input Validation** (`app/main.py`)
   - Bounds checking (sepal: 0.1-10cm, petal: 0.0-5cm)
   - Type validation
   - Error messages with details

 **Docker Support**
   - `Dockerfile` - Container image
   - `docker-compose.yml` - Multi-container orchestration
   - `.dockerignore` - Build optimization

---

## Key URLs

| Service | URL | Purpose |
|---------|-----|---------|
| FastAPI | http://127.0.0.1:8000 | REST API |
| Swagger UI | http://127.0.0.1:8000/docs | Interactive API docs |
| ReDoc | http://127.0.0.1:8000/redoc | API documentation |
| Streamlit UI | http://127.0.0.1:8501 | Web application |

---

## Example Predictions

**Setosa**
```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
 prediction: setosa (confidence: 100%)
```

**Versicolor**
```json
{
  "sepal_length": 5.9,
  "sepal_width": 3.0,
  "petal_length": 4.2,
  "petal_width": 1.5
}
 prediction: versicolor (confidence: 96%)
```

**Virginica**
```json
{
  "sepal_length": 6.5,
  "sepal_width": 3.0,
  "petal_length": 5.5,
  "petal_width": 1.8
}
 prediction: virginica (confidence: 100%)
```

---

## Project Files

**Core Application**
- `app/main.py` - FastAPI with logging, validation, improved error handling
- `streamlit_app.py` - Web UI dashboard
- `train.py` - Model training script
- `models/iris_model.joblib` - Trained ML model

**Configuration & Deployment**
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container definition
- `docker-compose.yml` - Multi-container setup
- `.dockerignore` - Build exclusions
- `.gitignore` - Git exclusions

**Documentation**
- `README.md` - Full project documentation
- `QUICKSTART.md` - This file

---

## Logs

Check API logs:
```powershell
Get-Content api.log -Tail 20
# Shows last 20 log entries
```

---

## Troubleshooting

**"Streamlit won''t connect to API"**
 Ensure API is running first (Terminal 1)

**"Model not loaded"**
 Run: `python train.py`

**"Port 8000/8501 already in use"**
 Change port: `--port 8001` or `--server.port 8502`

**"Docker build fails"**
 Run: `docker-compose down && docker-compose up --build`

---

## Next Steps

- [ ] Push to GitHub
- [ ] Deploy to cloud (AWS/Azure/Heroku)
- [ ] Add unit tests
- [ ] Set up CI/CD pipeline
- [ ] Add prediction history database
- [ ] Implement authentication

---

**Status:**  Ready for Development & Deployment
**Last Updated:** Feb 16, 2026
