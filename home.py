import streamlit as st
from openai import OpenAI
import cohere
import random
from semantic_router import Route
from semantic_router.encoders import CohereEncoder, OpenAIEncoder
import os
from semantic_router.layer import RouteLayer

from filters import *
from functions import *

# We initialize the routing that will check the content
rl = start_router()

# Aesthetic for the Streamlit page
st.set_page_config(page_title="ArtificieAI Chatbot",initial_sidebar_state="collapsed")

##########

# API Initialization
co = cohere.Client(st.secrets["COHERE_API_KEY"])

st.info('This is an experimental AI tool, results might be innacurate')
st.markdown("#")

with st.sidebar:
    st.write("Tool created by ArtificieAI")
    st.markdown("***")
    with st.popover("Disclaimer"):
        st.write("This tool uses AI to generate a response, take into account that the information is based on data public available online. The answer might be subject to errors either from the AI or websites with wrong information. Consider checking the sources to validate the results")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! Ask me any question you have"}]
    st.session_state["counter"] = 0


look = {"assistant":":material/cognition:", "user": ":material/mood:"}



for msg in st.session_state.messages:
    st.chat_message(msg["role"], avatar=look[msg["role"]]).write(msg["content"])


if st.session_state["counter"] < 2:
    if prompt := st.chat_input():
        co = cohere.Client(st.secrets["COHERE_API_KEY"])
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user", avatar=":material/mood:").write(prompt)

        question_to = rl(prompt)

        handle_question(question_to, prompt)

else:
    st.session_state["messages"] = []
    st.error("Due to multiple discriminatory remarks, this conversation has been flagged and reported, and the access to the chat has been revoked")
