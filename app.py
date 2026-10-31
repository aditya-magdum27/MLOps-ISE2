"""Flask ML web app: Iris species classifier with Prometheus metrics."""
import os
import time

import joblib
from flask import Flask, Response, g, jsonify, render_template, request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

from train_model import CLASS_NAMES, FEATURES, MODEL_PATH, train

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "app_requests_total", "Total HTTP requests", ["method", "endpoint", "status"]
)
REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds", "Request latency in seconds", ["endpoint"]
)
PREDICTION_COUNT = Counter(
    "app_predictions_total", "Predictions made, by predicted class", ["species"]
)

if not os.path.exists(MODEL_PATH):
    train()
model = joblib.load(MODEL_PATH)


@app.before_request
def start_timer():
    g.start = time.time()


@app.after_request
def record_metrics(response):
    if request.path != "/metrics":
        elapsed = time.time() - g.get("start", time.time())
        REQUEST_LATENCY.labels(request.path).observe(elapsed)
        REQUEST_COUNT.labels(request.method, request.path, response.status_code).inc()
    return response


def _predict(values):
    species = CLASS_NAMES[int(model.predict([values])[0])]
    PREDICTION_COUNT.labels(species).inc()
    return species


@app.route("/")
def index():
    return render_template("index.html", features=FEATURES, result=None, error=None)


@app.route("/predict", methods=["POST"])
def predict():
    wants_json = request.is_json
    data = request.get_json(silent=True) if wants_json else request.form
    try:
        values = [float(data[f]) for f in FEATURES]
    except (KeyError, TypeError, ValueError):
        msg = f"Provide numeric values for: {', '.join(FEATURES)}"
        if wants_json:
            return jsonify(error=msg), 400
        return render_template("index.html", features=FEATURES, result=None, error=msg), 400

    species = _predict(values)
    if wants_json:
        return jsonify(prediction=species)
    return render_template("index.html", features=FEATURES, result=species, error=None)


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
