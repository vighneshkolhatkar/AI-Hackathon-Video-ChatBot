import openai
import os
import streamlit as st
from streamlit_chat import message
from streamlit_extras.add_vertical_space import add_vertical_space
from dotenv import load_dotenv
load_dotenv()
import os
openai.api_key = os.getenv('OPENAI_API_KEY')
import videoData
import random

#starter messages prompt
st.set_page_config(page_title="Video-chatbot- An LLM-powered app")

# Sidebar contents
with st.sidebar:
    st.title('🤗💬 Interactive AI App to save your time watching all the tutorial videos')
    st.markdown('''
    ## About
    You can interact with me and get to know a lot of stuff based on the videos you provide me to learn from. 
    This app is an LLM-powered chatbot built using:
    - OpenAI GPT models
    - Youtube Video Transcription using Whisper by OpenAI
    - LLM model
    ''')
    add_vertical_space(5)
    st.write('*Feel free to play around and provide feedback')

##


def gpt_response(messages):
    response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages
                    )
    content = response['choices'][0]['message']['content']
    role = response['choices'][0]['message']['role']
    update_chat(messages, role, content)
    return content


def update_chat(messages, role, content):
    messages.append({"role":role, "content":content})
    return messages

def generate_response(content, is_url, messages):
    if is_url:
        content = videoData.transcribe(content)
        update_chat(messages,"user", content)
        AI_response = gpt_response(messages)
    else:
        #get previous context from session variable
        print(st.session_state.generated)
        prevContext = ""
        for elem in st.session_state.generated:
            prevContext += elem
        update_chat(messages,"system", prevContext)
        AI_response = gpt_response(messages)
    return AI_response


# Generate empty lists for generated and past.
## generated stores AI generated responses
if 'generated' not in st.session_state:
    st.session_state['generated'] = ['Hi, How may I help you with your video?']
## past stores User's questions
if 'past' not in st.session_state:
    st.session_state['past'] = ['']

# User input
## Function for taking user provided prompt as input
def get_text():
    key=random.randint(0,10000)
    input_text = st.text_input("You: ", "", key="input")
    return input_text


def chatBot():
    messages=[{"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Vighnesh here, wanted to learn some stuff"},
        {"role": "assistant", "content": "Sure, provide me the URL to the video and I'll store the context"},
        ]
    user_input = get_text()
    is_url = False
    if user_input:
        if "youtube.com/watch?v" in user_input:
            is_url = True
            output = generate_response(user_input, is_url, messages)
            # store the output 
            st.session_state.past.append(user_input)
            st.session_state.generated.append(output)
            is_url = False
            # user_input = get_text()
        output = generate_response(user_input, is_url, messages)
        # store the output 
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)

    if st.session_state['generated']:
        
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

chatBot()