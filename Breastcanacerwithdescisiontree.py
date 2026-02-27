import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import PowerTransformer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# ================= USER-FRIENDLY FEATURE NAMES AND RANGES =================
# All 30 features of the breast cancer dataset with user-friendly names and ranges
FEATURE_INFO = {
    "mean radius": {"label": "Mean Radius", "range": "6.0 – 28.0", "unit": "mm"},
    "mean texture": {"label": "Mean Texture", "range": "9.0 – 40.0", "unit": "standard deviations"},
    "mean perimeter": {"label": "Mean Perimeter", "range": "40.0 – 190.0", "unit": "mm"},
    "mean area": {"label": "Mean Area", "range": "140.0 – 2500.0", "unit": "mm²"},
    "mean smoothness": {"label": "Mean Smoothness", "range": "0.05 – 0.16", "unit": "local variation"},
    "mean compactness": {"label": "Mean Compactness", "range": "0.02 – 0.35", "unit": "perimeter²/area - 1"},
    "mean concavity": {"label": "Mean Concavity", "range": "0.0 – 0.43", "unit": "severity of concave portions"},
    "mean concave points": {"label": "Mean Concave Points", "range": "0.0 – 0.20", "unit": "number of concave portions"},
    "mean symmetry": {"label": "Mean Symmetry", "range": "0.1 – 0.27", "unit": "symmetry measure"},
    "mean fractal dimension": {"label": "Mean Fractal Dimension", "range": "0.05 – 0.10", "unit": "coastline approximation"},
    "radius error": {"label": "Radius Error", "range": "0.1 – 2.0", "unit": "mm"},
    "texture error": {"label": "Texture Error", "range": "0.2 – 4.0", "unit": "standard deviations"},
    "perimeter error": {"label": "Perimeter Error", "range": "0.5 – 20.0", "unit": "mm"},
    "area error": {"label": "Area Error", "range": "2.0 – 550.0", "unit": "mm²"},
    "smoothness error": {"label": "Smoothness Error", "range": "0.001 – 0.03", "unit": "local variation"},
    "compactness error": {"label": "Compactness Error", "range": "0.002 – 0.08", "unit": "perimeter²/area - 1"},
    "concavity error": {"label": "Concavity Error", "range": "0.0 – 0.1", "unit": "severity of concave portions"},
    "concave points error": {"label": "Concave Points Error", "range": "0.0 – 0.05", "unit": "number of concave portions"},
    "symmetry error": {"label": "Symmetry Error", "range": "0.008 – 0.08", "unit": "symmetry measure"},
    "fractal dimension error": {"label": "Fractal Dimension Error", "range": "0.001 – 0.03", "unit": "coastline approximation"},
    "worst radius": {"label": "Worst Radius", "range": "7.0 – 36.0", "unit": "mm"},
    "worst texture": {"label": "Worst Texture", "range": "12.0 – 50.0", "unit": "standard deviations"},
    "worst perimeter": {"label": "Worst Perimeter", "range": "50.0 – 250.0", "unit": "mm"},
    "worst area": {"label": "Worst Area", "range": "200.0 – 4300.0", "unit": "mm²"},
    "worst smoothness": {"label": "Worst Smoothness", "range": "0.07 – 0.22", "unit": "local variation"},
    "worst compactness": {"label": "Worst Compactness", "range": "0.05 – 0.85", "unit": "perimeter²/area - 1"},
    "worst concavity": {"label": "Worst Concavity", "range": "0.0 – 1.0", "unit": "severity of concave portions"},
    "worst concave points": {"label": "Worst Concave Points", "range": "0.0 – 0.30", "unit": "number of concave portions"},
    "worst symmetry": {"label": "Worst Symmetry", "range": "0.15 – 0.45", "unit": "symmetry measure"},
    "worst fractal dimension": {"label": "Worst Fractal Dimension", "range": "0.06 – 0.15", "unit": "coastline approximation"},
}

def load_data():
    # Load dataset
    data = load_breast_cancer()

    X = pd.DataFrame(data.data, columns=data.feature_names)
    y = pd.Series(data.target, name="diagnosis")

    df = pd.concat([X, y], axis=1)
    print(df.head())

    print("\nSHAPE")
    print(df.shape)

    print("\nINFO")
    print(df.info())

    print("\nMISSING VALUES")
    print(df.isnull().sum())

    skewness = X.skew().sort_values(ascending=False)
    print("skweness",skewness)
    pt = PowerTransformer(method="yeo-johnson")
    X_normalized = pt.fit_transform(X)

    X_normalized = pd.DataFrame(
        X_normalized,
        columns=X.columns
    )

    print("skwenes  after ",X_normalized.skew().sort_values(ascending=False))
    df_normalized = pd.concat([X_normalized, y], axis=1)

    corr = df_normalized.corr()["diagnosis"].sort_values(ascending=False)

    print("\n===== FEATURE CORRELATION WITH TARGET =====")
    print(corr)

    plt.figure(figsize=(8, 10))
    sns.barplot(x=corr.values, y=corr.index)
    plt.title("Feature Correlation with Target")
    plt.show()

    return X_normalized, y

def split_data(X, y):
    return train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

def train_decision_tree(X_train, y_train):
    param_grid = {
        "max_depth": [3, 5, 7, 10, None],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4],
        "criterion": ["gini", "entropy"]
    }

    dt = DecisionTreeClassifier(random_state=42)

    grid = GridSearchCV(
        dt,
        param_grid,
        cv=5,
        scoring="accuracy",
        n_jobs=-1
    )

    grid.fit(X_train, y_train)

    print("\nBEST PARAMETERS")
    print(grid.best_params_)

    return grid.best_estimator_

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)

    print("\n ACCURACY")
    print(accuracy_score(y_test, y_pred))

    print("\n CONFUSION MATRIX")
    print(confusion_matrix(y_test, y_pred))

    print("\nCLASSIFICATION REPORT")
    print(classification_report(y_test, y_pred))

def visualize_tree(model, feature_names):
    plt.figure(figsize=(20, 10))
    plot_tree(
        model,
        feature_names=feature_names,
        class_names=["Malignant", "Benign"],
        filled=True
    )
    plt.show()

def save_model_components(model, transformer, feature_names, feature_info, output_path="breast_cancer_model.joblib"):
    """
    Save all model components to a single joblib file.
    
    Args:
        model: Trained Decision Tree model
        transformer: Fitted PowerTransformer
        feature_names: List of original feature names
        feature_info: Dictionary with user-friendly feature information
        output_path: Path to save the joblib file
    """
    import os
    
    # Extract feature importance
    feature_importance = dict(zip(feature_names, model.feature_importances_.tolist()))
    
    # Sort by importance
    feature_importance_sorted = dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=True))
    
    components = {
        "model": model,
        "transformer": transformer,
        "feature_names": feature_names,
        "feature_info": feature_info,
        "feature_importance": feature_importance_sorted,
        "classes": ["Malignant", "Benign"]  # 0 = Malignant, 1 = Benign
    }
    
    joblib.dump(components, output_path)
    print(f"\n===== MODEL SAVED TO {output_path} =====")
    print(f"Feature importance saved:")
    for i, (feature, importance) in enumerate(list(feature_importance_sorted.items())[:10]):
        print(f"  {i+1}. {feature}: {importance:.4f}")
    print(f"  ... and {len(feature_importance_sorted) - 10} more features")
    
    return components

def main():
    X, y = load_data()

    X_train, X_test, y_train, y_test = split_data(X, y)

    model = train_decision_tree(X_train, y_train)

    evaluate_model(model, X_test, y_test)

    visualize_tree(model, X.columns)
    
    # Get the PowerTransformer from the load_data function
    # Re-create it since we need to save it
    data = load_breast_cancer()
    X_original = pd.DataFrame(data.data, columns=data.feature_names)
    transformer = PowerTransformer(method="yeo-johnson")
    transformer.fit(X_original)
    
    # Save all components
    save_model_components(
        model=model,
        transformer=transformer,
        feature_names=data.feature_names.tolist(),
        feature_info=FEATURE_INFO
    )

if __name__ == "__main__":
    main()
