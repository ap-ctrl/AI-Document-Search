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
        "model": "phi3:latest",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=data, timeout=120)
        response.raise_for_status()

        result = response.json()
        return result["response"]

    except Exception as e:
        return f"Error: {str(e)}"