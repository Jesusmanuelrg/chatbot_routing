import streamlit as st
import cohere


def highlight_snippets_markdown(paragraph: str, citations: list[dict[str, int | str]]) -> str:
    """
    Highlight snippets in a paragraph based on the provided citations.

    Args:
        paragraph (str): The original text where snippets must be highlighted.
        citations (list[dict[str, int | str]]): A list of dictionaries, each containing:
            - 'start' (int): The starting index of the snippet to be highlighted.
            - 'end' (int): The ending index of the snippet to be highlighted.
            - 'text' (str): The snippet's text to be highlighted.

    Returns:
        str: The paragraph with the specified snippets highlighted using Markdown syntax.
    """
    highlighted_text = ""
    current_index = 0

    for citation in citations:
        start = citation["start"]
        end = citation["end"]
        text = citation["text"]

        # Append text before the snippet
        highlighted_text += paragraph[current_index:start]
        # Append the highlighted snippet
        highlighted_text += f"`{text}`"
        # Update the current index to the end of the snippet
        current_index = end

    # Append any remaining text after the last snippet
    highlighted_text += paragraph[current_index:]
    return highlighted_text



def cohere_generation(prompt: str) -> tuple[str, list[str], str, list[str]]:
    """
    Generates a response using the Cohere API based on the given prompt, 
    performs a web search for supporting data, and highlights citations in the response text.

    Args:
        prompt (str): The input prompt/question to be answered by the Cohere API.

    Returns:
        tuple[str, list[str], str, list[str]]:
            - response.text (str): The generated response from the Cohere API.
            - urls_search (list[str]): URLs of the sources used.
            - content_high (str): The response text with highlighted citations in Markdown.
            - urls_names (list[str]): A list of the titles of the sources used.
    """
    resources = {}

    with st.spinner("Answering query..."):
        st.write("Searching for data online...")
        
        # Assuming `co` is an instance of `CohereClient`
        response = co.chat(
            message=prompt,
            max_tokens=4000,
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
        except AttributeError:
            st.error("No citations found in the response.")

        content_high = highlight_snippets_markdown(response.text, formatted_citations)

        st.write("Returning answer...")
        return response.text, urls_search, content_high, urls_names


def handle_response(role: str, avatar: str, message: str, error: bool = False, increment_counter: bool = False):
    """
    Handles the chat response for the assistant by displaying the appropriate message and updating the session state.

    Args:
        role (str): The role of the message sender (e.g., "assistant").
        avatar (str): The avatar to display with the message.
        message (str): The content of the message to display.
        error (bool, optional): Whether to display the message as an error. Defaults to False.
        increment_counter (bool, optional): Whether to increment the counter in session state. Defaults to False.
    """
    with st.chat_message(role, avatar=avatar):
        if error:
            st.error(message)
        else:
            st.write(message)

    st.session_state.messages.append({"role": role, "content": message})

    if increment_counter:
        st.session_state["counter"] += 1



def handle_question(question_to, prompt: str):
    """
    Handles the incoming question and determines the appropriate response.

    Args:
        question_to: The question object containing the name attribute to identify the type of question.
        prompt (str): The input prompt/question to be answered by the Cohere API.
    """
    responses = {
        "procedence": ("I'm a showcase created by Jesús Remón trained to answer your questions, I'm based in Cohere's Command R+", False, False),
        "medical": ("Sorry, I'm not a medical doctor", True, False),
        "chitchat": ("Hello, everything going great in here, do you have any question?", False, False),
        "confidential": ("I'm not going to provide any kind of confidential information, my access is limited to public available data", True, False),
        "filter": ("We do not tolerate discriminatory or offensive language. Your comment has been flagged and reported. Please adhere to our community guidelines and maintain respectful communication.", True, True)
    }

    if question_to.name in responses:
        message, is_error, increment_counter = responses[question_to.name]
        handle_response("assistant", ":material/cognition:", message, error=is_error, increment_counter=increment_counter)
    else:
        msg, sources, content_high, urls_names = cohere_generation(prompt)
        display_response_with_sources(msg, content_high, sources, urls_names)



def display_response_with_sources(msg: str, content_high: str, sources: list[str], urls_names: list[str]):
    """
    Displays the response and sources in a structured format.

    Args:
        msg (str): The main response message.
        content_high (str): The response text with highlighted citations.
        sources (list[str]): A list of URLs of the sources used.
        urls_names (list[str]): A list of the titles of the sources used.
    """
    with st.chat_message("assistant", avatar=":material/cognition:"):
        tab1, tab2 = st.tabs(["Response", "Grounded Response"])
        with tab1:
            st.write(msg)

        with tab2:
            st.write(content_high)

        if len(urls_names) > 1:
            with st.popover("Sources"):
                st.subheader("Sources Used")
                for i in range(len(sources)):
                    with st.container():
                        st.text(urls_names[i])
                        st.link_button(f"Link {i + 1}", sources[i])

        st.session_state.messages.append({"role": "assistant", "content": msg})
