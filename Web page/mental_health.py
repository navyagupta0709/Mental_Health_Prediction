import streamlit as st
import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

st.title("Mental Health Prediction App")

# -------- File Path Fix --------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "mental_health.csv")

# -------- Load Dataset Safely --------
try:
    data = pd.read_csv(DATA_PATH, encoding="latin1")
    st.success("Dataset Loaded Successfully ✅")
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# -------- Basic Data Display --------
st.subheader("Dataset Preview")
st.write(data.head())

# -------- Simple Model Example --------
if st.button("Train Model"):

    # Assuming last column is target
    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]

    # Convert categorical to numeric
    X = pd.get_dummies(X)
    
    if y.dtype == "object":
        y = y.astype("category").cat.codes

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)

    st.success(f"Model Trained Successfully 🎉")
    st.write(f"Accuracy: {acc:.2f}")
