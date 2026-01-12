from fastapi import FastAPI, UploadFile, File, HTTPException,Query
from typing import List
from vector_store import resume_to_database, query_resumes
import uvicorn
from uuid import uuid4

app = FastAPI()


@app.post("/upload")
async def upload_resumes(namespace:str=Query(...,description="Pinecone namespace"),files: List[UploadFile] = File(...)):
    ids = []
    for file in files:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(400, f"Invalid file: {file.filename}")

        file_bytes = await file.read()
        resume_id = resume_to_database(file_bytes, file.filename,namespace)
        ids.append(resume_id)

    return {"uploaded": len(ids), "resumes": ids}

from pydantic import BaseModel
class jd(BaseModel):
    jd: str

@app.post("/rank")
async def rank_resumes(jd: jd,namespace:str=Query(...,description="Pinecone namespace"),):
    results = query_resumes(jd.jd,namespace)
    return [
        {
            "filename": r[0].metadata["filename"],
            "score": round(r[1], 2)*100
        }
        for r in results
    ]

if __name__=="__main__":
    uvicorn.run(app)
    