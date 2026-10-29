
from flask import Flask, request, jsonify
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

# Load dataset and train model
iris = load_iris()
X = iris.data
y = iris.target

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
model.fit(X, y)

@app.route("/")
def home():
    return """
    <h1>Iris Flower Prediction</h1>
    <p>Use /predict?sl=5.1&sw=3.5&pl=1.4&pw=0.2</p>
    """

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

@app.route("/predict")
def predict():
    try:
        values = [
            float(request.args["sl"]),
            float(request.args["sw"]),
            float(request.args["pl"]),
            float(request.args["pw"])
        ]
        prediction = model.predict([values])[0]
        return jsonify({
            "prediction": iris.target_names[prediction]
        })
    except (KeyError, ValueError):
        return jsonify({
            "error": "Provide numeric sl, sw, pl and pw values"
        }), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
