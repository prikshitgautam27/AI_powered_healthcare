#  Healthcare RAG Chatbot
### Powered by Gale Encyclopedia + HuggingFace + Streamlit
#### ACCESS: https://pgautam-healthcare-limited.streamlit.app/
##  Project Structure
```
healthcare_rag_chatbot/
│
├── app.py                  # Main Streamlit app
├── rag_pipeline.py         # Core RAG logic
├── pdf_ingestion.py        # PDF loader & chunker
├── vector_store.py         # FAISS vector store manager
├── requirements.txt        # All dependencies
├── .env.example            # Environment variables template
├── data/
│   └── (place your Gale Encyclopedia PDF here)
├── vectorstore/
│   └── (auto-created FAISS index saved here)
└── README.md
```

##  Setup & Run

### 1. Clone / setup project
```bash
mkdir healthcare_rag_chatbot && cd healthcare_rag_chatbot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your PDF
Place your **Gale Encyclopedia of Medicine PDF** inside the `data/` folder.

### 4. Build the vector store (run once)
```bash
python pdf_ingestion.py
```

### 5. Run the Streamlit app
```bash
streamlit run app.py
```

## 🔧 Models Used
| Component | Model |
|-----------|-------|
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` |
| LLM | `google/flan-t5-large` |
| Vector DB | `FAISS` (local, no server needed) |
| PDF Parsing | `PyMuPDF (fitz)` |

## ☁️ Deploy on Streamlit Cloud
1. Push this folder to a GitHub repo
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo → set `app.py` as entry point
4. Add secrets if needed in Streamlit Cloud dashboard
5. Deploy! 

## 📌 Notes
- First run downloads models (~500MB). Subsequent runs use cache.
- Vector store is built once from PDF; rebuilding takes ~2-5 min depending on PDF size.
- Works fully offline after first model download.
