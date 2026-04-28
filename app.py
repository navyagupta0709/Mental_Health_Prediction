import streamlit as st
import os
from groq import Groq
from datetime import datetime

# ─── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Mental Health Companion",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --sage:        #7BA05B;
    --sage-light:  #A8C48A;
    --sage-dark:   #4E6B35;
    --cream:       #FAF7F2;
    --charcoal:    #2C3E35;
    --muted:       #7A8B80;
    --accent:      #C17B4E;
    --danger:      #D4574A;
    --warning:     #E8A04A;
    --success:     #5B9B7A;
    --card-bg:     rgba(255,255,255,0.92);
    --shadow:      0 4px 24px rgba(44,62,53,0.10);
    --radius:      16px;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--cream);
    color: var(--charcoal);
}
.stApp { background: var(--cream); }
#MainMenu, footer, header { visibility: hidden; }

[data-testid="stSidebar"] {
    background: linear-gradient(160deg, var(--charcoal) 0%, #1a2a22 100%);
    border-right: 1px solid rgba(123,160,91,0.2);
}
[data-testid="stSidebar"] * { color: #e8f0ea !important; }
[data-testid="stSidebar"] hr { border-color: rgba(123,160,91,0.2); }

.sidebar-brand {
    text-align: center;
    padding: 1.5rem 0 1rem;
    border-bottom: 1px solid rgba(123,160,91,0.25);
    margin-bottom: 1.5rem;
}
.sidebar-brand h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 1.8rem;
    color: #A8C48A !important;
    margin: 0;
}
.sidebar-brand p {
    font-size: 0.78rem;
    color: #7A8B80 !important;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 4px;
}

.page-header {
    background: linear-gradient(135deg, var(--charcoal) 0%, #3a5a45 100%);
    border-radius: var(--radius);
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.page-header::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 160px; height: 160px;
    background: radial-gradient(circle, rgba(123,160,91,0.25) 0%, transparent 70%);
    border-radius: 50%;
}
.page-header h1 { font-family: 'DM Serif Display', serif; font-size: 2.2rem; color: #fff; margin: 0 0 0.4rem; }
.page-header p  { color: #b8cfc0; margin: 0; font-size: 0.95rem; }

.card {
    background: var(--card-bg);
    border-radius: var(--radius);
    padding: 1.5rem;
    box-shadow: var(--shadow);
    border: 1px solid rgba(123,160,91,0.12);
    margin-bottom: 1rem;
}

.chat-scroll { max-height: 480px; overflow-y: auto; padding: 0.5rem 0; }

.msg-user { display:flex; justify-content:flex-end; margin-bottom:1rem; }
.msg-user .bubble {
    background: linear-gradient(135deg, #4E6B35, #7BA05B);
    color: #fff;
    border-radius: 18px 18px 4px 18px;
    padding: 0.75rem 1.1rem;
    max-width: 70%;
    font-size: 0.93rem;
    line-height: 1.55;
    box-shadow: 0 2px 12px rgba(78,107,53,0.25);
}
.msg-ai { display:flex; align-items:flex-start; gap:0.6rem; margin-bottom:1rem; }
.msg-ai .avatar {
    width:34px; height:34px;
    background: linear-gradient(135deg, #A8C48A, #7BA05B);
    border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    font-size:1rem; flex-shrink:0;
}
.msg-ai .bubble {
    background: white; color: var(--charcoal);
    border-radius: 4px 18px 18px 18px;
    padding: 0.75rem 1.1rem;
    max-width: 72%;
    font-size: 0.93rem; line-height: 1.6;
    box-shadow: var(--shadow);
    border: 1px solid rgba(123,160,91,0.1);
}
.msg-ts { font-size:0.72rem; color:var(--muted); margin-top:3px; text-align:right; }

.risk-badge { display:inline-block; padding:0.35rem 1rem; border-radius:50px; font-size:0.8rem; font-weight:600; letter-spacing:0.05em; text-transform:uppercase; }
.risk-low    { background:#e8f5ee; color:#2d7a52; border:1px solid #a8d5bc; }
.risk-medium { background:#fff4e0; color:#9b6a1a; border:1px solid #f0c97a; }
.risk-high   { background:#fde8e6; color:#9b2a22; border:1px solid #f0a09a; }

.score-bar  { background:#e8efe8; border-radius:50px; height:10px; overflow:hidden; margin-top:6px; }
.score-fill { height:100%; border-radius:50px; }

.metric-grid { display:grid; grid-template-columns:repeat(auto-fit, minmax(150px, 1fr)); gap:1rem; margin-bottom:1.5rem; }
.metric-card { background:white; border-radius:var(--radius); padding:1.2rem 1rem; box-shadow:var(--shadow); border-left:4px solid var(--sage); text-align:center; }
.metric-card .label { font-size:0.78rem; color:var(--muted); text-transform:uppercase; letter-spacing:0.08em; }
.metric-card .value { font-family:'DM Serif Display',serif; font-size:2rem; color:var(--charcoal); }

.crisis-banner { background:linear-gradient(135deg,#7a1a14,#c0392b); border-radius:var(--radius); padding:1rem 1.5rem; color:white; margin-bottom:1rem; border-left:5px solid #ff6b5a; }
.crisis-banner h3 { margin:0 0 0.4rem; font-size:1rem; }
.crisis-banner p  { margin:0; font-size:0.87rem; opacity:0.9; }

.section-title { font-family:'DM Serif Display',serif; font-size:1.35rem; color:var(--charcoal); margin-bottom:0.8rem; padding-bottom:0.5rem; border-bottom:2px solid rgba(123,160,91,0.2); }

.disclaimer { background:rgba(123,160,91,0.08); border:1px solid rgba(123,160,91,0.2); border-radius:10px; padding:0.8rem 1rem; font-size:0.82rem; color:var(--muted); line-height:1.5; }

.stButton > button {
    background: linear-gradient(135deg, #4E6B35, #7BA05B) !important;
    color: white !important; border:none !important;
    border-radius:10px !important;
    font-family:'DM Sans',sans-serif !important;
    font-weight:500 !important;
}
.stButton > button:hover { transform:translateY(-1px) !important; box-shadow:0 4px 16px rgba(78,107,53,0.3) !important; }
.stSlider > div > div > div > div { background: #7BA05B !important; }
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>

/* FIX: Card text visibility */
.card, .metric-card, .msg-ai .bubble {
    color: #2C3E35 !important;
}

/* FIX: Recommended resources text */
.card p, .card li, .card span {
    color: #2C3E35 !important;
    font-weight: 500;
}

/* FIX: headings inside cards */
.card h1, .card h2, .card h3 {
    color: #1f2d26 !important;
}

/* FIX: make white cards slightly visible */
.card {
    background: rgba(255,255,255,0.96) !important;
}

/* OPTIONAL: add subtle hover (premium feel) */
.card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(44,62,53,0.15);
}

/* FIX: ensure all text inside main area is visible */
section.main * {
    color: #2C3E35;
}

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
        <h1>🌿 MindEase</h1>
        <p>AI Mental Health Companion</p>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio("Navigation", [
        "💬 AI Therapist Chat",
        "📋 Mental Health Assessment",
        "📊 My Wellness Report"
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("**⚙️ Configuration**")
    key_in = st.text_input("Groq API Key", type="password",
                            value=st.session_state.groq_api_key,
                            placeholder="gsk_...",
                            help="Get free key at console.groq.com")
    if key_in:
        st.session_state.groq_api_key = key_in

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.78rem; color:#7A8B80; line-height:1.8;">
    🆘 <strong style="color:#ff8a80;">Crisis Helplines</strong><br>
    iCall (India): <strong>9152987821</strong><br>
    Vandrevala: <strong>1860-2662-345</strong><br>
    NIMHANS: <strong>080-46110007</strong><br>
    iCall WhatsApp: <strong>9152987821</strong>
    </div>
    """, unsafe_allow_html=True)

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
            <p>Your assessment suggests you may need immediate support. Please reach out to a crisis helpline or mental health professional right away. You are not alone.</p>
        </div>
        """, unsafe_allow_html=True)

    col_chat, col_tools = st.columns([3, 1])

    with col_chat:
        # Build chat HTML
        html = '<div class="chat-scroll">'
        if not st.session_state.messages:
            html += """
            <div class="msg-ai">
                <div class="avatar">🌿</div>
                <div>
                    <div class="bubble">
                        Hello, I'm MindEase — your compassionate AI companion. 💚<br><br>
                        I'm here to listen without judgment. Feel free to share anything — stress, anxiety, relationship issues, work pressure, or simply how your day went.<br><br>
                        <em>How are you feeling today?</em>
                    </div>
                </div>
            </div>"""
        for msg in st.session_state.messages:
            ts = msg.get("timestamp", "")
            if msg["role"] == "user":
                html += f'<div class="msg-user"><div><div class="bubble">{msg["content"]}</div><div class="msg-ts">{ts}</div></div></div>'
            else:
                html += f'<div class="msg-ai"><div class="avatar">🌿</div><div><div class="bubble">{msg["content"]}</div><div class="msg-ts">{ts}</div></div></div>'
        html += '</div>'

        st.markdown(f'<div class="card">{html}</div>', unsafe_allow_html=True)

        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_area("", placeholder="Share what's on your mind...", height=90, label_visibility="collapsed")
            c1, c2 = st.columns([5, 1])
            with c2:
                send = st.form_submit_button("Send 💬", use_container_width=True)

        if send and user_input.strip():
            client = get_client()
            if not client:
                st.error("⚠️ Please enter your Groq API key in the sidebar to start chatting.")
            else:
                ts = datetime.now().strftime("%H:%M")
                st.session_state.messages.append({"role": "user", "content": user_input.strip(), "timestamp": ts})

                SYSTEM = """You are MindEase, a compassionate and empathetic AI mental health companion trained in:
- Cognitive Behavioral Therapy (CBT) techniques
- Mindfulness-Based Stress Reduction (MBSR)
- Supportive counseling and active listening
- Crisis intervention awareness

Your guidelines:
1. Always validate emotions first before offering advice
2. Ask thoughtful follow-up questions to understand the user's situation
3. Offer evidence-based coping strategies gently and appropriately
4. Never diagnose or prescribe — you are a supportive companion, not a clinician
5. If you detect signs of self-harm, suicidal ideation, or acute crisis — immediately provide crisis resources
6. Keep responses warm, calm, and hopeful (2–4 short paragraphs max)
7. Occasionally remind users to seek professional mental health support

Crisis resources to share when needed:
- iCall (India): 9152987821
- Vandrevala Foundation: 1860-2662-345
- NIMHANS helpline: 080-46110007"""

                api_msgs = [{"role": "system", "content": SYSTEM}]
                for m in st.session_state.messages[-14:]:
                    api_msgs.append({"role": m["role"], "content": m["content"]})

                with st.spinner("MindEase is responding..."):
                    try:
                        resp = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=api_msgs,
                            max_tokens=600,
                            temperature=0.75
                        )
                        reply = resp.choices[0].message.content
                        st.session_state.messages.append({
                            "role": "assistant", "content": reply,
                            "timestamp": datetime.now().strftime("%H:%M")
                        })
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")

    with col_tools:
        st.markdown('<div class="section-title">🛠 Quick Tools</div>', unsafe_allow_html=True)

        with st.expander("🌬 Breathing", color="black"):
            st.markdown("""**4-7-8 Technique**
1. Inhale **4 sec**
2. Hold **7 sec**
3. Exhale **8 sec**

Repeat 3–4 cycles.""")

        with st.expander("⚓ Grounding 5-4-3-2-1",  color="black"):
            st.markdown("""Notice:
- **5** things you see
- **4** things you touch
- **3** things you hear
- **2** things you smell
- **1** thing you taste""")

        with st.expander("✍ Journal Prompts",  color="black"):
            for p in [
                "What am I feeling right now, and why?",
                "What is one thing I'm grateful for today?",
                "What would I tell a friend in my situation?",
                "What do I need most right now?",
            ]:
                st.markdown(f"• _{p}_")

        with st.expander("💊 Self-Care Checklist"):
            st.checkbox("💧 Drank enough water")
            st.checkbox("🍎 Ate a proper meal")
            st.checkbox("🚶 Moved my body today")
            st.checkbox("😴 Got enough sleep")
            st.checkbox("🤝 Connected with someone")

        st.markdown('<div class="disclaimer">⚕️ Not a substitute for professional care.</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — ASSESSMENT
# ═══════════════════════════════════════════════════════════════════════════════
elif "📋 Mental Health Assessment" in page:
    st.markdown("""
    <div class="page-header">
        <h1>📋 Mental Health Assessment</h1>
        <p>Clinically-informed screening using PHQ-9, GAD-7, PSS & ISI tools</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="disclaimer">
    📌 This uses validated clinical screening tools for personal awareness only. Results are <strong>not</strong> a clinical diagnosis. Please consult a mental health professional for a full evaluation. Completing this takes about 5 minutes.
    </div><br>
    """, unsafe_allow_html=True)

    opts4 = ["Not at all (0)", "Several days (1)", "More than half the days (2)", "Nearly every day (3)"]
    opts5 = ["Never (0)", "Almost never (1)", "Sometimes (2)", "Fairly often (3)", "Very often (4)"]
    opts_sleep = ["None (0)", "Mild (1)", "Moderate (2)", "Severe (3)", "Very Severe (4)"]
    opts_sat   = ["Very satisfied (0)", "Satisfied (1)", "Neutral (2)", "Dissatisfied (3)", "Very dissatisfied (4)"]

    with st.form("assessment_form"):

        # ── Depression PHQ-9 ──
        st.markdown('<div class="section-title">😔 Section 1: Depression (PHQ-9)</div>', unsafe_allow_html=True)
        st.caption("Over the **past 2 weeks**, how often have you been bothered by the following?")
        d1 = st.selectbox("Little interest or pleasure in doing things", opts4, key="d1")
        d2 = st.selectbox("Feeling down, depressed, or hopeless", opts4, key="d2")
        d3 = st.selectbox("Trouble falling/staying asleep, or sleeping too much", opts4, key="d3")
        d4 = st.selectbox("Feeling tired or having little energy", opts4, key="d4")
        d5 = st.selectbox("Poor appetite or overeating", opts4, key="d5")
        d6 = st.selectbox("Feeling bad about yourself or that you are a failure", opts4, key="d6")
        d7 = st.selectbox("Trouble concentrating on things such as reading or watching TV", opts4, key="d7")
        d8 = st.selectbox("Moving or speaking so slowly that others noticed — or being restless", opts4, key="d8")
        d9 = st.selectbox("Thoughts that you would be better off dead or of hurting yourself", opts4, key="d9")

        st.markdown("---")
        # ── Anxiety GAD-7 ──
        st.markdown('<div class="section-title">😰 Section 2: Anxiety (GAD-7)</div>', unsafe_allow_html=True)
        st.caption("Over the **past 2 weeks**, how often have you been bothered by the following?")
        a1 = st.selectbox("Feeling nervous, anxious, or on edge", opts4, key="a1")
        a2 = st.selectbox("Not being able to stop or control worrying", opts4, key="a2")
        a3 = st.selectbox("Worrying too much about different things", opts4, key="a3")
        a4 = st.selectbox("Trouble relaxing", opts4, key="a4")
        a5 = st.selectbox("Being so restless it is hard to sit still", opts4, key="a5")
        a6 = st.selectbox("Becoming easily annoyed or irritable", opts4, key="a6")
        a7 = st.selectbox("Feeling afraid as if something awful might happen", opts4, key="a7")

        st.markdown("---")
        # ── Stress PSS ──
        st.markdown('<div class="section-title">😤 Section 3: Stress (PSS-4)</div>', unsafe_allow_html=True)
        st.caption("Over the **past month**, how often have you felt...")
        s1 = st.selectbox("Unable to control the important things in your life", opts5, key="s1")
        s2 = st.selectbox("Confident about your ability to handle personal problems", opts5, key="s2")
        s3 = st.selectbox("Things were going your way", opts5, key="s3")
        s4 = st.selectbox("Difficulties were piling up so high that you could not overcome them", opts5, key="s4")

        st.markdown("---")
        # ── Sleep ISI ──
        st.markdown('<div class="section-title">😴 Section 4: Sleep Quality (ISI)</div>', unsafe_allow_html=True)
        sl1 = st.selectbox("Severity of difficulty falling asleep", opts_sleep, key="sl1")
        sl2 = st.selectbox("Severity of difficulty staying asleep through the night", opts_sleep, key="sl2")
        sl3 = st.selectbox("Problem of waking up too early in the morning", opts_sleep, key="sl3")
        sl4 = st.selectbox("Satisfaction with your current sleep pattern", opts_sat, key="sl4")

        st.markdown("---")
        # ── Lifestyle ──
        st.markdown('<div class="section-title">🤝 Section 5: Lifestyle & Social Factors</div>', unsafe_allow_html=True)
        social   = st.slider("How connected do you feel to friends/family? (1=Very isolated, 10=Very connected)", 1, 10, 5)
        exercise = st.selectbox("How often do you exercise or engage in physical activity?",
                                 ["Never", "Rarely (once/month)", "Sometimes (1-2x/week)", "Regularly (3-4x/week)", "Daily"])
        substance = st.selectbox("Do you use alcohol or substances to cope with stress or emotions?",
                                  ["Never", "Rarely", "Sometimes", "Often", "Almost daily"])
        support   = st.selectbox("Current mental health professional support status",
                                  ["Yes, actively in therapy", "Had therapy before", "Considering it", "No support at all"])

        submitted = st.form_submit_button("🔍 Analyse My Mental Health", use_container_width=True)

    if submitted:
        dep_score   = sum(extract_score(i) for i in [d1,d2,d3,d4,d5,d6,d7,d8,d9])
        anx_score   = sum(extract_score(i) for i in [a1,a2,a3,a4,a5,a6,a7])
        stress_score = extract_score(s1) + (4-extract_score(s2)) + (4-extract_score(s3)) + extract_score(s4)
        sleep_score  = sum(extract_score(i) for i in [sl1,sl2,sl3,sl4])

        ex_map  = {"Never":6,"Rarely (once/month)":4,"Sometimes (1-2x/week)":2,"Regularly (3-4x/week)":0,"Daily":0}
        sub_map = {"Never":0,"Rarely":2,"Sometimes":4,"Often":6,"Almost daily":8}
        sup_map = {"Yes, actively in therapy":-4,"Had therapy before":-2,"Considering it":0,"No support at all":3}
        lifestyle_penalty = ex_map[exercise] + sub_map[substance] + max(0,(5-social)*2) + sup_map[support]

        dep_pct  = round(dep_score/27*100)
        anx_pct  = round(anx_score/21*100)
        str_pct  = round(stress_score/16*100)
        slp_pct  = round(sleep_score/16*100)
        lif_pct  = min(100, max(0, round(lifestyle_penalty/17*100)))
        overall  = round(dep_pct*0.30 + anx_pct*0.25 + str_pct*0.20 + slp_pct*0.15 + lif_pct*0.10)

        crisis = extract_score(d9) >= 2
        if crisis or overall >= 65:
            risk = "High"; rbadge = "risk-high"
        elif overall >= 35:
            risk = "Moderate"; rbadge = "risk-medium"
        else:
            risk = "Low"; rbadge = "risk-low"

        st.session_state.assessment_scores = {
            "depression": dep_pct, "anxiety": anx_pct,
            "stress": str_pct, "sleep": slp_pct,
            "lifestyle": lif_pct, "overall": overall
        }
        st.session_state.risk_level      = risk
        st.session_state.assessment_done = True

        st.markdown("---")
        if crisis:
            st.markdown("""
            <div class="crisis-banner">
                <h3>⚠️ Immediate Support Is Available</h3>
                <p>Your responses indicate thoughts of self-harm or suicide. Please reach out now:<br>
                <strong>iCall: 9152987821 | Vandrevala: 1860-2662-345 | NIMHANS: 080-46110007</strong></p>
            </div>""", unsafe_allow_html=True)

        c1, c2 = st.columns([1, 2])
        rcolor = "#D4574A" if risk=="High" else "#E8A04A" if risk=="Moderate" else "#5B9B7A"

        with c1:
            st.markdown(f"""
            <div class="card" style="text-align:center;padding:2rem;">
                <div style="font-size:0.82rem;color:#7A8B80;text-transform:uppercase;letter-spacing:0.1em;">Overall Risk</div>
                <div style="font-family:'DM Serif Display',serif;font-size:3.5rem;color:#2C3E35;margin:0.5rem 0;">
                    {overall}<span style="font-size:1.5rem;">%</span>
                </div>
                <span class="risk-badge {rbadge}">{risk} Risk</span>
                <div style="font-size:0.78rem;color:#7A8B80;margin-top:0.8rem;">PHQ-9 · GAD-7 · PSS · ISI</div>
            </div>""", unsafe_allow_html=True)

        with c2:
            for label, pct, color in [
                ("😔 Depression",  dep_pct, "#D4574A"),
                ("😰 Anxiety",     anx_pct, "#E8A04A"),
                ("😤 Stress",      str_pct, "#C17B4E"),
                ("😴 Sleep Issues",slp_pct, "#7BA05B"),
                ("🤝 Lifestyle",   lif_pct, "#5B9B7A"),
            ]:
                c = "#D4574A" if pct>=65 else "#E8A04A" if pct>=35 else "#5B9B7A"
                st.markdown(f"""
                <div style="background:white;border-radius:10px;padding:0.8rem 1rem;margin-bottom:0.6rem;border-left:4px solid {c};box-shadow:0 2px 8px rgba(0,0,0,0.06);">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="font-weight:500;font-size:0.9rem;">{label}</span>
                        <span style="font-size:0.9rem;font-weight:600;color:{c};">{pct}%</span>
                    </div>
                    <div class="score-bar"><div class="score-fill" style="width:{pct}%;background:{c};"></div></div>
                </div>""", unsafe_allow_html=True)

        # AI Recommendations
        st.markdown("---")
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

Please provide:
1. A 2-sentence compassionate validation of their experience
2. Three specific, evidence-based coping strategies tailored to their highest-scoring areas
3. One concrete daily habit to start this week
4. Clear guidance on whether/what type of professional help to seek

Keep the tone warm, hopeful, and actionable. Avoid clinical jargon."""

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
        <p>Your holistic mental health snapshot and action plan</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.assessment_done:
        st.info("📋 Please complete the Mental Health Assessment first to view your Wellness Report.")
        st.stop()

    sc = st.session_state.assessment_scores
    risk = st.session_state.risk_level
    rcolor = {"Low":"#5B9B7A","Moderate":"#E8A04A","High":"#D4574A"}.get(risk,"#7A8B80")

    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card">
            <div class="label">Overall Risk</div>
            <div class="value" style="color:{rcolor};">{sc['overall']}%</div>
            <div style="font-size:0.8rem;color:{rcolor};font-weight:600;">{risk} Risk</div>
        </div>
        <div class="metric-card" style="border-color:#D4574A;">
            <div class="label">Depression</div>
            <div class="value">{sc['depression']}%</div>
        </div>
        <div class="metric-card" style="border-color:#E8A04A;">
            <div class="label">Anxiety</div>
            <div class="value">{sc['anxiety']}%</div>
        </div>
        <div class="metric-card" style="border-color:#C17B4E;">
            <div class="label">Stress</div>
            <div class="value">{sc['stress']}%</div>
        </div>
        <div class="metric-card" style="border-color:#5B9B7A;">
            <div class="label">Sleep Issues</div>
            <div class="value">{sc['sleep']}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-title">📈 Dimension Analysis</div>', unsafe_allow_html=True)
        for dim, val, c in [
            ("😔 Depression", sc['depression'], "#D4574A"),
            ("😰 Anxiety",    sc['anxiety'],    "#E8A04A"),
            ("😤 Stress",     sc['stress'],     "#C17B4E"),
            ("😴 Sleep",      sc['sleep'],      "#7BA05B"),
            ("🤝 Lifestyle",  sc['lifestyle'],  "#5B9B7A"),
        ]:
            fc = "#D4574A" if val>=65 else "#E8A04A" if val>=35 else "#5B9B7A"
            lbl = "⚠ High" if val>=65 else "⚡ Moderate" if val>=35 else "✔ Low"
            st.markdown(f"""
            <div style="margin-bottom:1rem;">
                <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                    <span style="font-weight:500;font-size:0.9rem;">{dim}</span>
                    <span style="font-size:0.85rem;color:{fc};">{lbl} — {val}%</span>
                </div>
                <div class="score-bar">
                    <div class="score-fill" style="width:{val}%;background:linear-gradient(90deg,{fc}88,{fc});"></div>
                </div>
            </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-title">🎯 Priority Action Plan</div>', unsafe_allow_html=True)
        actions = []
        if sc['depression']>=50: actions.append(("🧠 Seek CBT Therapy","Depression indicators elevated. CBT is gold-standard treatment.","#D4574A"))
        if sc['anxiety']>=50:    actions.append(("🌬 Daily Mindfulness","Practice 4-7-8 breathing + 10-min meditation each morning.","#E8A04A"))
        if sc['stress']>=50:     actions.append(("📅 Stress Management","Break tasks into steps, schedule breaks, practice time-blocking.","#C17B4E"))
        if sc['sleep']>=50:      actions.append(("🌙 Sleep Hygiene","Fixed sleep schedule, no screens 1hr before bed, dark cool room.","#7BA05B"))
        if sc['lifestyle']>=40:  actions.append(("🏃 Daily 20-min Walk","Exercise reduces depression and anxiety significantly.","#5B9B7A"))
        if not actions:          actions.append(("✨ Maintain Wellness","Your scores are healthy — keep up your self-care routine!","#5B9B7A"))

        for title, desc, c in actions:
            st.markdown(f"""
            <div style="background:white;border-radius:10px;padding:1rem;margin-bottom:0.8rem;border-left:4px solid {c};box-shadow:0 2px 8px rgba(0,0,0,0.06);">
                <div style="font-weight:600;font-size:0.92rem;color:#2C3E35;">{title}</div>
                <div style="font-size:0.84rem;color:#7A8B80;margin-top:4px;">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-title">📚 Recommended Resources</div>', unsafe_allow_html=True)
    rc1, rc2, rc3 = st.columns(3)
    for col, title, items in [
        (rc1, "📱 Apps", ["Wysa — AI mental health","Headspace — Meditation","Calm — Sleep & anxiety","Sanvello — CBT-based"]),
        (rc2, "📖 Books", ["Feeling Good — David Burns","The Anxiety Workbook","Why Has Nobody Told Me This?","Lost Connections — Johann Hari"]),
        (rc3, "🏥 Professional Help", ["Psychiatrist (medication)","Clinical Psychologist (CBT)","Licensed Counsellor (talking)","Group Therapy (peer support)"]),
    ]:
        with col:
            st.markdown(f'<div class="card"><strong>{title}</strong><br><br>' + "<br>".join(f"• {i}" for i in items) + "</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <br><div class="disclaimer">
    📌 <strong>Disclaimer:</strong> This wellness report is generated from self-reported data using validated screening instruments for personal awareness only. It does not constitute a clinical diagnosis. Please share these results with a qualified mental health professional for proper evaluation.<br>
    Session: {st.session_state.session_start} · Risk Level: <strong>{risk}</strong>
    </div>""", unsafe_allow_html=True)
