import os
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import numpy as np


def main():
    data = load_iris()
    X = data.data
    y = data.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    preds = clf.predict(X_test)
    acc = accuracy_score(y_test, preds)
    os.makedirs("models", exist_ok=True)
    joblib.dump({"model": clf, "target_names": data.target_names}, "models/iris_model.joblib")
    print(f"Trained RandomForest on Iris — accuracy: {acc:.4f}")
    print("Saved model to models/iris_model.joblib")


if __name__ == "__main__":
    main()
