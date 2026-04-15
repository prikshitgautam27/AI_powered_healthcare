# AI Powered Healthcare - RAG Chatbot

## Overview

AI Powered Healthcare is a sophisticated Retrieval-Augmented Generation (RAG) chatbot system that combines the power of the Mistral-7B-Instruct-v0.3 Large Language Model with FAISS for efficient similarity search. This intelligent system processes medical documents and provides accurate, context-aware responses to healthcare-related queries.

---

## Technology Stack

| Technology | Purpose |
|-----------|---------|
| **Mistral-7B-Instruct-v0.3** | Advanced language model for intelligent text generation |
| **FAISS** | Facebook AI Similarity Search for fast vector retrieval |
| **Streamlit** | Interactive web interface and user dashboard |
| **Hugging Face** | Model hosting and API integration |
| **LangChain** | Framework for RAG pipeline orchestration |
| **PyPDF2** | PDF document processing and extraction |

---

## Key Features

### Core Capabilities
- **Retrieval-Augmented Generation (RAG)**: Combines LLM capabilities with document retrieval for accurate, context-aware responses
- **Advanced Language Model**: Leverages Mistral-7B-Instruct-v0.3 for sophisticated text generation
- **Fast Vector Search**: FAISS integration enables quick retrieval of relevant document chunks from large knowledge bases
- **Intuitive Web Interface**: Streamlit-based UI for seamless user interaction
- **Multi-Document Processing**: Handles multiple PDF files to build comprehensive knowledge bases
- **Customizable Prompts**: Flexible prompt templates for controlled response generation

### Additional Benefits
- PDF document handling and intelligent chunking
- Efficient vector embedding generation
- Real-time query processing
- Contextual answer generation based on provided documents

---

## Project Structure 

## File Organization

| Location | Component | Function |
|----------|-----------|----------|
| `data/` | Input Documents | Stores PDF files for knowledge base |
| `vectorstore/db_faiss/` | Vector Database | Stores FAISS index and metadata |
| `connect_memory.py` | Processing | Loads PDFs, generates embeddings, builds FAISS index |
| `create_memory.py` | Web Interface | Streamlit application with chat UI |
| `medibot.py` | CLI Interface | Command-line chatbot interaction |
| `requirements.txt` | Dependencies | Python package requirements |

## File Descriptions

### connect_memory.py
- Loads PDF documents from `data/` directory
- Splits documents into text chunks
- Generates vector embeddings
- Creates and stores FAISS index in `vectorstore/db_faiss/`

### create_memory.py
- Main Streamlit web application
- Loads LLM and vector store
- Manages chat interface
- Generates context-aware responses

### medibot.py
- Command-line interface for RAG chatbot
- Processes user queries
- Retrieves relevant documents
- Generates responses using Mistral LLM

### requirements.txt
- Lists all Python package dependencies
- Includes: streamlit, faiss, langchain, huggingface, etc.

## Prerequisites

Before setting up the project, ensure you have:

- **Python 3.8 or higher** - Core programming language
- **Hugging Face API Token** - Access to Mistral-7B model
- **Git** - Version control
- **pip** - Python package manager
- **4GB+ RAM** - For model inference
- **Internet connection** - For downloading models and dependencies

**Note**: Obtain your Hugging Face API token from [Hugging Face Profile Settings](https://huggingface.co/settings/tokens)

---

## Installation Guide

### Step 1: Clone the Repository

```bash
git clone https://github.com/prikshitgautam27/AI_powered_healthcare.git
cd AI_powered_healthcare
```bash
### Step2 
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

### Step 3 : Install Dependencies
pip install -r requirements.txt

### Step 4: Configure Hugging face token

# On Windows (Command Prompt):
set HF_TOKEN=hf_YOUR_HUGGINGFACE_TOKEN

# On Windows (PowerShell):
$env:HF_TOKEN = "hf_YOUR_HUGGINGFACE_TOKEN"

# On macOS/Linux:
export HF_TOKEN="hf_YOUR_HUGGINGFACE_TOKEN"


### Prepare Documents
AI_powered_healthcare/
├── data/
│   ├── medical_document1.pdf
│   ├── medical_document2.pdf
│   └── medical_document3.pdf
├── vectorstore/
├── connect_memory.py
├── create_memory.py
├── medibot.py
├── requirements.txt
└── README.md

### step6: build Vector DB
python connect_memory.py


##USAGE
streamlit run create_memory.py(option1)
python medibot.py(option2)

Contributinns
Welcome contributions! To contribute:

Fork the repository
Create a feature branch (git checkout -b feature/YourFeature)
Commit changes (git commit -m 'Add YourFeature')
Push to branch (git push origin feature/YourFeature)
Open a Pull Request
##Contribution Guidelines
Follow PEP 8 style guide
Add documentation for new features
Test thoroughly before submitting PR
Include clear commit messages
License
This project is licensed under the MIT License. See the LICENSE file for complete details.

Summary: You are free to use, modify, and distribute this software with attribution.

Support & Documentation
For additional help:

Review the Mistral Documentation
Check FAISS GitHub Repository
Visit Streamlit Documentation
Consult Hugging Face Docs
Authors
Prikshit Gautam

GitHub: @prikshitgautam27
Disclaimer
This healthcare chatbot is designed for informational purposes only and should not be used as a substitute for professional medical advice. Always consult qualified healthcare professionals for medical concerns.
