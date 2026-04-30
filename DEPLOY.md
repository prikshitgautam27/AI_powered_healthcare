# Deploying to Streamlit Community Cloud

## Step 1 - Get Free Groq API Key
1. Go to https://console.groq.com
2. Sign up (free, no credit card)
3. Click "Create API Key"
4. Copy the key (starts with gsk_...)

## Step 2 - Prepare GitHub Repo
1. Create a new GitHub repository
2. Upload ALL project files EXCEPT:
   - vectorstore/  (too large, rebuild on cloud)
   - data/*.pdf    (optional, see note below)
   - .env
   - .streamlit/secrets.toml

Files to commit:
   app.py
   rag_pipeline.py
   vector_store.py
   pdf_ingestion.py
   requirements.txt
   .streamlit/config.toml
   .gitignore
   README.md

## Step 3 - Handle the PDF on Cloud
Option A (Recommended): Commit the PDF to the repo
  - Just upload your PDF to the data/ folder in GitHub
  - Add a startup script to run pdf_ingestion.py on first launch

Option B: Host PDF on Google Drive
  - Add gdown to requirements.txt
  - Add download code to pdf_ingestion.py

## Step 4 - Deploy on Streamlit Cloud
1. Go to https://share.streamlit.io
2. Click "New app"
3. Connect your GitHub account
4. Select your repository
5. Set Main file path: app.py
6. Click "Advanced settings"
7. Under "Secrets" paste:
   GROQ_API_KEY = "gsk_your_actual_key_here"
8. Click "Deploy!"

## Step 5 - Build Vector Store on Cloud
After deploy, open your app URL and click
"Rebuild Vector Store" in the sidebar.

## Done!
Your app is live at:
https://your-app-name.streamlit.app
