from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def search(query, model, chunks, embeddings, top_k=3):

    if not chunks or len(embeddings) == 0:
        return []

    # Convert query into embedding
    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    )

    # Compare similarity
    similarities = cosine_similarity(
        query_embedding,
        embeddings
    )[0]

    # Best matches
    top_indices = np.argsort(
        similarities
    )[-top_k:][::-1]

    # Get retrieved chunks
    results = [
        chunks[i]
        for i in top_indices
    ]

    # Print retrieved chunks in terminal
    print("\n--- RETRIEVED CHUNKS ---")

    for i, result in enumerate(results):
        print(f"\nChunk {i + 1}:")
        print(result)

    return results
# from sklearn.metrics.pairwise import cosine_similarity
# import numpy as np


# def search(query, model, chunks, embeddings, top_k=3):

#     if not chunks or len(embeddings) == 0:
#         return []

#     # Convert query into embedding
#     query_embedding = model.encode(
#         [query],
#         normalize_embeddings=True
#     )

#     # Compare similarity
#     similarities = cosine_similarity(
#         query_embedding, embeddings
#     )[0]

#     # Best matches
#     top_indices = np.argsort(similarities)[-top_k:][::-1]

#     Return chunks
#     results = [chunks[i] for i in top_indices]

#     print("\n--- RETRIEVED CHUNKS ---")

#     for i, result in enumerate(results):
#         print(f"\nChunk {i + 1}:")
#         print(result)

#     return results