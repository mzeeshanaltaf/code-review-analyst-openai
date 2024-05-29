import streamlit as st
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

