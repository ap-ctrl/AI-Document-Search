from sentence_transformers import SentenceTransformer

# Load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks):
    if not chunks:
        return []

    embeddings = model.encode(
        chunks,
        batch_size=32,
        show_progress_bar=True,
        normalize_embeddings=True
    )

    return embeddings
# from sentence_transformers import SentenceTransformer

# # Load model (only once)
# model = SentenceTransformer('all-MiniLM-L6-v2')

# def create_embeddings(chunks):
#     embeddings = model.encode(chunks)
#     return embeddings