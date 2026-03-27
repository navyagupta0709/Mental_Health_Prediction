import streamlit as st

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Mental Health AI", layout="wide")

# -------------------------------
# CUSTOM CSS (PREMIUM LOOK)
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
    border-radius: 12px;
    height: 3em;
    width: 100%;
    font-size: 16px;
    border: none;
}

.card {
    background: #1e293b;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0px 0px 20px rgba(56,189,248,0.3);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# SESSION STATE
# -------------------------------
if "page" not in st.session_state:
    st.session_state.page = 1

# -------------------------------
# HEADER
# -------------------------------
st.markdown("<h1>🧠 Mental Health AI Therapist</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Your smart companion for mental wellness 💙</p>", unsafe_allow_html=True)

# =====================================================
# PAGE 1 → USER DETAILS
# =====================================================
if st.session_state.page == 1:

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📋 Enter Your Details")

    age = st.slider("Age", 10, 60, 25)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    family = st.selectbox("Family History of Mental Illness", ["Yes", "No"])

    if st.button("Next ➡"):
        st.session_state.age = age
        st.session_state.gender = gender
        st.session_state.family = family
        st.session_state.page = 2

    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# PAGE 2 → ASSESSMENT
# =====================================================
elif st.session_state.page == 2:

    st.markdown("<div class='card'>", unsafe_allow_html=True)
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

    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# PAGE 3 → RESULT + AI THERAPIST
# =====================================================
elif st.session_state.page == 3:

    score = st.session_state.score

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
            return "You might be going through a tough time. Please consider professional help 🤍"

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("💬 AI Therapist Suggestion")
    st.write(therapist_response(result))
    st.markdown("</div>", unsafe_allow_html=True)

    # CHATBOT
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("💭 Talk to AI Therapist")

    user_input = st.text_input("How are you feeling today?")

    if user_input:
        user_input = user_input.lower()

        if "sad" in user_input:
            st.write("I'm here for you 💙 Want to talk more?")
        elif "stress" in user_input:
            st.write("Take a deep breath 🌿 You're strong!")
        elif "happy" in user_input:
            st.write("That's amazing! Keep smiling ✨")
        else:
            st.write("Tell me more 🙂")

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🔄 Start Again"):
        st.session_state.page = 1
