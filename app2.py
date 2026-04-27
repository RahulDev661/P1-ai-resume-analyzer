import streamlit as st
import pandas as pd
import fitz  # PyMuPDF
import re

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AI Resume Intelligence", 
    page_icon="🎯", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- MODERN STYLING ----------
st.markdown("""
    <style>
    /* Main background and glassmorphism effect */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    
    /* Custom Card Design */
    .job-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    .job-card:hover {
        transform: translateY(-5px);
        border: 1px solid #6366f1;
    }
    
    /* Skill Badge */
    .skill-tag {
        display: inline-block;
        background: #6366f1;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- LOGIC FUNCTIONS ----------
def extract_text_from_pdf(file):
    """Extracts and cleans text from uploaded PDF."""
    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = " ".join(page.get_text() for page in doc)
        return text.strip()
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

def get_matches(resume_text, df):
    """Calculates matching scores based on keyword intersection."""
    resume_words = set(re.findall(r'\w+', resume_text.lower()))
    matches = []
    
    for _, row in df.iterrows():
        job_keywords = set(row["description"].lower().split())
        # Calculate intersection score
        common_skills = job_keywords.intersection(resume_words)
        score = len(common_skills)
        
        if score > 0:
            matches.append({
                "title": row["title"],
                "score": score,
                "skills": list(common_skills)[:5] # Show top 5 matching keywords
            })
    
    return sorted(matches, key=lambda x: x['score'], reverse=True)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3858/3858684.png", width=100)
    st.title("Settings")
    st.markdown("---")
    uploaded_file = st.file_uploader("Upload your Resume (PDF)", type="pdf")
    st.info("The AI will analyze your skills against available job descriptions.")

# ---------- MAIN UI ----------
st.markdown("<h1 style='text-align: center; color: #818cf8;'>🎯 AI Resume Intelligence</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Unlock your career potential with smart matching</p>", unsafe_allow_html=True)
st.write("---")

if uploaded_file:
    with st.spinner("Analyzing your profile..."):
        text = extract_text_from_pdf(uploaded_file)
        
        if text:
            col1, col2 = st.columns([1, 1.5], gap="large")
            
            with col1:
                st.subheader("📝 Analysis Summary")
                with st.expander("View Extracted Text"):
                    st.write(text[:1000] + "...")
                
                # Define skill library
                skill_library = ["python", "sql", "aws", "react", "machine learning", "tableau", "excel", "docker"]
                found = [s for s in skill_library if s in text.lower()]
                
                st.write("**Top Skills Identified:**")
                if found:
                    html_tags = "".join([f"<span class='skill-tag'>{s.upper()}</span>" for s in found])
                    st.markdown(html_tags, unsafe_allow_html=True)
                else:
                    st.warning("No specific technical skills identified.")

            with col2:
                st.subheader("💼 Recommended Opportunities")
                try:
                    df = pd.read_csv("jobs.csv")
                    results = get_matches(text, df)
                    
                    if results:
                        for job in results:
                            st.markdown(f"""
                                <div class="job-card">
                                    <h3 style='margin:0; color:#818cf8;'>{job['title']}</h3>
                                    <p style='color:#94a3b8;'>Match Strength: <b>{job['score']} points</b></p>
                                    <div style='margin-top:10px;'>
                                        {' '.join([f"<span style='font-size:10px; opacity:0.8;'>• {sk}</span>" for sk in job['skills']])}
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.error("No direct matches found. Try updating your resume with more keywords.")
                except FileNotFoundError:
                    st.error("Dataset 'jobs.csv' not found. Please ensure the file exists.")
else:
    # Empty State
    st.container()
    st.image("https://illustrations.popsy.co/white/searching.svg", width=400)
    st.markdown("<h3 style='text-align: center; color: #64748b;'>Waiting for your resume...</h3>", unsafe_allow_html=True)
