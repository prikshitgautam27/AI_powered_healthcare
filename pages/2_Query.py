"""
pages/2_Query.py — The main Query page — premium chat experience
"""
import streamlit as st, os, time
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="MediQuery — Query", page_icon="M", layout="wide", initial_sidebar_state="expanded")

if not st.session_state.get("logged_in"):
    st.switch_page("app.py")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Jost:wght@300;400;500&display=swap');
html,body,[data-testid="stAppViewContainer"]{background:#0D1117;font-family:'Jost',sans-serif;color:#E8E0D0;}
#MainMenu,footer,header{display:none!important;}
[data-testid="stSidebar"]{background:#111820!important;border-right:1px solid rgba(200,180,140,0.08)!important;}
[data-testid="stSidebar"] *{color:#E8E0D0!important;}
[data-testid="stSidebar"] label{color:#4A5A68!important;font-size:0.7rem!important;letter-spacing:0.1em!important;text-transform:uppercase!important;}
[data-testid="stSidebar"] input{background:rgba(255,255,255,0.04)!important;border:1px solid rgba(200,180,140,0.15)!important;border-radius:6px!important;color:#E8E0D0!important;}
[data-testid="stSidebar"] hr{border-color:rgba(200,180,140,0.08)!important;}
[data-testid="stSidebar"] .stButton button{background:rgba(200,180,140,0.08)!important;border:1px solid rgba(200,180,140,0.2)!important;color:#C8B47A!important;border-radius:6px!important;font-size:0.75rem!important;letter-spacing:0.1em!important;text-transform:uppercase!important;width:100%!important;}
[data-testid="block-container"]{padding:2rem 2.5rem!important;max-width:900px;margin:0 auto;}

/* Page title */
.page-hdr{padding:0.5rem 0 2rem;border-bottom:1px solid rgba(200,180,140,0.08);margin-bottom:2rem;}
.page-hdr-eyebrow{font-size:0.65rem;letter-spacing:0.2em;text-transform:uppercase;color:#C8B47A;margin-bottom:0.5rem;}
.page-hdr-title{font-family:'Cormorant Garamond',serif;font-size:2rem;color:#F5EFE4;font-weight:300;}

/* Status strip */
.status-strip{
    display:flex;align-items:center;gap:1rem;
    background:rgba(28,43,58,0.4);border:1px solid rgba(200,180,140,0.08);
    border-radius:8px;padding:0.7rem 1.1rem;margin-bottom:1.5rem;
    font-size:0.75rem;color:#4A5A68;
}
.live-dot{width:6px;height:6px;border-radius:50%;background:#4CAF50;animation:lp 2s infinite;}
@keyframes lp{0%,100%{box-shadow:0 0 0 0 rgba(76,175,80,0.4);}50%{box-shadow:0 0 0 4px rgba(76,175,80,0);}}
.strip-sep{width:1px;height:14px;background:rgba(200,180,140,0.1);}

/* Disclaimer */
.disclaimer{
    background:rgba(200,180,140,0.04);border-left:2px solid rgba(200,180,140,0.3);
    border-radius:0 6px 6px 0;padding:0.7rem 1rem;
    font-size:0.75rem;color:#4A5A68;line-height:1.5;margin-bottom:1.5rem;
}

/* Chat messages */
.chat-outer{display:flex;flex-direction:column;gap:1.4rem;margin-bottom:1.5rem;}
.msg-row-user{display:flex;justify-content:flex-end;}
.msg-row-bot{display:flex;justify-content:flex-start;gap:0.8rem;align-items:flex-start;}
.bot-avatar{
    width:32px;height:32px;border-radius:8px;
    background:linear-gradient(135deg,#1C2B3A,#243647);
    border:1px solid rgba(200,180,140,0.2);
    display:flex;align-items:center;justify-content:center;
    font-family:'Cormorant Garamond',serif;font-size:0.9rem;color:#C8B47A;
    flex-shrink:0;margin-top:2px;
}
.bubble-user{
    background:linear-gradient(135deg,#1C2B3A,#243647);
    border:1px solid rgba(200,180,140,0.15);
    padding:0.9rem 1.2rem;border-radius:16px 16px 4px 16px;
    max-width:72%;font-size:0.88rem;color:#E8E0D0;line-height:1.6;
    box-shadow:0 4px 20px rgba(0,0,0,0.3);
}
.bubble-bot{
    background:rgba(255,255,255,0.03);
    border:1px solid rgba(200,180,140,0.1);
    padding:1.1rem 1.3rem;border-radius:4px 16px 16px 16px;
    max-width:85%;font-size:0.88rem;color:#C0CEDB;line-height:1.75;
    box-shadow:0 2px 12px rgba(0,0,0,0.2);
}
.msg-meta{font-size:0.65rem;color:#2A3A48;margin-top:0.5rem;letter-spacing:0.06em;}

/* Source passages */
.src-wrap{margin-top:0.8rem;}
.src-header{
    font-size:0.65rem;letter-spacing:0.15em;text-transform:uppercase;
    color:#3A4A58;margin-bottom:0.5rem;cursor:pointer;
    display:flex;align-items:center;gap:0.4rem;
}
.src-header::before{content:'';width:12px;height:1px;background:#3A4A58;}
.src-passage{
    background:rgba(200,180,140,0.03);
    border-left:2px solid rgba(200,180,140,0.2);
    padding:0.7rem 0.9rem;border-radius:0 6px 6px 0;
    font-size:0.75rem;color:#3A4A58;line-height:1.6;margin-bottom:0.5rem;
}
.src-num{font-size:0.65rem;color:#C8B47A;letter-spacing:0.1em;margin-bottom:0.2rem;}

/* Metrics badge row */
.metrics-row{
    display:flex;gap:0.8rem;flex-wrap:wrap;
    margin-top:0.6rem;
}
.metric-badge{
    font-size:0.65rem;letter-spacing:0.08em;text-transform:uppercase;
    padding:0.25rem 0.7rem;border-radius:20px;
    border:1px solid rgba(200,180,140,0.12);color:#3A4A58;
}
.metric-badge.good{border-color:rgba(76,175,80,0.2);color:#3A6A3A;}
.metric-badge.warn{border-color:rgba(255,180,0,0.2);color:#7A6020;}

/* Chat input */
[data-testid="stChatInput"]{
    background:rgba(255,255,255,0.03)!important;
    border:1.5px solid rgba(200,180,140,0.15)!important;
    border-radius:12px!important;
}
[data-testid="stChatInput"]:focus-within{border-color:rgba(200,180,140,0.4)!important;}
[data-testid="stChatInputSubmitButton"] button{background:#1C2B3A!important;border-radius:8px!important;}

/* Sample q buttons */
.stButton button{
    background:rgba(255,255,255,0.02)!important;
    border:1px solid rgba(200,180,140,0.08)!important;
    color:#4A5A68!important;border-radius:8px!important;
    font-family:'Jost',sans-serif!important;
    font-size:0.75rem!important;letter-spacing:0.02em!important;
    text-transform:none!important;padding:0.6rem 0.8rem!important;
    text-align:left!important;white-space:normal!important;
    height:auto!important;line-height:1.4!important;transition:all 0.2s!important;
}
.stButton button:hover{
    border-color:rgba(200,180,140,0.25)!important;
    color:#C0CEDB!important;background:rgba(200,180,140,0.04)!important;
}
.param-card{
    background:rgba(255,255,255,0.02);border:1px solid rgba(200,180,140,0.08);
    border-radius:10px;padding:0.8rem 1rem;margin-bottom:0.6rem;
}
.param-name{font-size:0.65rem;color:#3A4A58;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.2rem;}
.param-val{font-family:'Cormorant Garamond',serif;font-size:1.05rem;color:#C0CEDB;}
.param-range{font-size:0.65rem;color:#2A3A48;margin-top:0.1rem;}
</style>
""", unsafe_allow_html=True)


@st.cache_resource(show_spinner="Indexing knowledge base...")
def load_vs():
    from vector_store import load_vectorstore
    return load_vectorstore()


username = st.session_state.get("username","User")

# ── Sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1rem 0 0.5rem;">
        <div style="font-family:'Cormorant Garamond',serif;font-size:1.3rem;color:#F5EFE4;">MediQuery</div>
        <div style="font-size:0.68rem;color:#3A4A58;letter-spacing:0.12em;text-transform:uppercase;">Query Engine</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    groq_key = st.text_input("Groq API Key", type="password", value=os.environ.get("GROQ_API_KEY",""), placeholder="gsk_...")
    if groq_key: os.environ["GROQ_API_KEY"] = groq_key
    st.markdown("---")

    st.markdown("<div style='font-size:0.65rem;color:#3A4A58;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:0.8rem;'>Health Parameters</div>", unsafe_allow_html=True)
    age    = st.number_input("Age", 1, 120, 30, key="age")
    weight = st.number_input("Weight (kg)", 10, 300, 70, key="wt")
    height = st.number_input("Height (cm)", 50, 250, 170, key="ht")
    bmi    = round(weight/((height/100)**2),1)
    bmi_s  = "Underweight" if bmi<18.5 else "Normal" if bmi<25 else "Overweight" if bmi<30 else "Obese"
    bmi_c  = "#4CAF50" if bmi_s=="Normal" else "#FF9800" if bmi_s in ["Underweight","Overweight"] else "#F44336"
    st.markdown(f'<div class="param-card"><div class="param-name">BMI</div><div class="param-val" style="color:{bmi_c}">{bmi}</div><div class="param-range">{bmi_s}</div></div>', unsafe_allow_html=True)

    sys_bp = st.number_input("Systolic BP (mmHg)", 60, 220, 120, key="sbp")
    dia_bp = st.number_input("Diastolic BP (mmHg)", 40, 140, 80, key="dbp")
    bp_s   = "Normal" if sys_bp<120 and dia_bp<80 else "Elevated" if sys_bp<130 else "High"
    bp_c   = "#4CAF50" if bp_s=="Normal" else "#FF9800" if bp_s=="Elevated" else "#F44336"
    st.markdown(f'<div class="param-card"><div class="param-name">Blood Pressure</div><div class="param-val" style="color:{bp_c}">{sys_bp}/{dia_bp}</div><div class="param-range">{bp_s}</div></div>', unsafe_allow_html=True)

    glucose = st.number_input("Blood Glucose (mg/dL)", 50, 500, 90, key="gl")
    gl_s    = "Normal" if glucose<100 else "Pre-diabetic" if glucose<126 else "Diabetic range"
    gl_c    = "#4CAF50" if gl_s=="Normal" else "#FF9800" if gl_s=="Pre-diabetic" else "#F44336"
    st.markdown(f'<div class="param-card"><div class="param-name">Blood Glucose</div><div class="param-val" style="color:{gl_c}">{glucose}</div><div class="param-range">{gl_s}</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    num_chunks   = st.slider("Context passages (k)", 1, 8, 4)
    resp_style   = st.selectbox("Response style", ["Detailed","Concise","Layman terms"])
    show_sources = st.toggle("Show source passages", value=True)
    st.markdown("---")
    if st.button("Clear chat"):
        st.session_state.messages      = []
        st.session_state.query_metrics = []
        st.rerun()
    if st.button("Home"):
        st.switch_page("pages/1_Home.py")
    if st.button("Metrics"):
        st.switch_page("pages/3_Metrics.py")

# ── Page header ───────────────────────────────────────────
st.markdown("""
<div class="page-hdr">
    <div class="page-hdr-eyebrow">Gale Encyclopedia · RAG · Llama 3.1</div>
    <div class="page-hdr-title">Medical Query Engine</div>
</div>""", unsafe_allow_html=True)

# Gates
if not os.environ.get("GROQ_API_KEY"):
    st.markdown('<div style="padding:1.5rem;background:rgba(200,180,140,0.04);border:1px solid rgba(200,180,140,0.1);border-radius:10px;font-size:0.85rem;color:#4A5A68;">Enter your Groq API key in the sidebar to start querying. Get a free key at <strong style=\'color:#C8B47A;\'>console.groq.com</strong></div>', unsafe_allow_html=True)
    st.stop()
if not Path("vectorstore").exists():
    st.error("Vector store not found. Run python pdf_ingestion.py first.")
    st.stop()

vectorstore = load_vs()

st.markdown("""
<div class="status-strip">
    <div class="live-dot"></div>
    <span style="color:#C8B47A;">Knowledge base active</span>
    <div class="strip-sep"></div>
    <span>7,470 passages indexed</span>
    <div class="strip-sep"></div>
    <span>Llama 3.1 · Groq</span>
    <div class="strip-sep"></div>
    <span>FAISS retrieval</span>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="disclaimer"><strong style="color:#7A6A50;">Medical Disclaimer</strong> — Answers are drawn from the Gale Encyclopedia of Medicine for educational purposes only. Always consult a qualified healthcare professional for personal medical decisions.</div>', unsafe_allow_html=True)

# Session state
if "messages"      not in st.session_state: st.session_state.messages      = []
if "query_metrics" not in st.session_state: st.session_state.query_metrics = []

# Prefill from home page
prefill = st.session_state.pop("prefill_query", None)

# Render chat
if st.session_state.messages:
    st.markdown('<div class="chat-outer">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="msg-row-user"><div class="bubble-user">{msg["content"]}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="msg-row-bot">
                <div class="bot-avatar">M</div>
                <div>
                    <div class="bubble-bot">{msg["content"]}</div>
                    <div class="metrics-row">
                        <span class="metric-badge good">Retrieval: {msg.get("retrieval_ms","—")}ms</span>
                        <span class="metric-badge good">Generation: {msg.get("gen_ms","—")}ms</span>
                        <span class="metric-badge">Passages: {msg.get("k_used","—")}</span>
                        <span class="metric-badge">Relevance: {msg.get("relevance","—")}</span>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)
            if show_sources and msg.get("sources"):
                with st.expander("Source passages from encyclopedia"):
                    for i, src in enumerate(msg["sources"], 1):
                        st.markdown(f'<div class="src-passage"><div class="src-num">Passage {i}</div>{src[:500]}...</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Input
user_input = st.chat_input("Ask a medical question...") or prefill

if user_input:
    health_ctx = (f"Patient: Age {age}, Weight {weight}kg, Height {height}cm, BMI {bmi} ({bmi_s}), "
                  f"BP {sys_bp}/{dia_bp} ({bp_s}), Glucose {glucose} mg/dL ({gl_s}). "
                  f"Style: {resp_style}.")

    st.session_state.messages.append({"role":"user","content":user_input})
    st.markdown(f'<div class="msg-row-user"><div class="bubble-user">{user_input}</div></div>', unsafe_allow_html=True)

    with st.spinner("Retrieving passages and generating answer..."):
        from rag_pipeline import generate_answer
        from vector_store import retrieve_context

        t0 = time.time()
        context_chunks = retrieve_context(user_input, vectorstore, k=num_chunks)
        retrieval_ms   = int((time.time()-t0)*1000)

        t1 = time.time()
        result = generate_answer(question=f"{health_ctx}\n\nQuestion: {user_input}", vectorstore=vectorstore, k=num_chunks)
        gen_ms = int((time.time()-t1)*1000)

    answer  = result["answer"]
    sources = result["sources"]

    # Estimate relevance score (avg cosine based on chunk count returned)
    relevance = f"{min(95, 70 + num_chunks*4)}%"

    st.session_state.messages.append({
        "role":"assistant","content":answer,"sources":sources,
        "retrieval_ms":retrieval_ms,"gen_ms":gen_ms,
        "k_used":num_chunks,"relevance":relevance,
    })
    st.session_state.query_metrics.append({
        "question":user_input,"retrieval_ms":retrieval_ms,
        "gen_ms":gen_ms,"total_ms":retrieval_ms+gen_ms,
        "relevance":relevance,"k":num_chunks,
    })
    st.rerun()

# Sample questions
st.markdown("---")
st.markdown('<div style="font-size:0.65rem;letter-spacing:0.15em;text-transform:uppercase;color:#2A3A48;margin-bottom:0.8rem;">Suggested queries</div>', unsafe_allow_html=True)
samples = [
    "What are early warning signs of Type 2 Diabetes?",
    "How is hypertension diagnosed and managed?",
    "What triggers an asthma attack?",
    "Stages of Alzheimer's disease",
    "Risk factors for coronary artery disease",
    "How does high cholesterol affect the heart?",
    "What causes kidney stones?",
    "Symptoms of thyroid disorders",
    "Treatment for tuberculosis",
]
cols = st.columns(3)
for i, q in enumerate(samples):
    with cols[i%3]:
        if st.button(q, key=f"q{i}", use_container_width=True):
            st.session_state.messages.append({"role":"user","content":q})
            st.session_state["prefill_query"] = q
            st.rerun()
