import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import PowerTransformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score


def load_data():
    df = pd.read_csv("bank_note_authentication.csv")

    print(df.head(10))
    print(df.columns.tolist())
    print(df.shape)
    print(df.info())
    print(df.isnull().sum())

    print("\nSkewness before transform:")
    print(df.skew())

    X = df.drop(columns=["auth"])
    y = df["auth"]

    return X, y


def train_and_test_data():
    X, y = load_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Apply PowerTransformer ONLY on training data
    pt = PowerTransformer(method="yeo-johnson")
    X_train[['curt', 'entr']] = pt.fit_transform(X_train[['curt', 'entr']])
    X_test[['curt', 'entr']] = pt.transform(X_test[['curt', 'entr']])

    print("\nSkewness after transform (train data):")
    print(X_train.skew())

    model = LogisticRegression(solver="liblinear", random_state=0)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("\nAccuracy:", accuracy_score(y_test, y_pred))
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # Save trained model
    joblib.dump(model, "bank_note_authentication_model.joblib")
    joblib.dump(pt, "power_transformer.joblib")

    print("\nModel and transformer saved successfully!")


if __name__ == "__main__":
    train_and_test_data()
