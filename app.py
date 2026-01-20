import streamlit as st 
from pdfextractor import text_extractor
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# First lets configure the model 

gemini_api_key = os.getenv('GOOGLE_API_KEY1')
model = ChatGoogleGenerativeAI(
    model = 'gemini-2.5-flash-lite',
    api_key = gemini_api_key,
    temperature = 0.9
)

# Lets create the side bar to upload the resume

st.sidebar.title(':blue[Upload Your Resume (PDF)]')
file = st.sidebar.file_uploader('Resume', type = ['pdf'])
if file:
    file_text = text_extractor(file)
    st.sidebar.success('File Uploaded Successfully')
    

# Create the main page of the application 

st.title(':orange[SKILL MATCH:-] :blue[AI Assisted Skill Matching App]', width='content')
st.markdown('This Application will match and analyze your resume and the job description provided', width='content')

tips = '''
Follow these steps:-
1. Upload your resume (PDF Only) in side bar
2. Copy and paste the job description below
3. Click on submit'''
st.write(tips)

job_desc = st.text_area(':blue[Copy and Paste your job description over here.]', max_chars=5000)

if st.button('Submit'):
    prompt = f'''
    <Role> you are an expert in analyzing resume and matching it with the job description
    <Goal> Match your resume and the job descriptin provided by the applicant and create a report
    <Context> The following content has been provided by the applicant
    * Resume : {file_text}
    * Job Description: {job_desc}
    <Format> The report should follow these steps:
    * Give a brief description of the applicant in 3 to 5 lines.
    * Describe in percentage what are the chances of this resume of getting selected.
    * Need not be the exact percentage, you can give interval of percentage.
    * Give the expected ATS Score along with matching and non matching keywords.
    * Perform SWAT Anaalysis and explain each parameter i.e. strength, Weekness, Oppurinity and threat.
    * Give what all the section in the current resume that are required to be change in order to improve the ATS score and selection percentage
    * Show both current version and improve version of the section in resume.
    * Create two samples resume which can maximize the ATS score and selection percentage.

    <Instruction>
    * Use bullets for explanation wherever possible.
    * Create tables for description wherever required.
    * Strictly do not add any new skill in sample resume.
    * The format of sample resumes should be in such a way that they can be copied and pasted directly in word.
    '''


    response = model.invoke(prompt)
    st.write(response.content)