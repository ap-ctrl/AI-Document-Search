import pickle
from search import search
from sentence_transformers import SentenceTransformer

# Load saved data
with open("data.pkl", "rb") as f:
    chunks, embeddings = pickle.load(f)

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Take user input
query = input("Enter your question: ")

# Search
results = search(query, model, chunks, embeddings)

from rag import generate_answer

# Generate final answer using AI
answer = generate_answer(query, results)

print("\nFinal Answer:\n")
print(answer)