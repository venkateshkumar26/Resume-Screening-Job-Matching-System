import os

PINECONE_API_KEY=os.getenv("PINECONE_API_KEY")
PINECONE_ENV='gcp-starter'
PINECONE_INDEX='resume-ranker'

EMBEDDING_MODEL="sentence-transformers/all-mpnet-base-v2"
