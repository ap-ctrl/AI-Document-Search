from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def keyword_score(query, chunk):

    query_words = query.lower().split()
    chunk_lower = chunk.lower()

    score = 0

    for word in query_words:
        if word in chunk_lower:
            score += 1

    return score


def search(query, model, chunks, embeddings, top_k=3):

    if not chunks or len(embeddings) == 0:
        return []

    # Dense retrieval
    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    )

    semantic_scores = cosine_similarity(
        query_embedding,
        embeddings
    )[0]

    # Keyword retrieval
    keyword_scores = np.array([
        keyword_score(query, chunk)
        for chunk in chunks
    ])

    # Normalize keyword scores
    if keyword_scores.max() > 0:
        keyword_scores = keyword_scores / keyword_scores.max()

    # Hybrid score
    final_scores = (
        0.7 * semantic_scores +
        0.3 * keyword_scores
    )

    # Top chunks
    top_indices = np.argsort(
        final_scores
    )[-top_k:][::-1]

    results = [
        chunks[i]
        for i in top_indices
    ]

    return results
# import pickle
# from search import search
# from sentence_transformers import SentenceTransformer
# from rag import generate_answer

# # Load saved data
# with open("data.pkl", "rb") as f:
#     chunks, embeddings = pickle.load(f)

# # Load model
# model = SentenceTransformer('all-MiniLM-L6-v2')

# # Take user input
# query = input("Enter your question: ")

# # Search
# results = search(query, model, chunks, embeddings)

# from rag import generate_answer

# # Generate final answer using AI
# answer = generate_answer(query, results)

# print("\nFinal Answer:\n")
# print(answer)