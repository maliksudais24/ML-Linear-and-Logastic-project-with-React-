from flask import Flask, jsonify, request
from flask_cors import CORS
import joblib
import numpy as np

app = Flask(__name__)
CORS(app)

# ================================
# Load Models (ONCE at startup)
# ================================
diabetes_model = joblib.load("best_diabetes_model.joblib")

banknote_model = joblib.load("bank_note_authentication_model.joblib")
banknote_transformer = joblib.load("power_transformer.joblib")

# ================================
# Health Check
# ================================
@app.route("/info", methods=["GET"])
def info():
    return jsonify({
        "status": "API is running",
        "models": ["diabetes", "banknote"]
    })

# ================================
# Diabetes Prediction API
# ================================
@app.route("/api/diabetes/predict", methods=["POST"])
def predict_diabetes():
    try:
        data = request.get_json()

        features = np.array([[
            float(data["age"]),
            float(data["bmi"]),
            float(data["bp"]),
            float(data["s1"]),
            float(data["s2"]),
            float(data["s3"]),
            float(data["s4"]),
            float(data["s5"]),
            float(data["s6"]),
        ]])

        prediction = diabetes_model.predict(features)[0]

        return jsonify({
            "prediction": float(prediction)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ================================
# Bank Note Authentication API
# ================================
@app.route("/api/banknote/authenticate", methods=["POST"])
def authenticate_banknote():
    try:
        data = request.get_json()

        features = np.array([[
            float(data["var"]),
            float(data["skew"]),
            float(data["curt"]),
            float(data["entr"]),
        ]])

        # Apply power transformer ONLY on curt & entr
        features[:, 2:4] = banknote_transformer.transform(features[:, 2:4])

        prediction = int(banknote_model.predict(features)[0])
        probability = banknote_model.predict_proba(features).tolist()

        return jsonify({
            "prediction": prediction,
            "probability": probability
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ================================
# Run Server
# ================================
if __name__ == "__main__":
    app.run(port=5000, debug=True)
