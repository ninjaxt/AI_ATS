import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

load_dotenv()  # Load all environment variables

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

# Prompt Template
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
input_prompt1 = """
You are an advanced Applicant Tracking System (ATS) designed to analyze resumes and compare it with the input job description. Provide detailed suggestions and actionable tips to enhance the given resume. Focus on optimizing keyword usage, formatting, and content to improve its chances of passing through ATS filters and appealing to hiring managers.
"""
# Streamlit app
st.title("Application Tracking System")
st.text("Improve Your Resume for ATS")
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

submit = st.button("Submit")
submit1 = st.button("How Can I Improve My Skills")

if submit:
    if uploaded_file is not None and jd:
        resume_text = input_pdf_text(uploaded_file)
        input_prompt = input_prompt_template.format(resume_text=resume_text, jd_text=jd)
        response = get_gemini_response(input_prompt)
        st.subheader("ATS Evaluation")
        st.json(response)  # Display response as JSON for clarity

elif submit1:
    if uploaded_file is not None and jd:
        resume_text = input_pdf_text(uploaded_file)
        input_prompt = input_prompt1.format(resume_text=resume_text, jd_text=jd)
        response = get_gemini_response(input_prompt1)
        st.subheader("ATS Evaluation")
        st.write(response) # Display response as JSON for clarity
