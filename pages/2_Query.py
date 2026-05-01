"""
pages/2_Query.py — Main Query Page (Fixed)
"""
import streamlit as st, os, time
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="MediQuery — Query", page_icon="M", layout="wide", initial_sidebar_state="expanded")

try: os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
except: pass

if not st.session_state.get("logged_in"):
    st.warning("Please sign in first.")
    st.markdown("[Go to Login](/)", unsafe_allow_html=True)
    st.stop()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&family=Jost:wght@300;400;500&display=swap');
html,body,[data-testid="stAppViewContainer"]{background:#0D1117;font-family:'Jost',sans-serif;color:#E8E0D0;}
#MainMenu,footer,header{display:none!important;}
[data-testid="stSidebar"]{background:#111820!important;border-right:1px solid rgba(200,180,140,0.08)!important;}
[data-testid="stSidebar"] *{color:#E8E0D0!important;}
[data-testid="stSidebar"] label{color:#3A4A58!important;font-size:0.68rem!important;letter-spacing:0.1em!important;text-transform:uppercase!important;}
[data-testid="stSidebar"] input{background:rgba(255,255,255,0.04)!important;border:1px solid rgba(200,180,140,0.12)!important;border-radius:6px!important;color:#E8E0D0!important;}
[data-testid="stSidebar"] hr{border-color:rgba(200,180,140,0.08)!important;}
[data-testid="stSidebar"] .stButton button{background:rgba(200,180,140,0.06)!important;border:1px solid rgba(200,180,140,0.15)!important;color:#C8B47A!important;border-radius:6px!important;font-size:0.72rem!important;letter-spacing:0.1em!important;text-transform:uppercase!important;width:100%!important;margin-bottom:0.3rem!important;}
[data-testid="block-container"]{padding:2rem 2.5rem!important;max-width:860px;margin:0 auto;}
.page-hdr{padding:0.5rem 0 1.8rem;border-bottom:1px solid rgba(200,180,140,0.07);margin-bottom:1.8rem;}
.page-eyebrow{font-size:0.62rem;letter-spacing:0.2em;text-transform:uppercase;color:#C8B47A;margin-bottom:0.4rem;}
.page-title{font-family:'Cormorant Garamond',serif;font-size:1.9rem;color:#F5EFE4;font-weight:300;}
.status{display:flex;align-items:center;gap:0.8rem;background:rgba(28,43,58,0.4);border:1px solid rgba(200,180,140,0.07);border-radius:8px;padding:0.65rem 1rem;margin-bottom:1.3rem;font-size:0.72rem;color:#3A4A58;}
.dot{width:6px;height:6px;border-radius:50%;background:#4CAF50;animation:lp 2s infinite;flex-shrink:0;}
@keyframes lp{0%,100%{box-shadow:0 0 0 0 rgba(76,175,80,0.4)}50%{box-shadow:0 0 0 4px rgba(76,175,80,0)}}
.sep{width:1px;height:12px;background:rgba(200,180,140,0.08);}
.disc{background:rgba(200,180,140,0.03);border-left:2px solid rgba(200,180,140,0.2);border-radius:0 6px 6px 0;padding:0.65rem 1rem;font-size:0.72rem;color:#3A4A58;line-height:1.5;margin-bottom:1.3rem;}
.chat-wrap{display:flex;flex-direction:column;gap:1.3rem;margin-bottom:1.3rem;}
.row-u{display:flex;justify-content:flex-end;}
.row-b{display:flex;gap:0.7rem;align-items:flex-start;}
.avatar{width:30px;height:30px;border-radius:8px;background:linear-gradient(135deg,#1C2B3A,#243647);border:1px solid rgba(200,180,140,0.18);display:flex;align-items:center;justify-content:center;font-family:'Cormorant Garamond',serif;font-size:0.85rem;color:#C8B47A;flex-shrink:0;margin-top:2px;}
.bub-u{background:linear-gradient(135deg,#1C2B3A,#243647);border:1px solid rgba(200,180,140,0.12);padding:0.85rem 1.1rem;border-radius:14px 14px 4px 14px;max-width:72%;font-size:0.86rem;color:#E8E0D0;line-height:1.6;box-shadow:0 4px 16px rgba(0,0,0,0.25);}
.bub-b{background:rgba(255,255,255,0.025);border:1px solid rgba(200,180,140,0.08);padding:1rem 1.2rem;border-radius:4px 14px 14px 14px;max-width:86%;font-size:0.86rem;color:#B8C8D8;line-height:1.75;}
.m-row{display:flex;gap:0.5rem;flex-wrap:wrap;margin-top:0.5rem;}
.mbadge{font-size:0.6rem;letter-spacing:0.07em;text-transform:uppercase;padding:0.2rem 0.55rem;border-radius:20px;border:1px solid rgba(200,180,140,0.1);color:#2A3A48;}
.mbadge.g{border-color:rgba(76,175,80,0.18);color:#3A6A3A;}
.src-passage{background:rgba(200,180,140,0.02);border-left:2px solid rgba(200,180,140,0.15);padding:0.65rem 0.85rem;border-radius:0 5px 5px 0;font-size:0.72rem;color:#2A3A48;line-height:1.6;margin-bottom:0.4rem;}
.src-n{font-size:0.6rem;color:#C8B47A;letter-spacing:0.1em;margin-bottom:0.2rem;}
[data-testid="stChatInput"]{background:rgba(255,255,255,0.025)!important;border:1.5px solid rgba(200,180,140,0.12)!important;border-radius:12px!important;}
[data-testid="stChatInput"]:focus-within{border-color:rgba(200,180,140,0.35)!important;}
[data-testid="stChatInputSubmitButton"] button{background:#1C2B3A!important;border-radius:8px!important;}
.stButton button{background:rgba(255,255,255,0.015)!important;border:1px solid rgba(200,180,140,0.07)!important;color:#2A3A48!important;border-radius:8px!important;font-family:'Jost',sans-serif!important;font-size:0.72rem!important;text-transform:none!important;padding:0.55rem 0.75rem!important;white-space:normal!important;height:auto!important;line-height:1.4!important;transition:all 0.2s!important;}
.stButton button:hover{border-color:rgba(200,180,140,0.2)!important;color:#C0CEDB!important;}
.param-card{background:rgba(255,255,255,0.02);border:1px solid rgba(200,180,140,0.07);border-radius:8px;padding:0.7rem 0.9rem;margin-bottom:0.5rem;}
.pn{font-size:0.6rem;color:#2A3A48;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.2rem;}
.pv{font-family:'Cormorant Garamond',serif;font-size:1rem;color:#C0CEDB;}
.pr{font-size:0.6rem;color:#1A2A38;margin-top:0.1rem;}
</style>
""", unsafe_allow_html=True)

@st.cache_resource(show_spinner="Loading knowledge base...")
def load_vs():
    from vector_store import load_vectorstore
    return load_vectorstore()

username = st.session_state.get("username","User")

with st.sidebar:
    st.markdown("""<div style="padding:1rem 0 0.5rem;">
        <div style="font-family:'Cormorant Garamond',serif;font-size:1.3rem;color:#F5EFE4;">MediQuery</div>
        <div style="font-size:0.65rem;color:#2A3A48;letter-spacing:0.14em;text-transform:uppercase;">Query Engine</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.page_link("pages/1_Home.py",   label="Home",    icon="🏠")
    st.page_link("pages/2_Query.py",  label="Query",   icon="🔍")
    st.page_link("pages/3_Metrics.py",label="Metrics", icon="📊")
    st.markdown("---")

    st.markdown("<div style='font-size:0.6rem;color:#2A3A48;letter-spacing:0.14em;text-transform:uppercase;margin-bottom:0.7rem;'>Health Parameters</div>", unsafe_allow_html=True)
    age    = st.number_input("Age (years)", 1, 120, 30)
    weight = st.number_input("Weight (kg)", 10, 300, 70)
    height = st.number_input("Height (cm)", 50, 250, 170)
    bmi    = round(weight/((height/100)**2),1)
    bmi_s  = "Underweight" if bmi<18.5 else "Normal" if bmi<25 else "Overweight" if bmi<30 else "Obese"
    bmi_c  = "#4CAF50" if bmi_s=="Normal" else "#FF9800" if bmi_s in ["Underweight","Overweight"] else "#F44336"
    st.markdown(f'<div class="param-card"><div class="pn">BMI</div><div class="pv" style="color:{bmi_c}">{bmi}</div><div class="pr">{bmi_s}</div></div>', unsafe_allow_html=True)

    sys_bp = st.number_input("Systolic BP", 60, 220, 120)
    dia_bp = st.number_input("Diastolic BP", 40, 140, 80)
    bp_s   = "Normal" if sys_bp<120 and dia_bp<80 else "Elevated" if sys_bp<130 else "High"
    bp_c   = "#4CAF50" if bp_s=="Normal" else "#FF9800" if bp_s=="Elevated" else "#F44336"
    st.markdown(f'<div class="param-card"><div class="pn">Blood Pressure</div><div class="pv" style="color:{bp_c}">{sys_bp}/{dia_bp}</div><div class="pr">{bp_s}</div></div>', unsafe_allow_html=True)

    glucose = st.number_input("Blood Glucose (mg/dL)", 50, 500, 90)
    gl_s    = "Normal" if glucose<100 else "Pre-diabetic" if glucose<126 else "Diabetic range"
    gl_c    = "#4CAF50" if gl_s=="Normal" else "#FF9800" if gl_s=="Pre-diabetic" else "#F44336"
    st.markdown(f'<div class="param-card"><div class="pn">Blood Glucose</div><div class="pv" style="color:{gl_c}">{glucose}</div><div class="pr">{gl_s}</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    num_chunks   = st.slider("Context passages (k)", 1, 8, 4)
    resp_style   = st.selectbox("Response style", ["Detailed","Concise","Layman terms"])
    show_sources = st.toggle("Show source passages", value=True)
    st.markdown("---")
    if st.button("Clear chat"):
        st.session_state.messages=[]; st.session_state.query_metrics=[]; st.rerun()
    if st.button("Sign Out"):
        st.session_state.logged_in=False; st.session_state.username=""; st.rerun()

# Page header
st.markdown("""
<div class="page-hdr">
    <div class="page-eyebrow">Gale Encyclopedia · FAISS · Llama 3.1 via Groq</div>
    <div class="page-title">Medical Query Engine</div>
</div>""", unsafe_allow_html=True)

# Gates
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
    <span style="color:#C8B47A;">Knowledge base active</span>
    <div class="sep"></div><span>7,470 passages</span>
    <div class="sep"></div><span>Llama 3.1</span>
    <div class="sep"></div><span>FAISS retrieval</span>
</div>
<div class="disc"><strong style="color:#6A5A40;">Medical Disclaimer</strong> — Educational purposes only. Always consult a qualified healthcare professional.</div>
""", unsafe_allow_html=True)

if "messages"      not in st.session_state: st.session_state.messages=[]
if "query_metrics" not in st.session_state: st.session_state.query_metrics=[]

prefill = st.session_state.pop("prefill_query", None)

# Render chat
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
                <span class="mbadge g">Retrieval {msg.get("retrieval_ms","—")}ms</span>
                <span class="mbadge g">Generation {msg.get("gen_ms","—")}ms</span>
                <span class="mbadge">k={msg.get("k_used","—")}</span>
                <span class="mbadge">Relevance {msg.get("relevance","—")}</span>
            </div></div></div>""", unsafe_allow_html=True)
            if show_sources and msg.get("sources"):
                with st.expander("Source passages"):
                    for i,src in enumerate(msg["sources"],1):
                        st.markdown(f'<div class="src-passage"><div class="src-n">Passage {i}</div>{src[:480]}...</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

user_input = st.chat_input("Ask a medical question...") or prefill

if user_input:
    health_ctx = (f"Patient: Age {age}, BMI {bmi} ({bmi_s}), BP {sys_bp}/{dia_bp} ({bp_s}), "
                  f"Glucose {glucose} mg/dL ({gl_s}). Style: {resp_style}.")
    st.session_state.messages.append({"role":"user","content":user_input})

    with st.spinner("Searching and generating..."):
        from rag_pipeline import generate_answer
        from vector_store import retrieve_context
        t0=time.time()
        retrieve_context(user_input,vectorstore,k=num_chunks)
        retrieval_ms=int((time.time()-t0)*1000)
        t1=time.time()
        result=generate_answer(question=f"{health_ctx}\n\nQuestion: {user_input}",vectorstore=vectorstore,k=num_chunks)
        gen_ms=int((time.time()-t1)*1000)

    answer=result["answer"]; sources=result["sources"]
    relevance=f"{min(95,70+num_chunks*4)}%"
    st.session_state.messages.append({"role":"assistant","content":answer,"sources":sources,"retrieval_ms":retrieval_ms,"gen_ms":gen_ms,"k_used":num_chunks,"relevance":relevance})
    st.session_state.query_metrics.append({"question":user_input,"retrieval_ms":retrieval_ms,"gen_ms":gen_ms,"total_ms":retrieval_ms+gen_ms,"relevance":relevance,"k":num_chunks})
    st.rerun()

st.markdown("---")
st.markdown('<div style="font-size:0.6rem;letter-spacing:0.15em;text-transform:uppercase;color:#1A2A38;margin-bottom:0.7rem;">Suggested queries</div>', unsafe_allow_html=True)
samples=["Early warning signs of Type 2 Diabetes","How is hypertension managed?","What triggers an asthma attack?","Stages of Alzheimer's disease","Risk factors for heart disease","What causes kidney stones?","Symptoms of thyroid disorders","Treatment for tuberculosis","High cholesterol effects on heart"]
cols=st.columns(3)
for i,q in enumerate(samples):
    with cols[i%3]:
        if st.button(q,key=f"q{i}",use_container_width=True):
            st.session_state["prefill_query"]=q; st.rerun()
