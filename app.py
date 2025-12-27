from flask import Flask, jsonify, request
from flask_cors import CORS
import joblib
import numpy as np

app = Flask(__name__)
CORS(app)

model = joblib.load("best_diabetes_model.joblib")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        user_data = request.get_json()
        print("Received data:", user_data)  # Debug log
        # Extract values (SEX REMOVED!)
        features = [
            float(user_data['age']),
            float(user_data['bmi']),
            float(user_data['bp']),
            float(user_data['s1']),
            float(user_data['s2']),
            float(user_data['s3']),
            float(user_data['s4']),
            float(user_data['s5']),
            float(user_data['s6'])
        ]
        print("Features:", features)  # Debug log

        # reshape for sklearn
        features = np.array(features).reshape(1, -1)

        # prediction
        prediction = model.predict(features)[0]
        print("Prediction:", prediction)  # Debug log

        return jsonify({
            "prediction": float(prediction)
        })

    except Exception as e:
        print("Error:", str(e))  # Debug log
        return jsonify({"error": str(e)}), 500

@app.route('/info', methods=['GET'])
def info():
    return jsonify({"message": "API working successfully"})
if __name__ == "__main__":
    app.run(debug=True)
