import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app  # noqa: E402

client = app.test_client()


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json() == {"status": "ok"}


def test_home_page():
    assert client.get("/").status_code == 200


def test_predict_json_setosa():
    r = client.post(
        "/predict",
        json={"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2},
    )
    assert r.status_code == 200
    assert r.get_json()["prediction"] == "setosa"


def test_predict_form():
    r = client.post(
        "/predict",
        data={"sepal_length": 6.7, "sepal_width": 3.0, "petal_length": 5.2, "petal_width": 2.3},
    )
    assert r.status_code == 200
    assert b"virginica" in r.data


def test_predict_bad_input():
    r = client.post("/predict", json={"sepal_length": "abc"})
    assert r.status_code == 400


def test_metrics():
    client.get("/health")
    r = client.get("/metrics")
    assert r.status_code == 200
    assert b"app_requests_total" in r.data
