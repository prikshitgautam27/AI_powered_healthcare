"""
app.py — MediQuery Home
Recruiter-friendly landing page. No authentication.
"""
import streamlit as st
import os

st.set_page_config(
    page_title="MediQuery — AI Medical Assistant",
    page_icon="M",
    layout="wide",
    initial_sidebar_state="expanded",
)

try:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
except Exception:
    pass

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: #F8F6F2 !important;
    font-family: 'Inter', sans-serif;
    color: #1A1A2E;
}
#MainMenu, footer, header, [data-testid="stToolbar"] { display: none !important; }

[data-testid="stSidebar"] { background: #FFFFFF !important; border-right: 1px solid #EDE8E0 !important; }
[data-testid="stSidebar"] * { color: #1A1A2E !important; }
[data-testid="stSidebar"] hr { border-color: #EDE8E0 !important; }
[data-testid="stPageLink"] a, [data-testid="stPageLink"] a span, [data-testid="stPageLink"] p {
    color: #1B4332 !important; font-size: 0.88rem !important; font-weight: 500 !important; text-decoration: none !important;
}
[data-testid="stPageLink"]:hover a { color: #2D6A4F !important; }

[data-testid="block-container"] { padding: 2rem 2.5rem !important; max-width: 1100px; margin: 0 auto; }

.fade{animation:fadeUp 0.5s ease forwards;opacity:0;}
.f1{animation-delay:0.05s}.f2{animation-delay:0.15s}.f3{animation-delay:0.25s}
@keyframes fadeUp{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}

.hero{background:linear-gradient(135deg,#1B4332 0%,#2D6A4F 60%,#40916C 100%);border-radius:16px;padding:3.5rem 3.5rem;position:relative;overflow:hidden;margin-bottom:1.5rem;}
.hero::before{content:'';position:absolute;right:-80px;top:-80px;width:280px;height:280px;background:radial-gradient(circle,rgba(255,255,255,0.07) 0%,transparent 70%);border-radius:50%;}
.hero::after{content:'';position:absolute;bottom:-40px;left:30%;width:180px;height:180px;background:radial-gradient(circle,rgba(255,255,255,0.04) 0%,transparent 70%);border-radius:50%;}
.hero-badge{display:inline-block;background:rgba(255,255,255,0.12);border:1px solid rgba(255,255,255,0.2);border-radius:20px;padding:0.3rem 0.9rem;font-size:0.62rem;letter-spacing:0.18em;text-transform:uppercase;color:#B7E4C7;margin-bottom:1rem;}
.hero-title{font-family:'Playfair Display',serif;font-size:2.6rem;color:#FFFFFF;font-weight:400;line-height:1.2;margin-bottom:0.9rem;}
.hero-title em{font-style:italic;color:#95D5B2;}
.hero-desc{font-size:0.92rem;color:rgba(255,255,255,0.72);line-height:1.75;max-width:560px;font-weight:300;}
.badge-row{display:flex;flex-wrap:wrap;gap:0.5rem;margin-top:1.6rem;}
.tbadge{font-size:0.6rem;letter-spacing:0.08em;text-transform:uppercase;padding:0.28rem 0.8rem;border-radius:20px;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.15);color:rgba(255,255,255,0.7);}

.kpi-row{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-bottom:1.6rem;}
.kpi{background:#FFFFFF;border:1px solid #EDE8E0;border-radius:12px;padding:1.3rem 1.5rem;transition:all 0.2s;box-shadow:0 1px 4px rgba(0,0,0,0.04);}
.kpi:hover{border-color:#B7E4C7;transform:translateY(-2px);box-shadow:0 6px 20px rgba(27,67,50,0.08);}
.kpi-label{font-size:0.6rem;letter-spacing:0.14em;text-transform:uppercase;color:#A0ADB8;margin-bottom:0.4rem;font-weight:500;}
.kpi-value{font-family:'Playfair Display',serif;font-size:1.9rem;color:#1A1A2E;font-weight:400;line-height:1;}
.kpi-sub{font-size:0.68rem;color:#B0BDC8;margin-top:0.3rem;}
.kpi-accent{color:#2D6A4F;}

.fc-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:1rem;margin-bottom:1rem;}
.fc{background:#FFFFFF;border:1px solid #EDE8E0;border-radius:12px;padding:1.6rem;transition:all 0.2s;box-shadow:0 1px 4px rgba(0,0,0,0.04);}
.fc:hover{border-color:#95D5B2;transform:translateY(-2px);box-shadow:0 8px 24px rgba(27,67,50,0.1);}
.fc-num{font-size:0.58rem;letter-spacing:0.15em;text-transform:uppercase;color:#2D6A4F;margin-bottom:0.5rem;font-weight:600;}
.fc-title{font-family:'Playfair Display',serif;font-size:1.15rem;color:#1A1A2E;margin-bottom:0.5rem;}
.fc-desc{font-size:0.8rem;color:#8A9BB0;line-height:1.65;}

.sec-hdr{display:flex;align-items:center;gap:1rem;margin:1.8rem 0 1rem;}
.sec-title{font-size:0.68rem;letter-spacing:0.15em;text-transform:uppercase;color:#A0ADB8;white-space:nowrap;font-weight:500;}
.sec-line{flex:1;height:1px;background:#EDE8E0;}

.stButton button{background:#1B4332!important;border:none!important;color:#FFFFFF!important;border-radius:8px!important;font-family:'Inter',sans-serif!important;font-size:0.78rem!important;font-weight:500!important;letter-spacing:0.05em!important;text-transform:uppercase!important;padding:0.8rem 1.2rem!important;transition:all 0.2s!important;box-shadow:0 2px 8px rgba(27,67,50,0.25)!important;}
.stButton button:hover{background:#2D6A4F!important;transform:translateY(-1px)!important;}

.footer-note{text-align:center;font-size:0.72rem;color:#B0BDC8;margin-top:2rem;padding-top:1.5rem;border-top:1px solid #EDE8E0;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style="padding:1.2rem 0 0.8rem;">
        <div style="font-family:'Playfair Display',serif;font-size:1.4rem;color:#1A1A2E;font-weight:400;">MediQuery</div>
        <div style="font-size:0.62rem;color:#A0ADB8;letter-spacing:0.14em;text-transform:uppercase;margin-top:0.2rem;">AI Health Assistant</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.page_link("app.py",             label="Home")
    st.page_link("pages/1_Query.py",   label="Live Demo")
    st.page_link("pages/2_About.py",   label="About the Project")
    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.72rem;color:#A0ADB8;line-height:1.7;">
        Retrieval-Augmented Generation over the Gale Encyclopedia of Medicine.<br><br>
        Built with FAISS, Sentence-Transformers, and Groq-hosted LLMs.
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="hero fade f1">
    <div class="hero-badge">Retrieval-Augmented Generation · Portfolio Project</div>
    <div class="hero-title">Medi<em>Query</em></div>
    <div class="hero-desc">An end-to-end RAG system that answers medical questions grounded in the Gale Encyclopedia of Medicine — combining semantic search, structured prompting, and a low-latency LLM backend into a single production-style app.</div>
    <div class="badge-row">
        <span class="tbadge">FAISS</span>
        <span class="tbadge">Sentence-Transformers</span>
        <span class="tbadge">Groq LPU Inference</span>
        <span class="tbadge">Streamlit</span>
        <span class="tbadge">PyMuPDF</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="kpi-row fade f2">
    <div class="kpi"><div class="kpi-label">Source pages</div><div class="kpi-value">759</div><div class="kpi-sub">Gale Encyclopedia</div></div>
    <div class="kpi"><div class="kpi-label">Indexed passages</div><div class="kpi-value">7,470</div><div class="kpi-sub">512-char chunks</div></div>
    <div class="kpi"><div class="kpi-label">Avg response</div><div class="kpi-value kpi-accent">&lt;2s</div><div class="kpi-sub">End-to-end latency</div></div>
    <div class="kpi"><div class="kpi-label">Embedding dim</div><div class="kpi-value">384</div><div class="kpi-sub">Cosine similarity</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="sec-hdr"><div class="sec-title">Explore</div><div class="sec-line"></div></div>', unsafe_allow_html=True)

st.markdown("""
<div class="fc-grid fade f3">
    <div class="fc"><div class="fc-num">Live Demo</div><div class="fc-title">Ask the encyclopedia a question</div><div class="fc-desc">Try the working RAG pipeline yourself — ask a medical question and see the retrieved source passages alongside the generated answer.</div></div>
    <div class="fc"><div class="fc-num">About the Project</div><div class="fc-title">Architecture, models & design</div><div class="fc-desc">A deeper look at how the system is built: the ingestion pipeline, the embedding and generation models, UI/UX choices, and what makes this project distinct.</div></div>
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    if st.button("Try the Live Demo  →", use_container_width=True):
        st.switch_page("pages/1_Query.py")
with c2:
    if st.button("View Architecture & Design  →", use_container_width=True):
        st.switch_page("pages/2_About.py")

st.markdown('<div class="footer-note">Built as a portfolio project · Not intended for real medical diagnosis</div>', unsafe_allow_html=True)