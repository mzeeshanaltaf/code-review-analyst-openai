import streamlit as st
import time
import base64
import json


# Function to load lottie file from json
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


# Function to configure sidebar to verify and get the model  api key
def configure_apikey_sidebar():
    api_key = st.sidebar.text_input(f'Enter the OpenAI API Key', type='password',
                                    help='Get API Key from: https://platform.openai.com/api-keys')
    if api_key == '':
        st.sidebar.warning('Enter the API key')
        is_active = False
    elif api_key.startswith('sk-') and (len(api_key) == 51):
        st.sidebar.success('Proceed to uploading the file!', icon='️👉')
        is_active = True
    else:
        st.sidebar.warning('Please enter the correct credentials!', icon='⚠️')
        is_active = False

    return api_key, is_active


# Function to download text content as a file using Streamlit
def text_downloader(raw_text):
    # Generate a timestamp for the filename to ensure uniqueness
    time_str = time.strftime("%Y%m%d-%H%M%S")

    # Encode the raw text in base64 format for file download
    b64 = base64.b64encode(raw_text.encode()).decode()

    # Create a new filename with a timestamp
    new_filename = "code_review_analysis_file_{}_.txt".format(time_str)

    # Create an HTML link with the encoded content and filename for download
    href = f'<a href="data:file/txt;base64,{b64}" download="{new_filename}">Click Here!!</a>'

    return href
