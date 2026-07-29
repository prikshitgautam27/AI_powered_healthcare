import streamlit as st, os

st.set_page_config(page_title="MediQuery — Metrics", page_icon="M", layout="wide", initial_sidebar_state="expanded")

try: os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
except: pass

if not st.session_state.get("logged_in"):
    st.warning("Please sign in first.")
    st.page_link("app.py", label="Go to Login" )
    st.stop()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');
html,body,[data-testid="stAppViewContainer"]{background:#F8F6F2!important;font-family:'Inter',sans-serif;color:#1A1A2E;}
#MainMenu,footer,header{display:none!important;}
[data-testid="stSidebar"]{background:#FFFFFF!important;border-right:1px solid #EDE8E0!important;}
[data-testid="stSidebar"] *{color:#1A1A2E!important;}
[data-testid="stSidebar"] hr{border-color:#EDE8E0!important;}
[data-testid="stSidebar"] .stButton button{background:#1B4332!important;border:none!important;color:#FFFFFF!important;border-radius:8px!important;font-size:0.72rem!important;letter-spacing:0.1em!important;text-transform:uppercase!important;width:100%!important;margin-bottom:0.3rem!important;}
[data-testid="stPageLink"] a{color:#1B4332!important;font-size:0.82rem!important;font-weight:500!important;}
[data-testid="block-container"]{padding:2rem 2.5rem!important;max-width:1200px;margin:0 auto;}

.page-hdr{padding:0.5rem 0 1.5rem;border-bottom:1px solid #EDE8E0;margin-bottom:1.8rem;}
.page-eyebrow{font-size:0.62rem;letter-spacing:0.18em;text-transform:uppercase;color:#2D6A4F;margin-bottom:0.4rem;font-weight:500;}
.page-title{font-family:'Playfair Display',serif;font-size:1.9rem;color:#1A1A2E;font-weight:400;}
.page-sub{font-size:0.8rem;color:#8A9BB0;margin-top:0.3rem;}

.kpi-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-bottom:1.5rem;}
.kpi{background:#FFFFFF;border:1px solid #EDE8E0;border-radius:12px;padding:1.3rem 1.5rem;transition:all 0.2s;box-shadow:0 1px 4px rgba(0,0,0,0.04);}
.kpi:hover{border-color:#95D5B2;transform:translateY(-2px);box-shadow:0 6px 20px rgba(27,67,50,0.08);}
.kl{font-size:0.58rem;letter-spacing:0.14em;text-transform:uppercase;color:#A0ADB8;margin-bottom:0.4rem;font-weight:500;}
.kv{font-family:'Playfair Display',serif;font-size:2rem;color:#1A1A2E;font-weight:400;line-height:1;}
.ku{font-size:0.72rem;color:#8A9BB0;margin-left:0.2rem;}
.kd{font-size:0.65rem;margin-top:0.3rem;}
.kd.up{color:#16A34A;font-weight:500;}.kd.ok{color:#D97706;font-weight:500;}

.sec-hdr{display:flex;align-items:center;gap:1rem;margin:2rem 0 1rem;}
.sec-title{font-family:'Playfair Display',serif;font-size:1.05rem;color:#6A7A8A;white-space:nowrap;}
.sec-line{flex:1;height:1px;background:#EDE8E0;}

.m-table{width:100%;border-collapse:collapse;font-size:0.78rem;background:#FFFFFF;border-radius:12px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,0.04);}
.m-table th{font-size:0.6rem;letter-spacing:0.12em;text-transform:uppercase;color:#A0ADB8;padding:0.8rem 1rem;text-align:left;border-bottom:1px solid #EDE8E0;font-weight:500;background:#FAFAF8;}
.m-table td{padding:0.75rem 1rem;border-bottom:1px solid #F5F2EE;color:#4A5568;}
.m-table tr:hover td{background:#F8FFF8;}
.m-table tr:last-child td{border-bottom:none;}
.badge{display:inline-block;padding:0.2rem 0.6rem;border-radius:20px;font-size:0.6rem;letter-spacing:0.07em;text-transform:uppercase;font-weight:500;}
.bg{background:#F0FDF4;border:1px solid #BBF7D0;color:#16A34A;}
.bo{background:#FFFBEB;border:1px solid #FDE68A;color:#D97706;}
.bb{background:#EFF6FF;border:1px solid #BFDBFE;color:#2563EB;}

.arch-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-top:1rem;}
.ac{background:#FFFFFF;border:1px solid #EDE8E0;border-radius:12px;padding:1.3rem;box-shadow:0 1px 4px rgba(0,0,0,0.04);transition:all 0.2s;}
.ac:hover{border-color:#95D5B2;box-shadow:0 4px 16px rgba(27,67,50,0.08);}
.ac-step{font-size:0.58rem;letter-spacing:0.15em;text-transform:uppercase;color:#2D6A4F;margin-bottom:0.4rem;font-weight:600;}
.ac-name{font-family:'Playfair Display',serif;font-size:1rem;color:#1A1A2E;margin-bottom:0.4rem;}
.ac-detail{font-size:0.72rem;color:#8A9BB0;line-height:1.6;}

.info-banner{background:#F0FDF4;border:1px solid #BBF7D0;border-radius:8px;padding:0.7rem 1rem;font-size:0.78rem;color:#166534;margin-bottom:1rem;}
</style>
""", unsafe_allow_html=True)

username = st.session_state.get("username","User")

with st.sidebar:
    st.markdown(f"""
    <div style="padding:1.2rem 0 0.8rem;">
        <div style="font-family:'Playfair Display',serif;font-size:1.4rem;color:#1A1A2E;">MediQuery</div>
        <div style="font-size:0.62rem;color:#A0ADB8;letter-spacing:0.14em;text-transform:uppercase;margin-top:0.2rem;">Metrics</div>
    </div>
    <div style="font-size:0.75rem;color:#8A9BB0;margin-bottom:0.8rem;">Signed in as <strong style="color:#2D6A4F;">{username}</strong></div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.page_link("pages/1_Home.py",    label="Home" )
    st.page_link("pages/2_Query.py",   label="Query" )
    st.page_link("pages/3_Metrics.py", label="Metrics" )
    st.markdown("---")
    if st.button("Sign Out"):
        st.session_state.logged_in=False; st.session_state.username=""; st.rerun()

st.markdown("""
<div class="page-hdr">
    <div class="page-eyebrow">System Performance · RAG Pipeline Analysis</div>
    <div class="page-title">Metrics Dashboard</div>
    <div class="page-sub">Real-time performance data from your query session</div>
</div>""", unsafe_allow_html=True)

raw = st.session_state.get("query_metrics",[])
if not raw:
    st.markdown('<div class="info-banner">No queries yet. Head to the <strong>Query</strong> page and ask some questions — your live metrics will appear here.</div>', unsafe_allow_html=True)
    raw=[
        {"question":"Diabetes symptoms","retrieval_ms":45,"gen_ms":1240,"total_ms":1285,"relevance":"94%","k":4},
        {"question":"Hypertension treatment","retrieval_ms":38,"gen_ms":1180,"total_ms":1218,"relevance":"91%","k":4},
        {"question":"Asthma management","retrieval_ms":42,"gen_ms":1320,"total_ms":1362,"relevance":"89%","k":4},
        {"question":"Heart disease risk","retrieval_ms":51,"gen_ms":1150,"total_ms":1201,"relevance":"93%","k":4},
        {"question":"Kidney stone causes","retrieval_ms":39,"gen_ms":1290,"total_ms":1329,"relevance":"87%","k":4},
    ]
    showing_demo = True
else:
    showing_demo = False

n=len(raw)
ar=sum(r["retrieval_ms"] for r in raw)/n
ag=sum(r["gen_ms"] for r in raw)/n
at=sum(r["total_ms"] for r in raw)/n
av=sum(int(r["relevance"].replace("%","")) for r in raw)/n

# KPIs row 1
st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi"><div class="kl">Avg Retrieval</div><div class="kv">{ar:.0f}<span class="ku">ms</span></div><div class="kd up">FAISS semantic search</div></div>
    <div class="kpi"><div class="kl">Avg Generation</div><div class="kv">{ag/1000:.2f}<span class="ku">s</span></div><div class="kd ok">Llama 3.1 via Groq</div></div>
    <div class="kpi"><div class="kl">Avg Total Response</div><div class="kv">{at/1000:.2f}<span class="ku">s</span></div><div class="kd up">End-to-end</div></div>
    <div class="kpi"><div class="kl">Avg Relevance</div><div class="kv">{av:.0f}<span class="ku">%</span></div><div class="kd up">Cosine similarity</div></div>
</div>
<div class="kpi-grid">
    <div class="kpi"><div class="kl">{"Live" if not showing_demo else "Demo"} Queries</div><div class="kv">{n}</div><div class="kd ok">This session</div></div>
    <div class="kpi"><div class="kl">Indexed Passages</div><div class="kv">7,470</div><div class="kd ok">512-char chunks</div></div>
    <div class="kpi"><div class="kl">Embedding Dim</div><div class="kv">384</div><div class="kd ok">MiniLM-L6-v2</div></div>
    <div class="kpi"><div class="kl">Source Pages</div><div class="kv">759</div><div class="kd ok">Gale Encyclopedia</div></div>
</div>
""", unsafe_allow_html=True)

# Query log
st.markdown('<div class="sec-hdr"><div class="sec-title">Query Log</div><div class="sec-line"></div></div>', unsafe_allow_html=True)
rows=""
for i,r in enumerate(reversed(raw),1):
    rel=int(r["relevance"].replace("%",""))
    rc="bg" if rel>=90 else "bo"
    ts=r["total_ms"]/1000; sc="bg" if ts<1.5 else "bo"
    rows+=f"<tr><td style='color:#A0ADB8;font-size:0.62rem;'>{i}</td><td style='color:#1A1A2E;font-weight:500;'>{r['question'][:52]}{'...' if len(r['question'])>52 else ''}</td><td><span class='badge bb'>{r['retrieval_ms']}ms</span></td><td><span class='badge bb'>{r['gen_ms']}ms</span></td><td><span class='badge {sc}'>{ts:.2f}s</span></td><td><span class='badge {rc}'>{r['relevance']}</span></td><td style='color:#A0ADB8;'>{r['k']}</td></tr>"
st.markdown(f"""
<table class="m-table">
    <thead><tr><th>#</th><th>Query</th><th>Retrieval</th><th>Generation</th><th>Total</th><th>Relevance</th><th>k</th></tr></thead>
    <tbody>{rows}</tbody>
</table>""", unsafe_allow_html=True)

# Architecture
st.markdown('<div class="sec-hdr"><div class="sec-title">System Architecture</div><div class="sec-line"></div></div>', unsafe_allow_html=True)
st.markdown("""
<div class="arch-grid">
    <div class="ac"><div class="ac-step">Step 01</div><div class="ac-name">Document Ingestion</div><div class="ac-detail">PyMuPDF extracts 3.1M characters from 759 pages. Chunked into 7,470 passages — 512 chars each, 64-char overlap.</div></div>
    <div class="ac"><div class="ac-step">Step 02</div><div class="ac-name">Vector Embedding</div><div class="ac-detail">all-MiniLM-L6-v2 encodes each chunk into 384-dimensional vectors. FAISS IndexFlatL2 stores them for fast retrieval.</div></div>
    <div class="ac"><div class="ac-step">Step 03</div><div class="ac-name">Semantic Retrieval</div><div class="ac-detail">User query is embedded at inference time. Top-k cosine-similar passages retrieved in ~40ms via FAISS similarity search.</div></div>
    <div class="ac"><div class="ac-step">Step 04</div><div class="ac-name">Context Augmentation</div><div class="ac-detail">Retrieved passages combined with patient vitals — age, BMI, blood pressure, glucose — and injected into a structured prompt.</div></div>
    <div class="ac"><div class="ac-step">Step 05</div><div class="ac-name">LLM Generation</div><div class="ac-detail">Llama-3.1-8B-Instant via Groq API generates a grounded answer. Temperature 0.2 for factual, consistent responses.</div></div>
    <div class="ac"><div class="ac-step">Step 06</div><div class="ac-name">Response & Tracing</div><div class="ac-detail">Answer delivered with full source attribution. Retrieval latency, generation time, and relevance score logged per query.</div></div>
</div>
""", unsafe_allow_html=True)
