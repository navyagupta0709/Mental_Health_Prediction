import streamlit as st
import random

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
    height: 3em;
    width: 100%;
}
.card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)

# -------- SESSION --------
if "page" not in st.session_state:
    st.session_state.page = "home"

# -------- HOME --------
if st.session_state.page == "home":
    st.title("🧠 Mental Health AI Therapist")
    st.subheader("Your smart companion for emotional wellness 💙")

    col1, col2 = st.columns(2)

    if col1.button("🚀 Start Assessment"):
        st.session_state.page = "form"

    if col2.button("💬 Talk to AI"):
        st.session_state.page = "chat"

# -------- FORM --------
elif st.session_state.page == "form":
    st.title("📋 Basic Information")

    st.session_state.age = st.slider("Age", 10, 60, 22)
    st.session_state.gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    st.session_state.family = st.selectbox("Family History of Mental Illness", ["Yes", "No"])

    if st.button("Next ➡"):
        st.session_state.page = "questions"

# -------- QUESTIONS --------
elif st.session_state.page == "questions":
    st.title("🧠 Mental Health Assessment")

    q1 = st.radio("Do you feel stressed frequently?", ["Never", "Sometimes", "Often"])
    q2 = st.radio("Do you feel tired or depressed?", ["Never", "Sometimes", "Often"])
    q3 = st.radio("Do you feel motivated?", ["Yes", "Sometimes", "No"])
    q4 = st.radio("Do you have trouble sleeping?", ["Never", "Sometimes", "Often"])

    if st.button("Submit ✅"):
        score = 0

        if q1 == "Often": score += 2
        if q2 == "Often": score += 2
        if q3 == "No": score += 2
        if q4 == "Often": score += 2

        st.session_state.score = score
        st.session_state.page = "result"

# -------- RESULT --------
elif st.session_state.page == "result":
    st.title("📊 Your Mental Health Report")

    score = st.session_state.score

    if score <= 2:
        status = "😊 Healthy"
        advice = "You are doing well. Keep maintaining a healthy routine 🌿"
    elif score <= 5:
        status = "😐 Moderate Stress"
        advice = "Try meditation, take breaks, and talk to someone you trust 🧘"
    else:
        status = "😟 High Stress"
        advice = "Consider seeking professional help and don't ignore your feelings 💬"

    col1, col2, col3 = st.columns(3)

    col1.metric("Status", status)
    col2.metric("Stress Score", f"{score * 15}%")
    col3.metric("Mood", random.choice(["Happy", "Neutral", "Low"]))

    st.markdown(f"### 💡 Suggestion: {advice}")

    if st.button("💬 Talk to AI Therapist"):
        st.session_state.page = "chat"

# -------- CHAT --------
elif st.session_state.page == "chat":
    st.title("💬 AI Therapist")

    user_input = st.text_input("Share your feelings...")

    if st.button("Send"):
        msg = user_input.lower()

        if "sad" in msg or "depressed" in msg:
            reply = "I'm really sorry you're feeling this way 💙. Want to share what's bothering you?"
        
        elif "stress" in msg or "anxiety" in msg:
            reply = "It sounds stressful. Try taking a deep breath. I'm here to listen 🧘"
        
        elif "happy" in msg:
            reply = "That's great to hear 😊! What made your day better?"
        
        elif "alone" in msg or "lonely" in msg:
            reply = "You’re not alone 🤝. I'm here with you. Tell me more."
        
        elif "tired" in msg:
            reply = "It sounds like you need rest. Try to relax and take care of yourself 🌸"
        
        else:
            reply = "I understand. I'm here to listen. Tell me more about what you're feeling 💬"

        st.write("🤖:", reply)

    if st.button("🔄 Back to Home"):
        st.session_state.page = "home"
