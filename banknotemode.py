import pandas as pd 
import numpy as np
from sklearn.preprocessing import PowerTransformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

df = pd.read_csv("bank_note_authentication.csv")
print(df.head(10))
print(df.columns.tolist())
print(df.shape)
print(df.info())
print(df.isnull().sum())

print(df.skew())
pt = PowerTransformer(method='yeo-johnson')
df[['curt', 'entr']] = pt.fit_transform(df[['curt', 'entr']])

print(df.skew())

class_counts = df['auth'].value_counts()
print(class_counts)

x = df.drop(columns=["auth"]).values
y = df["auth"].values

x_train , X_test , Y_train , Y_test = train_test_split(
x , y , test_size=0.2 , random_state=42
)
model = LogisticRegression(solver= "liblinear" , random_state=0)

model.fit(x_train,Y_train)

y_pred = model.predict(X_test)

# You can also predict probabilities using .predict_proba()
probabilities = model.predict_proba(X_test)

print(f"Accuracy: {accuracy_score(Y_test, y_pred)}")
print("Confusion Matrix:")
print(confusion_matrix(Y_test, y_pred))
print("Classification Report:")
print(classification_report(Y_test, y_pred))

