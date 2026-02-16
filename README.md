# Iris classifier + FastAPI

## Setup (Windows PowerShell)

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

## Train

python train.py

## Run API

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

## Test

curl -X POST "http://127.0.0.1:8000/predict" -H "Content-Type: application/json" -d "{\"sepal_length\":5.1,\"sepal_width\":3.5,\"petal_length\":1.4,\"petal_width\":0.2}"
