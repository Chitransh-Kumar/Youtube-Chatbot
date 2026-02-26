import streamlit as st
from dotenv import load_dotenv

from utils import get_video_id
from transcript import transcript_generation
from splitter import split_text
from vectorstore import build_vector_stores
from query import classify_query
from chains import build_chain, build_summary_chain

load_dotenv()

st.set_page_config(page_title="YouTube Chatbot", layout="wide")

st.title("YouTube Video Chatbot")

video_url = st.text_input("Enter YouTube Video URL")

if video_url:

    video_id = get_video_id(video_url)

    if not video_id:
        st.error("Invalid YouTube URL")
        st.stop()

    st.video(f"https://www.youtube.com/watch?v={video_id}")

    # Whole Pipeline

    if "video_id" not in st.session_state or st.session_state.video_id != video_id:

        with st.spinner("Processing transcript..."):

            transcript = transcript_generation(video_url)

            if not transcript:
                st.error("No captions available")
                st.stop()

            docs = split_text(transcript)

            vector_store = build_vector_stores(
                docs,
                index_name=f"video_{video_id}"
            )

            retriever = vector_store.as_retriever(
                search_type='similarity',
                search_kwargs={'k': 2}
            )

            st.session_state.video_id = video_id
            st.session_state.transcript = transcript
            st.session_state.docs = docs
            st.session_state.rag_chain = build_chain(retriever)
            st.session_state.summary_chain = build_summary_chain()

            # Reset chat history for new video
            st.session_state.messages = []

    # Chat History Storage

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display Chat History

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input Box

    query = st.chat_input("Ask something about the video")

    if query:

        # Store user message
        st.session_state.messages.append({
            "role": "user",
            "content": query
        })

        with st.chat_message("user"):
            st.markdown(query)

        query_type = classify_query(query)

        with st.spinner("Thinking..."):

            if query_type == "summary":

                result = st.session_state.summary_chain.invoke({
                    "text": st.session_state.transcript
                })

            else:

                result = st.session_state.rag_chain.invoke(query)

        # Store assistant response
        st.session_state.messages.append({
            "role": "assistant",
            "content": result
        })

        with st.chat_message("assistant"):
            st.markdown(result)