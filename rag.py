import requests

def generate_answer(query, retrieved_chunks):

    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
You are an intelligent document assistant.

Answer ONLY from the provided context.
If answer is not found, say:
Not found in document.

Context:
{context}

Question:
{query}

Answer:
"""

    url = "http://localhost:11434/api/generate"

    data = {
        "model": "llama3.1:8b",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=data)

    return response.json()["response"]