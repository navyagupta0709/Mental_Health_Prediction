import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel("gemini-pro")
import streamlit as st
import os
import google.generativeai as genai
import random
import google.generativeai as genai

genai.configure(api_key="AIzaSyXXXXXXXXXXXX")

# -------- API CONFIG --------
genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel("gemini-pro")

# -------- PAGE CONFIG --------
st.set_page_config(page_title="Mental Health AI", layout="wide")

# -------- CUSTOM CSS --------
st.markdown("""
<style>
body {background-color: #0f172a;}
.main {color: white;}
.stButton>button {
    background: linear-gradient(45deg, #6366f1, #9333ea);
    color: white;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# -------- SESSION --------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "messages" not in st.session_state:
    st.session_state.messages = []

# -------- HOME --------
if st.session_state.page == "home":
    st.title("🧠 Mental Health AI Therapist")
    st.subheader("Your smart companion for mental wellness 💙")

    col1, col2 = st.columns(2)

    if col1.button("🚀 Start Assessment"):
        st.session_state.page = "form"

    if col2.button("💬 Talk to AI"):
        st.session_state.page = "chat"

# -------- FORM --------
elif st.session_state.page == "form":
    st.title("📋 Enter Details")

    st.session_state.age = st.slider("Age", 10, 60, 25)
    st.session_state.gender = st.selectbox("Gender", ["Male", "Female"])
    st.session_state.family = st.selectbox("Family History", ["Yes", "No"])

    if st.button("Next ➡"):
        st.session_state.page = "questions"

# -------- QUESTIONS --------
elif st.session_state.page == "questions":
    st.title("🧠 Mental Health Assessment")

    q1 = st.radio("Do you feel stressed frequently?", ["Never", "Sometimes", "Often"])
    q2 = st.radio("Do you feel tired or depressed?", ["Never", "Sometimes", "Often"])
    q3 = st.radio("Do you feel motivated?", ["Yes", "Sometimes", "No"])

    if st.button("Submit ✅"):
        score = 0

        if q1 == "Often": score += 2
        if q2 == "Often": score += 2
        if q3 == "No": score += 2

        st.session_state.score = score
        st.session_state.page = "result"

# -------- RESULT --------
elif st.session_state.page == "result":
    st.title("📊 Your Mental Health Report")

    score = st.session_state.score

    if score <= 2:
        status = "😊 Healthy"
        advice = "Keep maintaining balance 🌿"
    elif score <= 4:
        status = "😐 Moderate Stress"
        advice = "Try meditation and take breaks 🧘"
    else:
        status = "😟 High Stress"
        advice = "Consider talking to someone 💬"

    st.metric("Status", status)
    st.metric("Stress Score", f"{score * 20}%")

    st.markdown(f"### 💡 Suggestion: {advice}")

    if st.button("💬 Talk to AI Therapist"):
        st.session_state.page = "chat"

# -------- CHAT (AI THERAPIST) --------
elif st.session_state.page == "chat":
    st.title("💬 AI Therapist")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Share your feelings...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        prompt = f"""
        You are a professional mental health therapist.
        Give empathetic, calm, and supportive responses.
        Avoid giving harmful advice.

        User: {user_input}
        """

        response = model.generate_content(prompt)
        reply = response.text

        st.session_state.messages.append({"role": "assistant", "content": reply})

        with st.chat_message("assistant"):
            st.markdown(reply)

    if st.button("🔄 Start Again"):
        st.session_state.page = "home"
