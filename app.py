import streamlit as st
from ai_therapist import generate_reply

# Page config
st.set_page_config(page_title="AI Therapist", layout="centered")

st.title("🧠 AI Mental Health Therapist")
st.write("Answer a few questions to assess your mental health and talk to AI therapist.")

# -------------------------------
# Questionnaire Section
# -------------------------------
st.subheader("📝 Mental Health Assessment")

q1 = st.radio("Do you feel anxious frequently?", ["Never", "Sometimes", "Often"])
q2 = st.radio("Do you feel low or depressed?", ["Never", "Sometimes", "Often"])
q3 = st.radio("Do you have trouble sleeping?", ["No", "Sometimes", "Yes"])
q4 = st.radio("Do you feel motivated in daily life?", ["Yes", "Sometimes", "No"])

# -------------------------------
# Assessment Logic
# -------------------------------
if st.button("Assess My Mental Health"):

    mapping = {
        "Never": 0,
        "No": 0,
        "Sometimes": 1,
        "Often": 2,
        "Yes": 2
    }

    score = mapping[q1] + mapping[q2] + mapping[q3] + mapping[q4]

    if score <= 2:
        result = "Healthy 😊"
        advice = "You're doing well! Keep maintaining a balanced lifestyle 🌿"
    elif score <= 5:
        result = "Mild Stress 😐"
        advice = "You might be experiencing some stress. Try meditation, exercise, and talking to friends 💙"
    else:
        result = "High Stress ⚠️"
        advice = "It seems you're going through a tough time. Consider talking to a professional 🤍"

    st.success(f"Your Mental Health Status: {result}")
    st.info(advice)

# -------------------------------
# Chatbot Section
# -------------------------------
st.subheader("💬 Talk to AI Therapist")

# session memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# show chat
for role, msg in st.session_state.chat_history:
    if role == "user":
        st.markdown(f"🧑 You: {msg}")
    else:
        st.markdown(f"🤖 Therapist: {msg}")

user_input = st.text_input("Share your feelings...")

col1, col2 = st.columns(2)

if col1.button("Send"):
    if user_input:
        st.session_state.chat_history.append(("user", user_input))

        reply = generate_reply(user_input, st.session_state.chat_history)

        st.session_state.chat_history.append(("bot", reply))

if col2.button("Clear Chat"):
    st.session_state.chat_history = []
