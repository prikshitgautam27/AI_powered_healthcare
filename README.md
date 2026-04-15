# 🏥 AI Powered Healthcare — RAG Chatbot

> An intelligent Retrieval-Augmented Generation (RAG) chatbot that combines **Mistral-7B-Instruct-v0.3** with **FAISS** vector search to deliver accurate, context-aware responses to healthcare queries from medical documents.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Technology Stack](#technology-stack)
- [Key Features](#key-features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Disclaimer](#disclaimer)

---

## 🔍 Overview

AI Powered Healthcare is a sophisticated RAG-based chatbot system that processes medical PDF documents, builds a FAISS vector index, and provides intelligent, document-grounded answers to healthcare-related queries — all via a clean Streamlit web interface or a CLI.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| **Mistral-7B-Instruct-v0.3** | Advanced LLM for intelligent text generation |
| **FAISS** | Facebook AI Similarity Search for fast vector retrieval |
| **Streamlit** | Interactive web interface and user dashboard |
| **Hugging Face** | Model hosting and API integration |
| **LangChain** | Framework for RAG pipeline orchestration |
| **PyPDF2** | PDF document processing and text extraction |

---

## ✨ Key Features

- **Retrieval-Augmented Generation (RAG)** — Combines LLM capabilities with document retrieval for accurate, grounded responses
- **Mistral-7B LLM** — Leverages a state-of-the-art instruction-tuned model for sophisticated text generation
- **Fast Vector Search** — FAISS integration enables quick retrieval of relevant document chunks from large knowledge bases
- **Streamlit Web UI** — Clean, intuitive interface for seamless user interaction
- **Multi-Document Processing** — Handles multiple PDF files to build comprehensive knowledge bases
- **Customizable Prompts** — Flexible prompt templates for controlled response generation
- **CLI Support** — Lightweight command-line interface for quick queries

---

## 📁 Project Structure

```
AI_powered_healthcare/
├── data/                        # Input PDF documents for the knowledge base
│   ├── medical_document1.pdf
│   ├── medical_document2.pdf
│   └── medical_document3.pdf
├── vectorstore/
│   └── db_faiss/                # Stored FAISS index and metadata
├── connect_memory.py            # Loads PDFs, generates embeddings, builds FAISS index
├── create_memory.py             # Streamlit web app with chat UI
├── medibot.py                   # CLI chatbot interface
├── requirements.txt             # Python package dependencies
└── README.md
```

### File Descriptions

| File | Description |
|---|---|
| `connect_memory.py` | Loads PDFs from `data/`, splits into chunks, generates vector embeddings, and saves FAISS index to `vectorstore/db_faiss/` |
| `create_memory.py` | Main Streamlit web application — loads LLM and vector store, manages chat interface, and generates context-aware responses |
| `medibot.py` | Command-line interface — processes user queries, retrieves relevant document chunks, and generates responses using the Mistral LLM |
| `requirements.txt` | Lists all Python package dependencies (streamlit, faiss, langchain, huggingface, etc.) |

---

## ✅ Prerequisites

Before setting up the project, ensure you have the following:

- **Python 3.8+** — Core programming language
- **Hugging Face API Token** — Required for Mistral-7B model access ([Get your token here](https://huggingface.co/settings/tokens))
- **Git** — Version control
- **pip** — Python package manager
- **4 GB+ RAM** — Required for model inference
- **Internet connection** — For downloading models and dependencies

---

## 🚀 Installation

### Step 1 — Clone the Repository

```bash
git clone https://github.com/prikshitgautam27/AI_powered_healthcare.git
cd AI_powered_healthcare
```

### Step 2 — Create and Activate a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate — macOS/Linux
source venv/bin/activate

# Activate — Windows (Command Prompt)
venv\Scripts\activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Configure Your Hugging Face Token

```bash
# macOS/Linux
export HF_TOKEN="hf_YOUR_HUGGINGFACE_TOKEN"

# Windows — Command Prompt
set HF_TOKEN=hf_YOUR_HUGGINGFACE_TOKEN

# Windows — PowerShell
$env:HF_TOKEN = "hf_YOUR_HUGGINGFACE_TOKEN"
```

### Step 5 — Add Your Medical Documents

Place your PDF files inside the `data/` directory:

```
data/
├── medical_document1.pdf
├── medical_document2.pdf
└── medical_document3.pdf
```

### Step 6 — Build the Vector Database

```bash
python connect_memory.py
```

This processes all PDFs, generates embeddings, and stores the FAISS index in `vectorstore/db_faiss/`.

---

## 💬 Usage

### Option 1 — Streamlit Web Interface (Recommended)

```bash
streamlit run create_memory.py
```

Open your browser and navigate to `http://localhost:8501` to start chatting.

### Option 2 — Command-Line Interface

```bash
python medibot.py
```

---

## 🤝 Contributing

Contributions are welcome! To get started:

1. **Fork** the repository
2. **Create** a feature branch
   ```bash
   git checkout -b feature/YourFeature
   ```
3. **Commit** your changes
   ```bash
   git commit -m "Add YourFeature"
   ```
4. **Push** to your branch
   ```bash
   git push origin feature/YourFeature
   ```
5. **Open** a Pull Request

### Contribution Guidelines

- Follow the [PEP 8](https://pep8.org/) style guide
- Add documentation for any new features
- Test thoroughly before submitting a PR
- Write clear, descriptive commit messages

---

## 📚 Useful Resources

| Resource | Link |
|---|---|
| Mistral Documentation | [docs.mistral.ai](https://docs.mistral.ai) |
| FAISS GitHub | [github.com/facebookresearch/faiss](https://github.com/facebookresearch/faiss) |
| Streamlit Documentation | [docs.streamlit.io](https://docs.streamlit.io) |
| Hugging Face Docs | [huggingface.co/docs](https://huggingface.co/docs) |

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for complete details.

> You are free to use, modify, and distribute this software with proper attribution.

---

## ✍️ Author

**Prikshit Gautam**
GitHub: [@prikshitgautam27](https://github.com/prikshitgautam27)

---

## ⚠️ Disclaimer

This healthcare chatbot is designed **for informational purposes only** and should **not** be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional for any medical concerns.
