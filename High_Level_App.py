# app.py

import streamlit as st
from datetime import datetime,timedelta
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import Html2TextTransformer
import google.generativeai as genai
yesterday = (datetime.today() - timedelta(days=1)).strftime('%d-%m-%Y')
def generate_dynamic_url():
    
    yesterday = (datetime.today() - timedelta(days=1)).strftime('%d-%m-%Y')
    url = f'https://www.drishtiias.com/current-affairs-news-analysis-editorials/news-analysis/{yesterday}'
    return url

def generate_mcqs():
    url = generate_dynamic_url()
    
    # Load HTML
    loader = AsyncHtmlLoader([url])
    docs = loader.load()
    
    # Transform HTML to text
    html2text = Html2TextTransformer()
    docs_transformed = html2text.transform_documents(docs)
    
    # Configure and use GenerativeAI model
    GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-pro')
    query = "Act as an MCQ Generator. Generate 15 MCQs based on the provided context. Ignore unnecessary HTML content and focus on text starting from 'n min read' to 'Infographics'. Exclude all other content. Always Give Answer key in end" + "content" + str(docs_transformed)+"Start With Here are questions you need to practice"
    
    # Generate MCQs
    response = model.generate_content(query)
    
    return response.text

def main():
    st.title(str('UPSC MCQ Generator for today i.e ')+str(yesterday))
    st.write("This returns MCQ for yesterday")
    
    # Generate MCQs button
    if st.button('Generate MCQs for Today\'s Current Affairs'):
        mcqs = generate_mcqs()
        st.subheader('Generated MCQs:')
        st.write(mcqs)

if __name__ == '__main__':
    main()
