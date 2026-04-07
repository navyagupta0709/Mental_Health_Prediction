import random

def generate_reply(user_input, chat_history):

    msg = user_input.lower()   # ✅ only latest message

    if "sad" in msg or "depressed" in msg:
        return "I'm really sorry you're feeling this way 💙. What exactly made you feel sad today?"

    elif "stress" in msg or "anxiety" in msg or "nervous" in msg:
        return "It sounds like you're feeling nervous or stressed. Was it because of something specific like your presentation?"

    elif "presentation" in msg:
        return "Presentations can be really stressful 😔. What part made you most nervous — speaking, preparation, or audience?"

    elif "alone" in msg or "lonely" in msg:
        return "Feeling lonely can be really tough 🤝. Do you feel like you have someone you can talk to?"

    elif "tired" in msg:
        return "It sounds like you're exhausted. Have you been getting enough rest lately?"

    elif "fail" in msg or "exam" in msg:
        return "It's okay to feel upset after setbacks. One result doesn't define you. What part is worrying you the most?"

    elif "happy" in msg:
        return "That's really nice to hear 😊. What made you feel this way?"

    elif "suicide" in msg or "kill myself" in msg:
        return "I'm really sorry you're feeling this way 💔. You're not alone. Please reach out to someone you trust or a helpline immediately."

    # fallback (important)
    followups = [
        "I understand. Can you explain a bit more?",
        "How did that situation make you feel?",
        "What do you think is bothering you the most?",
        "I'm here for you. Tell me more about it."
    ]

    return random.choice(followups)
