import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib
import time

df = yf.download("BTC-USD", period="1d", interval="1m", progress=False)

if df.empty:
    raise Exception("No data retrieved.")

if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

df.head()

df = df.reset_index()

df.head()


df = df.rename(columns={"Datetime": "timestamp"})
df = df.rename(columns={"Close": "price"})
df = df[["timestamp", "price"]]
df.head(10)

# Feature Engineering
df["hour"] = df["timestamp"].dt.hour
df["minute"] = df["timestamp"].dt.minute
df["dayofweek"] = df["timestamp"].dt.dayofweek

df["lag1"] = df["price"].shift(1)
df["lag2"] = df["price"].shift(2)

#predict 2 minutes ahead
df["target"] = df["price"].shift(-2)

df = df.dropna()

print (df)

X = df[["lag1", "lag2", "price", "hour", "minute", "dayofweek"]]
y = df["target"]

model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X, y)

# Save model to joblib file
joblib.dump(model, "bitcoin_model.joblib")
print("Model saved to bitcoin_model.joblib")

def predict_next_two_minutes(model, current_price):
    now = pd.Timestamp.now()

    X = np.array([[
        current_price,
        current_price,
        current_price,
        now.hour,
        now.minute,
        now.dayofweek
    ]])

    return model.predict(X)[0]

# Only run prediction if this script is executed directly
if __name__ == "__main__":
    # Load the model from joblib file
    model = joblib.load("bitcoin_model.joblib")
    print("Model loaded from bitcoin_model.joblib")
    
    user_price = float(input("Enter current Bitcoin price: "))
    prediction = predict_next_two_minutes(model, user_price)

    print("\nPredicted price in next 2 minutes:", round(prediction, 2))

