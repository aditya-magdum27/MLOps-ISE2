# MLOps ISE-2: Iris Classifier with CI/CD and Monitoring

ML web application (Flask + scikit-learn) with a full CI/CD and monitoring setup.

**Course:** ML DevOps Laboratory (UAMPC0732), ISE-2
**Tools:** Python, Flask, Git, GitHub, GitHub Actions, Jenkins, Docker, Docker Compose, Prometheus, Grafana

## Project structure

```
.
├── app.py                  # Flask app (UI, /predict, /health, /metrics)
├── train_model.py          # Trains and saves the RandomForest model
├── templates/index.html    # Web UI
├── tests/test_app.py       # Pytest test suite
├── requirements.txt
├── Dockerfile
├── docker-compose.yml      # app + Prometheus + Grafana
├── monitoring/prometheus.yml
├── Jenkinsfile             # Jenkins CI/CD pipeline
├── .github/workflows/ci.yml# GitHub Actions CI
└── DOCUMENTATION.md        # Tool configuration notes for the lab template
```

## Run locally

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python train_model.py
python app.py                   # http://localhost:5000
pytest -v
```

## Run with Docker

```bash
docker build -t iris-mlops-app .
docker run -p 5000:5000 iris-mlops-app
```

## Run app + monitoring stack

```bash
docker compose up -d --build
```

| Service    | URL                          |
|------------|------------------------------|
| App        | http://localhost:5000        |
| Metrics    | http://localhost:5000/metrics|
| Prometheus | http://localhost:9090        |
| Grafana    | http://localhost:3000 (admin / admin) |

## API

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2}'
# {"prediction":"setosa"}
```

## CI/CD flow

1. Push code to GitHub, which triggers GitHub Actions (install, train, test, Docker build).
2. Jenkins pipeline (`Jenkinsfile`): Checkout, Install, Train, Test, Docker build, Smoke test, Deploy via Compose.
3. Prometheus scrapes `/metrics`, and Grafana visualises the data.

Custom metrics: `app_requests_total`, `app_request_latency_seconds`, `app_predictions_total`.
