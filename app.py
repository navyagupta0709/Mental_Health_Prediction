import streamlit as st
from ai_therapist import generate_reply
import re
import warnings

warnings.filterwarnings("ignore")

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="AI Therapist", layout="centered")

# -------------------------------
# UI (UNCHANGED STYLE)
# -------------------------------
st.markdown("""
<style>
.title {text-align:center;font-size:32px;font-weight:bold;}
.chat-user {background:#1E1E1E;padding:10px;border-radius:10px;margin:5px;}
.chat-bot {background:#262730;padding:10px;border-radius:10px;margin:5px;}
.stButton button {border-radius:10px;background:linear-gradient(90deg,#4CAF50,#00C9A7);color:white;}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🧠 AI Mental Health Therapist</div>", unsafe_allow_html=True)

# -------------------------------
# SESSION STATE
# -------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "result" not in st.session_state:
    st.session_state.result = None

# -------------------------------
# 📝 ASSESSMENT
# -------------------------------
st.subheader("📝 Mental Health Assessment")

q1 = st.radio("Do you feel anxious frequently?", ["Never", "Sometimes", "Often"])
q2 = st.radio("Do you feel low or depressed?", ["Never", "Sometimes", "Often"])
q3 = st.radio("Do you have trouble sleeping?", ["No", "Sometimes", "Yes"])
q4 = st.radio("Do you feel motivated in daily life?", ["Yes", "Sometimes", "No"])

if st.button("Assess My Mental Health"):

    mapping = {"Never":0,"No":0,"Sometimes":1,"Often":2,"Yes":2}
    score = mapping[q1] + mapping[q2] + mapping[q3] + mapping[q4]

    if score <= 2:
        result = "Healthy 😊"
        advice = "You're doing well! Maintain a balanced lifestyle 🌿"
    elif score <= 5:
        result = "Mild Stress 😐"
        advice = "Try meditation, exercise, and talking to friends 💙"
    else:
        result = "High Stress ⚠️"
        advice = "Consider talking to a professional 🤍"

    st.session_state.result = (result, advice)

if st.session_state.result:
    r, a = st.session_state.result
    st.success(f"Your Mental Health Status: {r}")
    st.info(f"💡 Suggestion: {a}")

# -------------------------------
# 💬 CHAT SECTION
# -------------------------------
st.subheader("💬 Talk to AI Therapist")

for role, msg in st.session_state.chat_history:
    if role == "user":
        st.markdown(f"<div class='chat-user'>🧑 {msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bot'>🤖 {msg}</div>", unsafe_allow_html=True)

user_input = st.text_input("Talk in any language...")

col1, col2 = st.columns(2)

# -------------------------------
# NLP INTENT DETECTION
# -------------------------------
def detect_intent(text):
    text = text.lower()

    if re.search(r"stress|anxiety|tension|nervous", text):
        return "stress"
    elif re.search(r"sad|depressed|low|cry", text):
        return "depression"
    elif re.search(r"lonely|alone", text):
        return "loneliness"
    elif re.search(r"fever|bukhar|headache|cold|cough", text):
        return "health"
    else:
        return "general"

# -------------------------------
# CBT STYLE RESPONSES
# -------------------------------
def therapy_response(intent):

    if intent == "stress":
        return "I understand this feels overwhelming 💙. Try a small grounding exercise: take a slow breath in for 4 seconds, hold for 4, and release for 6. What seems to be causing this stress?"

    elif intent == "depression":
        return "I'm really sorry you're feeling this way 💙. Sometimes even small steps matter—like getting out of bed or talking to someone. What’s been on your mind lately?"

    elif intent == "loneliness":
        return "Feeling alone can be really heavy 🤝. You’re not alone in this moment—we’re talking right now. Would you like to share what’s been making you feel this way?"

    elif intent == "health":
        return "It seems like a health concern. Basic care like rest, hydration, and paracetamol may help. If symptoms persist, please consult a doctor."

    return None

# -------------------------------
# SEND BUTTON
# -------------------------------
if col1.button("Send"):
    if user_input.strip() != "":

        st.session_state.chat_history.append(("user", user_input))

        intent = detect_intent(user_input)

        # first try NLP therapy response
        reply = therapy_response(intent)

        # fallback to AI
        if reply is None:
            try:
                reply = generate_reply(user_input, st.session_state.chat_history)
            except:
                reply = "I'm here for you 💙. Tell me more about how you're feeling."

        st.session_state.chat_history.append(("assistant", reply))

if col2.button("Clear Chat"):
    st.session_state.chat_history = []
