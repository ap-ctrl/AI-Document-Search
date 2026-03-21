from pypdf import PdfReader
import re

# -------- STEP 1: LOAD PDF --------
reader = PdfReader("sample.pdf")

# -------- STEP 2: EXTRACT TEXT --------
text = ""

for page in reader.pages:
    extracted = page.extract_text()
    if extracted:   # avoid None issues
        text += extracted

# -------- STEP 3: CLEAN TEXT --------
def clean_text(text):
    # Remove non-ASCII characters (weird symbols)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)
    
    return text

text = clean_text(text)

# -------- STEP 4: CHUNKING --------
def chunk_text(text, chunk_size=500):
    chunks = []
    
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i+chunk_size]
        chunks.append(chunk)
    
    return chunks

chunks = chunk_text(text)

# -------- STEP 5: PRINT CHUNKS --------
for i, chunk in enumerate(chunks):
    print(f"\n--- Chunk {i+1} ---\n")
    print(chunk)

from embeddings import create_embeddings

# Create embeddings
embeddings = create_embeddings(chunks)

print("\nNumber of chunks:", len(chunks))
print("Embedding shape:", embeddings.shape)

print("\nSample embedding:\n", embeddings[0])

import pickle

# Save chunks and embeddings
with open("data.pkl", "wb") as f:
    pickle.dump((chunks, embeddings), f)

print("\nData saved successfully!")