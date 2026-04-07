import streamlit as st
import google.generativeai as genai

# -------- API CONFIG --------
genai.configure(api_key="YOUR_API_KEY_HERE")

model = genai.GenerativeModel("gemini-pro")

# -------- PAGE --------
st.set_page_config(page_title="Mental Health AI", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🧠 Mental Health AI Therapist 💬")

# -------- CHAT HISTORY --------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------- USER INPUT --------
user_input = st.chat_input("Type your feelings...")

if user_input:
    # show user msg
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI response
    prompt = f"""
    You are a mental health therapist AI.
    Respond empathetically and supportively.

    User: {user_input}
    """

    response = model.generate_content(prompt)
    reply = response.text

    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.markdown(reply)
