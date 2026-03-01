import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# ---- Load Dataset ----
import streamlit as st
import pandas as pd

st.title("Mental Health Prediction App")

data = pd.read_csv(
    "mental_health.csv",
    encoding="latin1",
    sep=None,
    engine="python",
    on_bad_lines="skip"
)

st.success("Dataset Loaded Successfully ✅")
st.write(data.head())

# ---- Simple Example Columns ----
# IMPORTANT: apne dataset ke according column names change karna
X = data.iloc[:, :-1]
y = data.iloc[:, -1]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = LogisticRegression()
model.fit(X_train, y_train)

st.success("Model Trained Successfully ✅")

# ---- Take Input ----
inputs = []
for col in X.columns:
    value = st.number_input(f"Enter {col}")
    inputs.append(value)

if st.button("Predict"):
    prediction = model.predict([inputs])[0]

    if prediction == 1:
        st.error("You need treatment.")
    else:
        st.success("You do not need treatment.")
