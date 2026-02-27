# Bitcoin Price Prediction System - TODO

## Phase 1: Backend - Update Python Script
- [x] 1.1 Update bitcoinmodel.py to save model to joblib file
- [x] 1.2 Add model saving functionality

## Phase 2: Backend - Update API
- [x] 2.1 Load bitcoin model in app.py
- [x] 2.2 Add `/api/bitcoin/predict` endpoint
- [x] 2.3 Return prediction, price change, and percentage

## Phase 3: Frontend - Create Bitcoin Component
- [x] 3.1 Create bitcoin.jsx with price input field
- [x] 3.2 Display current price, predicted price, and change
- [x] 3.3 Style with orange theme (Bitcoin colors)

## Phase 4: Frontend - Setup
- [x] 4.1 Update App.jsx to include Bitcoin component

## Phase 5: Generate Model File
- [x] 5.1 Run bitcoinmodel.py to generate bitcoin_model.joblib
- [x] 5.2 Verify model file exists (4.4 MB)

## Model Information:
- Algorithm: RandomForestRegressor
- Features: lag1, lag2, price, hour, minute, dayofweek
- Target: Predict price 2 minutes ahead
- n_estimators: 200

