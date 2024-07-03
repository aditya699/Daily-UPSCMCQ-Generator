import streamlit as st
from streamlit_oauth import OAuth2Component
import os
import base64
import json
from datetime import datetime, timedelta
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import Html2TextTransformer
import google.generativeai as genai

# Set environment variables from Streamlit secrets
CLIENT_ID = st.secrets["client_id"]
CLIENT_SECRET = st.secrets["client_secret"]
AUTHORIZE_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
REVOKE_ENDPOINT = "https://oauth2.googleapis.com/revoke"

st.title("GKMCQ.AI")
st.write("Welcome to Government Exam GK MCQ Practice Zone :heart:")

# Sidebar content
st.sidebar.header("Made by Aditya Bhatt")
st.sidebar.image("https://saibaba9758140479.blob.core.windows.net/docs/pic_me.PNG")
st.sidebar.markdown("[Linkedin](https://www.linkedin.com/in/adityaabhatt/)")
st.sidebar.markdown("[Website](https://aiwithaditya.odoo.com/blog)")
st.sidebar.markdown("[Instagram](https://www.instagram.com/your_data_scientist/)")

# Main content image
st.image('static/ui_context.png', width=400)

# Define functions

def generate_dynamic_url():
    today = datetime.today()
    if today.weekday() in [5, 6]:  # 5 is Saturday, 6 is Sunday
        target_date = today - timedelta(days=2)
    else:
        target_date = today - timedelta(days=1)
    url = f'https://www.drishtiias.com/current-affairs-news-analysis-editorials/news-analysis/{target_date.strftime("%d-%m-%Y")}'
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
    query = "Act as an MCQ Generator. Generate 15 MCQs based on the provided context. Ignore unnecessary HTML content and focus on text starting from 'n min read' to 'Infographics'. Exclude all other content. Always Give Answer key in end" + "content" + str(docs_transformed) + "Start With Here are questions you need to practice"
    
    # Generate MCQs
    response = model.generate_content(query)
    
    return response.text

# Authentication process
if 'auth' not in st.session_state:
    oauth2 = OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZE_ENDPOINT, TOKEN_ENDPOINT, TOKEN_ENDPOINT, REVOKE_ENDPOINT)
    result = oauth2.authorize_button(
        name="Continue with Google and Generate Question",
        icon="https://www.google.com.tw/favicon.ico",
        redirect_uri="http://localhost:8501",
        scope="openid email profile",
        key="google",
        extras_params={"prompt": "consent", "access_type": "offline"},
        use_container_width=True,
        pkce='S256',
    )

    if result:
        id_token = result["token"]["id_token"]
        payload = id_token.split(".")[1]
        payload += "=" * (-len(payload) % 4)
        payload = json.loads(base64.b64decode(payload))
        email = payload["email"]
        st.session_state["auth"] = email
        st.session_state["token"] = result["token"]
        
        mcqs = generate_mcqs()
        st.session_state["mcqs"] = mcqs

        st.rerun()
else:
    st.write(f"Logged in as: {st.session_state['auth']}")
    if "mcqs" in st.session_state:
        st.subheader('Generated MCQs:')
        st.write(st.session_state["mcqs"])
    else:
        st.write("No MCQs generated yet. Click the button below to generate.")

    if st.button("Logout"):
        del st.session_state["auth"]
        del st.session_state["token"]
        if "mcqs" in st.session_state:
            del st.session_state["mcqs"]
        st.rerun()

def main():
    if 'auth' in st.session_state:
        # Generate MCQs button
        if st.button('Generate MCQs for Today\'s Current Affairs'):
            mcqs = generate_mcqs()
            st.session_state["mcqs"] = mcqs
            st.subheader('Generated MCQs:')
            st.write(mcqs)
    else:
        st.write("Just Signup and grab a coffee")

if __name__ == '__main__':
    main()
