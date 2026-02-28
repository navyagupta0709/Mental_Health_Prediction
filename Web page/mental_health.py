import streamlit as st
import pandas as pd
import numpy as np
import os
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

st.title("Mental Health Prediction App")

# -------- File Path Setup --------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "mental_health.csv")
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

# -------- Load Dataset --------
try:
    data = pd.read_csv(DATA_PATH, encoding="latin1")
    st.success("Dataset Loaded Successfully ✅")
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

st.subheader("Dataset Preview")
st.write(data.head())

# -------- Train or Load Model --------
model = None

if os.path.exists(MODEL_PATH):
    try:
        model = pickle.load(open(MODEL_PATH, "rb"))
        st.info("Existing Model Loaded ✅")
    except:
        st.warning("Model file found but couldn't load. Retrain required.")

if st.button("Train Model"):

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

    # Save model
    pickle.dump(model, open(MODEL_PATH, "wb"))

    st.success("Model Trained & Saved Successfully 🎉")
    st.write(f"Accuracy: {acc:.2f}")
