import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Mental Health Prediction",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Mental Health Prediction App")

# ---------------- Load Dataset ----------------
try:
    data = pd.read_csv(
        "survey.csv",
        encoding="latin1",
        sep=None,
        engine="python",
        on_bad_lines="skip"
    )
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

st.success("Dataset Loaded Successfully ✅")

# Show dataset
with st.expander("📊 View Dataset"):
    st.dataframe(data.head())

# ---------------- Preprocessing ----------------
data = data.dropna()

# Target column (IMPORTANT: ensure treatment is your target)
if "treatment" not in data.columns:
    st.error("Target column 'treatment' not found in dataset.")
    st.stop()

y = data["treatment"]

# Convert Yes/No to 1/0
y = y.map({"Yes": 1, "No": 0})

X = data.drop("treatment", axis=1)

# Convert categorical to numeric
X = pd.get_dummies(X, drop_first=True)

# ---------------- Train Model ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)

st.success("Model Trained Successfully ✅")
st.info(f"Model Accuracy: {accuracy:.2f}")

# ---------------- Prediction Section ----------------
st.markdown("---")
st.subheader("🔮 Enter Details For Prediction")

input_data = {}

for col in X.columns:
    input_data[col] = st.number_input(f"{col}", value=0.0)

if st.button("Predict"):
    input_df = pd.DataFrame([input_data])
    input_df = input_df[X.columns]  # ensure correct column order

    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1]

    st.markdown("---")

    if prediction == 1:
        st.error(f"⚠ You may need treatment.\n\nProbability: {probability:.2f}")
    else:
        st.success(f"✅ You may not need treatment.\n\nProbability: {probability:.2f}")
