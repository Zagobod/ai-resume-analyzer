import streamlit as st
from utils import calculate_match, extract_text_from_pdf, get_missing_keywords

st.title("AI Resume Analyzer")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
job_desc = st.text_area("Paste job description")

resume_text = ""

if uploaded_file is not None:
    resume_text = extract_text_from_pdf(uploaded_file)
    st.success("Resume uploaded successfully!")

if st.button("Analyze"):
    if resume_text and job_desc:
        score = calculate_match(resume_text, job_desc)
        missing_keywords = get_missing_keywords(resume_text, job_desc)

        st.success(f"Match Score: {score}%")

        st.subheader("Missing Keywords")
        if missing_keywords:
            st.write(", ".join(missing_keywords))
        else:
            st.write("No major keywords missing")
    else:
        st.warning("Please upload resume and enter job description")
