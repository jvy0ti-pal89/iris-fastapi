from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import numpy as np
from pathlib import Path
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("api.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Iris Classifier API", version="1.0", description="ML model for iris flower classification")

class IrisFeatures(BaseModel):
    sepal_length: float = Field(..., ge=0.1, le=10.0, description="Sepal length in cm (0.1-10.0)")
    sepal_width: float = Field(..., ge=0.1, le=10.0, description="Sepal width in cm (0.1-10.0)")
    petal_length: float = Field(..., ge=0.1, le=10.0, description="Petal length in cm (0.1-10.0)")
    petal_width: float = Field(..., ge=0.0, le=5.0, description="Petal width in cm (0.0-5.0)")
    
    class Config:
        schema_extra = {
            "example": {
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2
            }
        }

class PredictionResponse(BaseModel):
    prediction: str
    prediction_index: int
    probabilities: list
    confidence: float
    timestamp: str

# Load model at startup
model = None
target_names = []

@app.on_event("startup")
def load_model():
    global model, target_names
    project_root = Path(__file__).parent.parent
    model_path = project_root / "models" / "iris_model.joblib"
    
    logger.info(f"Loading model from: {model_path}")
    
    if model_path.exists():
        try:
            artifact = joblib.load(str(model_path))
            model = artifact.get("model")
            target_names = list(artifact.get("target_names", []))
            logger.info(f" Model loaded. Classes: {target_names}")
        except Exception as e:
            logger.error(f" Error loading model: {e}")
            raise RuntimeError(f"Failed to load model: {e}")
    else:
        logger.error(f" Model file not found at {model_path}")
        raise FileNotFoundError(f"Model file not found: {model_path}")

@app.get("/health", tags=["Health"])
def health():
    """Check server and model health"""
    status = {"status": "ok", "model_loaded": model is not None}
    logger.info(f"Health check: {status}")
    return status

@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
def predict(features: IrisFeatures):
    """
    Predict iris flower class from measurements
    
    - **sepal_length**: Sepal length (0.1-10.0 cm)
    - **sepal_width**: Sepal width (0.1-10.0 cm)
    - **petal_length**: Petal length (0.1-10.0 cm)
    - **petal_width**: Petal width (0.0-5.0 cm)
    """
    if model is None:
        logger.error("Prediction attempted but model not loaded")
        raise HTTPException(status_code=503, detail="Model not loaded. Run training first.")
    
    try:
        logger.info(f"Prediction request: sepal_length={features.sepal_length}, sepal_width={features.sepal_width}, petal_length={features.petal_length}, petal_width={features.petal_width}")
        
        x = np.array([[features.sepal_length, features.sepal_width, features.petal_length, features.petal_width]])
        pred = int(model.predict(x)[0])
        proba = model.predict_proba(x)[0]
        confidence = float(np.max(proba))
        label = target_names[pred] if target_names else f"Class {pred}"
        
        response = {
            "prediction": label,
            "prediction_index": pred,
            "probabilities": proba.tolist(),
            "confidence": round(confidence, 4),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Prediction result: {label} (confidence: {confidence:.4f})")
        return response
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

@app.get("/", tags=["Info"])
def root():
    """API information and available endpoints"""
    return {
        "message": "Iris Classifier REST API",
        "version": "1.0",
        "endpoints": {
            "/health": "GET - Server health check",
            "/predict": "POST - Classify iris flower",
            "/docs": "GET - Interactive Swagger UI",
            "/redoc": "GET - ReDoc documentation"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
