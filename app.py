"""
app.py - Healthcare RAG Chatbot — Premium UI
"""

import os
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title="MediQuery — AI Health Assistant",
    page_icon="assets/favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Full custom CSS ───────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #F7F4EF;
    font-family: 'DM Sans', sans-serif;
    color: #1A1A1A;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header, [data-testid="stToolbar"] { display: none !important; }
[data-testid="stAppViewContainer"] > .main { padding: 0 !important; }
[data-testid="block-container"] { padding: 2rem 2.5rem 4rem !important; max-width: 900px; margin: 0 auto; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #1C2B3A !important;
    border-right: none !important;
}
[data-testid="stSidebar"] * { color: #E8E2D9 !important; }
[data-testid="stSidebar"] .stSlider > div > div { background: #2E4459 !important; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {
    color: #C9B99A !important;
    font-family: 'DM Serif Display', serif !important;
    font-size: 1rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin: 1.5rem 0 0.5rem;
    border-bottom: 1px solid #2E4459;
    padding-bottom: 0.4rem;
}
[data-testid="stSidebar"] hr { border-color: #2E4459 !important; margin: 1rem 0 !important; }
[data-testid="stSidebar"] input, [data-testid="stSidebar"] .stTextInput input {
    background: #243647 !important;
    border: 1px solid #3A556A !important;
    color: #E8E2D9 !important;
    border-radius: 6px !important;
}
[data-testid="stSidebar"] .stSelectbox select {
    background: #243647 !important;
    color: #E8E2D9 !important;
}
[data-testid="stSidebar"] label { color: #A8BCC8 !important; font-size: 0.78rem !important; letter-spacing: 0.05em; text-transform: uppercase; }
[data-testid="stSidebar"] .stButton button {
    background: transparent !important;
    border: 1px solid #3A556A !important;
    color: #C9B99A !important;
    border-radius: 6px;
    font-size: 0.8rem;
    width: 100%;
    transition: all 0.2s;
}
[data-testid="stSidebar"] .stButton button:hover {
    background: #2E4459 !important;
    border-color: #C9B99A !important;
}

/* ── Hero Header ── */
.hero {
    background: linear-gradient(135deg, #1C2B3A 0%, #2E4459 60%, #1C2B3A 100%);
    border-radius: 16px;
    padding: 3rem 3rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 240px; height: 240px;
    background: radial-gradient(circle, rgba(201,185,154,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 30%;
    width: 160px; height: 160px;
    background: radial-gradient(circle, rgba(201,185,154,0.08) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-label {
    font-size: 0.72rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #C9B99A;
    margin-bottom: 0.8rem;
    font-weight: 500;
}
.hero h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 2.8rem;
    color: #F7F4EF;
    line-height: 1.15;
    margin-bottom: 1rem;
    font-weight: 400;
}
.hero h1 em {
    font-style: italic;
    color: #C9B99A;
}
.hero p {
    color: #A8BCC8;
    font-size: 0.95rem;
    line-height: 1.7;
    max-width: 560px;
    font-weight: 300;
}
.hero-stats {
    display: flex;
    gap: 2rem;
    margin-top: 2rem;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(201,185,154,0.2);
}
.hero-stat { display: flex; flex-direction: column; gap: 0.2rem; }
.hero-stat strong { font-family: 'DM Serif Display', serif; font-size: 1.4rem; color: #F7F4EF; font-weight: 400; }
.hero-stat span { font-size: 0.72rem; color: #6E8A9C; letter-spacing: 0.08em; text-transform: uppercase; }

/* ── Status bar ── */
.status-bar {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: #EEF7EE;
    border: 1px solid #C3DFC3;
    border-radius: 8px;
    padding: 0.7rem 1.1rem;
    margin-bottom: 1.5rem;
    font-size: 0.85rem;
    color: #2D6A2D;
}
.status-dot {
    width: 8px; height: 8px;
    background: #4CAF50;
    border-radius: 50%;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(76,175,80,0.4); }
    50% { opacity: 0.8; box-shadow: 0 0 0 4px rgba(76,175,80,0); }
}

/* ── Disclaimer ── */
.disclaimer {
    background: #FDF8F0;
    border: 1px solid #E8D5B0;
    border-left: 3px solid #C9B99A;
    border-radius: 8px;
    padding: 0.8rem 1.1rem;
    font-size: 0.82rem;
    color: #7A6040;
    margin-bottom: 1.8rem;
    line-height: 1.5;
}

/* ── Chat area ── */
.chat-wrap { display: flex; flex-direction: column; gap: 1.2rem; margin-bottom: 1.5rem; }

.msg-user {
    align-self: flex-end;
    background: #1C2B3A;
    color: #F7F4EF;
    padding: 0.9rem 1.2rem;
    border-radius: 16px 16px 4px 16px;
    max-width: 72%;
    font-size: 0.92rem;
    line-height: 1.55;
    box-shadow: 0 2px 12px rgba(28,43,58,0.15);
}

.msg-bot {
    align-self: flex-start;
    background: #FFFFFF;
    color: #1A1A1A;
    padding: 1.1rem 1.3rem;
    border-radius: 4px 16px 16px 16px;
    max-width: 85%;
    font-size: 0.92rem;
    line-height: 1.7;
    border: 1px solid #E8E2D9;
    box-shadow: 0 2px 16px rgba(0,0,0,0.05);
}
.msg-meta {
    font-size: 0.72rem;
    color: #9AA8B2;
    margin-top: 0.4rem;
    letter-spacing: 0.04em;
}

/* ── Source passages ── */
.source-passage {
    background: #F7F4EF;
    border-left: 3px solid #C9B99A;
    padding: 0.8rem 1rem;
    margin-top: 0.6rem;
    border-radius: 0 6px 6px 0;
    font-size: 0.78rem;
    color: #5A5040;
    line-height: 1.6;
}
.source-label {
    font-size: 0.68rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #C9B99A;
    font-weight: 600;
    margin-bottom: 0.3rem;
}

/* ── Sample questions ── */
.section-title {
    font-size: 0.72rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #9AA8B2;
    margin-bottom: 0.8rem;
    font-weight: 500;
}
.stButton button {
    background: #FFFFFF !important;
    border: 1px solid #E8E2D9 !important;
    color: #1C2B3A !important;
    border-radius: 8px !important;
    font-size: 0.82rem !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 0.6rem 0.9rem !important;
    text-align: left !important;
    transition: all 0.2s ease !important;
    white-space: normal !important;
    height: auto !important;
    line-height: 1.4 !important;
}
.stButton button:hover {
    border-color: #1C2B3A !important;
    background: #F7F4EF !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(28,43,58,0.1) !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
    background: #FFFFFF !important;
    border: 1.5px solid #D0C8BC !important;
    border-radius: 12px !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #1C2B3A !important;
    box-shadow: 0 0 0 3px rgba(28,43,58,0.08) !important;
}
[data-testid="stChatInputSubmitButton"] button {
    background: #1C2B3A !important;
    border-radius: 8px !important;
}

/* ── Divider ── */
.divider { height: 1px; background: #E8E2D9; margin: 1.5rem 0; }

/* ── Health parameters card ── */
.param-card {
    background: #FFFFFF;
    border: 1px solid #E8E2D9;
    border-radius: 10px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.6rem;
}
.param-name { font-size: 0.72rem; color: #9AA8B2; letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 0.2rem; }
.param-val { font-family: 'DM Serif Display', serif; font-size: 1.1rem; color: #1C2B3A; }
.param-range { font-size: 0.68rem; color: #B0A898; margin-top: 0.1rem; }

/* ── Developer card ── */
.dev-card {
    background: linear-gradient(135deg, #1C2B3A, #243647);
    border-radius: 12px;
    padding: 1.2rem;
    margin-top: 1rem;
    text-align: center;
}
.dev-avatar {
    width: 48px; height: 48px;
    background: #C9B99A;
    border-radius: 50%;
    margin: 0 auto 0.6rem;
    display: flex; align-items: center; justify-content: center;
    font-family: 'DM Serif Display', serif;
    font-size: 1.2rem;
    color: #1C2B3A;
}
.dev-name { font-family: 'DM Serif Display', serif; font-size: 1rem; color: #F7F4EF; margin-bottom: 0.2rem; }
.dev-role { font-size: 0.72rem; color: #6E8A9C; letter-spacing: 0.08em; text-transform: uppercase; }
.dev-links { display: flex; justify-content: center; gap: 0.8rem; margin-top: 0.8rem; }
.dev-links a { font-size: 0.75rem; color: #C9B99A !important; text-decoration: none; letter-spacing: 0.04em; }
</style>
""", unsafe_allow_html=True)


# ── Caching ───────────────────────────────────────────────
@st.cache_resource(show_spinner="Indexing knowledge base...")
def load_vs():
    from vector_store import load_vectorstore
    return load_vectorstore()


# ── Sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 1.2rem 0 0.5rem;">
        <div style="font-family:'DM Serif Display',serif; font-size:1.4rem; color:#F7F4EF; letter-spacing:-0.01em;">MediQuery</div>
        <div style="font-size:0.7rem; color:#6E8A9C; letter-spacing:0.12em; text-transform:uppercase; margin-top:0.2rem;">AI Health Assistant</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # API Key
    groq_key = st.text_input(
        "API Key",
        type="password",
        value=os.environ.get("GROQ_API_KEY", ""),
        placeholder="gsk_...",
    )
    if groq_key:
        os.environ["GROQ_API_KEY"] = groq_key

    st.markdown("---")
    st.markdown("### Context")
    num_chunks = st.slider("Retrieved passages", 1, 8, 4)
    show_sources = st.toggle("Show source passages", value=True)

    st.markdown("---")
    st.markdown("### Health Parameters")
    st.markdown("*Enter your vitals for context-aware answers*")

    age = st.number_input("Age (years)", min_value=1, max_value=120, value=30, step=1)
    weight = st.number_input("Weight (kg)", min_value=10, max_value=300, value=70, step=1)
    height = st.number_input("Height (cm)", min_value=50, max_value=250, value=170, step=1)

    bmi = round(weight / ((height / 100) ** 2), 1)
    bmi_status = "Underweight" if bmi < 18.5 else "Normal" if bmi < 25 else "Overweight" if bmi < 30 else "Obese"
    bmi_color = "#4CAF50" if bmi_status == "Normal" else "#FF9800" if bmi_status in ["Underweight","Overweight"] else "#F44336"

    st.markdown(f"""
    <div class="param-card">
        <div class="param-name">BMI</div>
        <div class="param-val" style="color:{bmi_color}">{bmi}</div>
        <div class="param-range">{bmi_status} &nbsp;·&nbsp; Normal: 18.5–24.9</div>
    </div>
    """, unsafe_allow_html=True)

    sys_bp = st.number_input("Systolic BP (mmHg)", 60, 220, 120, step=1)
    dia_bp = st.number_input("Diastolic BP (mmHg)", 40, 140, 80, step=1)
    bp_status = "Normal" if sys_bp < 120 and dia_bp < 80 else "Elevated" if sys_bp < 130 else "High"
    bp_color = "#4CAF50" if bp_status == "Normal" else "#FF9800" if bp_status == "Elevated" else "#F44336"

    st.markdown(f"""
    <div class="param-card">
        <div class="param-name">Blood Pressure</div>
        <div class="param-val" style="color:{bp_color}">{sys_bp}/{dia_bp}</div>
        <div class="param-range">{bp_status} &nbsp;·&nbsp; Normal: &lt;120/80</div>
    </div>
    """, unsafe_allow_html=True)

    blood_glucose = st.number_input("Blood Glucose (mg/dL)", 50, 500, 90, step=1)
    glucose_status = "Normal" if blood_glucose < 100 else "Pre-diabetic" if blood_glucose < 126 else "Diabetic range"
    gl_color = "#4CAF50" if glucose_status == "Normal" else "#FF9800" if glucose_status == "Pre-diabetic" else "#F44336"

    st.markdown(f"""
    <div class="param-card">
        <div class="param-name">Blood Glucose</div>
        <div class="param-val" style="color:{gl_color}">{blood_glucose} mg/dL</div>
        <div class="param-range">{glucose_status} &nbsp;·&nbsp; Normal: &lt;100</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Filters")
    response_style = st.selectbox("Response style", ["Detailed", "Concise", "Layman terms"])
    medical_area   = st.selectbox("Focus area", ["General", "Cardiology", "Neurology", "Endocrinology", "Pulmonology", "Oncology"])

    st.markdown("---")
    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()

    # Developer card
    st.markdown("""
    <div class="dev-card">
        <div class="dev-avatar">PG</div>
        <div class="dev-name">Prikshit Gautam</div>
        <div class="dev-role">Developer &amp; Researcher</div>
        <div class="dev-links">
            <a href="https://github.com/prikshitgautam27" target="_blank">GitHub</a>
            <a href="https://linkedin.com" target="_blank">LinkedIn</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top:1rem; font-size:0.68rem; color:#3A556A; text-align:center; line-height:1.5;">
        Built with Gale Encyclopedia of Medicine<br>
        FAISS · MiniLM · Llama 3.1 · Groq<br>
        <span style="color:#2E4459;">v2.0 &nbsp;·&nbsp; 2026</span>
    </div>
    """, unsafe_allow_html=True)


# ── Main area ─────────────────────────────────────────────

# Hero
st.markdown("""
<div class="hero">
    <div class="hero-label">Gale Encyclopedia of Medicine &nbsp;·&nbsp; RAG Pipeline</div>
    <h1>Your trusted<br><em>medical knowledge</em><br>companion</h1>
    <p>Evidence-based answers drawn directly from the Gale Encyclopedia of Medicine, powered by semantic search and large language models.</p>
    <div class="hero-stats">
        <div class="hero-stat">
            <strong>759</strong>
            <span>Source pages</span>
        </div>
        <div class="hero-stat">
            <strong>7,470</strong>
            <span>Indexed passages</span>
        </div>
        <div class="hero-stat">
            <strong>&lt; 2s</strong>
            <span>Response time</span>
        </div>
        <div class="hero-stat">
            <strong>Free</strong>
            <span>Always</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Gate: API key
if not os.environ.get("GROQ_API_KEY"):
    st.info("Enter your Groq API key in the sidebar to begin. Get a free key at console.groq.com", icon="🔑")
    st.stop()

# Gate: vectorstore
if not Path("vectorstore").exists():
    st.error("Vector store not found. Run `python pdf_ingestion.py` first.")
    st.stop()

# Load
vectorstore = load_vs()

# Status bar
st.markdown("""
<div class="status-bar">
    <div class="status-dot"></div>
    Knowledge base loaded &nbsp;·&nbsp; 7,470 passages indexed &nbsp;·&nbsp; Ready to answer
</div>
""", unsafe_allow_html=True)

# Disclaimer
st.markdown("""
<div class="disclaimer">
    <strong>Medical Disclaimer</strong> &mdash; This tool provides educational information based on published medical literature.
    It is not a substitute for professional medical advice, diagnosis, or treatment.
    Always consult a qualified healthcare provider for personal medical decisions.
</div>
""", unsafe_allow_html=True)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render chat
if st.session_state.messages:
    st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="msg-user">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="msg-bot">{msg["content"]}</div>', unsafe_allow_html=True)
            if show_sources and msg.get("sources"):
                with st.expander("View source passages"):
                    for i, src in enumerate(msg["sources"], 1):
                        st.markdown(f"""
                        <div class="source-passage">
                            <div class="source-label">Passage {i}</div>
                            {src[:480]}...
                        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Input
user_input = st.chat_input("Ask a medical question...")

if user_input:
    # Build health context string to pass to LLM
    health_ctx = (
        f"Patient context: Age {age}, Weight {weight}kg, Height {height}cm, BMI {bmi} ({bmi_status}), "
        f"BP {sys_bp}/{dia_bp} ({bp_status}), Glucose {blood_glucose} mg/dL ({glucose_status}). "
        f"Response style: {response_style}. Focus area: {medical_area}."
    )

    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f'<div class="msg-user">{user_input}</div>', unsafe_allow_html=True)

    with st.spinner("Searching knowledge base..."):
        from rag_pipeline import generate_answer
        result = generate_answer(
            question=f"{health_ctx}\n\nQuestion: {user_input}",
            vectorstore=vectorstore,
            k=num_chunks,
        )

    answer  = result["answer"]
    sources = result["sources"]

    st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})
    st.markdown(f'<div class="msg-bot">{answer}</div>', unsafe_allow_html=True)

    if show_sources and sources:
        with st.expander("View source passages"):
            for i, src in enumerate(sources, 1):
                st.markdown(f"""
                <div class="source-passage">
                    <div class="source-label">Passage {i}</div>
                    {src[:480]}...
                </div>""", unsafe_allow_html=True)
    st.rerun()

# Sample questions
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Suggested questions</div>', unsafe_allow_html=True)

samples = [
    "What are early warning signs of Type 2 Diabetes?",
    "How is hypertension diagnosed and managed?",
    "What triggers an asthma attack?",
    "Explain the progression of Alzheimer's disease.",
    "What are the risk factors for coronary artery disease?",
    "How is tuberculosis treated?",
    "What causes kidney stones and how to prevent them?",
    "What are symptoms of thyroid disorders?",
    "How does high cholesterol affect the heart?",
]

cols = st.columns(3)
for i, q in enumerate(samples):
    with cols[i % 3]:
        if st.button(q, key=f"sq{i}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": q})
            st.rerun()

# Footer
st.markdown("""
<div style="margin-top:3rem; padding-top:1.5rem; border-top:1px solid #E8E2D9; text-align:center;">
    <div style="font-family:'DM Serif Display',serif; font-size:1rem; color:#9AA8B2; margin-bottom:0.4rem;">MediQuery</div>
    <div style="font-size:0.72rem; color:#B0A898; letter-spacing:0.06em;">
        Built on the Gale Encyclopedia of Medicine &nbsp;&middot;&nbsp; For educational use only &nbsp;&middot;&nbsp; 2026
    </div>
</div>
""", unsafe_allow_html=True)