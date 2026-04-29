import streamlit as st
import os
from groq import Groq
from datetime import datetime

# ─── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mental Health AI Chatbot",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --sage:       #7BA05B;
    --sage-light: #A8C48A;
    --sage-dark:  #4E6B35;
    --cream:      #FAF7F2;
    --charcoal:   #2C3E35;
    --muted:      #5a6e62;
    --danger:     #D4574A;
    --warning:    #E8A04A;
    --success:    #5B9B7A;
    --card-bg:    #ffffff;
    --shadow:     0 4px 24px rgba(44,62,53,0.09);
    --radius:     14px;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--cream);
    color: var(--charcoal);
}
.stApp { background: var(--cream); }
#MainMenu, footer, header { visibility: hidden; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #2C3E35 0%, #1a2a22 100%);
    border-right: 1px solid rgba(123,160,91,0.18);
}
[data-testid="stSidebar"] * { color: #ddeedd !important; }
[data-testid="stSidebar"] hr { border-color: rgba(123,160,91,0.18) !important; }
[data-testid="stSidebar"] .stRadio label { color: #b8d4be !important; font-size: 0.93rem; }

.sidebar-brand {
    text-align: center;
    padding: 1.6rem 0.5rem 1.2rem;
    border-bottom: 1px solid rgba(123,160,91,0.22);
    margin-bottom: 1.4rem;
}
.sidebar-brand h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 1.15rem;
    color: #A8C48A !important;
    margin: 0;
    line-height: 1.3;
    letter-spacing: 0.01em;
}
.sidebar-brand .icon { font-size: 2rem; display: block; margin-bottom: 0.5rem; }

/* ── Page Header ── */
.page-header {
    background: linear-gradient(135deg, #2C3E35 0%, #3a5a45 100%);
    border-radius: var(--radius);
    padding: 1.8rem 2.2rem;
    margin-bottom: 1.8rem;
    position: relative;
    overflow: hidden;
}
.page-header::after {
    content: '';
    position: absolute;
    top: -50px; right: -50px;
    width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(123,160,91,0.2) 0%, transparent 70%);
    border-radius: 50%;
}
.page-header h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 1.9rem;
    color: #ffffff;
    margin: 0 0 0.3rem;
}
.page-header p { color: #b8d4be; margin: 0; font-size: 0.9rem; }

/* ── Cards ── */
.card {
    background: var(--card-bg);
    border-radius: var(--radius);
    padding: 1.4rem 1.6rem;
    box-shadow: var(--shadow);
    border: 1px solid rgba(123,160,91,0.13);
    margin-bottom: 1rem;
    color: var(--charcoal);
}
.card * { color: var(--charcoal) !important; }

/* ── Chat ── */
.chat-scroll { max-height: 460px; overflow-y: auto; padding: 0.4rem 0; }

.msg-user { display:flex; justify-content:flex-end; margin-bottom:0.9rem; }
.msg-user .bubble {
    background: linear-gradient(135deg, #4E6B35, #7BA05B);
    color: #fff !important;
    border-radius: 18px 18px 4px 18px;
    padding: 0.7rem 1rem;
    max-width: 68%;
    font-size: 0.92rem;
    line-height: 1.55;
    box-shadow: 0 2px 10px rgba(78,107,53,0.22);
}
.msg-ai { display:flex; align-items:flex-start; gap:0.55rem; margin-bottom:0.9rem; }
.msg-ai .avatar {
    width:32px; height:32px;
    background: linear-gradient(135deg, #A8C48A, #7BA05B);
    border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    font-size:0.95rem; flex-shrink:0;
    box-shadow: 0 2px 6px rgba(123,160,91,0.25);
}
.msg-ai .bubble {
    background: white;
    color: #2C3E35 !important;
    border-radius: 4px 18px 18px 18px;
    padding: 0.7rem 1rem;
    max-width: 72%;
    font-size: 0.92rem;
    line-height: 1.6;
    box-shadow: var(--shadow);
    border: 1px solid rgba(123,160,91,0.1);
}
.msg-ai .bubble * { color: #2C3E35 !important; }
.msg-ts { font-size:0.7rem; color:#7A8B80; margin-top:3px; text-align:right; }

/* ── Assessment question rows ── */
.q-row {
    background: white;
    border-radius: 10px;
    padding: 1rem 1.2rem 0.6rem;
    margin-bottom: 0.75rem;
    border: 1px solid rgba(123,160,91,0.15);
    box-shadow: 0 2px 8px rgba(44,62,53,0.05);
}
.q-label {
    font-size: 0.92rem;
    font-weight: 500;
    color: #2C3E35;
    margin-bottom: 0.55rem;
    line-height: 1.45;
}

/* ── Selectbox inside assessment cards ── */
.q-row .stSelectbox > div > div {
    background: #f5f9f3 !important;
    border: 1.5px solid rgba(123,160,91,0.35) !important;
    border-radius: 8px !important;
    color: #2C3E35 !important;
}
.q-row .stSelectbox label { display: none !important; }

/* ── Risk Badges ── */
.risk-badge { display:inline-block; padding:0.3rem 0.9rem; border-radius:50px; font-size:0.78rem; font-weight:600; letter-spacing:0.05em; text-transform:uppercase; }
.risk-low    { background:#e8f5ee; color:#2d7a52; border:1px solid #a8d5bc; }
.risk-medium { background:#fff4e0; color:#9b6a1a; border:1px solid #f0c97a; }
.risk-high   { background:#fde8e6; color:#9b2a22; border:1px solid #f0a09a; }

/* ── Score bars ── */
.score-bar  { background:#e8efe8; border-radius:50px; height:9px; overflow:hidden; margin-top:5px; }
.score-fill { height:100%; border-radius:50px; }

/* ── Metric grid ── */
.metric-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(140px,1fr)); gap:0.9rem; margin-bottom:1.4rem; }
.metric-card { background:white; border-radius:var(--radius); padding:1.1rem 0.9rem; box-shadow:var(--shadow); border-left:4px solid var(--sage); text-align:center; }
.metric-card .lbl { font-size:0.76rem; color:#5a6e62; text-transform:uppercase; letter-spacing:0.08em; }
.metric-card .val { font-family:'DM Serif Display',serif; font-size:1.9rem; color:#2C3E35; }

/* ── Crisis banner ── */
.crisis-banner { background:linear-gradient(135deg,#7a1a14,#c0392b); border-radius:var(--radius); padding:1rem 1.4rem; color:white; margin-bottom:1rem; border-left:5px solid #ff6b5a; }
.crisis-banner h3 { margin:0 0 0.3rem; font-size:0.95rem; color:white !important; }
.crisis-banner p  { margin:0; font-size:0.85rem; opacity:0.92; color:white !important; }

/* ── Section title ── */
.section-title { font-family:'DM Serif Display',serif; font-size:1.25rem; color:#2C3E35; margin-bottom:0.75rem; padding-bottom:0.45rem; border-bottom:2px solid rgba(123,160,91,0.2); }

/* ── Disclaimer ── */
.disclaimer { background:rgba(123,160,91,0.07); border:1px solid rgba(123,160,91,0.2); border-radius:10px; padding:0.75rem 1rem; font-size:0.81rem; color:#5a6e62; line-height:1.55; }

/* ── Quick Tools fix: dark text ── */
div[data-testid="stExpander"] {
    background: white !important;
    border: 1px solid rgba(123,160,91,0.18) !important;
    border-radius: 10px !important;
    margin-bottom: 0.5rem;
}
div[data-testid="stExpander"] p,
div[data-testid="stExpander"] li,
div[data-testid="stExpander"] span,
div[data-testid="stExpander"] strong,
div[data-testid="stExpander"] em,
div[data-testid="stExpander"] label {
    color: #2C3E35 !important;
}
div[data-testid="stExpander"] summary {
    color: #2C3E35 !important;
    font-weight: 500;
}
div[data-testid="stExpander"] svg { color: #7BA05B !important; }

/* ── Streamlit widget overrides ── */
.stButton > button {
    background: linear-gradient(135deg, #4E6B35, #7BA05B) !important;
    color: white !important;
    border: none !important;
    border-radius: 9px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    padding: 0.45rem 1.2rem !important;
    transition: all 0.15s !important;
}
.stButton > button:hover { transform:translateY(-1px) !important; box-shadow:0 4px 14px rgba(78,107,53,0.28) !important; }

.stTextArea > div > div > textarea,
.stTextInput > div > div > input {
    background: white !important;
    border: 1.5px solid rgba(123,160,91,0.3) !important;
    border-radius: 9px !important;
    color: #2C3E35 !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextArea > div > div > textarea:focus,
.stTextInput > div > div > input:focus {
    border-color: #7BA05B !important;
    box-shadow: 0 0 0 3px rgba(123,160,91,0.12) !important;
}

.stSelectbox > div > div {
    background: white !important;
    border: 1.5px solid rgba(123,160,91,0.28) !important;
    border-radius: 9px !important;
    color: #2C3E35 !important;
}
.stSelectbox > div > div > div { color: #2C3E35 !important; }

.stSlider > div > div > div > div { background: #7BA05B !important; }

/* section spacing */
.section-gap { margin-top: 1.6rem; margin-bottom: 0.3rem; }
</style>
""", unsafe_allow_html=True)


# ─── Helpers ──────────────────────────────────────────────────────────────────
def get_client():
    key = st.session_state.get("groq_api_key", "") or os.environ.get("GROQ_API_KEY", "")
    return Groq(api_key=key) if key else None

def extract_score(val):
    try: return int(val.split("(")[1].split(")")[0])
    except: return 0

def init():
    for k, v in {
        "messages": [], "groq_api_key": "",
        "assessment_done": False, "assessment_scores": {},
        "risk_level": None, "session_start": datetime.now().strftime("%Y-%m-%d %H:%M")
    }.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <span class="icon">🧠</span>
        <h1>Mental Health<br>AI Chatbot</h1>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio("Navigation", [
        "💬 AI Therapist Chat",
        "📋 Mental Health Assessment",
        "📊 My Wellness Report"
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("**⚙️ Configuration**")
    key_in = st.text_input(
        "Groq API Key", type="password",
        value=st.session_state.groq_api_key,
        placeholder="gsk_...",
        help="Get your free key at console.groq.com"
    )
    if key_in:
        st.session_state.groq_api_key = key_in

    st.markdown("---")
    if st.button("🗑 Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — AI THERAPIST CHAT
# ═══════════════════════════════════════════════════════════════════════════════
if "💬 AI Therapist Chat" in page:
    st.markdown("""
    <div class="page-header">
        <h1>💬 AI Therapist Chat</h1>
        <p>A safe, confidential space to share your thoughts and feelings</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.risk_level == "High":
        st.markdown("""
        <div class="crisis-banner">
            <h3>⚠️ We're Here for You</h3>
            <p>Your assessment indicates you may need immediate support. Please reach out to a mental health professional. You are not alone.</p>
        </div>
        """, unsafe_allow_html=True)

    col_chat, col_tools = st.columns([3, 1])

    with col_chat:
        # Build chat HTML
        html = '<div class="chat-scroll">'
        if not st.session_state.messages:
            html += """
            <div class="msg-ai">
                <div class="avatar">🧠</div>
                <div>
                    <div class="bubble">
                        Hello! I'm your Mental Health AI companion. 💚<br><br>
                        I'm here to listen without judgment. Feel free to share anything on your mind — stress, anxiety, relationships, or simply how your day went.<br><br>
                        <em>How are you feeling today?</em>
                    </div>
                </div>
            </div>"""
        for msg in st.session_state.messages:
            ts = msg.get("timestamp", "")
            if msg["role"] == "user":
                html += f'<div class="msg-user"><div><div class="bubble">{msg["content"]}</div><div class="msg-ts">{ts}</div></div></div>'
            else:
                html += f'<div class="msg-ai"><div class="avatar">🧠</div><div><div class="bubble">{msg["content"]}</div><div class="msg-ts">{ts}</div></div></div>'
        html += '</div>'

        st.markdown(f'<div class="card">{html}</div>', unsafe_allow_html=True)

        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_area(
                "", placeholder="Share what's on your mind...",
                height=90, label_visibility="collapsed"
            )
            c1, c2 = st.columns([5, 1])
            with c2:
                send = st.form_submit_button("Send 💬", use_container_width=True)

        if send and user_input.strip():
            client = get_client()
            if not client:
                st.error("⚠️ Please enter your Groq API key in the sidebar to start chatting.")
            else:
                ts = datetime.now().strftime("%H:%M")
                st.session_state.messages.append({
                    "role": "user", "content": user_input.strip(), "timestamp": ts
                })

                SYSTEM = """You are a compassionate and empathetic AI mental health companion trained in:
- Cognitive Behavioral Therapy (CBT) techniques
- Mindfulness-Based Stress Reduction (MBSR)
- Supportive counseling and active listening
- Crisis intervention awareness

Your guidelines:
1. Always validate emotions first before offering advice
2. Ask thoughtful follow-up questions to understand the user's situation
3. Offer evidence-based coping strategies gently and appropriately
4. Never diagnose or prescribe — you are a supportive companion, not a clinician
5. If you detect signs of self-harm or suicidal ideation — immediately suggest professional help
6. Keep responses warm, calm, and hopeful (2–4 short paragraphs max)
7. Occasionally remind users to seek professional mental health support"""

                api_msgs = [{"role": "system", "content": SYSTEM}]
                for m in st.session_state.messages[-14:]:
                    api_msgs.append({"role": m["role"], "content": m["content"]})

                with st.spinner("Thinking..."):
                    try:
                        resp = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=api_msgs,
                            max_tokens=600, temperature=0.75
                        )
                        reply = resp.choices[0].message.content
                        st.session_state.messages.append({
                            "role": "assistant", "content": reply,
                            "timestamp": datetime.now().strftime("%H:%M")
                        })
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")

    # ── Quick Tools ──
    with col_tools:
        st.markdown('<div class="section-title">🛠 Quick Tools</div>', unsafe_allow_html=True)

        with st.expander("🌬 Breathing Exercise"):
            st.markdown(
                "**4-7-8 Technique**\n\n"
                "1. **Inhale** — 4 seconds\n"
                "2. **Hold** — 7 seconds\n"
                "3. **Exhale** — 8 seconds\n\n"
                "Repeat 3–4 cycles to calm down."
            )

        with st.expander("⚓ Grounding 5-4-3-2-1"):
            st.markdown(
                "Notice around you:\n\n"
                "- **5** things you can **see**\n"
                "- **4** things you can **touch**\n"
                "- **3** things you can **hear**\n"
                "- **2** things you can **smell**\n"
                "- **1** thing you can **taste**"
            )

        with st.expander("✍ Journal Prompts"):
            st.markdown(
                "- *What am I feeling right now, and why?*\n"
                "- *What am I grateful for today?*\n"
                "- *What would I tell a friend in my situation?*\n"
                "- *What do I need most right now?*"
            )

        with st.expander("💊 Self-Care Check"):
            st.checkbox("💧 Drank enough water")
            st.checkbox("🍎 Ate a proper meal")
            st.checkbox("🚶 Moved my body today")
            st.checkbox("😴 Got enough sleep")
            st.checkbox("🤝 Connected with someone")

        st.markdown('<div class="disclaimer" style="margin-top:0.8rem;">⚕️ Not a substitute for professional care.</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — ASSESSMENT
# ═══════════════════════════════════════════════════════════════════════════════
elif "📋 Mental Health Assessment" in page:
    st.markdown("""
    <div class="page-header">
        <h1>📋 Mental Health Assessment</h1>
        <p>Clinically-informed screening · PHQ-9 · GAD-7 · PSS · ISI · ~5 minutes</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="disclaimer">
    📌 This screening uses validated clinical tools for <strong>personal awareness only</strong> — it is not a clinical diagnosis.
    Please consult a mental health professional for a full evaluation.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

    opts4      = ["Not at all (0)", "Several days (1)", "More than half the days (2)", "Nearly every day (3)"]
    opts5      = ["Never (0)", "Almost never (1)", "Sometimes (2)", "Fairly often (3)", "Very often (4)"]
    opts_sleep = ["None (0)", "Mild (1)", "Moderate (2)", "Severe (3)", "Very Severe (4)"]
    opts_sat   = ["Very satisfied (0)", "Satisfied (1)", "Neutral (2)", "Dissatisfied (3)", "Very dissatisfied (4)"]

    def q(label, options, key):
        """Render a question label + selectbox inside a styled card row."""
        st.markdown(f'<div class="q-row"><div class="q-label">{label}</div>', unsafe_allow_html=True)
        val = st.selectbox("_", options, key=key, label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        return val

    with st.form("assessment_form"):

        # ── Section 1: Depression ──
        st.markdown('<div class="section-title section-gap">😔 Section 1 — Depression (PHQ-9)</div>', unsafe_allow_html=True)
        st.caption("Over the **past 2 weeks**, how often have you been bothered by the following?")
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

        d1 = q("1. Little interest or pleasure in doing things", opts4, "d1")
        d2 = q("2. Feeling down, depressed, or hopeless", opts4, "d2")
        d3 = q("3. Trouble falling / staying asleep, or sleeping too much", opts4, "d3")
        d4 = q("4. Feeling tired or having little energy", opts4, "d4")
        d5 = q("5. Poor appetite or overeating", opts4, "d5")
        d6 = q("6. Feeling bad about yourself, or that you are a failure", opts4, "d6")
        d7 = q("7. Trouble concentrating on things (reading, TV, etc.)", opts4, "d7")
        d8 = q("8. Moving / speaking slowly noticed by others — or being restless / fidgety", opts4, "d8")
        d9 = q("9. Thoughts that you would be better off dead, or of hurting yourself", opts4, "d9")

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        # ── Section 2: Anxiety ──
        st.markdown('<div class="section-title section-gap">😰 Section 2 — Anxiety (GAD-7)</div>', unsafe_allow_html=True)
        st.caption("Over the **past 2 weeks**, how often have you been bothered by the following?")
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

        a1 = q("1. Feeling nervous, anxious, or on edge", opts4, "a1")
        a2 = q("2. Not being able to stop or control worrying", opts4, "a2")
        a3 = q("3. Worrying too much about different things", opts4, "a3")
        a4 = q("4. Trouble relaxing", opts4, "a4")
        a5 = q("5. Being so restless it is hard to sit still", opts4, "a5")
        a6 = q("6. Becoming easily annoyed or irritable", opts4, "a6")
        a7 = q("7. Feeling afraid as if something awful might happen", opts4, "a7")

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        # ── Section 3: Stress ──
        st.markdown('<div class="section-title section-gap">😤 Section 3 — Stress (PSS-4)</div>', unsafe_allow_html=True)
        st.caption("Over the **past month**, how often have you felt the following?")
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

        s1 = q("1. Unable to control the important things in your life", opts5, "s1")
        s2 = q("2. Confident about your ability to handle personal problems", opts5, "s2")
        s3 = q("3. Things were going your way", opts5, "s3")
        s4 = q("4. Difficulties were piling up so high that you could not overcome them", opts5, "s4")

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        # ── Section 4: Sleep ──
        st.markdown('<div class="section-title section-gap">😴 Section 4 — Sleep Quality (ISI)</div>', unsafe_allow_html=True)
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

        sl1 = q("1. Severity of difficulty falling asleep", opts_sleep, "sl1")
        sl2 = q("2. Severity of difficulty staying asleep through the night", opts_sleep, "sl2")
        sl3 = q("3. Problem of waking up too early in the morning", opts_sleep, "sl3")
        sl4 = q("4. How satisfied are you with your current sleep pattern?", opts_sat, "sl4")

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        # ── Section 5: Lifestyle ──
        st.markdown('<div class="section-title section-gap">🤝 Section 5 — Lifestyle & Social Factors</div>', unsafe_allow_html=True)
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

        social    = st.slider("How connected do you feel to friends / family?  (1 = Very isolated · 10 = Very connected)", 1, 10, 5)
        exercise  = st.selectbox("How often do you exercise or engage in physical activity?",
                                  ["Never", "Rarely (once/month)", "Sometimes (1-2x/week)", "Regularly (3-4x/week)", "Daily"])
        substance = st.selectbox("Do you use alcohol or substances to cope with stress or emotions?",
                                  ["Never", "Rarely", "Sometimes", "Often", "Almost daily"])
        support   = st.selectbox("Current mental health professional support status",
                                  ["Yes, actively in therapy", "Had therapy before", "Considering it", "No support at all"])

        st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🔍 Analyse My Mental Health", use_container_width=True)

    # ── Scoring ──
    if submitted:
        dep_score    = sum(extract_score(i) for i in [d1,d2,d3,d4,d5,d6,d7,d8,d9])
        anx_score    = sum(extract_score(i) for i in [a1,a2,a3,a4,a5,a6,a7])
        stress_score = extract_score(s1) + (4-extract_score(s2)) + (4-extract_score(s3)) + extract_score(s4)
        sleep_score  = sum(extract_score(i) for i in [sl1,sl2,sl3,sl4])

        ex_map  = {"Never":6,"Rarely (once/month)":4,"Sometimes (1-2x/week)":2,"Regularly (3-4x/week)":0,"Daily":0}
        sub_map = {"Never":0,"Rarely":2,"Sometimes":4,"Often":6,"Almost daily":8}
        sup_map = {"Yes, actively in therapy":-4,"Had therapy before":-2,"Considering it":0,"No support at all":3}
        lifestyle_penalty = ex_map[exercise] + sub_map[substance] + max(0,(5-social)*2) + sup_map[support]

        dep_pct = round(dep_score/27*100)
        anx_pct = round(anx_score/21*100)
        str_pct = round(stress_score/16*100)
        slp_pct = round(sleep_score/16*100)
        lif_pct = min(100, max(0, round(lifestyle_penalty/17*100)))
        overall = round(dep_pct*0.30 + anx_pct*0.25 + str_pct*0.20 + slp_pct*0.15 + lif_pct*0.10)

        crisis = extract_score(d9) >= 2
        if crisis or overall >= 65:
            risk = "High";     rbadge = "risk-high"
        elif overall >= 35:
            risk = "Moderate"; rbadge = "risk-medium"
        else:
            risk = "Low";      rbadge = "risk-low"

        st.session_state.assessment_scores = {
            "depression": dep_pct, "anxiety": anx_pct,
            "stress": str_pct, "sleep": slp_pct,
            "lifestyle": lif_pct, "overall": overall
        }
        st.session_state.risk_level      = risk
        st.session_state.assessment_done = True

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        if crisis:
            st.markdown("""
            <div class="crisis-banner">
                <h3>⚠️ Immediate Support Is Available</h3>
                <p>Your responses indicate thoughts of self-harm or suicide. Please reach out to a mental health professional or trusted person immediately.</p>
            </div>""", unsafe_allow_html=True)

        rcolor = "#D4574A" if risk=="High" else "#E8A04A" if risk=="Moderate" else "#5B9B7A"
        c1, c2 = st.columns([1, 2])

        with c1:
            st.markdown(f"""
            <div class="card" style="text-align:center;padding:2rem;">
                <div style="font-size:0.78rem;color:#5a6e62;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.3rem;">Overall Risk</div>
                <div style="font-family:'DM Serif Display',serif;font-size:3.2rem;color:#2C3E35;line-height:1.1;">
                    {overall}<span style="font-size:1.3rem;">%</span>
                </div>
                <div style="margin:0.6rem 0;">
                    <span class="risk-badge {rbadge}">{risk} Risk</span>
                </div>
                <div style="font-size:0.76rem;color:#7A8B80;margin-top:0.6rem;">PHQ-9 · GAD-7 · PSS · ISI</div>
            </div>""", unsafe_allow_html=True)

        with c2:
            for label, pct in [
                ("😔 Depression",   dep_pct),
                ("😰 Anxiety",      anx_pct),
                ("😤 Stress",       str_pct),
                ("😴 Sleep Issues", slp_pct),
                ("🤝 Lifestyle",    lif_pct),
            ]:
                fc = "#D4574A" if pct>=65 else "#E8A04A" if pct>=35 else "#5B9B7A"
                st.markdown(f"""
                <div style="background:white;border-radius:10px;padding:0.75rem 1rem;margin-bottom:0.55rem;border-left:4px solid {fc};box-shadow:0 2px 8px rgba(0,0,0,0.05);">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="font-weight:500;font-size:0.88rem;color:#2C3E35;">{label}</span>
                        <span style="font-size:0.88rem;font-weight:600;color:{fc};">{pct}%</span>
                    </div>
                    <div class="score-bar"><div class="score-fill" style="width:{pct}%;background:{fc};"></div></div>
                </div>""", unsafe_allow_html=True)

        # AI Recommendations
        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">🤖 Personalised AI Recommendations</div>', unsafe_allow_html=True)
        client = get_client()
        if client:
            prompt = f"""Mental health screening results:
- Depression (PHQ-9): {dep_pct}% ({dep_score}/27)
- Anxiety (GAD-7): {anx_pct}% ({anx_score}/21)
- Stress (PSS): {str_pct}%
- Sleep Issues (ISI): {slp_pct}%
- Lifestyle: {lif_pct}%
- Overall Risk: {overall}% — {risk} Risk
- Crisis flag: {"YES" if crisis else "No"}

Provide:
1. A 2-sentence compassionate validation of their experience
2. Three specific evidence-based coping strategies tailored to their highest-scoring areas
3. One concrete daily habit to begin this week
4. Clear guidance on whether and what type of professional help to seek

Tone: warm, hopeful, and actionable. Avoid clinical jargon."""

            with st.spinner("Generating personalised recommendations..."):
                try:
                    r = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role":"user","content":prompt}],
                        max_tokens=700, temperature=0.65
                    )
                    st.markdown(f'<div class="card">{r.choices[0].message.content}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.warning(f"Could not generate recommendations: {e}")
        else:
            st.info("💡 Add your Groq API key in the sidebar for personalised AI recommendations.")

        st.success("✅ Assessment complete! Navigate to **My Wellness Report** for your full dashboard.")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — WELLNESS REPORT
# ═══════════════════════════════════════════════════════════════════════════════
elif "📊 My Wellness Report" in page:
    st.markdown("""
    <div class="page-header">
        <h1>📊 My Wellness Report</h1>
        <p>Your holistic mental health snapshot and personalised action plan</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.assessment_done:
        st.info("📋 Please complete the Mental Health Assessment first to view your Wellness Report.")
        st.stop()

    sc   = st.session_state.assessment_scores
    risk = st.session_state.risk_level
    rcolor = {"Low":"#5B9B7A","Moderate":"#E8A04A","High":"#D4574A"}.get(risk,"#7A8B80")

    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card">
            <div class="lbl">Overall Risk</div>
            <div class="val" style="color:{rcolor};">{sc['overall']}%</div>
            <div style="font-size:0.78rem;color:{rcolor};font-weight:600;margin-top:3px;">{risk} Risk</div>
        </div>
        <div class="metric-card" style="border-color:#D4574A;">
            <div class="lbl">Depression</div>
            <div class="val">{sc['depression']}%</div>
        </div>
        <div class="metric-card" style="border-color:#E8A04A;">
            <div class="lbl">Anxiety</div>
            <div class="val">{sc['anxiety']}%</div>
        </div>
        <div class="metric-card" style="border-color:#C17B4E;">
            <div class="lbl">Stress</div>
            <div class="val">{sc['stress']}%</div>
        </div>
        <div class="metric-card" style="border-color:#5B9B7A;">
            <div class="lbl">Sleep Issues</div>
            <div class="val">{sc['sleep']}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-title">📈 Dimension Analysis</div>', unsafe_allow_html=True)
        for dim, val in [
            ("😔 Depression", sc['depression']),
            ("😰 Anxiety",    sc['anxiety']),
            ("😤 Stress",     sc['stress']),
            ("😴 Sleep",      sc['sleep']),
            ("🤝 Lifestyle",  sc['lifestyle']),
        ]:
            fc  = "#D4574A" if val>=65 else "#E8A04A" if val>=35 else "#5B9B7A"
            lbl = "⚠ High" if val>=65 else "⚡ Moderate" if val>=35 else "✔ Low"
            st.markdown(f"""
            <div style="margin-bottom:0.9rem;">
                <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                    <span style="font-weight:500;font-size:0.88rem;color:#2C3E35;">{dim}</span>
                    <span style="font-size:0.84rem;color:{fc};">{lbl} — {val}%</span>
                </div>
                <div class="score-bar">
                    <div class="score-fill" style="width:{val}%;background:linear-gradient(90deg,{fc}99,{fc});"></div>
                </div>
            </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-title">🎯 Priority Action Plan</div>', unsafe_allow_html=True)
        actions = []
        if sc['depression']>=50: actions.append(("🧠 Seek CBT Therapy","Depression indicators elevated. CBT is the gold-standard treatment.","#D4574A"))
        if sc['anxiety']>=50:    actions.append(("🌬 Daily Mindfulness","Practice 4-7-8 breathing + 10-min meditation each morning.","#E8A04A"))
        if sc['stress']>=50:     actions.append(("📅 Stress Management","Break tasks into steps, schedule breaks, practice time-blocking.","#C17B4E"))
        if sc['sleep']>=50:      actions.append(("🌙 Improve Sleep Hygiene","Fixed sleep schedule, no screens 1hr before bed, keep room cool and dark.","#7BA05B"))
        if sc['lifestyle']>=40:  actions.append(("🏃 Daily 20-min Walk","Regular exercise significantly reduces depression and anxiety.","#5B9B7A"))
        if not actions:          actions.append(("✨ Maintain Your Wellness","Your scores are in a healthy range — keep up your self-care habits!","#5B9B7A"))

        for title, desc, c in actions:
            st.markdown(f"""
            <div style="background:white;border-radius:10px;padding:0.9rem 1rem;margin-bottom:0.7rem;border-left:4px solid {c};box-shadow:0 2px 8px rgba(0,0,0,0.05);">
                <div style="font-weight:600;font-size:0.9rem;color:#2C3E35;">{title}</div>
                <div style="font-size:0.82rem;color:#5a6e62;margin-top:4px;">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">📚 Recommended Resources</div>', unsafe_allow_html=True)
    rc1, rc2, rc3 = st.columns(3)
    for col, title, items in [
        (rc1, "📱 Apps", ["Wysa — AI mental health","Headspace — Meditation","Calm — Sleep & anxiety","Sanvello — CBT-based"]),
        (rc2, "📖 Books", ["Feeling Good — David Burns","The Anxiety Workbook","Why Has Nobody Told Me This?","Lost Connections — Johann Hari"]),
        (rc3, "🏥 Professional Help", ["Psychiatrist (medication)","Clinical Psychologist (CBT)","Licensed Counsellor (talking)","Group Therapy (peer support)"]),
    ]:
        with col:
            items_html = "".join(f'<div style="font-size:0.85rem;color:#2C3E35;padding:0.25rem 0;border-bottom:1px solid rgba(123,160,91,0.1);">• {i}</div>' for i in items)
            st.markdown(f'<div class="card"><div style="font-weight:600;color:#2C3E35;margin-bottom:0.6rem;">{title}</div>{items_html}</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="disclaimer" style="margin-top:1rem;">
    📌 <strong>Disclaimer:</strong> This wellness report is generated from self-reported data using validated screening instruments for personal awareness only.
    It does not constitute a clinical diagnosis. Please share these results with a qualified mental health professional for proper evaluation.<br>
    <span style="font-size:0.78rem;">Session: {st.session_state.session_start} · Risk Level: <strong>{risk}</strong></span>
    </div>""", unsafe_allow_html=True)
