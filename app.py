import streamlit as st

# -------------------------------
# CONFIG
# -------------------------------
st.set_page_config(page_title="Mental Health AI", layout="centered")

# -------------------------------
# CSS (CLEAN PREMIUM)
# -------------------------------
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}

h1, h2, h3 {
    text-align: center;
    color: #38bdf8;
}

.stButton>button {
    background: linear-gradient(90deg, #38bdf8, #6366f1);
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    border: none;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# SESSION STATE
# -------------------------------
if "page" not in st.session_state:
    st.session_state.page = 1

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------------------
# HEADER
# -------------------------------
st.title("🧠 Mental Health AI Therapist")
st.write("Your smart companion for mental wellness 💙")

# =====================================================
# PAGE 1
# =====================================================
if st.session_state.page == 1:

    st.subheader("📋 Enter Details")

    age = st.slider("Age", 10, 60, 25)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    family = st.selectbox("Family History", ["Yes", "No"])

    if st.button("Next ➡"):
        st.session_state.page = 2

# =====================================================
# PAGE 2
# =====================================================
elif st.session_state.page == 2:

    st.subheader("📝 Mental Health Assessment")

    q1 = st.radio("Do you feel anxious frequently?", ["Never", "Sometimes", "Often"])
    q2 = st.radio("Do you feel low or depressed?", ["Never", "Sometimes", "Often"])
    q3 = st.radio("Do you have trouble sleeping?", ["No", "Sometimes", "Yes"])
    q4 = st.radio("Do you feel motivated?", ["Yes", "Sometimes", "No"])

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅ Back"):
            st.session_state.page = 1

    with col2:
        if st.button("Analyze 🚀"):
            mapping = {"Never": 0, "No": 0, "Sometimes": 1, "Often": 2, "Yes": 2}
            score = mapping[q1] + mapping[q2] + mapping[q3] + mapping[q4]

            st.session_state.score = score
            st.session_state.page = 3

# =====================================================
# PAGE 3
# =====================================================
elif st.session_state.page == 3:

    score = st.session_state.score

    if score <= 2:
        result = "Healthy 😊"
    elif score <= 5:
        result = "Mild Stress 😐"
    else:
        result = "High Stress ⚠️"

    st.subheader(f"📊 Your Status: {result}")

    # AI Suggestion
    if "Healthy" in result:
        suggestion = "You're doing great! Keep maintaining balance 🌿"
    elif "Mild" in result:
        suggestion = "You may be stressed. Try meditation & talking to loved ones 💙"
    else:
        suggestion = "Please consider professional help 🤍 You’re not alone."

    st.subheader("💬 AI Therapist Suggestion")
    st.write(suggestion)

# ---------------- CHATBOT ----------------
st.subheader("💭 Talk to AI Therapist")

# Initialize
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat
for sender, msg in st.session_state.chat_history:
    st.write(f"**{sender}:** {msg}")

# Form (IMPORTANT FIX 🔥)
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message...")
    submit = st.form_submit_button("Send 💬")

    if submit and user_input.strip() != "":

        # AI logic
        if "sad" in user_input.lower():
            response = "I'm here for you 💙 Want to tell me what happened?"
        elif "stress" in user_input.lower():
            response = "Take a deep breath 🌿 What's stressing you out?"
        elif "happy" in user_input.lower():
            response = "That's amazing! Tell me more ✨"
        else:
            response = "I understand 🙂 Tell me more."

        # Save chat
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("AI", response))

    # Show chat history
    for sender, msg in st.session_state.chat_history:
        st.write(f"**{sender}:** {msg}")

    # RESET BUTTON
    if st.button("🔄 Start Again"):
    st.session_state.page = 1
    st.session_state.chat_history = []
