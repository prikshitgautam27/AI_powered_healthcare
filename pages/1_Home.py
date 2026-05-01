"""
pages/1_Home.py — Animated Home / Dashboard
"""
import streamlit as st, time, os
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="MediQuery — Home", page_icon="M", layout="wide", initial_sidebar_state="expanded")

if not st.session_state.get("logged_in"):
    st.switch_page("app.py")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Jost:wght@300;400;500&display=swap');
html, body, [data-testid="stAppViewContainer"] { background:#0D1117; font-family:'Jost',sans-serif; color:#E8E0D0; }
#MainMenu, footer, header { display:none !important; }
[data-testid="stSidebar"] { background:#111820 !important; border-right:1px solid rgba(200,180,140,0.08) !important; }
[data-testid="stSidebar"] * { color:#E8E0D0 !important; }
[data-testid="stSidebar"] label { color:#4A5A68 !important; font-size:0.7rem !important; letter-spacing:0.1em !important; text-transform:uppercase !important; }
[data-testid="stSidebar"] input { background:rgba(255,255,255,0.04) !important; border:1px solid rgba(200,180,140,0.15) !important; border-radius:6px !important; color:#E8E0D0 !important; }
[data-testid="stSidebar"] hr { border-color:rgba(200,180,140,0.08) !important; }
[data-testid="stSidebar"] .stButton button { background:rgba(200,180,140,0.08) !important; border:1px solid rgba(200,180,140,0.2) !important; color:#C8B47A !important; border-radius:6px !important; font-size:0.75rem !important; letter-spacing:0.1em !important; text-transform:uppercase !important; width:100% !important; }
[data-testid="block-container"] { padding:2rem 2.5rem !important; max-width:1200px; margin:0 auto; }

/* Fade-in animation */
.fade-in { animation: fadeIn 0.7s ease forwards; opacity:0; }
.fade-in-1 { animation-delay:0.1s; }
.fade-in-2 { animation-delay:0.25s; }
.fade-in-3 { animation-delay:0.4s; }
.fade-in-4 { animation-delay:0.55s; }
@keyframes fadeIn { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:translateY(0)} }

/* Nav bar */
.topnav {
    display:flex; align-items:center; justify-content:space-between;
    padding:1rem 0 2rem; border-bottom:1px solid rgba(200,180,140,0.08);
    margin-bottom:2.5rem;
}
.topnav-brand { font-family:'Cormorant Garamond',serif; font-size:1.3rem; color:#F5EFE4; }
.topnav-brand span { color:#C8B47A; }
.topnav-links { display:flex; gap:2rem; }
.topnav-link { font-size:0.75rem; letter-spacing:0.1em; text-transform:uppercase; color:#4A5A68; text-decoration:none; cursor:pointer; transition:color 0.2s; }
.topnav-link:hover, .topnav-link.active { color:#C8B47A; }
.topnav-user { font-size:0.75rem; color:#4A5A68; letter-spacing:0.06em; }
.topnav-user strong { color:#C8B47A; }

/* Hero welcome */
.welcome-hero {
    background: linear-gradient(135deg, rgba(28,43,58,0.6) 0%, rgba(18,28,38,0.8) 100%);
    border:1px solid rgba(200,180,140,0.1);
    border-radius:16px; padding:3rem 3rem 2.5rem;
    position:relative; overflow:hidden; margin-bottom:2rem;
}
.welcome-hero::before {
    content:''; position:absolute; right:-80px; top:-80px;
    width:260px; height:260px;
    background:radial-gradient(circle, rgba(200,180,140,0.08) 0%, transparent 70%);
    border-radius:50%;
}
.welcome-time { font-size:0.68rem; letter-spacing:0.2em; text-transform:uppercase; color:#C8B47A; margin-bottom:0.8rem; }
.welcome-title { font-family:'Cormorant Garamond',serif; font-size:2.4rem; color:#F5EFE4; font-weight:300; line-height:1.2; margin-bottom:0.8rem; }
.welcome-title em { font-style:italic; color:#C8B47A; }
.welcome-desc { font-size:0.88rem; color:#4A5A68; line-height:1.7; max-width:520px; }

/* Stat cards */
.stats-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:1rem; margin-bottom:2rem; }
.stat-card {
    background:rgba(255,255,255,0.025);
    border:1px solid rgba(200,180,140,0.08);
    border-radius:12px; padding:1.3rem 1.5rem;
    transition:border-color 0.2s, transform 0.2s;
}
.stat-card:hover { border-color:rgba(200,180,140,0.2); transform:translateY(-2px); }
.stat-card-label { font-size:0.65rem; letter-spacing:0.15em; text-transform:uppercase; color:#3A4A58; margin-bottom:0.5rem; }
.stat-card-value { font-family:'Cormorant Garamond',serif; font-size:2rem; color:#F5EFE4; font-weight:300; line-height:1; }
.stat-card-sub { font-size:0.72rem; color:#4A5A68; margin-top:0.3rem; }
.stat-card-accent { color:#C8B47A; }

/* Feature cards */
.features-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:1rem; margin-bottom:2rem; }
.feature-card {
    background:rgba(255,255,255,0.02);
    border:1px solid rgba(200,180,140,0.07);
    border-radius:12px; padding:1.5rem;
    cursor:pointer; transition:all 0.25s;
    text-decoration:none;
}
.feature-card:hover { background:rgba(200,180,140,0.04); border-color:rgba(200,180,140,0.2); transform:translateY(-3px); }
.fc-icon { font-size:1.4rem; margin-bottom:0.8rem; filter:grayscale(0.3); }
.fc-title { font-family:'Cormorant Garamond',serif; font-size:1.1rem; color:#C0CEDB; margin-bottom:0.4rem; }
.fc-desc { font-size:0.78rem; color:#3A4A58; line-height:1.6; }
.fc-arrow { font-size:0.75rem; color:#C8B47A; margin-top:0.8rem; letter-spacing:0.1em; }

/* Section header */
.section-hdr { display:flex; align-items:center; gap:1rem; margin-bottom:1rem; }
.section-hdr-title { font-family:'Cormorant Garamond',serif; font-size:1.2rem; color:#C0CEDB; }
.section-hdr-line { flex:1; height:1px; background:rgba(200,180,140,0.08); }

/* Quick ask */
.qa-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:0.6rem; }
.qa-chip {
    background:rgba(255,255,255,0.025);
    border:1px solid rgba(200,180,140,0.08);
    border-radius:8px; padding:0.8rem 1rem;
    font-size:0.78rem; color:#6A7A88;
    cursor:pointer; transition:all 0.2s; line-height:1.4;
}
.qa-chip:hover { border-color:rgba(200,180,140,0.25); color:#C0CEDB; background:rgba(200,180,140,0.04); }

/* Tech stack badge */
.stack-row { display:flex; flex-wrap:wrap; gap:0.5rem; margin-top:1rem; }
.stack-badge {
    font-size:0.68rem; letter-spacing:0.08em;
    padding:0.3rem 0.8rem; border-radius:20px;
    border:1px solid rgba(200,180,140,0.15); color:#5A6A78;
    text-transform:uppercase;
}

.stButton button {
    background:linear-gradient(135deg,#1C2B3A,#243647) !important;
    border:1px solid rgba(200,180,140,0.25) !important;
    color:#C8B47A !important; border-radius:8px !important;
    font-family:'Jost',sans-serif !important;
    font-size:0.75rem !important; letter-spacing:0.1em !important;
    text-transform:uppercase !important; transition:all 0.2s !important;
}
.stButton button:hover { border-color:rgba(200,180,140,0.5) !important; transform:translateY(-1px) !important; }
</style>
""", unsafe_allow_html=True)

username = st.session_state.get("username","User")
hour = time.localtime().tm_hour
greeting = "Good morning" if hour < 12 else "Good afternoon" if hour < 17 else "Good evening"

# Sidebar
with st.sidebar:
    st.markdown(f"""
    <div style="padding:1rem 0 0.5rem;">
        <div style="font-family:'Cormorant Garamond',serif;font-size:1.3rem;color:#F5EFE4;">MediQuery</div>
        <div style="font-size:0.68rem;color:#3A4A58;letter-spacing:0.12em;text-transform:uppercase;margin-top:0.2rem;">AI Health Assistant</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f"<div style='font-size:0.75rem;color:#4A5A68;'>Signed in as <strong style='color:#C8B47A;'>{username}</strong></div>", unsafe_allow_html=True)
    st.markdown("---")
    groq_key = st.text_input("Groq API Key", type="password", value=os.environ.get("GROQ_API_KEY",""), placeholder="gsk_...")
    if groq_key: os.environ["GROQ_API_KEY"] = groq_key
    st.markdown("---")
    if st.button("Go to Query  →"):
        st.switch_page("2_Query.py")
    if st.button("View Metrics  →"):
        st.switch_page("3_Metrics.py")
    st.markdown("---")
    if st.button("Sign Out"):
        st.session_state.logged_in = False
        st.session_state.username  = ""
        st.switch_page("app.py")

# Top nav
st.markdown(f"""
<div class="topnav fade-in fade-in-1">
    <div class="topnav-brand">Medi<span>Query</span></div>
    <div class="topnav-links">
        <span class="topnav-link active">Home</span>
        <span class="topnav-link">Query</span>
        <span class="topnav-link">Metrics</span>
    </div>
    <div class="topnav-user">{greeting}, <strong>{username}</strong></div>
</div>
""", unsafe_allow_html=True)

# Welcome hero
st.markdown(f"""
<div class="welcome-hero fade-in fade-in-2">
    <div class="welcome-time">Gale Encyclopedia of Medicine · RAG Pipeline · Live</div>
    <div class="welcome-title">{greeting},<br><em>{username}.</em></div>
    <div class="welcome-desc">
        Your AI-powered medical knowledge assistant is ready. Ask anything grounded in
        evidence-based medical literature — with context, sources, and precision.
    </div>
    <div class="stack-row">
        <span class="stack-badge">MiniLM-L6-v2</span>
        <span class="stack-badge">FAISS</span>
        <span class="stack-badge">Llama 3.1</span>
        <span class="stack-badge">Groq API</span>
        <span class="stack-badge">RAG Pipeline</span>
        <span class="stack-badge">Streamlit</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Stats
st.markdown("""
<div class="stats-grid fade-in fade-in-3">
    <div class="stat-card">
        <div class="stat-card-label">Source pages</div>
        <div class="stat-card-value">759</div>
        <div class="stat-card-sub">Gale Encyclopedia</div>
    </div>
    <div class="stat-card">
        <div class="stat-card-label">Indexed passages</div>
        <div class="stat-card-value">7,470</div>
        <div class="stat-card-sub">512-char chunks</div>
    </div>
    <div class="stat-card">
        <div class="stat-card-label">Avg response</div>
        <div class="stat-card-value stat-card-accent">&lt; 2s</div>
        <div class="stat-card-sub">Via Groq inference</div>
    </div>
    <div class="stat-card">
        <div class="stat-card-label">Retrieval model</div>
        <div class="stat-card-value" style="font-size:1.1rem;padding-top:0.4rem;">MiniLM</div>
        <div class="stat-card-sub">384-dim embeddings</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Feature cards
st.markdown("""
<div class="features-grid fade-in fade-in-4">
    <div class="feature-card">
        <div class="fc-icon">&#9670;</div>
        <div class="fc-title">Medical Query</div>
        <div class="fc-desc">Ask any health question. Personalized with your vitals — age, BMI, blood pressure, glucose.</div>
        <div class="fc-arrow">Open Query →</div>
    </div>
    <div class="feature-card">
        <div class="fc-icon">&#9633;</div>
        <div class="fc-title">Performance Metrics</div>
        <div class="fc-desc">Live dashboard of retrieval accuracy, response latency, relevance scores, and system health.</div>
        <div class="fc-arrow">View Metrics →</div>
    </div>
    <div class="feature-card">
        <div class="fc-icon">&#9651;</div>
        <div class="fc-title">Source Passages</div>
        <div class="fc-desc">Every answer is traceable. See exactly which encyclopedia passages informed the response.</div>
        <div class="fc-arrow">Explore →</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Quick questions
st.markdown('<div class="section-hdr"><div class="section-hdr-title">Quick access</div><div class="section-hdr-line"></div></div>', unsafe_allow_html=True)
st.markdown('<div class="qa-grid">', unsafe_allow_html=True)
samples = [
    "Symptoms of Type 2 Diabetes",
    "Hypertension diagnosis & treatment",
    "Asthma triggers and management",
    "Alzheimer's disease stages",
    "Heart disease risk factors",
    "Kidney stone prevention",
]
cols = st.columns(3)
for i, q in enumerate(samples):
    with cols[i % 3]:
        if st.button(q, key=f"home_q{i}", use_container_width=True):
            st.session_state["prefill_query"] = q
            st.switch_page("2_Query.py")
st.markdown('</div>', unsafe_allow_html=True)
