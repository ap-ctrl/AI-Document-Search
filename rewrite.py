import os
import requests


def rewrite_query(user_question, chat_history):

    # Combine the last 4 messages from the conversation
    history_text = ""

    for msg in chat_history[-4:]:
        history_text += (
            f"{msg['role']}: "
            f"{msg['content']}\n"
        )

    # Prompt for rewriting vague follow-up questions
    prompt = f"""
You are a query rewriting assistant.

Your job is to rewrite vague follow-up questions
into clear standalone questions.

Conversation:
{history_text}

Current Question:
{user_question}

Rewrite the question clearly.
Only return the rewritten question.
"""

    # Get Ollama URL from environment variable.
    # Local development:
    # http://localhost:11434
    #
    # Docker deployment:
    # http://ollama:11434

    ollama_url = os.getenv(
        "OLLAMA_URL",
        "http://localhost:11434"
    )

    try:

        response = requests.post(
            f"{ollama_url}/api/generate",
            json={
                "model": "qwen2.5:1.5b",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        rewritten_query = (
            response.json()["response"]
        )

        return rewritten_query.strip()

    except Exception:

        # If query rewriting fails,
        # use the original user question.
        # This prevents the whole application
        # from crashing.

        return user_question

# import requests


# def rewrite_query(user_question, chat_history):

#     # Combine recent chat
#     history_text = ""

#     for msg in chat_history[-4:]:
#         history_text += f"{msg['role']}: {msg['content']}\n"

#     prompt = f"""
# You are a query rewriting assistant.

# Your job is to rewrite vague follow-up questions
# into clear standalone questions.

# Conversation:
# {history_text}

# Current Question:
# {user_question}

# Rewrite the question clearly.
# Only return the rewritten question.
# """

#     response = requests.post(
#         "http://localhost:11434/api/generate",
#         json={
#             "model": "qwen2.5:1.5b",
#             "prompt": prompt,
#             "stream": False
#         }
#     )

#     rewritten_query = response.json()["response"]

#     return rewritten_query.strip()