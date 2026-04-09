import streamlit as st

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="AI Therapist 💙", layout="centered")

st.title("💙 DeepChat - AI Therapist")
st.write("Talk freely. I'm here to listen 🤗")

# -------------------------------
# Session State Initialize
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# -------------------------------
# Dummy AI Response Function
# (You can replace with your ML model / OpenAI API later)
# -------------------------------
def generate_response(user_text):
    if "sad" in user_text.lower():
        return "I'm really sorry you're feeling sad. Want to talk about what's bothering you?"
    elif "stress" in user_text.lower():
        return "Stress can be tough. Try taking a deep breath. I'm here with you."
    elif "happy" in user_text.lower():
        return "That's wonderful! 😊 What made you feel happy today?"
    else:
        return "I understand. Tell me more about how you're feeling."

# -------------------------------
# Clear Input Function (IMPORTANT FIX)
# -------------------------------
def clear_input():
    st.session_state.user_input = ""

# -------------------------------
# Chat Input
# -------------------------------
user_input = st.text_input("Type your message...", key="user_input")

# -------------------------------
# Send Button
# -------------------------------
if st.button("Send"):
    if user_input.strip() != "":
        # Save user message
        st.session_state.messages.append(("You", user_input))

        # Generate AI reply
        response = generate_response(user_input)
        st.session_state.messages.append(("AI Therapist", response))

        # Clear input safely
        clear_input()

# -------------------------------
# Display Chat
# -------------------------------
st.divider()

for sender, msg in st.session_state.messages:
    if sender == "You":
        st.markdown(f"🧑‍💬 **You:** {msg}")
    else:
        st.markdown(f"🤖 **AI Therapist:** {msg}")
