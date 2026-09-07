"""
rag_pipeline.py  - Groq API version (fast, free, cloud-ready)
Uses llama3-8b-8192 via Groq for answer generation.
No local model download needed!
"""

import os
from groq import Groq
from vector_store import retrieve_context

# ── Config ────────────────────────────────────────────────
GROQ_MODEL  = "openai/gpt-oss-120b"   # Free, fast, high quality
MAX_TOKENS  = 512

SYSTEM_PROMPT = """You are a helpful medical assistant trained on the Gale Encyclopedia of Medicine.
Use ONLY the provided encyclopedia context to answer the user's question.
Be clear, accurate, and concise. If the context doesn't have enough information, say so honestly.
Never make up medical information. Always recommend consulting a doctor for personal medical advice."""


def get_groq_client():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not found!\n"
            "Local: create a .env file with GROQ_API_KEY=your_key\n"
            "Streamlit Cloud: add it in App Settings > Secrets"
        )
    return Groq(api_key=api_key)


def build_prompt(context_chunks: list, question: str) -> str:
    context = "\n\n---\n\n".join(context_chunks)
    return (
        f"Context from Gale Encyclopedia of Medicine:\n\n{context}\n\n"
        f"Question: {question}\n\n"
        f"Answer based only on the context above:"
    )


def generate_answer(question: str, vectorstore, k: int = 4) -> dict:
    """
    Full RAG pipeline: retrieve -> prompt -> Groq API -> answer

    Returns dict with:
        answer  : str
        sources : list[str]
    """
    # 1. Retrieve relevant chunks retrival is imp
    context_chunks = retrieve_context(question, vectorstore, k=k)

    # 2. Build prompt
    prompt = build_prompt(context_chunks, question)

    # 3. Call Groq API
    client = get_groq_client()
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": prompt},
        ],
        max_tokens=MAX_TOKENS,
        temperature=0.2,   # low temp = more factual
    )

    answer = response.choices[0].message.content.strip()

    return {
        "answer":  answer or "I could not find a relevant answer in the encyclopedia.",
        "sources": context_chunks,
    }
