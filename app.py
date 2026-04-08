import streamlit as st
from ai_therapist import generate_reply

st.set_page_config(page_title="AI Therapist", layout="centered")

st.title("🧠 Mental Health AI Therapist")
st.write("Assess your mental health and talk to an AI therapist 💙")

# -------------------------------
# SESSION STATE
# -------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "result" not in st.session_state:
    st.session_state.result = None

# -------------------------------
# ASSESSMENT SECTION
# -------------------------------
st.subheader("📝 Mental Health Assessment")

q1 = st.radio("Do you feel anxious frequently?", ["Never", "Sometimes", "Often"])
q2 = st.radio("Do you feel low or depressed?", ["Never", "Sometimes", "Often"])
q3 = st.radio("Do you have trouble sleeping?", ["No", "Sometimes", "Yes"])
q4 = st.radio("Do you feel motivated in daily life?", ["Yes", "Sometimes", "No"])

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

    st.session_state.result = (result, advice)

# -------------------------------
# SHOW RESULT
# -------------------------------
if st.session_state.result:
    result, advice = st.session_state.result

    st.success(f"Your Mental Health Status: {result}")
    st.info(f"💡 Suggestion: {advice}")

# -------------------------------
# CHAT SECTION
# -------------------------------
st.subheader("💬 Talk to AI Therapist")

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

        st.session_state.chat_history.append(("assistant", reply))

if col2.button("Clear Chat"):
    st.session_state.chat_history = []
