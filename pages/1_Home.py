"""
pages/1_Home.py — Home Dashboard
Fixed: no st.switch_page, uses sidebar navigation only
"""
import streamlit as st, os, time
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="MediQuery — Home", page_icon="M", layout="wide", initial_sidebar_state="expanded")

# Load key from secrets
try:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
except: pass

# Auth guard — show warning instead of switch_page
if not st.session_state.get("logged_in"):
    st.warning("Please sign in first.")
    st.markdown("[Go to Login](/) ", unsafe_allow_html=True)
    st.stop()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&family=Jost:wght@300;400;500&display=swap');
html,body,[data-testid="stAppViewContainer"]{background:#0D1117;font-family:'Jost',sans-serif;color:#E8E0D0;}
#MainMenu,footer,header{display:none!important;}
[data-testid="stSidebar"]{background:#111820!important;border-right:1px solid rgba(200,180,140,0.08)!important;}
[data-testid="stSidebar"] *{color:#E8E0D0!important;}
[data-testid="stSidebar"] label{color:#3A4A58!important;font-size:0.68rem!important;letter-spacing:0.1em!important;text-transform:uppercase!important;}
[data-testid="stSidebar"] hr{border-color:rgba(200,180,140,0.08)!important;}
[data-testid="stSidebar"] .stButton button{background:rgba(200,180,140,0.06)!important;border:1px solid rgba(200,180,140,0.15)!important;color:#C8B47A!important;border-radius:6px!important;font-size:0.72rem!important;letter-spacing:0.1em!important;text-transform:uppercase!important;width:100%!important;margin-bottom:0.3rem!important;}
[data-testid="block-container"]{padding:2rem 2.5rem!important;max-width:1200px;margin:0 auto;}
.fade{animation:fadeUp 0.6s ease forwards;opacity:0;}
.f1{animation-delay:0.05s}.f2{animation-delay:0.15s}.f3{animation-delay:0.25s}.f4{animation-delay:0.35s}
@keyframes fadeUp{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:translateY(0)}}
.topbar{display:flex;align-items:center;justify-content:space-between;padding-bottom:1.5rem;border-bottom:1px solid rgba(200,180,140,0.07);margin-bottom:2rem;}
.tb-brand{font-family:'Cormorant Garamond',serif;font-size:1.3rem;color:#F5EFE4;}
.tb-brand span{color:#C8B47A;}
.tb-user{font-size:0.72rem;color:#3A4A58;}
.tb-user strong{color:#C8B47A;}
.hero{background:linear-gradient(135deg,rgba(28,43,58,0.7),rgba(18,28,38,0.9));border:1px solid rgba(200,180,140,0.1);border-radius:16px;padding:2.8rem 3rem;position:relative;overflow:hidden;margin-bottom:1.5rem;}
.hero::before{content:'';position:absolute;right:-60px;top:-60px;width:220px;height:220px;background:radial-gradient(circle,rgba(200,180,140,0.07) 0%,transparent 70%);border-radius:50%;}
.hero-eyebrow{font-size:0.62rem;letter-spacing:0.2em;text-transform:uppercase;color:#C8B47A;margin-bottom:0.7rem;}
.hero-title{font-family:'Cormorant Garamond',serif;font-size:2.2rem;color:#F5EFE4;font-weight:300;line-height:1.2;margin-bottom:0.7rem;}
.hero-title em{font-style:italic;color:#C8B47A;}
.hero-desc{font-size:0.85rem;color:#3A4A58;line-height:1.7;max-width:500px;}
.badge-row{display:flex;flex-wrap:wrap;gap:0.5rem;margin-top:1.5rem;}
.badge{font-size:0.62rem;letter-spacing:0.08em;text-transform:uppercase;padding:0.25rem 0.75rem;border-radius:20px;border:1px solid rgba(200,180,140,0.12);color:#3A4A58;}
.kpi-row{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-bottom:1.5rem;}
.kpi{background:rgba(255,255,255,0.02);border:1px solid rgba(200,180,140,0.07);border-radius:12px;padding:1.2rem 1.4rem;transition:border-color 0.2s,transform 0.2s;}
.kpi:hover{border-color:rgba(200,180,140,0.18);transform:translateY(-2px);}
.kpi-label{font-size:0.6rem;letter-spacing:0.14em;text-transform:uppercase;color:#2A3A48;margin-bottom:0.4rem;}
.kpi-value{font-family:'Cormorant Garamond',serif;font-size:1.9rem;color:#F5EFE4;font-weight:300;line-height:1;}
.kpi-sub{font-size:0.68rem;color:#3A4A58;margin-top:0.25rem;}
.kpi-accent{color:#C8B47A;}
.fc-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-bottom:1.5rem;}
.fc{background:rgba(255,255,255,0.015);border:1px solid rgba(200,180,140,0.07);border-radius:12px;padding:1.4rem;transition:all 0.2s;}
.fc:hover{background:rgba(200,180,140,0.03);border-color:rgba(200,180,140,0.18);transform:translateY(-2px);}
.fc-num{font-size:0.6rem;letter-spacing:0.15em;text-transform:uppercase;color:#C8B47A;margin-bottom:0.5rem;}
.fc-title{font-family:'Cormorant Garamond',serif;font-size:1.05rem;color:#C0CEDB;margin-bottom:0.3rem;}
.fc-desc{font-size:0.75rem;color:#2A3A48;line-height:1.55;}
.sec-hdr{display:flex;align-items:center;gap:1rem;margin:1.5rem 0 1rem;}
.sec-title{font-family:'Cormorant Garamond',serif;font-size:1rem;color:#5A6A78;white-space:nowrap;}
.sec-line{flex:1;height:1px;background:rgba(200,180,140,0.06);}
.stButton button{background:rgba(255,255,255,0.02)!important;border:1px solid rgba(200,180,140,0.07)!important;color:#3A4A58!important;border-radius:8px!important;font-family:'Jost',sans-serif!important;font-size:0.75rem!important;text-transform:none!important;padding:0.6rem 0.8rem!important;white-space:normal!important;height:auto!important;line-height:1.4!important;transition:all 0.2s!important;}
.stButton button:hover{border-color:rgba(200,180,140,0.2)!important;color:#C0CEDB!important;}
</style>
""", unsafe_allow_html=True)

username = st.session_state.get("username","User")
hour = time.localtime().tm_hour
greeting = "Good morning" if hour<12 else "Good afternoon" if hour<17 else "Good evening"

with st.sidebar:
    st.markdown(f"""<div style="padding:1rem 0 0.5rem;">
        <div style="font-family:'Cormorant Garamond',serif;font-size:1.3rem;color:#F5EFE4;">MediQuery</div>
        <div style="font-size:0.65rem;color:#2A3A48;letter-spacing:0.14em;text-transform:uppercase;margin-top:0.2rem;">AI Health Assistant</div>
    </div>
    <div style="font-size:0.72rem;color:#3A4A58;margin:0.5rem 0 1rem;">Signed in as <strong style="color:#C8B47A;">{username}</strong></div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.page_link("pages/1_Home.py",   label="Home",    icon="○")
    st.page_link("pages/2_Query.py",  label="Query",   icon="◇")
    st.page_link("pages/3_Metrics.py",label="Metrics", icon="△")
    st.markdown("---")
    if st.button("Sign Out"):
        st.session_state.logged_in=False; st.session_state.username=""
        st.rerun()

# Topbar
st.markdown(f"""
<div class="topbar fade f1">
    <div class="tb-brand">Medi<span>Query</span></div>
    <div class="tb-user">{greeting}, <strong>{username}</strong></div>
</div>""", unsafe_allow_html=True)

# Hero
st.markdown(f"""
<div class="hero fade f2">
    <div class="hero-eyebrow">Gale Encyclopedia of Medicine &nbsp;·&nbsp; RAG Pipeline &nbsp;·&nbsp; Live</div>
    <div class="hero-title">{greeting},<br><em>{username}.</em><br>How can I help today?</div>
    <div class="hero-desc">Evidence-based answers grounded in published medical literature. Ask anything — from symptoms to treatments to risk factors.</div>
    <div class="badge-row">
        <span class="badge">MiniLM-L6-v2</span>
        <span class="badge">FAISS</span>
        <span class="badge">Llama 3.1</span>
        <span class="badge">Groq API</span>
        <span class="badge">RAG Pipeline</span>
    </div>
</div>""", unsafe_allow_html=True)

# KPIs
st.markdown("""
<div class="kpi-row fade f3">
    <div class="kpi"><div class="kpi-label">Source pages</div><div class="kpi-value">759</div><div class="kpi-sub">Gale Encyclopedia</div></div>
    <div class="kpi"><div class="kpi-label">Indexed passages</div><div class="kpi-value">7,470</div><div class="kpi-sub">512-char chunks · 64 overlap</div></div>
    <div class="kpi"><div class="kpi-label">Avg response</div><div class="kpi-value kpi-accent">&lt;2s</div><div class="kpi-sub">End-to-end latency</div></div>
    <div class="kpi"><div class="kpi-label">Embedding dim</div><div class="kpi-value">384</div><div class="kpi-sub">MiniLM cosine similarity</div></div>
</div>""", unsafe_allow_html=True)

# Feature cards
st.markdown("""
<div class="fc-grid fade f4">
    <div class="fc"><div class="fc-num">01</div><div class="fc-title">Medical Query</div><div class="fc-desc">Ask any health question. Personalised with your vitals — BMI, blood pressure, glucose.</div></div>
    <div class="fc"><div class="fc-num">02</div><div class="fc-title">Performance Metrics</div><div class="fc-desc">Live dashboard of retrieval accuracy, latency, and relevance scores. Resume-ready data.</div></div>
    <div class="fc"><div class="fc-num">03</div><div class="fc-title">Source Passages</div><div class="fc-desc">Every answer is traceable — see the exact encyclopedia passages that informed it.</div></div>
</div>""", unsafe_allow_html=True)

# Quick questions
st.markdown('<div class="sec-hdr"><div class="sec-title">Quick access</div><div class="sec-line"></div></div>', unsafe_allow_html=True)
samples = ["Symptoms of Type 2 Diabetes","Hypertension diagnosis & treatment","Asthma triggers and management","Alzheimer's disease stages","Heart disease risk factors","Kidney stone prevention"]
cols = st.columns(3)
for i,q in enumerate(samples):
    with cols[i%3]:
        if st.button(q, key=f"hq{i}", use_container_width=True):
            st.session_state["prefill_query"] = q
