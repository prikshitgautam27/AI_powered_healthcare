# AI_powered_healthcare
🤖 RAG Chatbot with Mistral and FAISS
This project implements a Retrieval-Augmented Generation (RAG) chatbot that leverages the Mistral-7B-Instruct-v0.3 Large Language Model (LLM) and FAISS for efficient similarity search. The chatbot can answer questions based on information extracted from your provided PDF documents. It features a user-friendly Streamlit interface for interactive conversations.

✨ Features
Retrieval-Augmented Generation (RAG): Combines the power of an LLM with information retrieved from your documents to provide accurate and context-aware answers.

Mistral-7B-Instruct-v0.3: Utilizes the Mistral LLM via Hugging Face for powerful text generation.

FAISS Integration: Employs FAISS (Facebook AI Similarity Search) for fast and efficient vector similarity search, enabling quick retrieval of relevant document chunks.

Streamlit UI: Provides an intuitive web interface for seamless interaction with the chatbot.

PDF Document Processing: Capable of loading and processing multiple PDF files to create a searchable knowledge base.

Custom Prompt Template: Allows for flexible control over the LLM's response generation based on the provided context.

🚀 Getting Started
Follow these steps to set up and run the RAG Chatbot.

Prerequisites
Python 3.8+

A Hugging Face API Token. You can obtain one from your Hugging Face profile settings.

Installation
Clone the repository:

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

Create a virtual environment (recommended):

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install the dependencies:

pip install -r requirements.txt

Setup
Place your PDF documents:
Create a directory named data in the root of your project and place all the PDF files you want the chatbot to learn from inside this directory.

your-repo-name/
├── data/
│   ├── document1.pdf
│   └── document2.pdf
├── connect_memory.py
├── create_memory.py
├── medibot.py
└── requirements.txt

Set your Hugging Face API Token:
The application requires your Hugging Face API token to access the Mistral LLM. Set it as an environment variable:

export HF_TOKEN="hf_YOUR_HUGGINGFACE_TOKEN"

Replace "hf_YOUR_HUGGINGFACE_TOKEN" with your actual token. For persistent setting, add this line to your .bashrc, .zshrc, or equivalent profile file.

Create the Vector Store:
This step processes your PDF documents, creates text chunks, generates embeddings, and stores them in a FAISS vector database.

python connect_memory.py

This will create a vectorstore/db_faiss directory containing your vector database.

💡 Usage
You can interact with the chatbot in two ways: via a Streamlit web application or directly through the command line.

🌐 Streamlit Web Application (Recommended)
To launch the interactive chatbot UI:

streamlit run create_memory.py

This will open the Streamlit application in your web browser, usually at http://localhost:8501. You can then type your questions in the chat interface.

💻 Command Line Interface (CLI)
For direct interaction via the terminal:

python medibot.py

The script will prompt you to "Write Query Here: ". Enter your question, and the chatbot will provide a response.

📁 Project Structure
data/: Directory to store your input PDF documents.

vectorstore/db_faiss/: Directory where the FAISS vector database is stored after processing.

connect_memory.py: Script responsible for loading PDF documents, splitting them into chunks, generating embeddings, and building the FAISS vector store.

create_memory.py: The main script for the Streamlit web application. It sets up the LLM, loads the vector store, and handles the chat interface.

medibot.py: A command-line interface script for direct interaction with the RAG model.

requirements.txt: Lists all the Python dependencies required to run the project.

🤝 Contributing
Contributions are welcome! If you have suggestions for improvements or new features, please feel free to open an issue or submit a pull request.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details (you might need to create this file if it doesn't exist).
