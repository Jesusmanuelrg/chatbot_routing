import streamlit as st
from openai import OpenAI
import cohere
import random
from semantic_router import Route
from semantic_router.encoders import CohereEncoder, OpenAIEncoder
import os
from semantic_router.layer import RouteLayer

from filters import *

rl = start_router()

st.set_page_config(page_title="ArtificieAI Chatbot",initial_sidebar_state="collapsed")

##########

co = cohere.Client(st.secrets["COHERE_API_KEY"])

def highlight_snippets_markdown(paragraph, citations):
    highlighted_text = ""
    current_index = 0

    for citation in citations:
        start = citation["start"]
        end = citation["end"]
        text = citation["text"]

        highlighted_text += paragraph[current_index:start]
        highlighted_text += f"`{text}`"
        current_index = end

    highlighted_text += paragraph[current_index:]
    return highlighted_text


def cohere_generation(prompt):
    resources = {}

    with st.status("Answering query..."):
        st.write("Searching for data online...")
        response = co.chat(
        message=prompt,
        max_tokens=4000,
        # perform web search before answering the question. You can also use your own custom connector.
        connectors=[{"id": "web-search"}],
        )

        st.write("Structuring sources...")
        for doc in response.documents:
            resources[doc["title"]] = doc["url"]

        urls_names = list(resources.keys())
        urls_search = list(resources.values())

        formatted_citations = []

        st.write("Grounding result...")
        try:
            for citation in response.citations:
                formatted_citation = {
                    "start": citation.start,
                    "end": citation.end,
                    "text": citation.text
                }
                formatted_citations.append(formatted_citation)
        except:
            pass

        content_high = highlight_snippets_markdown(response.text, formatted_citations)

        st.write("Returning answer...")
        return (response.text, urls_search, content_high, urls_names)


st.info('This is an experimental AI tool, results might be innacurate')
st.markdown("#")

with st.sidebar:
    st.write("Tool created by ArtificieAI")
    st.markdown("***")
    with st.popover("Disclaimer"):
        st.write("This tool uses AI in order to generate a response, take into account that the information is based in data public available online. The answer might be subject to errors either from the AI or websites with wrong information. Consider checking the sources to validate the results")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! Ask me any question you have"}]
    st.session_state["counter"] = 0


look = {"assistant":":material/cognition:", "user": ":material/mood:"}



for msg in st.session_state.messages:
    st.chat_message(msg["role"], avatar=look[msg["role"]]).write(msg["content"])


if st.session_state["counter"] < 2:
    if prompt := st.chat_input():
        co = cohere.Client("Hug1J6GQYuJNOvd99WTrDDyrakDSGrkVY3sPSQMp")
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user", avatar=":material/mood:").write(prompt)

        question_to = rl(prompt)

        if question_to.name == "procedence":
            with st.chat_message("assistant", avatar=":material/cognition:"):
                st.write("I'm a showcase created by ArtificieAI trained to answer your questions")

                st.session_state.messages.append({"role": "assistant", "content": "I'm a showcase created by ArtificieAI trained to answer your questions"})

        elif question_to.name == "medical":
            with st.chat_message("assistant", avatar=":material/cognition:"):
                st.error("Sorry, I'm not a medical doctor")

                st.session_state.messages.append({"role": "assistant", "content": "Sorry, I'm not a medical doctor"})

        elif question_to.name == "chitchat":
            with st.chat_message("assistant", avatar=":material/cognition:"):
                st.write("Hello, everything going great in here, do you have any question?")

                st.session_state.messages.append({"role": "assistant", "content": "Hello, everything going great in here, do you have any question?"})

        elif question_to.name == "confidential":
            with st.chat_message("assistant", avatar=":material/cognition:"):
                st.error("I'm not going to provide any kind of confidential information, my access is limited to public available data")

                st.session_state.messages.append({"role": "assistant", "content": "[Redacted message due to violation of policy]"})

        elif question_to.name == "filter":
            with st.chat_message("assistant", avatar=":material/cognition:"):
                st.session_state["counter"] += 1
                st.error("We do not tolerate discriminatory or offensive language. Your comment has been flagged and reported. Please adhere to our community guidelines and maintain respectful communication.")

            st.session_state.messages.append({"role": "assistant", "content": "[Redacted message due to violation of policy]"})

        else:
            msg, sources, content_high, urls_names = cohere_generation(prompt)

            content = ""

            with st.chat_message("assistant", avatar=":material/cognition:"):
                tab1, tab2 = st.tabs(["Response", "Grounded Response"])
                with tab1:
                    result = st.write(msg)

                with tab2:
                    result = st.write(content_high)

                #result = st.write(msg)

                if len(urls_names) > 1:
                    with st.popover("Sources"):
                        st.subheader("Sources Used")
                        for i in range(len(sources)):
                            with st.container(border=True):
                                st.text(urls_names[i])
                                st.link_button(f"Link {i+1}", sources[i])

                    
                st.session_state.messages.append({"role": "assistant", "content": msg})

else:
    st.session_state["messages"] = []
    st.error("Due to multiple discriminatory remarks, this conversation has been flagged and reported, and the access to the chat has been revoked")
