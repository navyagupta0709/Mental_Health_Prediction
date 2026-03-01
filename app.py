import streamlit as st
import pickle
import numpy as np
import os

st.title("Mental Health Prediction App")

# ---- Load Model Safely ----
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "model.pkl")

with open(model_path, "rb") as f:
    model = pickle.load(f)

st.success("Model Loaded Successfully ✅")

# ---- Input Fields ----
age = st.number_input("Enter Age", min_value=1, max_value=100)
work_hours = st.number_input("Working Hours per day", min_value=1, max_value=24)

if st.button("Predict"):
    features = np.array([[age, work_hours]])
    prediction = model.predict_proba(features)[0][1]

    if prediction > 0.5:
        st.error(f"You need treatment. Probability: {prediction:.2f}")
    else:
        st.success(f"You do not need treatment. Probability: {prediction:.2f}")
