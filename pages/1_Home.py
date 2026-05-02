import streamlit as st, os, time
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="MediQuery — Home", page_icon="M", layout="wide", initial_sidebar_state="expanded")

try: os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
except: pass

if not st.session_state.get("logged_in"):
    st.warning("Please sign in first.")
    st.page_link("app.py", label="Go to Login", icon="🔐")
    st.stop()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');
html,body,[data-testid="stAppViewContainer"]{background:#F8F6F2!important;font-family:'Inter',sans-serif;color:#1A1A2E;}
#MainMenu,footer,header{display:none!important;}

[data-testid="stSidebar"]{background:#FFFFFF!important;border-right:1px solid #EDE8E0!important;}
[data-testid="stSidebar"] *{color:#1A1A2E!important;}
[data-testid="stSidebar"] label{color:#8A9BB0!important;font-size:0.68rem!important;letter-spacing:0.1em!important;text-transform:uppercase!important;font-weight:500!important;}
[data-testid="stSidebar"] input{background:#F8F6F2!important;border:1.5px solid #E2DDD6!important;border-radius:8px!important;color:#1A1A2E!important;}
[data-testid="stSidebar"] input:focus{border-color:#2D6A4F!important;}
[data-testid="stSidebar"] hr{border-color:#EDE8E0!important;}
[data-testid="stSidebar"] .stButton button{background:#1B4332!important;border:none!important;color:#FFFFFF!important;border-radius:8px!important;font-size:0.72rem!important;letter-spacing:0.1em!important;text-transform:uppercase!important;width:100%!important;margin-bottom:0.3rem!important;box-shadow:0 2px 6px rgba(27,67,50,0.2)!important;}
[data-testid="stSidebar"] .stButton button:hover{background:#2D6A4F!important;}
[data-testid="stPageLink"] a{color:#1B4332!important;font-size:0.82rem!important;font-weight:500!important;}

[data-testid="block-container"]{padding:2rem 2.5rem!important;max-width:1200px;margin:0 auto;}

.fade{animation:fadeUp 0.5s ease forwards;opacity:0;}
.f1{animation-delay:0.05s}.f2{animation-delay:0.15s}.f3{animation-delay:0.25s}.f4{animation-delay:0.35s}
@keyframes fadeUp{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}

.topbar{display:flex;align-items:center;justify-content:space-between;padding-bottom:1.5rem;border-bottom:1px solid #EDE8E0;margin-bottom:2rem;}
.tb-brand{font-family:'Playfair Display',serif;font-size:1.4rem;color:#1A1A2E;font-weight:400;}
.tb-brand span{color:#2D6A4F;}
.tb-user{font-size:0.78rem;color:#8A9BB0;}
.tb-user strong{color:#2D6A4F;font-weight:600;}

.hero{background:linear-gradient(135deg,#1B4332 0%,#2D6A4F 60%,#40916C 100%);border-radius:16px;padding:3rem 3.5rem;position:relative;overflow:hidden;margin-bottom:1.5rem;}
.hero::before{content:'';position:absolute;right:-80px;top:-80px;width:280px;height:280px;background:radial-gradient(circle,rgba(255,255,255,0.07) 0%,transparent 70%);border-radius:50%;}
.hero::after{content:'';position:absolute;bottom:-40px;left:30%;width:180px;height:180px;background:radial-gradient(circle,rgba(255,255,255,0.04) 0%,transparent 70%);border-radius:50%;}
.hero-badge{display:inline-block;background:rgba(255,255,255,0.12);border:1px solid rgba(255,255,255,0.2);border-radius:20px;padding:0.3rem 0.9rem;font-size:0.62rem;letter-spacing:0.18em;text-transform:uppercase;color:#B7E4C7;margin-bottom:1rem;}
.hero-title{font-family:'Playfair Display',serif;font-size:2.2rem;color:#FFFFFF;font-weight:400;line-height:1.2;margin-bottom:0.8rem;}
.hero-title em{font-style:italic;color:#95D5B2;}
.hero-desc{font-size:0.88rem;color:rgba(255,255,255,0.65);line-height:1.7;max-width:500px;font-weight:300;}
.badge-row{display:flex;flex-wrap:wrap;gap:0.5rem;margin-top:1.5rem;}
.tbadge{font-size:0.6rem;letter-spacing:0.08em;text-transform:uppercase;padding:0.25rem 0.75rem;border-radius:20px;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.15);color:rgba(255,255,255,0.65);}

.kpi-row{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-bottom:1.5rem;}
.kpi{background:#FFFFFF;border:1px solid #EDE8E0;border-radius:12px;padding:1.3rem 1.5rem;transition:all 0.2s;box-shadow:0 1px 4px rgba(0,0,0,0.04);}
.kpi:hover{border-color:#B7E4C7;transform:translateY(-2px);box-shadow:0 6px 20px rgba(27,67,50,0.08);}
.kpi-label{font-size:0.6rem;letter-spacing:0.14em;text-transform:uppercase;color:#A0ADB8;margin-bottom:0.4rem;font-weight:500;}
.kpi-value{font-family:'Playfair Display',serif;font-size:1.9rem;color:#1A1A2E;font-weight:400;line-height:1;}
.kpi-sub{font-size:0.68rem;color:#B0BDC8;margin-top:0.3rem;}
.kpi-accent{color:#2D6A4F;}

.fc-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-bottom:1.5rem;}
.fc{background:#FFFFFF;border:1px solid #EDE8E0;border-radius:12px;padding:1.5rem;transition:all 0.2s;box-shadow:0 1px 4px rgba(0,0,0,0.04);}
.fc:hover{border-color:#95D5B2;transform:translateY(-2px);box-shadow:0 8px 24px rgba(27,67,50,0.1);}
.fc-num{font-size:0.58rem;letter-spacing:0.15em;text-transform:uppercase;color:#2D6A4F;margin-bottom:0.5rem;font-weight:600;}
.fc-title{font-family:'Playfair Display',serif;font-size:1.05rem;color:#1A1A2E;margin-bottom:0.4rem;}
.fc-desc{font-size:0.76rem;color:#8A9BB0;line-height:1.6;}

.sec-hdr{display:flex;align-items:center;gap:1rem;margin:1.5rem 0 1rem;}
.sec-title{font-size:0.68rem;letter-spacing:0.15em;text-transform:uppercase;color:#A0ADB8;white-space:nowrap;font-weight:500;}
.sec-line{flex:1;height:1px;background:#EDE8E0;}

.stButton button{background:#FFFFFF!important;border:1.5px solid #EDE8E0!important;color:#1B4332!important;border-radius:8px!important;font-family:'Inter',sans-serif!important;font-size:0.76rem!important;font-weight:500!important;text-transform:none!important;padding:0.65rem 0.8rem!important;white-space:normal!important;height:auto!important;line-height:1.4!important;transition:all 0.2s!important;text-align:left!important;box-shadow:0 1px 3px rgba(0,0,0,0.04)!important;}
.stButton button:hover{border-color:#2D6A4F!important;background:#F0FDF4!important;color:#1B4332!important;}
</style>
""", unsafe_allow_html=True)

username = st.session_state.get("username","User")
hour = time.localtime().tm_hour
greeting = "Good morning" if hour<12 else "Good afternoon" if hour<17 else "Good evening"

with st.sidebar:
    st.markdown(f"""
    <div style="padding:1.2rem 0 0.8rem;">
        <div style="font-family:'Playfair Display',serif;font-size:1.4rem;color:#1A1A2E;">MediQuery</div>
        <div style="font-size:0.62rem;color:#A0ADB8;letter-spacing:0.14em;text-transform:uppercase;margin-top:0.2rem;">AI Health Assistant</div>
    </div>
    <div style="font-size:0.75rem;color:#8A9BB0;margin-bottom:0.8rem;">Signed in as <strong style="color:#2D6A4F;">{username}</strong></div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.page_link("pages/1_Home.py",    label="Home",    icon="🏠")
    st.page_link("pages/2_Query.py",   label="Query",   icon="🔍")
    st.page_link("pages/3_Metrics.py", label="Metrics", icon="📊")
    st.markdown("---")
    if st.button("Sign Out"):
        st.session_state.logged_in=False; st.session_state.username=""; st.rerun()

st.markdown(f"""
<div class="topbar fade f1">
    <div class="tb-brand">Medi<span>Query</span></div>
    <div class="tb-user">{greeting}, <strong>{username}</strong></div>
</div>
<div class="hero fade f2">
    <div class="hero-badge">Gale Encyclopedia of Medicine · RAG Pipeline · Live</div>
    <div class="hero-title">{greeting},<br><em>{username}.</em><br>How can I help today?</div>
    <div class="hero-desc">Evidence-based answers grounded in published medical literature. Ask anything — symptoms, treatments, conditions, or risk factors.</div>
    <div class="badge-row">
        <span class="tbadge">MiniLM-L6-v2</span>
        <span class="tbadge">FAISS</span>
        <span class="tbadge">Llama 3.1</span>
        <span class="tbadge">Groq API</span>
        <span class="tbadge">RAG Pipeline</span>
    </div>
</div>
<div class="kpi-row fade f3">
    <div class="kpi"><div class="kpi-label">Source pages</div><div class="kpi-value">759</div><div class="kpi-sub">Gale Encyclopedia</div></div>
    <div class="kpi"><div class="kpi-label">Indexed passages</div><div class="kpi-value">7,470</div><div class="kpi-sub">512-char chunks</div></div>
    <div class="kpi"><div class="kpi-label">Avg response</div><div class="kpi-value kpi-accent">&lt;2s</div><div class="kpi-sub">End-to-end latency</div></div>
    <div class="kpi"><div class="kpi-label">Embedding dim</div><div class="kpi-value">384</div><div class="kpi-sub">Cosine similarity</div></div>
</div>
<div class="fc-grid fade f4">
    <div class="fc"><div class="fc-num">01</div><div class="fc-title">Medical Query</div><div class="fc-desc">Ask any health question. Personalised with your vitals — BMI, blood pressure, glucose.</div></div>
    <div class="fc"><div class="fc-num">02</div><div class="fc-title">Performance Metrics</div><div class="fc-desc">Live dashboard of retrieval accuracy, latency, and relevance scores. Resume-ready.</div></div>
    <div class="fc"><div class="fc-num">03</div><div class="fc-title">Source Passages</div><div class="fc-desc">Every answer is traceable — see the exact encyclopedia passages that informed it.</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="sec-hdr"><div class="sec-title">Quick access</div><div class="sec-line"></div></div>', unsafe_allow_html=True)
samples = ["Symptoms of Type 2 Diabetes","Hypertension diagnosis & treatment","Asthma triggers and management","Alzheimer's disease stages","Heart disease risk factors","Kidney stone prevention"]
cols = st.columns(3)
for i,q in enumerate(samples):
    with cols[i%3]:
        if st.button(q, key=f"hq{i}", use_container_width=True):
            st.session_state["prefill_query"]=q
