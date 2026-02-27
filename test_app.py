#!/usr/bin/env python3

import sys
import os

# Add the current directory to the path
sys.path.append(os.getcwd())

print("Testing Flask app startup...")

try:
    # Test imports
    from flask import Flask, jsonify, request
    from flask_cors import CORS
    import joblib
    import numpy as np
    print("✓ All imports successful")
    
    # Test app creation
    app = Flask(__name__)
    CORS(app)
    print("✓ Flask app created successfully")
    
    # Test model loading
    diabetes_model = joblib.load("best_diabetes_model.joblib")
    banknote_model = joblib.load("bank_note_authentication_model.joblib")
    banknote_transformer = joblib.load("power_transformer.joblib")
    print("✓ All models loaded successfully")
    
    # Test routes
    @app.route("/test", methods=["GET"])
    def test():
        return jsonify({"status": "success"})
    
    print("✓ Routes defined successfully")
    print("\n🎉 Flask app is ready to run!")
    print("Run 'python app.py' to start the server on port 5000")
    
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
