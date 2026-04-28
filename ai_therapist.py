import streamlit as st
from groq import Groq

# Initialize client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def generate_reply(user_input, chat_history):

    # Therapist system prompt
    messages = [
        {
            "role": "system",
            "content": """
You are a professional mental health therapist.

Rules:
- Always be empathetic and comforting
- Validate the user's feelings first
- Respond in the SAME language as the user
- Keep responses short and human-like
- Ask 1 follow-up question
- Avoid robotic tone
"""
        }
    ]

    # Add chat history
    for role, msg in chat_history:
        if role == "user":
            messages.append({"role": "user", "content": msg})
        else:
            messages.append({"role": "assistant", "content": msg})

    # Add current input
    messages.append({"role": "user", "content": user_input})

    # Generate response
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # ✅ working model
            messages=messages
        )

        return response.choices[0].message.content

    except Exception as e:
        return "I'm here for you 💙. Can you tell me more about how you're feeling?"
