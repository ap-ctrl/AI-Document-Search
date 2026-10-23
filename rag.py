
import streamlit as st
import requests

def generate_answer(query, retrieved_chunks):
    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
You are an intelligent document assistant.
Answer ONLY from the provided context.
If the answer is not found in the document, say exactly:
Not found in document.

Context:
{context}

Question:
{query}

Answer:
"""

    try:
        api_key = st.secrets["OLLAMA_API_KEY"]

        response = requests.post(
            "https://ollama.com/api/chat",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gemma4:31b",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()
        result = response.json()

        return result["message"]["content"].strip()

    except Exception as e:
        return f"Error generating answer: {str(e)}"
