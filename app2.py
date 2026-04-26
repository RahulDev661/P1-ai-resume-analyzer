import streamlit as st
import pandas as pd
import fitz  # PyMuPDF

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="AI Resume Analyzer", page_icon="🚀", layout="wide")

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
.main {
    background-color: #0f172a;
    color: white;
}
.stButton>button {
    background-color: #4f46e5;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}
.card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("""
<h1 style='text-align: center;'>🚀 AI Resume Analyzer</h1>
<p style='text-align: center;'>Upload your resume and get smart job recommendations</p>
""", unsafe_allow_html=True)

# ---------- LAYOUT ----------
col1, col2 = st.columns([1, 2])

# ---------- FILE UPLOAD ----------
with col1:
    st.markdown("### 📄 Upload Resume")
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")

# ---------- MAIN OUTPUT ----------
with col2:
    if uploaded_file is not None:
        st.success("File uploaded successfully ✅")

        try:
            # ---------- EXTRACT TEXT ----------
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            resume_text = "".join(page.get_text() for page in doc).lower()

            # ---------- PREVIEW ----------
            st.markdown("### 📄 Resume Preview")
            st.markdown(f"<div class='card'>{resume_text[:500]}...</div>", unsafe_allow_html=True)

            # ---------- SKILLS DETECTION ----------
            skills = ["python", "sql", "html", "css", "machine learning", "excel", "javascript", "react"]
            found_skills = [skill for skill in skills if skill in resume_text]

            st.markdown("### 🧠 Skills Detected")
            if found_skills:
                skill_cols = st.columns(len(found_skills))
                for i, skill in enumerate(found_skills):
                    skill_cols[i].success(skill.upper())
            else:
                st.warning("No common skills detected")

            # ---------- LOAD JOB DATA ----------
            df = pd.read_csv("jobs.csv")

            # ---------- JOB MATCHING ----------
            st.markdown("### 💼 Job Matches")

            matches = []
            for _, row in df.iterrows():
                job_desc = row["description"].lower()
                score = sum(skill in resume_text for skill in job_desc.split())
                if score > 0:
                    matches.append((row['title'], score))

            if matches:
                matches = sorted(matches, key=lambda x: x[1], reverse=True)
                for title, score in matches:
                    st.markdown(f"""
                    <div class='card'>
                        <h4>✅ {title}</h4>
                        <p>Match Score: <b>{score}</b></p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("❌ No matching jobs found")

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.info("⬅️ Upload a resume to get started")

