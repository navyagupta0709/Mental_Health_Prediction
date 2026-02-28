import streamlit as st
import os
import pickle

st.title("Mental Health Prediction App")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

if os.path.exists(MODEL_PATH):
    model = pickle.load(open(MODEL_PATH, "rb"))
    st.success("Model Loaded Successfully ✅")
else:
    st.warning("Model file not found ⚠️")
