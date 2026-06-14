import streamlit as st
from sentence_transformers import (
    SentenceTransformer
)

@st.cache_resource
def load_embedding_model():

    return SentenceTransformer(
        "mixedbread-ai/mxbai-embed-large-v1"
    )

model = load_embedding_model()

def generate_embedding(text):

    embedding = model.encode(
        text,
        normalize_embeddings=True
    )

    return embedding.tolist()