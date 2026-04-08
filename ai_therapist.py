import os
import streamlit as st
from langchain_groq import ChatGroq

# -------- API KEY --------
groq_api_key = os.getenv("GROQ_API_KEY") or st.secrets["GROQ_API_KEY"]

# -------- MODEL --------
llm = ChatGroq(
    api_key=groq_api_key,
    model="llama3-70b-8192"
)

# -------- FUNCTION --------
def generate_reply(user_input, chat_history):

    # convert chat history to text (IMPORTANT FIX)
    history_text = ""
    for role, msg in chat_history:
        if role == "user":
            history_text += f"User: {msg}\n"
        else:
            history_text += f"Therapist: {msg}\n"

    prompt = f"""
You are a professional mental health therapist.

Rules:
- Be empathetic and supportive
- Ask follow-up questions
- Keep answers short (2-4 lines)

Conversation so far:
{history_text}

User: {user_input}
Therapist:
"""

    response = llm.invoke(prompt)

    return response.content
