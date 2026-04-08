import os
import streamlit as st
from groq import Groq

# -------- API KEY --------
api_key = os.getenv("GROQ_API_KEY") or st.secrets["GROQ_API_KEY"]

client = Groq(api_key=api_key)

# -------- FUNCTION --------
def generate_reply(user_input, chat_history):

    messages = [
        {
            "role": "system",
            "content": """
You are a professional mental health therapist.

Rules:
- Be empathetic and calm
- Support the user emotionally
- Ask 1 follow-up question
- Keep answers short (2-4 lines)
"""
        }
    ]

    # -------- CHAT HISTORY --------
    for role, msg in chat_history:
        if role == "user":
            messages.append({"role": "user", "content": msg})
        else:
            messages.append({"role": "assistant", "content": msg})

    # -------- CURRENT MESSAGE --------
    messages.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",   # ✅ FINAL WORKING MODEL
            messages=messages
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ Error: {str(e)}"
