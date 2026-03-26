import streamlit as st

# Page config
st.set_page_config(page_title="AI Therapist", layout="centered")

st.title("🧠 AI Mental Health Therapist")

st.write("Answer a few questions to assess your mental health and get suggestions.")

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

    score = (
        mapping[q1] +
        mapping[q2] +
        mapping[q3] +
        mapping[q4]
    )

    # Classification
    if score <= 2:
        result = "Healthy 😊"
    elif score <= 5:
        result = "Mild Stress 😐"
    else:
        result = "High Stress ⚠️"

    st.success(f"Your Mental Health Status: {result}")

    # -------------------------------
    # AI Therapist Response
    # -------------------------------
    def therapist_response(result):
        if result == "Healthy 😊":
            return "You're doing well! Keep maintaining a balanced lifestyle 🌿"
        elif result == "Mild Stress 😐":
            return "You might be experiencing some stress. Try meditation, exercise, and talking to friends 💙"
        else:
            return "It seems you're going through a tough time. Consider talking to a professional or someone you trust 🤍"

    st.subheader("💬 AI Therapist Suggestion")
    st.info(therapist_response(result))

# -------------------------------
# Chatbot Section
# -------------------------------
st.subheader("💭 Talk to AI Therapist")

user_input = st.text_input("How are you feeling today?")

if user_input:
    user_input = user_input.lower()

    if "sad" in user_input or "depressed" in user_input:
        st.write("I'm really sorry you're feeling this way 💙 Do you want to share what's bothering you?")
    elif "stress" in user_input or "anxious" in user_input:
        st.write("Try taking a deep breath. You're stronger than you think 🌿")
    elif "happy" in user_input:
        st.write("That's great to hear! Keep spreading positivity ✨")
    else:
        st.write("I'm here to listen 🙂 Tell me more about your feelings.")
