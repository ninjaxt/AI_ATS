import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_text)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Initialize session state for profile
if 'profile' not in st.session_state:
    st.session_state.profile = {
        'name': '',
        'email': '',
        'profession': '',
        'experience': '0-2 years',
        'skills': '',
        'preferred_roles': '',
        'resume_count': 0,
        'analyses_run': 0
    }

# Prompt Templates
input_prompt_template = """
Hey, act like a skilled and experienced ATS (Applicant Tracking System) 
with a deep understanding of tech fields like software engineering, data science, data analysis, and big data engineering. 
Your task is to evaluate the resume based on the given job description. 
Consider that the job market is very competitive and provide the best assistance for improving the resume. 
Assign a percentage match based on the job description and list the missing keywords with high accuracy.
Resume: {resume_text}
Description: {jd_text}

I want the response in one single string with the structure:
{{"JD Match":"%","MissingKeywords":[],"Profile Summary":""}}
"""

input_prompt_skills = """
You are an advanced Applicant Tracking System (ATS) designed to analyze resumes and compare it with the input job description. 
Provide detailed suggestions and actionable tips to enhance the given resume. 
Focus on optimizing keyword usage, formatting, and content to improve its chances of passing through ATS filters and appealing to hiring managers.
Resume: {resume_text}
Description: {jd_text}
"""

# Set page configuration
st.set_page_config(
    page_title="ATS Resume Scanner",
    page_icon="📄",
    layout="wide"
)

# Sidebar
with st.sidebar:
    st.title("Profile")
    
    # Profile Section
    with st.expander("✏️ Edit Profile", expanded=True):
        st.session_state.profile['name'] = st.text_input("Full Name", st.session_state.profile['name'])
        st.session_state.profile['email'] = st.text_input("Email", st.session_state.profile['email'])
        st.session_state.profile['profession'] = st.text_input("Current Profession", st.session_state.profile['profession'])
        st.session_state.profile['experience'] = st.select_slider(
            "Years of Experience",
            options=['0-2 years', '2-5 years', '5-8 years', '8-12 years', '12+ years'],
            value=st.session_state.profile['experience']
        )
        st.session_state.profile['skills'] = st.text_area("Key Skills (comma-separated)", st.session_state.profile['skills'])
        st.session_state.profile['preferred_roles'] = st.text_area("Preferred Job Roles", st.session_state.profile['preferred_roles'])

    # Profile Statistics
    with st.expander("📊 Your Statistics", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Resumes Analyzed", st.session_state.profile['resume_count'])
        with col2:
            st.metric("Analyses Run", st.session_state.profile['analyses_run'])
    
    st.divider()
    
    # About Section
    st.title("About")
    st.markdown("""
    ### ATS Resume Scanner
    This tool helps you:
    - Analyze your resume against job descriptions
    - Get ATS compatibility score
    - Identify missing keywords
    - Receive improvement suggestions
    
    ### How to Use
    1. Complete your profile
    2. Paste the job description
    3. Upload your resume (PDF)
    4. Choose analysis type:
        - Basic ATS Evaluation
        - Detailed Skill Analysis
    
    ### Tips
    - Use PDF format for best results
    - Ensure clear formatting in your resume
    - Include relevant keywords from the job description
    
    ### Contact
    For support or feedback, reach out at:
    - Email: support@atsscanner.com
    - GitHub: [Project Repository](https://github.com/atsscanner)
    """)

# Main content
if st.session_state.profile['name']:
    st.title(f"Welcome, {st.session_state.profile['name']}! 👋")
else:
    st.title("📄 ATS Resume Scanner")
st.markdown("### Optimize Your Resume for Applicant Tracking Systems")

# Create two columns for input
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Job Description")
    jd = st.text_area("Paste the job description here", height=300)

with col2:
    st.markdown("### Resume Upload")
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF format)",
        type="pdf",
        help="Please upload your resume in PDF format for best results"
    )

# Analysis options
st.markdown("### Choose Analysis Type")
col3, col4 = st.columns(2)

with col3:
    basic_analysis = st.button("🎯 Basic ATS Evaluation", use_container_width=True)
with col4:
    detailed_analysis = st.button("🔍 Detailed Skill Analysis", use_container_width=True)

# Results section
if basic_analysis or detailed_analysis:
    if uploaded_file is not None and jd:
        with st.spinner("Analyzing your resume..."):
            resume_text = input_pdf_text(uploaded_file)
            
            # Update statistics
            st.session_state.profile['resume_count'] += 1
            st.session_state.profile['analyses_run'] += 1
            
            if basic_analysis:
                input_prompt = input_prompt_template.format(resume_text=resume_text, jd_text=jd)
                response = get_gemini_response(input_prompt)
                st.markdown("### 📊 ATS Evaluation Results")
                st.json(response)
                
            elif detailed_analysis:
                input_prompt = input_prompt_skills.format(resume_text=resume_text, jd_text=jd)
                response = get_gemini_response(input_prompt)
                st.markdown("### 📋 Detailed Skill Analysis")
                st.markdown(response)
                
    else:
        st.error("Please upload both a resume and provide a job description.")

# Recent Activity (if profile exists)
if st.session_state.profile['name']:
    st.markdown("### 📅 Recent Activity")
    st.info(f"""
    - Total Resumes Analyzed: {st.session_state.profile['resume_count']}
    - Total Analyses Run: {st.session_state.profile['analyses_run']}
    - Current Role: {st.session_state.profile['profession']}
    - Experience Level: {st.session_state.profile['experience']}
    """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Made with ❤️ for job seekers</p>
        <p>© 2024 ATS Resume Scanner</p>
    </div>
    """,
    unsafe_allow_html=True
)

