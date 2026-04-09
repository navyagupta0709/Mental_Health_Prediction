import streamlit as st
from ai_therapist import generate_reply

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="AI Therapist", layout="centered")

# -------------------------------
# PREMIUM UI
# -------------------------------
st.markdown("""
<style>
.title {text-align:center;font-size:32px;font-weight:bold;}
.subtitle {text-align:center;color:gray;margin-bottom:20px;}
.chat-user {background:#1E1E1E;padding:10px;border-radius:10px;margin:5px;}
.chat-bot {background:#262730;padding:10px;border-radius:10px;margin:5px;}
.stButton button {border-radius:10px;background:linear-gradient(90deg,#4CAF50,#00C9A7);color:white;}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🧠 AI Health & Mental Therapist</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Talk freely in any language 💙</div>", unsafe_allow_html=True)

# -------------------------------
# SESSION STATE
# -------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# -------------------------------
# CHAT DISPLAY
# -------------------------------
st.subheader("💬 Talk to AI Therapist")

for role, msg in st.session_state.chat_history:
    if role == "user":
        st.markdown(f"<div class='chat-user'>🧑 {msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bot'>🤖 {msg}</div>", unsafe_allow_html=True)

# -------------------------------
# INPUT
# -------------------------------
user_input = st.text_input("Type in any language...", key="user_input")

col1, col2 = st.columns(2)

if col1.button("Send"):
    if st.session_state.user_input.strip() != "":
        user_msg = st.session_state.user_input

        st.session_state.chat_history.append(("user", user_msg))

        # -------------------------------
        # BASIC MEDICAL LOGIC (SAFE)
        # -------------------------------
        msg_lower = user_msg.lower()

        if "fever" in msg_lower:
            reply = "It seems like you may have a fever 🤒. You can take rest, drink fluids, and use paracetamol for relief. If it continues, please consult a doctor."
        
        elif "headache" in msg_lower:
            reply = "Headaches can happen due to stress or dehydration. Try rest, hydration, and paracetamol if needed."
        
        elif "cold" in msg_lower or "cough" in msg_lower:
            reply = "For cold or cough, stay warm, drink fluids, and consider steam inhalation. If severe, consult a doctor."

        else:
            # AI therapist response
            reply = generate_reply(user_msg, st.session_state.chat_history)

        st.session_state.chat_history.append(("assistant", reply))

        st.session_state.user_input = ""

if col2.button("Clear Chat"):
    st.session_state.chat_history = []
