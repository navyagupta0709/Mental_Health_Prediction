import random

def generate_reply(user_input, chat_history):
    # combine history + current message
    history_text = " ".join([msg for role, msg in chat_history if role == "user"])
    msg = (history_text + " " + user_input).lower()

    # -------- THERAPIST LOGIC --------
    if "sad" in msg or "depressed" in msg:
        return "I'm really sorry you're feeling this way 💙. Can you tell me what’s been bothering you lately?"

    elif "stress" in msg or "anxiety" in msg:
        return "That sounds overwhelming. What do you think is causing this stress right now?"

    elif "alone" in msg or "lonely" in msg:
        return "Feeling lonely can be really tough 🤝. Do you feel like you have someone you can talk to?"

    elif "tired" in msg:
        return "It sounds like you're exhausted. Have you been getting enough rest lately?"

    elif "fail" in msg or "exam" in msg:
        return "Setbacks can feel really heavy. But one result doesn’t define you. What part is worrying you the most?"

    elif "angry" in msg:
        return "It's okay to feel angry sometimes. What happened that made you feel this way?"

    elif "happy" in msg:
        return "That's really nice to hear 😊. What made you feel this way?"

    elif "suicide" in msg or "kill myself" in msg:
        return "I'm really sorry you're feeling this way 💔. You're not alone. Please reach out to someone you trust or a helpline immediately."

    # -------- DEFAULT FOLLOW-UP --------
    followups = [
        "I understand. Can you tell me more about what's going on?",
        "How long have you been feeling this way?",
        "What do you think might be causing this?",
        "How does this affect your daily life?"
    ]

    return random.choice(followups)
