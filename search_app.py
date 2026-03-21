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

print("\nMost relevant results:\n")

for i, res in enumerate(results):
    print(f"\n--- Result {i+1} ---\n")
    print(res)