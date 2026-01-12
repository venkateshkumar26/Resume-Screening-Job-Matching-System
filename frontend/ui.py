import streamlit as st
import requests

UPLOAD_URL = "http://backend:8000/upload"
RANK_URL = "http://backend:8000/rank"

from uuid import uuid4


st.title("Resume Screening & Job Matching System")

st.subheader("Upload Resumes")
resumes = st.file_uploader(
    "Upload PDF resumes",
    type="pdf",
    accept_multiple_files=True
)

st.subheader("Job Description")
jd_text = st.text_area(
    "Paste the job description here",
    height=250
)

if f"{jd_text}" not in st.session_state:
    st.session_state[f"{jd_text}"]=uuid4()

if st.button("Submit resume"):
    if not resumes:
        st.error("Please upload at least one resume.")
    else:
        with st.spinner("Uploading resumes..."):
            files = [
                ("files", (r.name, r.getvalue(), "application/pdf"))
                for r in resumes
            ]
            upload_resp = requests.post(UPLOAD_URL, params={"namespace": st.session_state[f"{jd_text}"]}, files=files)

        if upload_resp.status_code != 200:
            st.error("Failed to upload resumes.")
            st.stop()
        else:
            st.success("Uploaded successfully")
if st.button("Rank candidates"):
    if not jd_text.strip():
        st.error("Please provide a job description.")
    else:
        with st.spinner("Ranking candidates..."):
            rank_resp = requests.post(
                RANK_URL,
                json={"jd": jd_text},
                params={"namespace": st.session_state[f"{jd_text}"]}
            )

        if rank_resp.status_code != 200:
            st.error("Ranking failed.")
            st.stop()

        results = rank_resp.json()
        results.sort(key=lambda x: x["score"], reverse=True)

        st.success("Ranking complete!")

        st.subheader("Ranked Candidates")
        for i, r in enumerate(results, start=1):
            st.write(f"**{i}. {r['filename']}** — Score: `{r['score']}`%")
