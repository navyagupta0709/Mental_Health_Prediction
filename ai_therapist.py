import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# -------- API KEY --------
groq_api_key = os.getenv("GROQ_API_KEY") or st.secrets["GROQ_API_KEY"]

# -------- LLM --------
llm = ChatGroq(
    api_key=groq_api_key,
    model="llama3-70b-8192"
)

# -------- PROMPT --------
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a professional AI mental health therapist.

Rules:
- Be empathetic and calm
- Ask follow-up questions
- Keep answers short (2-4 lines)
- Support the user emotionally
- If user is very distressed, suggest talking to someone trusted

Talk like a real human therapist.
"""
        ),
        ("placeholder", "{history}"),
        ("user", "{question}")
    ]
)

chain = prompt | llm

# -------- FUNCTION --------
def generate_reply(user_input, chat_history):

    history = []
    for role, msg in chat_history:
        if role == "user":
            history.append(("user", msg))
        else:
            history.append(("assistant", msg))

    response = chain.invoke({
        "history": history,
        "question": user_input
    })

    return response.content
