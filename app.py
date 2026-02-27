from flask import Flask, jsonify, request
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)
CORS(app)

# ================================
# Load Models (ONCE at startup)
# ================================
diabetes_model = joblib.load("best_diabetes_model.joblib")

banknote_model = joblib.load("bank_note_authentication_model.joblib")
banknote_transformer = joblib.load("power_transformer.joblib")

# Load breast cancer model components
breast_cancer_components = joblib.load("breast_cancer_model.joblib")
breast_cancer_model = breast_cancer_components["model"]
breast_cancer_transformer = breast_cancer_components["transformer"]
breast_cancer_feature_names = breast_cancer_components["feature_names"]
breast_cancer_feature_importance = breast_cancer_components["feature_importance"]
breast_cancer_feature_info = breast_cancer_components["feature_info"]

# Load Bitcoin model
bitcoin_model = joblib.load("bitcoin_model.joblib")

# ================================
# Health Check
# ================================
@app.route("/info", methods=["GET"])
def info():
    return jsonify({
        "status": "API is running",
        "models": ["diabetes", "banknote", "breastcancer", "bitcoin"]
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
# Breast Cancer Prediction API
# ================================
@app.route("/api/breastcancer/predict", methods=["POST"])
def predict_breast_cancer():
    try:
        data = request.get_json()

        # Extract all 30 features in the correct order
        features = np.array([[float(data[feature]) for feature in breast_cancer_feature_names]])

        # Apply power transformer to normalize skewed features
        features_normalized = breast_cancer_transformer.transform(features)

        # Make prediction
        prediction = int(breast_cancer_model.predict(features_normalized)[0])
        probability = breast_cancer_model.predict_proba(features_normalized).tolist()

        # Get prediction class name
        prediction_label = breast_cancer_components["classes"][prediction]

        # Format feature importance for response (top 10)
        feature_importance_list = [
            {"feature": k, "importance": float(v), "label": breast_cancer_feature_info.get(k, {}).get("label", k)}
            for k, v in list(breast_cancer_feature_importance.items())[:10]
        ]

        return jsonify({
            "prediction": prediction,
            "prediction_label": prediction_label,
            "probability": probability,
            "confidence": float(max(probability[0])) * 100,
            "feature_importance": feature_importance_list
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ================================
# Bitcoin Price Prediction API
# ================================

@app.route("/api/bitcoin/predict", methods=["POST"])
def predict_bitcoin():
    try:
        data = request.get_json()
        
        current_price = float(data["price"])
        
        # Get current time features
        now = pd.Timestamp.now()
        
        # Prepare features: [lag1, lag2, price, hour, minute, dayofweek]
        # For prediction, we use current_price as both lag1 and lag2
        features = np.array([[
            current_price,  # lag1
            current_price,  # lag2
            current_price,  # price
            now.hour,
            now.minute,
            now.dayofweek
        ]])
        
        prediction = float(bitcoin_model.predict(features)[0])
        
        # Calculate price change
        price_change = prediction - current_price
        price_change_percent = (price_change / current_price) * 100
        
        return jsonify({
            "current_price": current_price,
            "predicted_price": round(prediction, 2),
            "price_change": round(price_change, 2),
            "price_change_percent": round(price_change_percent, 2),
            "prediction_timeframe": "2 minutes ahead"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ================================
# Run Server
# ================================
if __name__ == "__main__":
    app.run(port=5000, debug=True)
