import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import PowerTransformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.tree import DecisionTreeClassifier

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

    dt_model = DecisionTreeClassifier(
       max_depth=8,
    min_samples_split=2,
    min_samples_leaf=1,
    criterion="gini",
    random_state=42
    )

    dt_model.fit(X_train,y_train)

    dt_predict = dt_model.predict(X_test)

    print("\nDecision Tree Accuracy:", accuracy_score(y_test, dt_predict))
    print("\nDecision Tree Confusion Matrix:")
    print(confusion_matrix(y_test, dt_predict))
    print("\nDecision Tree Classification Report:")
    print(classification_report(y_test, dt_predict))

    joblib.dump(dt_model, "bank_note_authentication_model.joblib")
    joblib.dump(pt, "power_transformer.joblib")

    print("\nModel and transformer saved successfully!")


if __name__ == "__main__":
    train_and_test_data()
