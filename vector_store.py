"""
vector_store.py - Load and query FAISS index
"""

from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

VECTORSTORE_DIR = Path("vectorstore")
EMBED_MODEL     = "sentence-transformers/all-MiniLM-L6-v2"


def load_vectorstore() -> FAISS:
    if not VECTORSTORE_DIR.exists():
        raise FileNotFoundError(
            "Vector store not found. Run: python pdf_ingestion.py"
        )
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBED_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    return FAISS.load_local(
        str(VECTORSTORE_DIR),
        embeddings,
        allow_dangerous_deserialization=True,
    )


def retrieve_context(query: str, vectorstore: FAISS, k: int = 4) -> list:
    docs = vectorstore.similarity_search(query, k=k)
    return [doc.page_content for doc in docs]
