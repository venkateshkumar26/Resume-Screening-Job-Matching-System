Problem Statement: Resume formats are unstructured and inconsistent. Keyword-based filtering misses relevant candidates. Manual screening does not scale

Objective:
Build a system that automatically ranks resumes based on their semantic relevance to a job description.

Solution Approach:
Extract text from uploaded PDF resumes
Generate semantic embeddings using a pretrained transformer model
Store resume embeddings in a vector database
Embed the job description
Perform cosine similarity search to rank resumes
Display ranked results in a web interface

System Architecture

Flow:
Resume Upload (Batch),
Text Extraction & Cleaning,
Embedding Generation,
Vector Storage (Pinecone),
Job Description Embedding,
Semantic Similarity Search,
Ranked Output

Tech Stack

Backend: FastAPI, Sentence Transformers (all-mpnet-base-v2), Pinecone (vector database), LangChain, pdfplumber

Frontend: Streamlit

DevOps: Docker, Docker Compose

Features:
Batch resume upload (PDF)
Semantic resume–job matching
Candidate ranking using cosine similarity
Duplicate resume prevention using content hashing
Interactive web UI
Fully containerized frontend and backend

Sample Output
[
  { "filename": "candidate_1.pdf", "score": 0.617 },
  { "filename": "candidate_2.pdf", "score": 0.608 }
]


Higher scores indicate stronger semantic alignment with the job description.

Project Structure
job_matcher/
│
├── backend/
│   ├── app.py
│   ├── vector_store.py
│   ├── resume_ingestion.py
│   ├── jd_ingestion.py
│   ├── config.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── streamlit_app.py
│   ├── Dockerfile
│   └── requirements.txt
│
└── docker-compose.yml

Getting Started
Prerequisites

Docker & Docker Compose

Pinecone account and API key

Clone the Repository
git clone https://github.com/your-username/resume-job-matcher.git
cd resume-job-matcher

Set Environment Variable
export PINECONE_API_KEY=your_pinecone_api_key


(On Windows PowerShell)

setx PINECONE_API_KEY "your_pinecone_api_key"

Run the Application
docker compose build
docker compose up

Access the Services

Frontend (Streamlit):
http://localhost:8501

Backend API (FastAPI Docs):
http://localhost:8000/docs

Design Decisions:
Semantic similarity is used instead of keyword matching. 
Resumes are treated as independent documents. 
Duplicate resumes are prevented using content-based hashing. 
The system assists recruiters; it does not automate hiring decisions. 
Pretrained models are used (no fine-tuning).

Future Enhancements:
Explainable matching (highlight matched skills), 
Skill-based re-ranking, 
Multi-job support using namespaces, 
Resume preview and download, 
Authentication and user roles, 
Cloud deployment (AWS / GCP)
