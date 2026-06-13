import streamlit as st

from backend.services.rag_service import (
    ask_recruiter_bot
)

if "messages" not in st.session_state:

    st.session_state.messages = []

st.title(
    "🤖 Recruiter Chatbot"
)

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

query = st.chat_input(
    "Ask a recruitment question"
)

if query:

    st.session_state.messages.append({

        "role": "user",

        "content": query
    })

    with st.chat_message(
        "user"
    ):

        st.markdown(
            query
        )

    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "Thinking..."
        ):

            answer = (
                ask_recruiter_bot(
                    query
                )
            )

            st.markdown(
                answer
            )

    st.session_state.messages.append({

        "role": "assistant",

        "content": answer
    })