import streamlit as st

st.set_page_config(page_title="MediQuery — About", page_icon="M", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');
html,body,[data-testid="stAppViewContainer"]{background:#F8F6F2!important;font-family:'Inter',sans-serif;color:#1A1A2E;}
#MainMenu,footer,header{display:none!important;}
[data-testid="stSidebar"]{background:#FFFFFF!important;border-right:1px solid #EDE8E0!important;}
[data-testid="stSidebar"] *{color:#1A1A2E!important;}
[data-testid="stSidebar"] hr{border-color:#EDE8E0!important;}
[data-testid="stPageLink"] a{color:#1B4332!important;font-size:0.82rem!important;font-weight:500!important;}
[data-testid="block-container"]{padding:2rem 2.5rem!important;max-width:1150px;margin:0 auto;}

.page-hdr{padding:0.5rem 0 1.5rem;border-bottom:1px solid #EDE8E0;margin-bottom:1.8rem;}
.page-eyebrow{font-size:0.62rem;letter-spacing:0.18em;text-transform:uppercase;color:#2D6A4F;margin-bottom:0.4rem;font-weight:500;}
.page-title{font-family:'Playfair Display',serif;font-size:1.9rem;color:#1A1A2E;font-weight:400;}
.page-sub{font-size:0.8rem;color:#8A9BB0;margin-top:0.3rem;}

.sec-title{font-family:'Playfair Display',serif;font-size:1.2rem;color:#1A1A2E;margin:1.6rem 0 0.6rem;}
.sec-desc{font-size:0.85rem;color:#6A7A8A;line-height:1.7;margin-bottom:1.2rem;max-width:760px;}

.arch-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-top:0.5rem;}
.ac{background:#FFFFFF;border:1px solid #EDE8E0;border-radius:12px;padding:1.3rem;box-shadow:0 1px 4px rgba(0,0,0,0.04);transition:all 0.2s;}
.ac:hover{border-color:#95D5B2;box-shadow:0 4px 16px rgba(27,67,50,0.08);}
.ac-step{font-size:0.58rem;letter-spacing:0.15em;text-transform:uppercase;color:#2D6A4F;margin-bottom:0.4rem;font-weight:600;}
.ac-name{font-family:'Playfair Display',serif;font-size:1rem;color:#1A1A2E;margin-bottom:0.4rem;}
.ac-detail{font-size:0.72rem;color:#8A9BB0;line-height:1.6;}

.flow{display:flex;align-items:center;gap:0.4rem;flex-wrap:wrap;margin:1rem 0 1.8rem;}
.flow-node{background:#FFFFFF;border:1px solid #EDE8E0;border-radius:10px;padding:0.7rem 1.1rem;font-size:0.76rem;font-weight:500;color:#1B4332;box-shadow:0 1px 4px rgba(0,0,0,0.04);}
.flow-arrow{color:#B0BDC8;font-size:1rem;}

.model-table{width:100%;border-collapse:collapse;font-size:0.82rem;background:#FFFFFF;border-radius:12px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,0.04);margin-bottom:1.5rem;}
.model-table th{font-size:0.6rem;letter-spacing:0.1em;text-transform:uppercase;color:#A0ADB8;padding:0.8rem 1rem;text-align:left;border-bottom:1px solid #EDE8E0;font-weight:500;background:#FAFAF8;}
.model-table td{padding:0.75rem 1rem;border-bottom:1px solid #F5F2EE;color:#4A5568;}
.model-table tr:last-child td{border-bottom:none;}
.model-table tr:hover td{background:#F8FFF8;}

.badge{display:inline-block;padding:0.2rem 0.6rem;border-radius:20px;font-size:0.6rem;letter-spacing:0.07em;text-transform:uppercase;font-weight:500;background:#F0FDF4;border:1px solid #BBF7D0;color:#16A34A;}

.design-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:1rem;margin-top:0.5rem;}
.dc{background:#FFFFFF;border:1px solid #EDE8E0;border-radius:12px;padding:1.4rem;box-shadow:0 1px 4px rgba(0,0,0,0.04);}
.dc-title{font-family:'Playfair Display',serif;font-size:1.02rem;color:#1A1A2E;margin-bottom:0.5rem;}
.dc-detail{font-size:0.78rem;color:#8A9BB0;line-height:1.65;}
.swatch-row{display:flex;gap:0.5rem;margin-top:0.7rem;}
.swatch{width:28px;height:28px;border-radius:6px;border:1px solid rgba(0,0,0,0.06);}

.novelty-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-top:0.5rem;}
.nc{background:#FFFFFF;border:1px solid #EDE8E0;border-radius:12px;padding:1.4rem;box-shadow:0 1px 4px rgba(0,0,0,0.04);transition:all 0.2s;}
.nc:hover{border-color:#95D5B2;transform:translateY(-2px);box-shadow:0 8px 24px rgba(27,67,50,0.1);}
.nc-tag{font-size:0.58rem;letter-spacing:0.14em;text-transform:uppercase;color:#2D6A4F;margin-bottom:0.5rem;font-weight:600;}
.nc-title{font-family:'Playfair Display',serif;font-size:1.02rem;color:#1A1A2E;margin-bottom:0.5rem;}
.nc-detail{font-size:0.78rem;color:#8A9BB0;line-height:1.65;}

.stTabs [data-baseweb="tab-list"]{gap:1.5rem;border-bottom:1px solid #EDE8E0;}
.stTabs [data-baseweb="tab"]{font-size:0.8rem;font-weight:500;color:#A0ADB8;padding:0.6rem 0;}
.stTabs [aria-selected="true"]{color:#1B4332!important;border-bottom-color:#1B4332!important;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style="padding:1.2rem 0 0.8rem;">
        <div style="font-family:'Playfair Display',serif;font-size:1.4rem;color:#1A1A2E;">MediQuery</div>
        <div style="font-size:0.62rem;color:#A0ADB8;letter-spacing:0.14em;text-transform:uppercase;margin-top:0.2rem;">About the Project</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.page_link("app.py",             label="Home")
    st.page_link("pages/1_Query.py",   label="Live Demo")
    st.page_link("pages/2_About.py",   label="About the Project")

st.markdown("""
<div class="page-hdr">
    <div class="page-eyebrow">Engineering Deep Dive</div>
    <div class="page-title">Architecture, Models & Design</div>
    <div class="page-sub">How MediQuery is built, why these choices were made, and what makes it distinct from a boilerplate RAG demo</div>
</div>""", unsafe_allow_html=True)

tab_arch, tab_model, tab_design, tab_novelty = st.tabs(["Architecture", "Models", "Design", "Novelty"])

# ── Architecture ──────────────────────────────────────────
with tab_arch:
    st.markdown('<div class="sec-title">Pipeline overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-desc">A classic RAG pipeline split into an offline ingestion stage (run once) and an online query stage (run per request). Keeping these decoupled means the vector index never has to be rebuilt at query time.</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="flow">
        <div class="flow-node">PDF Source</div><div class="flow-arrow">→</div>
        <div class="flow-node">PyMuPDF Extraction</div><div class="flow-arrow">→</div>
        <div class="flow-node">Recursive Chunking</div><div class="flow-arrow">→</div>
        <div class="flow-node">MiniLM Embedding</div><div class="flow-arrow">→</div>
        <div class="flow-node">FAISS Index</div>
    </div>
    <div class="flow">
        <div class="flow-node">User Query</div><div class="flow-arrow">→</div>
        <div class="flow-node">Query Embedding</div><div class="flow-arrow">→</div>
        <div class="flow-node">Top-k Retrieval</div><div class="flow-arrow">→</div>
        <div class="flow-node">Prompt Construction</div><div class="flow-arrow">→</div>
        <div class="flow-node">Groq LLM</div><div class="flow-arrow">→</div>
        <div class="flow-node">Answer + Sources</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-title">Stage breakdown</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="arch-grid">
        <div class="ac"><div class="ac-step">Step 01</div><div class="ac-name">Document Ingestion</div><div class="ac-detail">PyMuPDF extracts raw text page-by-page from the source PDF, preserving page numbers for later attribution.</div></div>
        <div class="ac"><div class="ac-step">Step 02</div><div class="ac-name">Chunking</div><div class="ac-detail">LangChain's RecursiveCharacterTextSplitter breaks text into 512-character passages with 64-character overlap, splitting on paragraph/sentence boundaries first to avoid cutting ideas mid-thought.</div></div>
        <div class="ac"><div class="ac-step">Step 03</div><div class="ac-name">Embedding</div><div class="ac-detail">Each chunk is encoded into a 384-dimensional vector with all-MiniLM-L6-v2, normalized for cosine similarity, and batched to keep memory usage bounded on modest hardware.</div></div>
        <div class="ac"><div class="ac-step">Step 04</div><div class="ac-name">Vector Storage</div><div class="ac-detail">Vectors are stored in a local FAISS index — no external vector database or network round-trip required, keeping the whole retrieval step on-box.</div></div>
        <div class="ac"><div class="ac-step">Step 05</div><div class="ac-name">Retrieval</div><div class="ac-detail">At query time, the question is embedded with the same model, and the top-k most similar passages are pulled via FAISS similarity search in tens of milliseconds.</div></div>
        <div class="ac"><div class="ac-step">Step 06</div><div class="ac-name">Grounded Generation</div><div class="ac-detail">Retrieved passages are assembled into a structured prompt with a strict system instruction, then sent to a Groq-hosted LLM for low-latency, context-grounded generation.</div></div>
    </div>
    """, unsafe_allow_html=True)

# ── Models ────────────────────────────────────────────────
with tab_model:
    st.markdown('<div class="sec-title">Models in the stack</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-desc">Every model was chosen for a specific trade-off between quality, latency, and cost — not just picked because it was the default in a tutorial.</div>', unsafe_allow_html=True)

    st.markdown("""
    <table class="model-table">
        <thead><tr><th>Component</th><th>Model</th><th>Why this one</th></tr></thead>
        <tbody>
            <tr><td><strong>Embeddings</strong></td><td>sentence-transformers/all-MiniLM-L6-v2</td><td>384-dim, CPU-friendly, strong semantic performance for its size — no GPU needed for ingestion.</td></tr>
            <tr><td><strong>Vector index</strong></td><td>FAISS (FlatL2)</td><td>Exact nearest-neighbor search at this corpus size (7,470 vectors) with zero infra overhead — no hosted vector DB needed.</td></tr>
            <tr><td><strong>LLM generation</strong></td><td>Groq-hosted open-weight model (e.g. openai/gpt-oss-120b)</td><td>Groq's LPU inference delivers sub-second generation, which keeps the whole query loop under ~2s end-to-end.</td></tr>
            <tr><td><strong>PDF parsing</strong></td><td>PyMuPDF (fitz)</td><td>Fast, dependency-light text extraction that preserves page structure for source attribution.</td></tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-title">Why not fine-tune an LLM?</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-desc">RAG was chosen deliberately over fine-tuning: the encyclopedia content can be swapped or updated without retraining anything, hallucination risk is reduced because the model is instructed to answer only from retrieved context, and every answer stays traceable to a specific source passage — which matters a lot in a medical-information context.</div>', unsafe_allow_html=True)

# ── Design ────────────────────────────────────────────────
with tab_design:
    st.markdown('<div class="sec-title">Design philosophy</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-desc">Streamlit apps default to a generic look. This one was styled from scratch to feel like a real clinical-software product rather than a notebook demo.</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="design-grid">
        <div class="dc">
            <div class="dc-title">Color palette</div>
            <div class="dc-detail">A muted clinical-green and warm off-white palette, chosen to read as calm and trustworthy rather than sterile hospital-white.</div>
            <div class="swatch-row">
                <div class="swatch" style="background:#1B4332;"></div>
                <div class="swatch" style="background:#2D6A4F;"></div>
                <div class="swatch" style="background:#95D5B2;"></div>
                <div class="swatch" style="background:#F8F6F2;"></div>
                <div class="swatch" style="background:#1A1A2E;"></div>
            </div>
        </div>
        <div class="dc">
            <div class="dc-title">Typography</div>
            <div class="dc-detail">Playfair Display for headings gives an editorial, confident feel; Inter for body text keeps everything else legible and neutral. The pairing is meant to feel more "product" than "prototype."</div>
        </div>
        <div class="dc">
            <div class="dc-title">Component system</div>
            <div class="dc-detail">Every surface — KPI tiles, chat bubbles, source-passage cards, architecture steps — reuses the same card, radius, shadow, and spacing rules so the whole app feels like one cohesive system instead of stitched-together widgets.</div>
        </div>
        <div class="dc">
            <div class="dc-title">Transparency by design</div>
            <div class="dc-detail">Every generated answer ships with its retrieval and generation latency and its source passages, visible in an expander. Nothing is presented as ground truth without a way to check it.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Novelty ───────────────────────────────────────────────
with tab_novelty:
    st.markdown('<div class="sec-title">What makes this project distinct</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-desc">Beyond "PDF in, chatbot out" — a few deliberate choices that go past the standard RAG tutorial.</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="novelty-grid">
        <div class="nc"><div class="nc-tag">Source-grounded answers</div><div class="nc-title">Every claim is traceable</div><div class="nc-detail">The system is instructed to answer only from retrieved context and to say so honestly when the context is insufficient — the raw passages are shown alongside the answer, not just cited by title.</div></div>
        <div class="nc"><div class="nc-tag">Context personalization</div><div class="nc-title">Optional vitals-aware answers</div><div class="nc-detail">Users can optionally inject basic health parameters (BMI, blood pressure, glucose) into the prompt context, letting the same knowledge base produce answers tailored to a specific patient profile.</div></div>
        <div class="nc"><div class="nc-tag">Latency-first architecture</div><div class="nc-title">Fully local retrieval, fast remote generation</div><div class="nc-detail">Retrieval never leaves the box (FAISS, in-process), and generation runs on Groq's LPU hardware — the combination is what keeps end-to-end response times under ~2 seconds.</div></div>
        <div class="nc"><div class="nc-tag">Provider resilience</div><div class="nc-title">Decoupled model configuration</div><div class="nc-detail">The generation model is a single config constant, not hardcoded through the app — swapping LLM providers or models (as happened when a model was deprecated from the free tier) is a one-line change.</div></div>
        <div class="nc"><div class="nc-tag">Response controllability</div><div class="nc-title">Adjustable retrieval depth & tone</div><div class="nc-detail">Users can tune how many passages are retrieved (k) and choose between detailed, concise, or layman-terms responses — exposing real RAG knobs instead of hiding them.</div></div>
        <div class="nc"><div class="nc-tag">Product-grade UI</div><div class="nc-title">Not a default Streamlit look</div><div class="nc-detail">A fully custom design system (typography, color, card components) makes the difference between "a script with a UI" and something that reads as a real, deployable product.</div></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown('<div style="text-align:center;font-size:0.72rem;color:#B0BDC8;">MediQuery · Portfolio project · Built with Streamlit, FAISS, and Groq</div>', unsafe_allow_html=True)
