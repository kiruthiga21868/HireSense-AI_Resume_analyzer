import os

os.environ["PATH"] += os.pathsep + r"E:\whisper\ffmpeg-2026-06-10-git-b29bdd3715-essentials_build\bin"

import whisper
import tempfile
from gtts import gTTS
import streamlit as st


@st.cache_resource
def load_whisper_model():

    return whisper.load_model(
        "base"
    )

model = load_whisper_model()


def speech_to_text(
    audio_path
):

    result = model.transcribe(
        audio_path
    )

    return result["text"]


def text_to_speech(
    text
):

    tts = gTTS(
        text=text,
        lang="en"
    )

    temp_file = (
        tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3"
        )
    )

    tts.save(
        temp_file.name
    )

    return temp_file.name