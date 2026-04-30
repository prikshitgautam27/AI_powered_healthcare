"""
app.py - Healthcare RAG Chatbot (Groq-powered, Streamlit Cloud ready)
"""

import os
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title="Healthcare RAG Chatbot",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.user-bubble {
    background: #0077b6; color: white;
    padding: 12px 18px; border-radius: 20px 20px 4px 20px;
    max-width: 75%; margin: 8px 0 8px auto; text-align: right;
    font-size: 15px;
}
.bot-bubble {
    background: #f1f8ff; color: #111; border: 1px solid #d0e8ff;
    padding: 12px 18px; border-radius: 20px 20px 20px 4px;
    max-width: 80%; margin: 8px auto 8px 0;
    font-size: 15px; line-height: 1.6;
}
.source-box {
    background: #eaf4fb; border-left: 4px solid #0077b6;
    padding: 10px 14px; border-radius: 4px;
    font-size: 0.8em; margin-top: 6px; color: #333;
}
.badge {
    display: inline-block; background: #0077b6; color: white;
    padding: 2px 10px; border-radius: 12px; font-size: 12px; margin: 2px;
}
</style>
""", unsafe_allow_html=True)


@st.cache_resource(show_spinner="Loading vector store ...")
def load_vs():
    from vector_store import load_vectorstore
    return load_vectorstore()


# ── Sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🩺 HealthBot")
    st.markdown("---")

    # API Key input (for local use; on cloud use Secrets)
    groq_key = st.text_input(
        "Groq API Key",
        type="password",
        value=os.environ.get("GROQ_API_KEY", ""),
        help="Get your free key at console.groq.com",
        placeholder="gsk_..."
    )
    if groq_key:
        os.environ["GROQ_API_KEY"] = groq_key

    st.markdown("---")
    num_chunks = st.slider("Context chunks (k)", 1, 8, 4,
                           help="More = richer context, slightly slower")
    show_sources = st.toggle("Show source passages", value=True)

    st.markdown("---")
    st.markdown("""
**Data Source**
📖 Gale Encyclopedia of Medicine

**Stack**
- 🔍 Embeddings: MiniLM-L6-v2
- 🗃️ Vector DB: FAISS
- ⚡ LLM: Llama3-8b via Groq

**Speed:** ~1-2 sec per answer
    """)

    st.markdown("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()


# ── Main ──────────────────────────────────────────────────
st.title("🩺 Healthcare RAG Chatbot")
st.caption("Powered by Gale Encyclopedia of Medicine · Groq · FAISS")

st.warning(
    "⚕️ **Medical Disclaimer:** For educational purposes only. "
    "Always consult a qualified healthcare professional for medical advice.",
)

# Check API key
if not os.environ.get("GROQ_API_KEY"):
    st.info("👈 **Enter your Groq API key in the sidebar to get started.** "
            "Get a free key at [console.groq.com](https://console.groq.com)", icon="🔑")
    st.stop()

# Check vectorstore
if not Path("vectorstore").exists():
    st.error("Vector store not found. Run `python pdf_ingestion.py` first.")
    st.stop()

# Load vector store
vectorstore = load_vs()
st.success("✅ Encyclopedia loaded and ready!", icon="📚")
st.markdown("---")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble">🧑 {msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-bubble">🤖 {msg["content"]}</div>', unsafe_allow_html=True)
        if show_sources and msg.get("sources"):
            with st.expander("📖 Source passages from encyclopedia"):
                for i, src in enumerate(msg["sources"], 1):
                    st.markdown(f'<div class="source-box"><b>Passage {i}:</b><br>{src[:500]}...</div>', unsafe_allow_html=True)

# Input
st.markdown("---")
user_input = st.chat_input("Ask a medical question, e.g. What are symptoms of diabetes?")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f'<div class="user-bubble">🧑 {user_input}</div>', unsafe_allow_html=True)

    with st.spinner("⚡ Searching encyclopedia and generating answer ..."):
        from rag_pipeline import generate_answer
        result = generate_answer(question=user_input, vectorstore=vectorstore, k=num_chunks)

    answer  = result["answer"]
    sources = result["sources"]

    st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})
    st.markdown(f'<div class="bot-bubble">🤖 {answer}</div>', unsafe_allow_html=True)

    if show_sources and sources:
        with st.expander("📖 Source passages from encyclopedia"):
            for i, src in enumerate(sources, 1):
                st.markdown(f'<div class="source-box"><b>Passage {i}:</b><br>{src[:500]}...</div>', unsafe_allow_html=True)
    st.rerun()

# Sample questions
st.markdown("---")
st.markdown("### 💡 Sample Questions")
samples = [
    "What are the symptoms of Type 2 Diabetes?",
    "How is hypertension diagnosed and treated?",
    "What causes asthma and how is it managed?",
    "Explain the stages of Alzheimer's disease.",
    "What are the risk factors for heart disease?",
    "What is the treatment for tuberculosis?",
]
cols = st.columns(3)
for i, q in enumerate(samples):
    with cols[i % 3]:
        if st.button(q, key=f"s{i}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": q})
            st.rerun()
