import pytest
import joblib
from pathlib import Path
import numpy as np

@pytest.fixture
def model():
    """Load the trained model"""
    model_path = Path(__file__).parent / "models" / "iris_model.joblib"
    artifact = joblib.load(str(model_path))
    return artifact["model"]

@pytest.fixture
def target_names():
    """Load target names"""
    model_path = Path(__file__).parent / "models" / "iris_model.joblib"
    artifact = joblib.load(str(model_path))
    return artifact["target_names"]

class TestModel:
    """Test the trained ML model"""
    
    def test_model_exists(self):
        """Test that model file exists"""
        model_path = Path(__file__).parent / "models" / "iris_model.joblib"
        assert model_path.exists(), "Model file not found"
    
    def test_model_loads(self, model):
        """Test that model loads correctly"""
        assert model is not None, "Model failed to load"
    
    def test_target_names(self, target_names):
        """Test that target names are correct"""
        expected = ["setosa", "versicolor", "virginica"]
        assert list(target_names) == expected, f"Expected {expected}, got {target_names}"
    
    def test_setosa_prediction(self, model):
        """Test prediction for setosa iris"""
        x = np.array([[5.1, 3.5, 1.4, 0.2]])  # Classic setosa
        pred = model.predict(x)[0]
        assert pred == 0, "Failed to predict setosa (class 0)"
    
    def test_versicolor_prediction(self, model):
        """Test prediction for versicolor iris"""
        x = np.array([[5.9, 3.0, 4.2, 1.5]])  # Classic versicolor
        pred = model.predict(x)[0]
        assert pred == 1, "Failed to predict versicolor (class 1)"
    
    def test_virginica_prediction(self, model):
        """Test prediction for virginica iris"""
        x = np.array([[6.3, 3.3, 6.0, 2.5]])  # Classic virginica
        pred = model.predict(x)[0]
        assert pred == 2, "Failed to predict virginica (class 2)"
    
    def test_probability_sum(self, model):
        """Test that probabilities sum to 1"""
        x = np.array([[5.1, 3.5, 1.4, 0.2]])
        proba = model.predict_proba(x)[0]
        assert np.isclose(np.sum(proba), 1.0), "Probabilities don''t sum to 1"
    
    def test_prediction_range(self, model):
        """Test that predictions are valid class indices"""
        random_samples = np.random.rand(10, 4) * 8  # Random valid inputs
        preds = model.predict(random_samples)
        assert np.all(preds >= 0) and np.all(preds <= 2), "Predictions out of range"
