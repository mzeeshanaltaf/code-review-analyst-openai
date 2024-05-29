from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from streamlit_lottie import st_lottie
from io import StringIO
from util import *
import time

PROGRAMMING_LANG = {"Python": ".py", "C++": "cpp", "Java": ".java", "JavaScript": ".js"}

# *** PAGE SETUP ***

# Page configuration
page_title = "AI Code Reviewer"
page_icon = ":robot_face:"
st.set_page_config(page_title=page_title, page_icon=page_icon, layout="centered")

# Load the lottie file
lottie_yt = load_lottiefile("code_review.json")
st_lottie(lottie_yt, speed=1, reverse=False, loop=True, quality="high", height=200, width=600, key=None)

# Setup page title
st.title("AI Code Reviewer")
st.write("*Streamline code quality with AI-powered code reviews.*")

# *** SIDEBAR Functionality ***

# Configure the API key
st.sidebar.title("Config️uration Options")
api_key, is_active = configure_apikey_sidebar()

# Choose the programing language
st.sidebar.subheader("Programing Language")
pro_language = st.sidebar.selectbox("Select the Programming Language", list(PROGRAMMING_LANG.keys()),
                                    disabled=not is_active)

# *** MAIN PAGE Functionality ***

st.subheader(f"Please upload the {pro_language} file:")

# Capture the file data
data = st.file_uploader(f"Upload {pro_language} file", type=PROGRAMMING_LANG[pro_language],
                        disabled=not is_active)

button = st.button("Start Code Review", type="primary", disabled=not data)

if button:
    # Create a StringIO object and initialize it with the decoded content of 'data'
    stringio = StringIO(data.getvalue().decode('utf-8'))

    # Read the content of the StringIO object and store it in the variable 'read_data'
    fetched_data = stringio.read()

    # Initialize a ChatOpenAI instance with the specified model name "gpt-3.5-turbo" and a temperature of 0.9.
    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.9, openai_api_key=api_key)

    # Create a SystemMessage instance with the specified content, providing information about the assistant's role.
    systemMessage = SystemMessage(
        content=f"You are a code review assistant. Provide detailed suggestions to improve the given {pro_language} "
                f"code along with mentioning the existing code line by line with proper indent")

    # Create a HumanMessage instance with content read from some data source.
    humanMessage = HumanMessage(content=fetched_data)

    # Call the chat method of the ChatOpenAI instance, passing a list of messages containing the system and
    # human messages.
    with st.spinner("Reviewing Code ..."):
        finalResponse = chat.invoke([systemMessage, humanMessage])

        st.subheader("AI Assistant Feedback")

        # Display review comments
        st.markdown(finalResponse.content)

        st.subheader('Download File')

        # Generate a timestamp for the filename to ensure uniqueness
        time_str = time.strftime("%Y%m%d-%H%M%S")

        # Create a new filename with a timestamp
        new_filename = "code_review_analysis_file_{}_.txt".format(time_str)

        st.download_button(label='Download File', data=finalResponse.content, file_name=new_filename, type="primary")
