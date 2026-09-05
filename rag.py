import os
import requests


def generate_answer(query, retrieved_chunks):

    # Join the retrieved document chunks
    context = "\n\n".join(retrieved_chunks)

    # Prompt sent to Ollama
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

    # Get Ollama URL from environment variable.
    # If running locally, localhost is used.
    # If running with Docker Compose, the "ollama" service is used.
    ollama_url = os.getenv(
        "OLLAMA_URL",
        "http://localhost:11434"
    )

    url = f"{ollama_url}/api/generate"

    data = {
        "model": "qwen2.5:1.5b",
        "prompt": prompt,
        "stream": False
    }

    try:

        response = requests.post(
            url,
            json=data,
            timeout=120
        )

        response.raise_for_status()

        result = response.json()

        return result["response"]

    except Exception as e:

        return f"Error: {str(e)}"
# import requests


# def generate_answer(query, retrieved_chunks):
#     context = "\n\n".join(retrieved_chunks)

#     prompt = f"""
# You are an intelligent document assistant.

# Answer ONLY from the provided context.
# If answer is not found, say:
# Not found in document.

# Context:
# {context}

# Question:
# {query}

# Answer:
# """

#     url = "http://localhost:11434/api/generate"

#     data = {
#         "model": "qwen2.5:1.5b",
#         # "model": "tinyllama",
#         "prompt": prompt,
#         "stream": False
#     }

#     try:
#         response = requests.post(url, json=data, timeout=120)
#         response.raise_for_status()

#         result = response.json()
#         return result["response"]

#     except Exception as e:
#         return f"Error: {str(e)}"