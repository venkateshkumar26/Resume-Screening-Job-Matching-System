from pinecone import Pinecone,ServerlessSpec
from config import *
from backend.resume_ingestion import load_resume
from jd_ingestion import load_jd
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from uuid import uuid4

embedder = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
pc = Pinecone(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
index = pc.Index(PINECONE_INDEX)

import hashlib

def compute_text_hash(text: str) -> str:
    normalized = " ".join(text.lower().split())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

def resume_to_database(file_bytes: bytes, filename: str,namespace: str) -> dict:
    resume_data = load_resume(file_bytes)
    resume_text = resume_data["text"]

    resume_hash = compute_text_hash(resume_text)

    db = PineconeVectorStore(
        index=index,
        namespace=namespace,
        embedding=embedder
    )

    existing = index.fetch(
        ids=[resume_hash],
        namespace=namespace
    )

    if existing.vectors:
        return {
            "status": "duplicate",
            "resume_id": resume_hash,
            "filename": filename
        }

    db.add_texts(
        texts=[resume_text],
        ids=[resume_hash],
        metadatas=[{"filename": filename}]
    )

    return {
        "status": "uploaded",
        "resume_id": resume_hash,
        "filename": filename
    }


def query_resumes(jd_text: str, namespace: str, top_k: int = 10):
    jd_cleaned = load_jd(jd_text)["job_description"]
    db = PineconeVectorStore(
        index=index,
        namespace=namespace,
        embedding=embedder
    )

    return db.similarity_search_with_score(jd_cleaned, k=top_k)
