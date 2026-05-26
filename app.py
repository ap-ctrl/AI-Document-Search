import streamlit as st
import pickle
from sentence_transformers import SentenceTransformer
from search import search
from rag import generate_answer

# Page settings
st.set_page_config(
    page_title="AI Document Chat",
    page_icon="📄",
    layout="wide"
)

# Title
st.title("📄 AI Document Chat")
st.write("Chat with your PDF using local AI (Ollama)")

# Load saved PDF knowledge
with open("data.pkl", "rb") as f:
    chunks, embeddings = pickle.load(f)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# User input
question = st.text_input("Ask a question from your PDF:")

# Ask button
if st.button("Get Answer"):

    if question.strip() == "":
        st.warning("Please enter a question.")

    else:
        with st.spinner("Thinking..."):

            # Search relevant chunks
            results = search(question, model, chunks, embeddings)

            # Generate answer
            answer = generate_answer(question, results)

            # Show answer
            st.success("Answer:")
            st.write(answer)