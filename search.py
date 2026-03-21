from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def search(query, model, chunks, embeddings, top_k=3):
    # Convert query to embedding
    query_embedding = model.encode([query])
    
    # Compute similarity
    similarities = cosine_similarity(query_embedding, embeddings)[0]
    
    # Get top k indices
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    
    # Return top chunks
    results = [chunks[i] for i in top_indices]
    
    return results