import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Mental Health AI", layout="wide")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {background-color: #0f172a; color: white;}
.stButton>button {
    background: linear-gradient(45deg, #6366f1, #9333ea);
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- SMART AI FUNCTION ----------------
def ai_therapist_reply(text):
    text = text.lower()

    if any(word in text for word in ["sad", "depressed", "cry", "upset"]):
        return "I'm really sorry you're feeling this way 💙 You don't have to go through this alone. Do you want to talk about what’s making you feel this way?"

    elif any(word in text for word in ["stress", "anxious", "worried", "pressure"]):
        return "That sounds really stressful. Let's slow down for a moment. Take a deep breath… what's been weighing on your mind?"

    elif any(word in text for word in ["lonely", "alone"]):
        return "Feeling lonely can be really hard. I'm here with you 🤝 Do you feel like something specific is causing this?"

    elif any(word in text for word in ["happy", "good", "great"]):
        return "That’s really nice to hear 😊 What made you feel this way today?"

    elif any(word in text for word in ["tired", "exhausted"]):
        return "You sound really drained. Have you been getting enough rest lately?"

    elif any(word in text for word in ["suicide", "kill myself", "end my life"]):
        return "I'm really concerned about you 💔 You're not alone. Please consider reaching out to a trusted person or a helpline immediately."

    else:
        return "I’m here to listen 💙 Tell me more about what you're experiencing."

# ---------------- HOME ----------------
if st.session_state.page == "home":
    st.title("🧠 Mental Health AI Therapist")
    st.subheader("Your smart companion for emotional wellness 💙")

    col1, col2 = st.columns(2)

    if col1.button("🚀 Start Assessment"):
        st.session_state.page = "form"

    if col2.button("💬 Talk to AI"):
        st.session_state.page = "chat"

# ---------------- FORM ----------------
elif st.session_state.page == "form":
    st.title("📋 Enter Details")

    st.session_state.age = st.slider("Age", 10, 60, 25)
    st.session_state.gender = st.selectbox("Gender", ["Male", "Female"])
    st.session_state.family = st.selectbox("Family History", ["Yes", "No"])

    if st.button("Next ➡"):
        st.session_state.page = "questions"

# ---------------- QUESTIONS ----------------
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

# ---------------- RESULT ----------------
elif st.session_state.page == "result":
    st.title("📊 Your Result")

    score = st.session_state.score

    if score <= 2:
        status = "😊 Healthy"
        advice = "Keep maintaining balance 🌿"
    elif score <= 4:
        status = "😐 Moderate Stress"
        advice = "Try meditation, take breaks, and talk to someone 🧘"
    else:
        status = "😟 High Stress"
        advice = "Please consider talking to a trusted person or therapist 💬"

    st.metric("Status", status)
    st.metric("Stress Score", f"{score * 20}%")

    st.markdown(f"### 💡 Suggestion: {advice}")

    if st.button("💬 Talk to AI Therapist"):
        st.session_state.page = "chat"

# ---------------- CHAT ----------------
elif st.session_state.page == "chat":
    st.title("💬 AI Therapist")

    user_input = st.text_input("Type your message...")

    if st.button("Send") and user_input:
        reply = ai_therapist_reply(user_input)

        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("AI", reply))

    # Show chat history
    for sender, message in st.session_state.chat_history:
        if sender == "You":
            st.markdown(f"**🧑 You:** {message}")
        else:
            st.markdown(f"**🤖 AI:** {message}")

    if st.button("🔄 Start Again"):
        st.session_state.page = "home"
        st.session_state.chat_history = []
