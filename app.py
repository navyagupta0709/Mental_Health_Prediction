import streamlit as st

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Mental Health AI", layout="wide")

# -------------------------------
# CUSTOM CSS (PREMIUM UI)
# -------------------------------
st.markdown("""
<style>
body {
    background-color: #0f172a;
}

.main {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    color: white;
}

h1, h2, h3 {
    color: #38bdf8;
    text-align: center;
}

.stButton>button {
    background: linear-gradient(90deg, #38bdf8, #6366f1);
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 16px;
    border: none;
}

.stTextInput>div>div>input {
    border-radius: 10px;
}

.card {
    background: #1e293b;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 0px 15px rgba(56,189,248,0.3);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# HEADER
# -------------------------------
st.markdown("<h1>🧠 Mental Health AI Therapist</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Your smart companion for mental wellness 💙</p>", unsafe_allow_html=True)

# -------------------------------
# USER DETAILS CARD
# -------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)

st.subheader("📋 Enter Details")

age = st.slider("Age", 10, 60, 25)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
family_history = st.selectbox("Family History of Mental Illness", ["Yes", "No"])

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# QUESTIONNAIRE CARD
# -------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)

st.subheader("📝 Mental Health Assessment")

q1 = st.radio("Do you feel anxious frequently?", ["Never", "Sometimes", "Often"])
q2 = st.radio("Do you feel low or depressed?", ["Never", "Sometimes", "Often"])
q3 = st.radio("Do you have trouble sleeping?", ["No", "Sometimes", "Yes"])
q4 = st.radio("Do you feel motivated?", ["Yes", "Sometimes", "No"])

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# ASSESSMENT BUTTON
# -------------------------------
if st.button("🚀 Analyze My Mental Health"):

    mapping = {
        "Never": 0,
        "No": 0,
        "Sometimes": 1,
        "Often": 2,
        "Yes": 2
    }

    score = mapping[q1] + mapping[q2] + mapping[q3] + mapping[q4]

    # Result classification
    if score <= 2:
        result = "Healthy 😊"
        color = "green"
    elif score <= 5:
        result = "Mild Stress 😐"
        color = "orange"
    else:
        result = "High Stress ⚠️"
        color = "red"

    # RESULT CARD
    st.markdown(f"""
    <div class='card'>
        <h2 style='color:{color};'>Your Status: {result}</h2>
    </div>
    """, unsafe_allow_html=True)

    # AI THERAPIST RESPONSE
    def therapist_response(result):
        if "Healthy" in result:
            return "You're doing great! Keep maintaining a balanced lifestyle 🌿"
        elif "Mild" in result:
            return "You may be experiencing stress. Try meditation, exercise, and talking to loved ones 💙"
        else:
            return "You might be going through a tough time. Please consider professional help or talk to someone you trust 🤍"

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("💬 AI Therapist Suggestion")
    st.write(therapist_response(result))
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# CHATBOT SECTION
# -------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)

st.subheader("💭 Talk to AI Therapist")

user_input = st.text_input("How are you feeling today?")

if user_input:
    user_input = user_input.lower()

    if "sad" in user_input or "depressed" in user_input:
        st.write("I'm really sorry you're feeling this way 💙 Want to talk more?")
    elif "stress" in user_input or "anxious" in user_input:
        st.write("Take a deep breath 🌿 You're stronger than you think.")
    elif "happy" in user_input:
        st.write("That's amazing! Keep smiling ✨")
    else:
        st.write("I'm here to listen 🙂 Tell me more.")

st.markdown("</div>", unsafe_allow_html=True)
