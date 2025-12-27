import pandas as pd
import joblib
from sklearn.datasets import load_diabetes
from sklearn.model_selection import KFold, GridSearchCV, train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score

def load_and_preprocess_data():
    data = load_diabetes(as_frame=True)

    # full dataframe
    df = data.frame.copy()
    print(df.head(10))
    print(df.columns.tolist())
    print(df.info())
    print(df.isnull().sum())

    # drop sex column
    df = df.drop(columns=["sex"])
    print("after drop the feature is now",df.columns.tolist())

    # separate X and Y properly (IMPORTANT FIX)
    X = df.drop(columns=["target"]).values
    Y = df["target"].values

    print("\nDataset Shape:", X.shape)
    print("Target Shape:", Y.shape)

    return X, Y

def train_model():

    X, Y = load_and_preprocess_data()
    x_train, x_test, y_train, y_test = train_test_split(
        X, Y, test_size=0.2, random_state=42
    )
    pipeline = Pipeline([
        ('poly', PolynomialFeatures(include_bias=False)),
        ('scaler', StandardScaler()),
        ('model', LinearRegression())
    ])

    param_grid = [
        {
            'poly__degree': [1, 2],
            'model': [LinearRegression()],
            'model__fit_intercept': [True, False]
        },
        {
            'poly__degree': [1, 2],
            'model': [Ridge()],
            'model__alpha': [0.1, 1, 10]
        },
        {
            'poly__degree': [1, 2],
            'model': [Lasso(max_iter=5000)],
            'model__alpha': [0.1, 1, 10]
        }
    ]

    kfold = KFold(n_splits=5, shuffle=True, random_state=42)

    grid = GridSearchCV(
        estimator=pipeline,
        param_grid=param_grid,
        cv=kfold,
        scoring='r2',
        n_jobs=-1,
        verbose=1
    )

    grid.fit(x_train, y_train)
    print("\nBest Grid Search Parameters:\n", grid.best_params_)
    print("\nBest Cross Validation Score:", grid.best_score_)

    y_pred = grid.predict(x_test)
    test_r2 = r2_score(y_test, y_pred)

    print("\nTest R² Score:", test_r2)
    print("\nSample Predictions:", y_pred[:5])

    joblib.dump(grid.best_estimator_, "best_diabetes_model.joblib")
    print("\nSaved model as best_diabetes_model.joblib")


if __name__ == "__main__":
    train_model()
