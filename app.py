'''
Author    - Aditya Bhatt
Date      - 30-06-2025 10:05 AM

Objectives-
Create an engaging and informative home page for GKMCQ.AI, a platform for government exam GK MCQ practice.

Comments  -
This is the main home page of the application.
'''

import streamlit as st
from streamlit_oauth import OAuth2Component
import os
import base64
import json
# create an OAuth2Component instance
CLIENT_ID = st.secrets["client_id"]
CLIENT_SECRET = st.secrets["client_secret"]
AUTHORIZE_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
REVOKE_ENDPOINT = "https://oauth2.googleapis.com/revoke"
# Set the title of the app
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

# User navigation buttons
st.write("## Get Started")
login = st.button("Login")
signup = st.button("Signup")
continue_without_signup = st.button("Continue Without Signup")

# Conditional navigation based on user choice
if login:
    st.write("Redirecting to login page...")
    # Implement your login page redirection here
elif signup:
    st.write("Redirecting to signup page...")
    if "auth" not in st.session_state:
            # create a button to start the OAuth2 flow
            oauth2 = OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZE_ENDPOINT, TOKEN_ENDPOINT, TOKEN_ENDPOINT, REVOKE_ENDPOINT)
            result = oauth2.authorize_button(
                name="Continue with Google",
                icon="https://www.google.com.tw/favicon.ico",
                redirect_uri="http://localhost:8501",
                scope="openid email profile",
                key="google",
                extras_params={"prompt": "consent", "access_type": "offline"},
                use_container_width=True,
                pkce='S256',
            )
    
            if result:
                st.write(result)
                # decode the id_token jwt and get the user's email address
                id_token = result["token"]["id_token"]
                # verify the signature is an optional step for security
                payload = id_token.split(".")[1]
                # add padding to the payload if needed
                payload += "=" * (-len(payload) % 4)
                payload = json.loads(base64.b64decode(payload))
                email = payload["email"]
                print("User Email" ,email)
                st.session_state["auth"] = email
                st.session_state["token"] = result["token"]
                st.rerun()
    else:
        st.write("You are logged in!")
        st.write(st.session_state["auth"])
        st.write(st.session_state["token"])
        if st.button("Logout"):
            del st.session_state["auth"]
            del st.session_state["token"]
elif continue_without_signup:
    st.write("Continuing without signup...")
    # Implement your logic for continuing without signup here
else:
    st.write("Please choose an option to proceed.")

# Footer message or additional information
st.markdown("---")
st.write("GKMCQ.AI is your one-stop solution for practicing government exam GK MCQs. Improve your knowledge, track your progress, and succeed in your exams!")

