import streamlit as st
from helper import ask_meeting

st.set_page_config(
    page_title="AI Meeting Notes Summarizer",
    layout="wide"
)

st.title("AI Meeting Notes Summarizer")

question = st.text_input(
    "Ask a question about the meeting"
)

if st.button("Ask AI"):

    if question.strip() == "":
        st.warning("Please enter a question.")
    else:
        response = ask_meeting(question)

        st.write("### AI Response")
        st.write(response)