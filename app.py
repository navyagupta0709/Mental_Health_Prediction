import streamlit as st

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Mental Health AI", layout="wide")

# -------------------------------
# PREMIUM CSS
# -------------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}

/* Title */
h1 {
    text-align: center;
    font-size: 42px;
    background: linear-gradient(90deg, #38bdf8, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 30px;
}

/* Cards */
.card {
    background: rgba(30, 41, 59, 0.6);
    backdrop-filter: blur(15px);
    border-radius: 20px;
    padding: 25px;
    margin-bottom: 25px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    border: 1px solid rgba(255,255,255,0.08);
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg, #6366f1, #38bdf8);
    border-radius: 12px;
    height: 3em;
    width: 100%;
    font-size: 17px;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0px 0px 20px rgba(99,102,241,0.6);
}

/* Result */
.result-box {
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    font-size: 22px;
    font-weight: bold;
}

/* Colors */
.green { background: rgba(34,197,94,0.2); }
.orange { background: rgba(251,146,60,0.2); }
.red { background: rgba(239,68,68,0.2); }

</style>
""", unsafe_allow_html=True)

# -------------------------------
# HEADER
# -------------------------------
st.markdown("<h1>🧠 Mental Health AI Therapist</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Your smart companion for mental wellness 💙</p>", unsafe_allow_html=True)

# -------------------------------
# USER DETAILS
# -------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📋 Enter Details")

col1, col2 = st.columns(2)

with col1:
    age = st.slider("Age", 10, 60, 25)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])

with col2:
    family_history = st.selectbox("Family History", ["Yes", "No"])
    work_stress = st.selectbox("Work Interference", ["Never", "Sometimes", "Often"])

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# QUESTIONNAIRE
# -------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📝 Mental Health Assessment")

q1 = st.radio("Do you feel anxious frequently?", ["Never", "Sometimes", "Often"])
q2 = st.radio("Do you feel low or depressed?", ["Never", "Sometimes", "Often"])
q3 = st.radio("Do you have trouble sleeping?", ["No", "Sometimes", "Yes"])
q4 = st.radio("Do you feel motivated?", ["Yes", "Sometimes", "No"])

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# ANALYZE BUTTON
# -------------------------------
if st.button("🚀 Analyze My Mental Health"):

    mapping = {"Never": 0, "No": 0, "Sometimes": 1, "Often": 2, "Yes": 2}

    score = mapping[q1] + mapping[q2] + mapping[q3] + mapping[q4]

    # Result
    if score <= 2:
        result = "Healthy 😊"
        color = "green"
    elif score <= 5:
        result = "Mild Stress 😐"
        color = "orange"
    else:
        result = "High Stress ⚠️"
        color = "red"

    # Progress bar 🔥
    st.progress(score / 8)

    # Result card
    st.markdown(f"""
    <div class="card result-box {color}">
        Your Status: {result}
    </div>
    """, unsafe_allow_html=True)

    # Therapist logic
    def therapist_response(result):
        if "Healthy" in result:
            return "You're doing great! Maintain balance 🌿"
        elif "Mild" in result:
            return "Try meditation, exercise, and talking to friends 💙"
        else:
            return "Please consider professional help or talk to someone you trust 🤍"

    # Therapist UI
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("💬 AI Therapist Suggestion")
    st.write(therapist_response(result))
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# CHATBOT
# -------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("💭 Talk to AI Therapist")

user_input = st.text_input("How are you feeling today?")

if user_input:
    text = user_input.lower()

    if "sad" in text or "depressed" in text:
        st.write("I'm here for you 💙 Want to share more?")
    elif "stress" in text or "anxious" in text:
        st.write("Take a deep breath 🌿 You're stronger than you think.")
    elif "happy" in text:
        st.write("That's amazing! Keep smiling ✨")
    else:
        st.write("Tell me more 🙂")

st.markdown("</div>", unsafe_allow_html=True)
