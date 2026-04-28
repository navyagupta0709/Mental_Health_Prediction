import streamlit as st
from groq import Groq

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MindSpace · AI Therapist",
    page_icon="🧘",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Root palette ── */
:root {
    --bg:        #0f1117;
    --surface:   #181c27;
    --border:    #2a2f3e;
    --accent:    #7c9fdb;
    --accent2:   #b08fd4;
    --text:      #e8ecf4;
    --muted:     #8891a8;
    --user-bg:   #1e2640;
    --bot-bg:    #1a2235;
    --radius:    14px;
}

/* ── Global resets ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 1.5rem 5rem !important; max-width: 780px !important; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
}
.hero h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 2.6rem;
    letter-spacing: -0.5px;
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.4rem;
}
.hero p {
    color: var(--muted);
    font-size: 0.95rem;
    font-weight: 300;
    margin: 0;
}

/* ── Divider ── */
.divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.2rem 0;
}

/* ── Chat messages ── */
.chat-wrap {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-bottom: 1rem;
}
.msg {
    display: flex;
    gap: 0.75rem;
    align-items: flex-start;
    animation: fadeUp 0.3s ease both;
}
.msg.user { flex-direction: row-reverse; }

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}

.avatar {
    width: 36px; height: 36px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    flex-shrink: 0;
    background: var(--border);
}
.msg.user  .avatar { background: linear-gradient(135deg, #3a5090, #6a4a9a); }
.msg.bot   .avatar { background: linear-gradient(135deg, #1e3a6e, #2e4a8e); }

.bubble {
    max-width: 82%;
    padding: 0.75rem 1rem;
    border-radius: var(--radius);
    font-size: 0.93rem;
    line-height: 1.65;
    border: 1px solid var(--border);
}
.msg.user .bubble {
    background: var(--user-bg);
    border-radius: var(--radius) 4px var(--radius) var(--radius);
    color: var(--text);
}
.msg.bot .bubble {
    background: var(--bot-bg);
    border-radius: 4px var(--radius) var(--radius) var(--radius);
    color: var(--text);
}

/* ── Sidebar styling ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* ── Input area ── */
[data-testid="stTextInput"] input {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: var(--radius) !important;
    padding: 0.6rem 1rem !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(124,159,219,0.18) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius) !important;
    font-weight: 500 !important;
    padding: 0.45rem 1.2rem !important;
    transition: opacity 0.2s;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* ── Select / text area ── */
[data-testid="stSelectbox"] > div,
[data-testid="stTextArea"] textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: var(--radius) !important;
}

/* ── Mood chip row ── */
.mood-row {
    display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 0.8rem;
}
.mood-chip {
    padding: 0.3rem 0.75rem;
    border-radius: 999px;
    background: var(--surface);
    border: 1px solid var(--border);
    font-size: 0.82rem;
    color: var(--muted);
}

/* ── Disclaimer banner ── */
.disclaimer {
    background: rgba(124,159,219,0.08);
    border: 1px solid rgba(124,159,219,0.2);
    border-radius: var(--radius);
    padding: 0.65rem 1rem;
    font-size: 0.8rem;
    color: var(--muted);
    margin-bottom: 1rem;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ── System prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are MindSpace, a compassionate and professional AI therapist assistant. Your role is to:

- Provide a safe, non-judgmental, and empathetic space for people to express their thoughts and feelings
- Use evidence-based therapeutic techniques such as Cognitive Behavioral Therapy (CBT), mindfulness, and active listening
- Ask thoughtful, open-ended questions to help users explore their feelings more deeply
- Offer coping strategies, grounding techniques, and gentle reframes when appropriate
- Recognize your limits — if someone expresses serious risk of self-harm or harm to others, always encourage them to contact emergency services or a licensed professional immediately
- Never diagnose, prescribe medication, or replace professional mental health care
- Keep responses warm, conversational, and appropriately concise (2–4 paragraphs unless more depth is needed)
- Begin each session by acknowledging what the person has shared and validating their experience

Remember: You are a supportive guide, not a replacement for professional therapy."""

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    groq_api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Get your key at console.groq.com",
    )

    st.markdown("---")
    st.markdown("### 🧠 Session")

    therapy_mode = st.selectbox(
        "Therapy style",
        ["Supportive Listening", "CBT-focused", "Mindfulness-based", "Solution-focused"],
    )

    language = st.selectbox("Language", ["English", "Hindi", "Spanish", "French", "German"])

    st.markdown("---")
    if st.button("🗑️ Clear conversation"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.78rem;color:#8891a8;'>"
        "MindSpace uses <b>Groq + LLaMA-3</b> for fast, private responses.<br><br>"
        "🔒 Your conversations are not stored beyond this session."
        "</div>",
        unsafe_allow_html=True,
    )

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>🧘 MindSpace</h1>
  <p>Your private AI therapist · Available 24 / 7 · Powered by Groq</p>
</div>
<hr class="divider">
""", unsafe_allow_html=True)

# ── Disclaimer ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="disclaimer">
  ⚠️ <b>Not a substitute for professional help.</b> If you're in crisis, please contact a licensed therapist
  or call a helpline (e.g. iCall India: <b>9152987821</b> · International: <b>findahelpline.com</b>).
</div>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Render chat history ───────────────────────────────────────────────────────
if st.session_state.messages:
    st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="msg user">
              <div class="avatar">🙂</div>
              <div class="bubble">{msg["content"]}</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="msg bot">
              <div class="avatar">🧘</div>
              <div class="bubble">{msg["content"]}</div>
            </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align:center;padding:2rem 0;color:#8891a8;">
      <div style="font-size:2.5rem;margin-bottom:0.75rem;">💬</div>
      <div style="font-size:0.95rem;">Start by sharing what's on your mind today…</div>
    </div>
    """, unsafe_allow_html=True)

# ── Input form ────────────────────────────────────────────────────────────────
col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input(
        label="Message",
        placeholder="How are you feeling today?",
        label_visibility="collapsed",
        key="user_input_field",
    )
with col2:
    send = st.button("Send", use_container_width=True)

# ── Quick mood starters ───────────────────────────────────────────────────────
st.markdown("""
<div class="mood-row">
  <span class="mood-chip">😔 Feeling low</span>
  <span class="mood-chip">😰 Anxious</span>
  <span class="mood-chip">😤 Stressed</span>
  <span class="mood-chip">😶 Numb</span>
  <span class="mood-chip">🌱 Want to grow</span>
</div>
""", unsafe_allow_html=True)

# ── Handle submission ─────────────────────────────────────────────────────────
if send and user_input.strip():
    if not groq_api_key:
        st.error("⚠️ Please enter your Groq API key in the sidebar to continue.")
        st.stop()

    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})

    # Build system prompt with selected style & language
    system = SYSTEM_PROMPT
    system += f"\n\nTherapy style for this session: {therapy_mode}."
    if language != "English":
        system += f" Please respond in {language}."

    # Call Groq
    try:
        client = Groq(api_key=groq_api_key)
        with st.spinner("MindSpace is thinking…"):
            response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "system", "content": system}] + st.session_state.messages,
                temperature=0.75,
                max_tokens=1024,
            )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

    except Exception as e:
        st.error(f"❌ Groq API error: {e}")
