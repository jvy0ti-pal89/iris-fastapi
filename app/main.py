from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import os

app = FastAPI(title="Iris Classifier API")

class IrisFeatures(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

model_path = os.path.join("models","iris_model.joblib")
if os.path.exists(model_path):
    model_artifact = joblib.load(model_path)
    model = model_artifact["model"]
    target_names = list(model_artifact.get("target_names", []))
else:
    model = None
    target_names = []

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(features: IrisFeatures):
    if model is None:
        return {"error": "Model not found. Run training first."}
    x = np.array([[features.sepal_length, features.sepal_width, features.petal_length, features.petal_width]])
    pred = int(model.predict(x)[0])
    proba = model.predict_proba(x)[0].tolist()
    label = target_names[pred] if target_names else pred
    return {"prediction": label, "prediction_index": pred, "probabilities": proba}
