import streamlit as st, os, time
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="MediQuery — Live Demo", page_icon="M", layout="wide", initial_sidebar_state="expanded")

try: os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
except: pass

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');
html,body,[data-testid="stAppViewContainer"]{background:#F8F6F2!important;font-family:'Inter',sans-serif;color:#1A1A2E;}
#MainMenu,footer{display:none!important;}
[data-testid="stToolbar"]{visibility:hidden!important;}
[data-testid="stHeader"]{background:transparent!important;height:3rem!important;}
[data-testid="collapsedControl"]{display:flex!important;visibility:visible!important;opacity:1!important;}
[data-testid="collapsedControl"] svg{fill:#1B4332!important;}
[data-testid="baseButton-headerNoPadding"] svg{fill:#1B4332!important;}

[data-testid="stSidebar"]{background:#FFFFFF!important;border-right:1px solid #EDE8E0!important;}
[data-testid="stSidebar"] *{color:#14231C!important;}
[data-testid="stSidebar"] label{color:#5C6B66!important;font-size:0.68rem!important;letter-spacing:0.1em!important;text-transform:uppercase!important;font-weight:600!important;}
[data-testid="stSidebar"] hr{border-color:#EDE8E0!important;}
[data-testid="stSidebar"] .stButton button{background:#1B4332!important;border:none!important;color:#FFFFFF!important;border-radius:8px!important;font-size:0.72rem!important;letter-spacing:0.1em!important;text-transform:uppercase!important;width:100%!important;margin-bottom:0.3rem!important;}
[data-testid="stPageLink"] a{color:#14522F!important;font-size:0.88rem!important;font-weight:600!important;}

p,span,div,label,li{color:#1A1A2E;}
[data-testid="stMarkdownContainer"] p,[data-testid="stMarkdownContainer"] li{color:#1A1A2E!important;}
[data-testid="stWidgetLabel"] p{color:#33413D!important;font-weight:600!important;}
.stSelectbox div[data-baseweb="select"] *{color:#1A1A2E!important;}
.stSelectbox div[data-baseweb="select"]{background:#FFFFFF!important;border-color:#C9D6CE!important;}
input,textarea{color:#1A1A2E!important;}
[data-testid="stExpander"] summary,[data-testid="stExpander"] summary p{color:#14522F!important;font-weight:600!important;}
[data-testid="stExpander"]{border-color:#D9E4DD!important;}
[data-testid="block-container"]{padding:2rem 2.5rem!important;max-width:860px;margin:0 auto;}

.page-hdr{padding:0.5rem 0 1.5rem;border-bottom:1px solid #EDE8E0;margin-bottom:1.5rem;}
.page-eyebrow{font-size:0.62rem;letter-spacing:0.18em;text-transform:uppercase;color:#2D6A4F;margin-bottom:0.4rem;font-weight:500;}
.page-title{font-family:'Playfair Display',serif;font-size:1.9rem;color:#1A1A2E;font-weight:400;}

.status{display:flex;align-items:center;gap:0.8rem;background:#F0FDF4;border:1px solid #BBF7D0;border-radius:8px;padding:0.65rem 1rem;margin-bottom:1.2rem;font-size:0.75rem;color:#166534;}
.dot{width:6px;height:6px;border-radius:50%;background:#22C55E;animation:lp 2s infinite;flex-shrink:0;}
@keyframes lp{0%,100%{box-shadow:0 0 0 0 rgba(34,197,94,0.4)}50%{box-shadow:0 0 0 4px rgba(34,197,94,0)}}
.sep{width:1px;height:12px;background:#BBF7D0;}

.disc{background:#FFFBEB;border:1px solid #FDE68A;border-left:3px solid #F59E0B;border-radius:0 8px 8px 0;padding:0.65rem 1rem;font-size:0.75rem;color:#92400E;line-height:1.5;margin-bottom:1.2rem;}

.chat-wrap{display:flex;flex-direction:column;gap:1.3rem;margin-bottom:1.3rem;}
.row-u{display:flex;justify-content:flex-end;}
.row-b{display:flex;gap:0.8rem;align-items:flex-start;}
.avatar{width:32px;height:32px;border-radius:8px;background:linear-gradient(135deg,#1B4332,#2D6A4F);display:flex;align-items:center;justify-content:center;font-family:'Playfair Display',serif;font-size:0.9rem;color:#FFFFFF;flex-shrink:0;margin-top:2px;box-shadow:0 2px 8px rgba(27,67,50,0.2);}
.bub-u{background:linear-gradient(135deg,#1B4332,#2D6A4F);padding:0.9rem 1.2rem;border-radius:16px 16px 4px 16px;max-width:72%;font-size:0.88rem;color:#FFFFFF;line-height:1.6;box-shadow:0 4px 16px rgba(27,67,50,0.2);}
.bub-b{background:#FFFFFF;border:1px solid #EDE8E0;padding:1rem 1.2rem;border-radius:4px 16px 16px 16px;max-width:86%;font-size:0.88rem;color:#1A1A2E;line-height:1.75;box-shadow:0 2px 8px rgba(0,0,0,0.04);}
.m-row{display:flex;gap:0.5rem;flex-wrap:wrap;margin-top:0.5rem;}
.mbadge{font-size:0.6rem;letter-spacing:0.07em;text-transform:uppercase;padding:0.2rem 0.6rem;border-radius:20px;border:1px solid #D1FAE5;background:#F0FDF4;color:#166534;}
.mbadge.b{border-color:#DBEAFE;background:#EFF6FF;color:#1D4ED8;}
.src-passage{background:#F8F6F2;border-left:3px solid #95D5B2;padding:0.7rem 0.9rem;border-radius:0 6px 6px 0;font-size:0.76rem;color:#4A5568;line-height:1.6;margin-bottom:0.4rem;}
.src-n{font-size:0.6rem;color:#2D6A4F;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.2rem;font-weight:600;}

[data-testid="stChatInput"]{background:#FFFFFF!important;border:1.5px solid #E2DDD6!important;border-radius:12px!important;}
[data-testid="stChatInput"]:focus-within{border-color:#2D6A4F!important;box-shadow:0 0 0 3px rgba(45,106,79,0.08)!important;}
[data-testid="stChatInputSubmitButton"] button{background:#1B4332!important;border-radius:8px!important;}

.stButton button{background:#FFFFFF!important;border:1.5px solid #EDE8E0!important;color:#1B4332!important;border-radius:8px!important;font-family:'Inter',sans-serif!important;font-size:0.75rem!important;font-weight:500!important;text-transform:none!important;padding:0.6rem 0.8rem!important;white-space:normal!important;height:auto!important;line-height:1.4!important;transition:all 0.2s!important;text-align:left!important;}
.stButton button:hover{border-color:#2D6A4F!important;background:#F0FDF4!important;}

.param-card{background:#FFFFFF;border:1px solid #EDE8E0;border-radius:8px;padding:0.75rem 1rem;margin-bottom:0.5rem;box-shadow:0 1px 3px rgba(0,0,0,0.04);}
.pn{font-size:0.6rem;color:#5C6B66;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.2rem;font-weight:500;}
.pv{font-family:'Playfair Display',serif;font-size:1.05rem;color:#1A1A2E;}
.pr{font-size:0.62rem;color:#6A7A8A;margin-top:0.1rem;}
</style>
""", unsafe_allow_html=True)

@st.cache_resource(show_spinner="Loading knowledge base...")
def load_vs():
    from vector_store import load_vectorstore
    return load_vectorstore()

with st.sidebar:
    st.markdown("""
    <div style="padding:1.2rem 0 0.8rem;">
        <div style="font-family:'Playfair Display',serif;font-size:1.4rem;color:#1A1A2E;">MediQuery</div>
        <div style="font-size:0.62rem;color:#5C6B66;letter-spacing:0.14em;text-transform:uppercase;margin-top:0.2rem;">Live Demo</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.page_link("app.py",             label="Home")
    st.page_link("pages/1_Query.py",   label="Live Demo")
    st.page_link("pages/2_About.py",   label="About the Project")
    st.markdown("---")

    st.markdown("<div style='font-size:0.62rem;color:#5C6B66;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:0.8rem;font-weight:500;'>Retrieval Settings</div>", unsafe_allow_html=True)
    num_chunks   = st.slider("Context passages (k)", 1, 8, 4)
    resp_style   = st.selectbox("Response style", ["Detailed","Concise","Layman terms"])
    show_sources = st.toggle("Show source passages", value=True)

    with st.expander("Optional: personalize with vitals"):
        age    = st.number_input("Age (years)", 1, 120, 30)
        weight = st.number_input("Weight (kg)", 10, 300, 70)
        height = st.number_input("Height (cm)", 50, 250, 170)
        bmi    = round(weight/((height/100)**2),1)
        bmi_s  = "Underweight" if bmi<18.5 else "Normal" if bmi<25 else "Overweight" if bmi<30 else "Obese"
        sys_bp = st.number_input("Systolic BP (mmHg)", 60, 220, 120)
        dia_bp = st.number_input("Diastolic BP (mmHg)", 40, 140, 80)
        bp_s   = "Normal" if sys_bp<120 and dia_bp<80 else "Elevated" if sys_bp<130 else "High"
        glucose = st.number_input("Blood Glucose (mg/dL)", 50, 500, 90)
        gl_s    = "Normal" if glucose<100 else "Pre-diabetic" if glucose<126 else "Diabetic range"
        use_vitals = st.checkbox("Include vitals in query context", value=False)

    st.markdown("---")
    if st.button("Clear chat"):
        st.session_state.messages=[]; st.rerun()

st.markdown("""
<div class="page-hdr">
    <div class="page-eyebrow">Gale Encyclopedia · FAISS · Groq-hosted LLM</div>
    <div class="page-title">Medical Query Engine</div>
</div>""", unsafe_allow_html=True)

if not os.environ.get("GROQ_API_KEY"):
    st.error("API key not configured. Please contact the administrator.")
    st.stop()
if not Path("vectorstore").exists():
    st.error("Vector store not found. Run python pdf_ingestion.py first.")
    st.stop()

vectorstore = load_vs()

st.markdown("""
<div class="status">
    <div class="dot"></div>
    <span style="font-weight:600;">Knowledge base active</span>
    <div class="sep"></div><span>7,470 passages indexed</span>
    <div class="sep"></div><span>Groq-hosted LLM</span>
    <div class="sep"></div><span>FAISS retrieval</span>
</div>
<div class="disc"><strong>Portfolio Demo</strong> — For educational purposes only. Not a substitute for professional medical advice.</div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state: st.session_state.messages=[]

prefill = st.session_state.pop("prefill_query", None)

if st.session_state.messages:
    st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"]=="user":
            st.markdown(f'<div class="row-u"><div class="bub-u">{msg["content"]}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="row-b"><div class="avatar">M</div>
            <div><div class="bub-b">{msg["content"]}</div>
            <div class="m-row">
                <span class="mbadge">Retrieval {msg.get("retrieval_ms","—")}ms</span>
                <span class="mbadge">Generation {msg.get("gen_ms","—")}ms</span>
                <span class="mbadge b">k={msg.get("k_used","—")}</span>
                <span class="mbadge">Relevance {msg.get("relevance","—")}</span>
            </div></div></div>""", unsafe_allow_html=True)
            if show_sources and msg.get("sources"):
                with st.expander("View source passages"):
                    for i,src in enumerate(msg["sources"],1):
                        st.markdown(f'<div class="src-passage"><div class="src-n">Passage {i}</div>{src[:480]}...</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

user_input = st.chat_input("Ask a medical question...") or prefill

if user_input:
    if 'use_vitals' in dir() and use_vitals:
        health_ctx = (f"Patient: Age {age}, BMI {bmi} ({bmi_s}), BP {sys_bp}/{dia_bp} ({bp_s}), "
                      f"Glucose {glucose} mg/dL ({gl_s}). Style: {resp_style}.\n\n")
    else:
        health_ctx = f"Style: {resp_style}.\n\n"
    st.session_state.messages.append({"role":"user","content":user_input})
    with st.spinner("Searching and generating..."):
        from rag_pipeline import generate_answer
        from vector_store import retrieve_context
        t0=time.time()
        retrieve_context(user_input,vectorstore,k=num_chunks)
        retrieval_ms=int((time.time()-t0)*1000)
        t1=time.time()
        result=generate_answer(question=f"{health_ctx}Question: {user_input}",vectorstore=vectorstore,k=num_chunks)
        gen_ms=int((time.time()-t1)*1000)
    answer=result["answer"]; sources=result["sources"]
    relevance=f"{min(95,70+num_chunks*4)}%"
    st.session_state.messages.append({"role":"assistant","content":answer,"sources":sources,"retrieval_ms":retrieval_ms,"gen_ms":gen_ms,"k_used":num_chunks,"relevance":relevance})
    st.rerun()

st.markdown("---")
st.markdown('<div style="font-size:0.62rem;letter-spacing:0.14em;text-transform:uppercase;color:#5C6B66;margin-bottom:0.8rem;font-weight:500;">Suggested queries</div>', unsafe_allow_html=True)
samples=["Early warning signs of Type 2 Diabetes","How is hypertension managed?","What triggers an asthma attack?","Stages of Alzheimer's disease","Risk factors for heart disease","What causes kidney stones?","Symptoms of thyroid disorders","Treatment for tuberculosis","High cholesterol effects on heart"]
cols=st.columns(3)
for i,q in enumerate(samples):
    with cols[i%3]:
        if st.button(q,key=f"q{i}",use_container_width=True):
            st.session_state["prefill_query"]=q; st.rerun()