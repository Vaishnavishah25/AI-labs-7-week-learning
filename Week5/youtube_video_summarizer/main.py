import ssl
import urllib3
import requests
import streamlit as st

from youtube_transcript_api import YouTubeTranscriptApi

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_ollama import ChatOllama


# =========================================
# SSL FIX
# =========================================

ssl._create_default_https_context = (
    ssl._create_unverified_context
)

urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)


# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="YouTube AI Summarizer",
    page_icon="🎥",
    layout="wide"
)


# =========================================
# UI
# =========================================

st.title("🎥 YouTube Video AI Summarizer")

st.write(
    "Enter a YouTube video URL and get AI-generated summary."
)


video_url = st.text_input(
    "Enter YouTube Video URL"
)


summary_language = st.selectbox(
    "Select Summary Language",
    ["English", "Hindi"]
)


model_name = st.selectbox(
    "Select Ollama Model",
    ["llama3", "phi3", "mistral"]
)


# =========================================
# EXTRACT VIDEO ID
# =========================================

def extract_video_id(url):

    if "watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]

    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]

    return None


# =========================================
# BUTTON
# =========================================

if st.button("Generate Summary"):

    if not video_url:
        st.error("Please enter YouTube URL")

    else:

        try:

            video_id = extract_video_id(video_url)

            if not video_id:
                st.error("Invalid YouTube URL")

            else:

                # =========================================
                # FETCH TRANSCRIPT
                # =========================================

                with st.spinner("Fetching transcript..."):

                    session = requests.Session()
                    session.verify = False

                    ytt_api = YouTubeTranscriptApi(
                        http_client=session
                    )

                    transcript_list = ytt_api.fetch(
                        video_id,
                        languages=[
                            "hi",
                            "en",
                            "en-IN",
                            "hi-IN"
                        ]
                    )

                    transcript = " ".join(
                        chunk.text
                        for chunk in transcript_list
                    )


                # =========================================
                # SPLIT TRANSCRIPT
                # =========================================

                with st.spinner("Splitting transcript..."):

                    splitter = RecursiveCharacterTextSplitter(
                        chunk_size=4000,
                        chunk_overlap=500
                    )

                    chunks = splitter.split_text(
                        transcript
                    )


                # =========================================
                # LOAD OLLAMA MODEL
                # =========================================

                llm = ChatOllama(
                    model=model_name,
                    temperature=0.2
                )


                # =========================================
                # GENERATE SUMMARIES
                # =========================================

                with st.spinner(
                    "Generating AI summary..."
                ):

                    summaries = []

                    for chunk in chunks:

                        if summary_language == "Hindi":

                            prompt = f'''
                            इस transcript का आसान हिंदी में
                            point-wise summary दो।

                            Transcript:
                            {chunk}
                            '''

                        else:

                            prompt = f'''
                            Summarize this transcript
                            in simple point-wise English.

                            Transcript:
                            {chunk}
                            '''

                        response = llm.invoke(prompt)

                        summaries.append(
                            response.content
                        )


                # =========================================
                # FINAL SUMMARY
                # =========================================

                final_summary = "\n\n".join(
                    summaries
                )


                # =========================================
                # DISPLAY OUTPUT
                # =========================================

                st.success(
                    "Summary Generated Successfully"
                )

                st.subheader("📌 AI Summary")

                st.write(final_summary)


                # =========================================
                # TRANSCRIPT
                # =========================================

                with st.expander(
                    "View Full Transcript"
                ):

                    st.write(transcript)


        except Exception as e:

            st.error(f"Error: {str(e)}")