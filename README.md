🌸 Iris Classification System – Production-Style ML API

End-to-end machine learning system that trains, serves, and deploys an Iris classifier using FastAPI, Scikit-learn, Docker, CI/CD, and Streamlit UI.

Live Demo:
App → https://iris-fastapi-idlx.onrender.com

API Docs → https://iris-fastapi-idlx.onrender.com/docs

🚀 Project Overview

This project demonstrates how to:

Train ML models using Scikit-learn

Compare multiple algorithms

Build a preprocessing pipeline

Serve predictions through FastAPI

Add automated testing with Pytest

Enable CI using GitHub Actions

Containerize using Docker

Deploy to cloud (Render)

Provide interactive UI using Streamlit

This simulates a real-world ML deployment workflow.

🧠 Model Training & Comparison

Instead of using only one model, multiple algorithms were evaluated:

Model	Accuracy
Logistic Regression	~96–98%
Support Vector Machine	~97–99%
Random Forest	100%

Final selected model: RandomForestClassifier (100 estimators)

Why?

Best performance on test split

Robust to feature scaling variations

Handles non-linear boundaries well

🔬 Preprocessing Pipeline

Implemented using sklearn.pipeline.Pipeline.

Pipeline steps:

Feature Scaling → StandardScaler

Model → Selected classifier

This ensures:

Consistent preprocessing during training & inference

Cleaner production architecture

No data leakage

📊 Confusion Matrix (Test Set)

RandomForest achieved perfect classification on Iris test split.

Confusion Matrix:

               Predicted
             Set  Ver  Vir
Actual Set    10    0    0
Actual Ver     0   10    0
Actual Vir     0    0   10


Total Test Accuracy: 100%

Note: Iris dataset is small and clean, so high accuracy is expected.

🏗 Architecture
4

Architecture Flow:

User → Streamlit UI
OR
Client → FastAPI REST API

FastAPI:

Validates input (Pydantic)

Loads trained pipeline

Returns prediction + probabilities

CI Pipeline:

Push to GitHub

GitHub Actions runs tests

Docker image builds

Deploy to Render

🛠 Tech Stack

Python

Pandas

NumPy

Scikit-learn

FastAPI

Uvicorn

Pydantic

Streamlit

Pytest

Docker

GitHub Actions

Render (Cloud Deployment)

📦 API Endpoints
Endpoint	Method	Description
/	GET	API info
/health	GET	Health check
/predict	POST	Prediction
/docs	GET	Swagger UI
/redoc	GET	ReDoc

Example Request:

{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}


Example Response:

{
  "prediction": "setosa",
  "prediction_index": 0,
  "probabilities": [1.0, 0.0, 0.0],
  "confidence": 1.0,
  "timestamp": "2026-02-16T16:45:30"
}

🐳 Docker Deployment

Build:

docker build -t iris-classifier .


Run:

docker run -p 8000:8000 iris-classifier


Docker Compose:

docker-compose up

🔁 CI/CD

GitHub Actions workflow:

Installs dependencies

Runs pytest

Verifies model file exists

Ensures API loads correctly

CI Status: Passing
Badge: https://github.com/jvy0ti-pal89/iris-fastapi/actions/workflows/ci.yml/badge.svg

🧪 Testing

Tests validate:

Model loads successfully

/predict endpoint works

Response format correctness

Status codes

This ensures production reliability.

📝 Logging

Application logs:

Model loading

Prediction requests

Errors

Confidence scores

Logs written to:

Console

api.log file

📂 Project Structure
iris-fastapi/
│
├── app/
│   └── main.py
├── models/
│   └── iris_model.joblib
├── tests/
├── train.py
├── streamlit_app.py
├── Dockerfile
├── docker-compose.yml
├── .github/workflows/
├── requirements.txt
└── README.md

🌍 Deployment

Hosted on Render.

Important deployment considerations:

Bind server to $PORT

Include model file inside Docker image

Ensure health endpoint passes

📈 Future Improvements

Add prediction history database

Add authentication

Add rate limiting

Add model monitoring

Replace Iris with real-world dataset

Add model versioning

🎯 What This Project Demonstrates

End-to-end ML system design

Backend API development

CI/CD automation

Containerization

Deployment pipeline

Clean project architecture

This project is designed to simulate production ML serving.
