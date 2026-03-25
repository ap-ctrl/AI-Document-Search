from transformers import pipeline

qa_pipeline = pipeline("text2text-generation", model="google/flan-t5-large")

def generate_answer(query, retrieved_chunks):
    
    context = "\n\n".join(retrieved_chunks)
    
    prompt = f"""
You are an intelligent assistant.

Read the context carefully and answer the question in 1-2 sentences.

DO NOT repeat the context.
DO NOT copy text.
Give a clear and direct answer.

Context:
{context}

Question:
{query}

Answer:
"""
    
    response = qa_pipeline(
        prompt,
        max_new_tokens=100,
        do_sample=False
    )
    
    return response[0]['generated_text']