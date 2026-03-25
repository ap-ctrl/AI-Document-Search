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
    sentences = re.split(r'(?<=[.!?]) +', text)
    
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= chunk_size:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
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