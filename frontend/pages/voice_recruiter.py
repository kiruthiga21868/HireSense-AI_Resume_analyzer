import streamlit as st
import sys
import os
import tempfile

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            ".."
        )
    )
)

from backend.services.voice_service import (
    speech_to_text,
    text_to_speech
)

from streamlit_mic_recorder import (
    mic_recorder
)

from backend.services.rag_service import (
    ask_recruiter_bot
)

st.title(
    "🎙 Voice Recruiter Assistant"
)

audio = mic_recorder(

    start_prompt="🎤 Start Recording",

    stop_prompt="⏹ Stop Recording",

    key="recorder"
)

if audio:

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    ) as temp_audio:

        temp_audio.write(
            audio["bytes"]
        )

        temp_path = (
            temp_audio.name
        )

    with st.spinner(
        "Transcribing..."
    ):

        query = speech_to_text(
            temp_path
        )

    st.subheader(
        "Recognized Question"
    )

    st.write(
        query
    )

    with st.spinner(
        "Analyzing Candidates..."
    ):

        answer = (
            ask_recruiter_bot(
                query
            )
        )

    st.subheader(
        "Recruiter Assistant Response"
    )

    st.write(
        answer
    )

    audio_path = (
        text_to_speech(
            answer
        )
    )

    with open(
        audio_path,
        "rb"
    ) as audio_file:

        st.audio(
            audio_file.read(),
            format="audio/mp3"
        )