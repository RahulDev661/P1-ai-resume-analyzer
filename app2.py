import streamlit as st
import pandas as pd
import fitz  # PyMuPDF

# ---------- PAGE SETTINGS ----------
st.set_page_config(page_title="Resume Analyzer", layout="centered")

st.title("🚀 AI Resume Analyzer")
st.write("Upload your resume and get job recommendations instantly")

# ---------- FILE UPLOAD ----------
uploaded_file = st.file_uploader("📄 Upload your Resume (PDF)", type="pdf")

if uploaded_file is not None:
    st.success("File uploaded successfully ✅")

    try:
        # ---------- EXTRACT TEXT ----------
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        
        resume_text = ""
        for page in doc:
            resume_text += page.get_text()

        resume_text = resume_text.lower()

        # ---------- SHOW TEXT ----------
        st.subheader("📄 Extracted Text (Preview)")
        st.write(resume_text[:500])

        # ---------- SKILLS DETECTION ----------
        skills = ["python", "sql", "html", "css", "machine learning", "excel", "javascript", "react"]

        found_skills = [skill for skill in skills if skill in resume_text]

        st.subheader("🧠 Skills Found")
        if found_skills:
            st.write(found_skills)
        else:
            st.write("No common skills detected")

        # ---------- LOAD JOB DATA ----------
        df = pd.read_csv("jobs.csv")

        # ---------- JOB MATCHING WITH SCORE ----------
        st.subheader("💼 Matched Jobs")

        found = False

        for index, row in df.iterrows():
            job_desc = row["description"].lower()

            score = sum(skill in resume_text for skill in job_desc.split())

            if score > 0:
                st.write(f"✅ {row['title']} (Match Score: {score})")
                found = True

        if not found:
            st.warning("❌ No matching jobs found")

    except Exception as e:
        st.error(f"Error: {e}")