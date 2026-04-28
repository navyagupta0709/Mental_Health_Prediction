import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_reply(user_input, chat_history):

    messages = [
        {
            "role": "system",
            "content": """
You are a professional mental health therapist.

Rules:
- Be empathetic and comforting
- Always validate feelings first
- Respond in SAME language
- Keep answers short
- Ask 1 follow-up question
"""
        }
    ]

    # history
    for role,msg in chat_history:
        if role=="user":
            messages.append({"role":"user","content":msg})
        else:
            messages.append({"role":"assistant","content":msg})

    messages.append({"role":"user","content":user_input})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    return response.choices[0].message.content
