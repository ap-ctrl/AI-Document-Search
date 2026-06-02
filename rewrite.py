import requests


def rewrite_query(user_question, chat_history):

    # Combine recent chat
    history_text = ""

    for msg in chat_history[-4:]:
        history_text += f"{msg['role']}: {msg['content']}\n"

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

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5:1.5b",
            "prompt": prompt,
            "stream": False
        }
    )

    rewritten_query = response.json()["response"]

    return rewritten_query.strip()