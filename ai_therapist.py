import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_reply(user_input, chat_history):

    messages = [
        {
            "role": "system",
            "content": """
You are a professional mental health therapist.

- Always be empathetic
- Validate feelings first
- Respond in same language
- Ask follow-up question
- Sound human, not robotic
"""
        }
    ]

    for role, msg in chat_history:
        messages.append({
            "role": role,
            "content": msg
        })

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    return response.choices[0].message.content
