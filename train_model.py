"""Train a simple Iris classifier and save it to disk."""
import os

import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model.joblib")
FEATURES = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
CLASS_NAMES = ["setosa", "versicolor", "virginica"]


def train(path: str = MODEL_PATH) -> float:
    """Train the model, save it to `path`, and return test accuracy."""
    iris = load_iris()
    x_train, x_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.2, random_state=42, stratify=iris.target
    )
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(x_train, y_train)
    accuracy = model.score(x_test, y_test)
    joblib.dump(model, path)
    return accuracy


if __name__ == "__main__":
    acc = train()
    print(f"Model trained and saved to {MODEL_PATH} (accuracy: {acc:.3f})")
