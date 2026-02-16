from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
from pathlib import Path
import os

app = FastAPI(title="Iris Classifier API", version="1.0")

class IrisFeatures(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# Load model at startup
model = None
target_names = []

@app.on_event("startup")
def load_model():
    global model, target_names
    # Try multiple path strategies
    project_root = Path(__file__).parent.parent  # app/main.py -> iris-fastapi/
    model_path = project_root / "models" / "iris_model.joblib"
    
    print(f"Project root: {project_root}")
    print(f"Model path: {model_path}")
    print(f"Model exists: {model_path.exists()}")
    
    if model_path.exists():
        try:
            artifact = joblib.load(str(model_path))
            model = artifact.get("model")
            target_names = list(artifact.get("target_names", []))
            print(f"Model loaded successfully. Classes: {target_names}")
        except Exception as e:
            print(f"Error loading model: {e}")
    else:
        print(f"Model file not found at {model_path}")

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}

@app.post("/predict")
def predict(features: IrisFeatures):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Run training first.")
    
    try:
        x = np.array([[features.sepal_length, features.sepal_width, features.petal_length, features.petal_width]])
        pred = int(model.predict(x)[0])
        proba = model.predict_proba(x)[0].tolist()
        label = target_names[pred] if target_names else f"Class {pred}"
        return {
            "prediction": label,
            "prediction_index": pred,
            "probabilities": proba
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

@app.get("/")
def root():
    return {
        "message": "Iris Classifier API",
        "endpoints": {
            "/health": "GET - Check server status",
            "/predict": "POST - Predict iris class",
            "/docs": "GET - Swagger UI"
        }
    }
