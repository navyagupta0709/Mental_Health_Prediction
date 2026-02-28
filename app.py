import streamlit as st
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

st.title("Mental Health Prediction App")

# ---- File Path ----
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "mental_health.csv")

# ---- Load Dataset ----
try:
    data = pd.read_csv(DATA_PATH, encoding="latin1")
    st.success("Dataset Loaded Successfully ✅")
except:
    st.error("Dataset not found ❌")
    st.stop()

st.write(data.head())

# ---- Train Model ----
if st.button("Train Model"):

    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]

    X = pd.get_dummies(X)

    if y.dtype == "object":
        y = y.astype("category").cat.codes

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    accuracy = accuracy_score(y_test, model.predict(X_test))

    st.success(f"Model Trained Successfully 🎉")
    st.write(f"Accuracy: {accuracy:.2f}")
