# 🚀 HireSense AI

**AI-Powered Recruitment Intelligence Platform**

HireSense AI is a smart recruitment platform that automates resume screening, ATS analysis, candidate ranking, semantic search, recruiter assistance, and hiring analytics using AI, Vector Search, and RAG.

## ✨ Features

* 📄 Resume Upload (Single, Multiple, ZIP)
* 🤖 AI Resume Parsing with Gemini
* 🔍 Semantic Candidate Search
* 📊 ATS Resume Analysis
* 🏆 Candidate Ranking Engine
* ✅ Shortlist / Hold / Reject Workflow
* 📈 Recruitment Analytics Dashboard
* 💬 RAG Recruiter Chatbot
* 🎙 Voice Recruiter Assistant
* 🗄 Supabase + ChromaDB Integration
* 👥 Multi-User Ready Architecture

## 🛠 Tech Stack

**Frontend**

* Streamlit

**Backend**

* Python

**Database**

* Supabase (PostgreSQL)

**Vector Database**

* ChromaDB

**AI Models**

* Gemini 2.5 Flash
* MXBAI Embed Large
* Whisper
* gTTS

**Libraries**

* Sentence Transformers
* Scikit-Learn
* Pandas
* Plotly
* pdfminer.six

📂 Project Structure
HireSense-AI/

├── frontend/
│   ├── app.py
│   └── pages/
│
├── backend/
│   ├── services/
│   ├── utils/
│   ├── auth/
│   └── database/
│
├── chromadb_store/
│
├── .env
│
├── requirements.txt
│
└── README.md

## 🚀 Run Locally

```bash
git clone <repository-url>

cd HireSense-AI

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

streamlit run frontend/app.py
```

## 📌 Project Highlights

* AI-powered resume intelligence
* Semantic candidate discovery
* ATS-aware recruitment workflow
* Voice-enabled recruiter assistant
* Analytics-driven hiring decisions
* Built using LLMs, RAG, Vector Search, and AI Automation


