"""
pdf_ingestion.py - Run once to build FAISS index from your PDF
python pdf_ingestion.py
"""

import fitz
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

PDF_SEARCH_DIRS = [Path("data"), Path("data/data"), Path(".")]
VECTORSTORE_DIR = Path("vectorstore")
EMBED_MODEL     = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE      = 512
CHUNK_OVERLAP   = 64


def find_pdfs():
    found = []
    for d in PDF_SEARCH_DIRS:
        if d.exists():
            pdfs = list(d.glob("*.pdf"))
            if pdfs:
                print(f"Found PDFs in: {d.resolve()}")
                found.extend(pdfs)
    seen, unique = set(), []
    for p in found:
        rp = p.resolve()
        if rp not in seen:
            seen.add(rp)
            unique.append(p)
    return unique


def load_pdf_text(pdf_path):
    print(f"Loading PDF: {pdf_path.name}")
    doc = fitz.open(str(pdf_path))
    num_pages = doc.page_count
    full_text = []
    for i in range(num_pages):
        text = doc[i].get_text("text")
        if text.strip():
            full_text.append(f"[Page {i+1}]\n{text}")
    doc.close()
    combined = "\n\n".join(full_text)
    print(f"   Extracted {len(combined):,} characters from {num_pages} pages.")
    return combined


def chunk_text(text):
    print("Chunking text ...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_text(text)
    print(f"   Created {len(chunks):,} chunks.")
    return chunks


def build_vectorstore(chunks):
    print(f"Embedding with {EMBED_MODEL} ...")
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBED_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    BATCH = 500
    batches = [chunks[i:i+BATCH] for i in range(0, len(chunks), BATCH)]
    vectorstore = None
    for idx, batch in enumerate(batches):
        print(f"   Batch {idx+1}/{len(batches)} ({len(batch)} chunks) ...")
        if vectorstore is None:
            vectorstore = FAISS.from_texts(batch, embeddings)
        else:
            vectorstore.merge_from(FAISS.from_texts(batch, embeddings))
    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(VECTORSTORE_DIR))
    print(f"   Vector store saved to '{VECTORSTORE_DIR}/'")


def main():
    pdf_files = find_pdfs()
    if not pdf_files:
        print("No PDF found in data/ or data/data/")
        return
    all_text = ""
    for p in pdf_files:
        all_text += load_pdf_text(p) + "\n\n"
    chunks = chunk_text(all_text)
    build_vectorstore(chunks)
    print("\nDone! Run:  streamlit run app.py")

if __name__ == "__main__":
    main()
