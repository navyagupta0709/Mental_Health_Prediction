import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

st.title("Mental Health Prediction App")

# -------- Safe CSV Loading --------
try:
    # Try normal comma separator first
    data = pd.read_csv("mental_health.csv", engine="python")
except:
    try:
        # Try semicolon separator
        data = pd.read_csv("mental_health.csv", sep=";", engine="python")
    except Exception as e:
        st.error(f"CSV Loading Error: {e}")
        st.stop()

st.success("Dataset Loaded Successfully ✅")
st.write(data.head())

# -------- Train Model --------
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

    st.success("Model Trained Successfully 🎉")
    st.write(f"Accuracy: {accuracy:.2f}")
