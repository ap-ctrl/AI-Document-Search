
<div align="center">

# 📄 AI Document Chat

### Ask questions about your PDFs using Retrieval-Augmented Generation (RAG)

A Python-based AI document question-answering application that extracts text from PDF files, handles scanned documents using OCR, retrieves relevant passages using semantic similarity, and generates answers grounded in the retrieved document context.

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-red.svg)](https://streamlit.io/)
[![RAG](https://img.shields.io/badge/AI-RAG-purple.svg)](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)
[![Ollama](https://img.shields.io/badge/LLM-Ollama-black.svg)](https://ollama.com/)
[![Docker](https://img.shields.io/badge/Docker-Supported-blue.svg)](https://www.docker.com/)

**[🚀 Try the Live Application](https://ai-document-search-5pzioxvgggkphc6mjfntsc.streamlit.app/) · [📂 View Source Code](https://github.com/ap-ctrl/AI-Document-Search)**

</div>

---

## 📌 Overview

AI Document Chat is an AI-powered PDF question-answering application built with Python and Streamlit. It allows users to upload a PDF and ask questions about its contents through a conversational interface.

Instead of sending the entire document to a language model for every question, the application processes the PDF into smaller text chunks, converts those chunks into vector embeddings, retrieves the most relevant passages, and supplies the retrieved context to a language model to generate an answer.

The project demonstrates the practical implementation of a Retrieval-Augmented Generation (RAG) pipeline, combining document processing, OCR, embedding generation, semantic search, query rewriting, and LLM-based answer generation.

The application is deployed on Streamlit Community Cloud, with answer generation configured to use the Ollama Cloud API.

## ✨ Features

| Feature | Description |
|---|---|
| 📄 PDF Upload | Upload a PDF through the Streamlit interface. |
| 📝 Text Extraction | Extract text from text-based PDF documents using `pypdf`. |
| 🔍 OCR Fallback | Use Tesseract OCR when normal text extraction does not produce sufficiently useful text. |
| ✂️ Text Chunking | Split extracted text into smaller, overlapping chunks for retrieval. |
| 🧠 Embeddings | Convert document chunks into numerical vector representations using Sentence Transformers. |
| 🔎 Semantic Search | Retrieve the top three document chunks using cosine similarity. |
| 🤖 AI Question Answering | Generate answers using retrieved document context and an LLM. |
| 💬 Conversational Interface | Ask questions and view previous messages within the Streamlit session. |
| 🔄 Query Rewriting | Attempt to convert vague follow-up questions into standalone questions using recent conversation history. |
| ☁️ Cloud Deployment | Access the deployed application through a public Streamlit URL. |
| 🐳 Docker Support | Build and run the application using Docker and Docker Compose. |

## 🌐 Live Demo

**Application:** [AI Document Chat](https://ai-document-search-5pzioxvgggkphc6mjfntsc.streamlit.app/)

### How to use it

1. Open the live application.
2. Upload a PDF document.
3. Wait for the document processing step to finish.
4. Enter a question about the document.
5. The application retrieves relevant passages and sends the question and retrieved context to the configured language model.
6. Read the generated response in the chat interface.

For best results, start with a clear question whose answer is explicitly stated in the PDF.

> **Privacy note:** The deployed application processes uploaded documents in the cloud environment and sends retrieved text to the configured Ollama Cloud API for answer generation. Do not upload confidential, sensitive, or personal documents unless you have verified that the service and provider policies are appropriate for your use case.

## 🛠️ Technology Stack

| Layer | Technologies | Purpose |
|---|---|---|
| User interface | Streamlit | PDF upload and conversational question-answering interface |
| Programming language | Python 3.11 | Application logic and pipeline orchestration |
| PDF text extraction | pypdf | Extract text from PDF pages |
| PDF rendering | PyMuPDF (`fitz`) | Render PDF pages as images for OCR |
| Image processing | Pillow | Convert rendered PDF pages into images |
| OCR | Tesseract, pytesseract | Recognize text in scanned PDF pages |
| Embeddings | Sentence Transformers | Represent document chunks and queries as vectors |
| Embedding model | `all-MiniLM-L6-v2` | Generate semantic vector representations |
| Similarity calculation | scikit-learn, NumPy | Calculate cosine similarity and rank retrieved chunks |
| LLM integration | Ollama Cloud API, Requests | Generate answers from retrieved context |
| Deployment | Streamlit Community Cloud | Host the public web application |
| Containerization | Docker, Docker Compose | Provide a container-based application setup |

## 🧠 System Architecture

The application follows a Retrieval-Augmented Generation workflow.

```text
                 ┌──────────────────────┐
                 │      User Uploads     │
                 │        a PDF          │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   PDF Processing     │
                 │                      │
                 │  pypdf Text Extract  │
                 │  OCR Fallback        │
                 │  Text Cleaning       │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │    Text Chunking     │
                 │                      │
                 │  Chunk Size: 500     │
                 │  Overlap: 100         │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │  Embedding Creation  │
                 │                      │
                 │ all-MiniLM-L6-v2     │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │    User Question     │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   Query Rewriting    │
                 │   If Available       │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   Semantic Search    │
                 │                      │
                 │ Query Embedding      │
                 │ Cosine Similarity    │
                 │ Top 3 Chunks          │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   Prompt Formation   │
                 │                      │
                 │ Question + Context   │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   Ollama Cloud API   │
                 │                      │
                 │   gemma4:31b         │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   Generated Answer   │
                 │   Streamlit Chat     │
                 └──────────────────────┘
```

*The query-rewriting stage currently uses a local Ollama endpoint. If that endpoint is unavailable, the code falls back to the original question and continues the pipeline.*

## ⚙️ How the RAG Pipeline Works

### 1. PDF ingestion and text extraction

**File:** `pdf_processor.py`

The application receives the uploaded PDF and temporarily writes it to a file so that PDF-processing libraries can read it.

The extraction process uses two approaches:

- **Normal extraction:** `pypdf.PdfReader` extracts text from the PDF pages.
- **OCR fallback:** If the extracted text does not meet the application's usefulness checks, PyMuPDF renders the pages into images and Tesseract attempts to recognize their text.

The extracted text is cleaned by removing repeated spaces and excessive blank lines.

The usefulness check is heuristic: it examines the amount of extracted text and the number of alphabetic characters. It does not guarantee that the extracted content is accurate or complete.

### 2. Text chunking

**File:** `pdf_processor.py`

Long documents are divided into smaller text segments called chunks.

The current configuration uses:

- Chunk size: `500` characters.
- Overlap: `100` characters.

The overlap preserves some surrounding context between adjacent chunks, reducing the chance that information near a chunk boundary becomes difficult to retrieve.

The implementation also attempts to split at a newline when doing so avoids cutting through a line.

These values are character-based, not token-based.

### 3. Embedding generation

**File:** `embeddings.py`

The application uses the Sentence Transformers model `all-MiniLM-L6-v2` to convert each text chunk into a numerical vector.

An embedding represents text in a vector space so that semantically related text can be compared mathematically.

The implementation uses:

- Batch encoding with a batch size of 32.
- Normalized embeddings.
- The generated vectors as input to the retrieval stage.

Embeddings are generated in memory during document processing; this implementation does not use a separate vector database.

### 4. Semantic retrieval

**File:** `search.py`

When the user asks a question, the application converts the question into an embedding and compares it with the document chunk embeddings using cosine similarity.

The similarity scores are ranked, and the three highest-ranked chunks are returned as retrieval results.

Conceptually, cosine similarity measures the angle between two vectors:

\[
\operatorname{similarity}(A,B)
=
\frac{A\cdot B}{\|A\|\|B\|}
\]

The current implementation uses scikit-learn's `cosine_similarity` and NumPy's sorting functionality.

This is semantic vector retrieval, not a full hybrid search system: there is no separate keyword index, reranker, or persistent vector database in the current implementation.

### 5. Query rewriting

**File:** `rewrite.py`

Follow-up questions can depend on earlier messages. For example, a user might ask, "What about its advantages?" without explicitly identifying the subject.

The query-rewriting function combines the current question with up to the last four conversation messages and asks a language model to rewrite the question as a standalone query.

The current implementation sends this request to a local Ollama endpoint configured through `OLLAMA_URL`, defaulting to `http://localhost:11434`.

If the request fails, it returns the original question rather than stopping the application. Consequently, query rewriting is best-effort and is not currently integrated with the cloud API used for answer generation.

### 6. Prompt construction and answer generation

**File:** `rag.py`

The application combines the retrieved text chunks into a context string and constructs a prompt containing:

- Instructions for the assistant.
- The retrieved document context.
- The user's question.
- An instruction to answer only from the supplied context.
- An instruction to return `Not found in document.` when the answer is not present in the supplied context.

The prompt is sent to the Ollama Cloud chat API. The current implementation uses the `gemma4:31b` model identifier and reads the generated text from the API response.

The answer is then displayed in the Streamlit chat interface.

The prompt encourages grounded answers but cannot guarantee that the model will never produce an unsupported statement. Generated answers should be checked against the source document.

## 📂 Project Structure

```text
AI-Document-Search/
│
├── app.py                 # Main Streamlit application
├── pdf_processor.py       # PDF extraction, OCR and chunking
├── embeddings.py          # Sentence Transformer embeddings
├── search.py              # Cosine-similarity retrieval
├── rag.py                 # RAG prompt and cloud answer generation
├── rewrite.py              # Follow-up query rewriting
│
├── main.py                # Additional PDF-processing entry point
├── search_app.py           # Additional search application entry point
│
├── requirements.txt        # Python dependencies
├── Dockerfile              # Application container definition
├── docker-compose.yml      # Application and Ollama services
├── .dockerignore           # Docker build exclusions
├── .gitignore              # Git exclusions
│
├── sample.pdf              # Sample PDF included in the repository
├── data.pkl                # Pickle data artifact included in the repository
│
├── test_ollama.py          # Ollama connectivity test script
├── test_tesseract.py       # Tesseract test script
│
└── README.md               # Project documentation
```

## 🚀 Run Locally

### Prerequisites

Install the following:

- Python 3.11
- Git
- Tesseract OCR
- An Ollama account and API key for the current answer-generation implementation

For local Docker use, install Docker Desktop with Docker Compose.

### 1. Clone the repository

```bash
git clone https://github.com/ap-ctrl/AI-Document-Search.git
cd AI-Document-Search
```

### 2. Create a virtual environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Install Tesseract OCR

The OCR fallback requires the Tesseract executable to be installed on the machine.

- Windows: install Tesseract OCR and ensure its executable path matches the configuration in `pdf_processor.py`.
- macOS: install Tesseract using a suitable package manager.
- Linux: install the `tesseract-ocr` system package.

The Python package `pytesseract` provides the Python interface; it does not install the Tesseract executable itself.

### 5. Configure the Ollama Cloud API key

Create an API key through [Ollama](https://ollama.com/settings/keys).

Create a file at `.streamlit/secrets.toml` in the project directory:

```toml
OLLAMA_API_KEY = "your-actual-ollama-api-key"
```

Replace the placeholder with your own key. Do not commit this file or share the key publicly.

The current `rag.py` reads `OLLAMA_API_KEY` from Streamlit Secrets and sends answer-generation requests to `https://ollama.com/api/chat`.

### 6. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal, typically:

```text
http://localhost:8501
```

**Note:** The current `rewrite.py` still targets a local Ollama server. Without a reachable local model, it falls back to the original question. The Docker configuration also starts a local Ollama service, but the current `rag.py` uses the cloud API for answer generation.

## 🐳 Docker Setup

The repository includes a `Dockerfile` and `docker-compose.yml`.

### Build and start the containers

```bash
docker compose up --build
```

The configuration defines two services:

| Service | Responsibility | Port |
|---|---|---|
| `app` | Runs the Streamlit application | `8501` |
| `ollama` | Runs a local Ollama server | `11434` |

The Ollama service uses a named volume to persist downloaded model data.

To download the model used by the earlier local Ollama configuration:

```bash
docker exec -it ai-document-chat-ollama ollama pull qwen2.5:1.5b
```

To inspect available local models:

```bash
docker exec -it ai-document-chat-ollama ollama list
```

Open the application at `http://localhost:8501`.

**Important implementation detail:** The current `rag.py` is configured for Ollama Cloud rather than the local Ollama service. The Docker Compose configuration has not yet been updated to make the local service the answer-generation backend. For the current cloud-based code, configure `OLLAMA_API_KEY` in the application's Streamlit Secrets. Do not assume that starting Docker alone makes the current cloud-based answer-generation path work without its credentials.

### Useful Docker commands

```bash
# Check running containers
docker ps

# View logs
docker compose logs

# Follow logs in real time
docker compose logs -f

# Stop and remove containers
docker compose down

# Rebuild after code changes
docker compose up --build
```

The named Ollama volume is retained when containers are stopped with `docker compose down`. Removing volumes explicitly will delete the associated persisted data.

## ☁️ Deployment on Streamlit Community Cloud

The application is deployed through Streamlit Community Cloud and uses the `app.py` entry point.

### Deployment steps

1. Push the project to a GitHub repository.
2. Open [Streamlit Community Cloud](https://share.streamlit.io/).
3. Create an app and select the repository.
4. Select the `main` branch and set `app.py` as the main file.
5. Add the required API key in the app's **Settings → Secrets** section.
6. Deploy the application and wait for the deployment to finish.
7. Open the generated public URL and test PDF upload and question answering.

For this project, the secret is configured as:

```toml
OLLAMA_API_KEY = "your-actual-ollama-api-key"
```

Keep API keys in Streamlit Secrets, not in Python source code or committed configuration files.

### Why Ollama Cloud is used for deployment

A cloud-hosted Streamlit application cannot reach an Ollama server running on the developer's personal computer through `localhost`.

In a hosted environment, `localhost` refers to the environment running the application. The cloud application therefore needs a model service that it can reach, such as the configured Ollama Cloud API.

## ⚠️ Current Limitations

The following points describe the current implementation rather than planned features.

- **PDF-only interface:** The main Streamlit application accepts PDF uploads.
- **Heuristic OCR fallback:** OCR is triggered based on extracted-text usefulness checks. Complex layouts, low-resolution scans, handwriting, and unusual fonts may reduce extraction quality.
- **Character-based chunks:** Chunk boundaries are based on characters rather than model tokens or semantic sections.
- **Top-three retrieval:** Only three chunks are selected for answer generation. Relevant information may be missed if it is not present in those chunks.
- **In-memory processing:** Document chunks and embeddings are created in memory; a persistent vector database is not configured.
- **Best-effort query rewriting:** `rewrite.py` targets local Ollama and falls back to the original question when that call fails.
- **No explicit source citations:** The current answer-generation implementation does not return structured page-level citations or clickable source references.
- **No guaranteed factuality:** The prompt requests document-grounded answers, but model output can still be incomplete or incorrect.
- **Cloud API dependency:** The deployed answer-generation path requires valid Ollama Cloud credentials and an available, supported model.
- **Local Docker integration:** Docker Compose starts a local Ollama service, but the current `rag.py` uses the cloud endpoint. The two configurations have not yet been unified.
- **Security and privacy:** The project does not currently document a dedicated authentication or authorization layer. The public deployment should not be treated as a secure private-document repository.

## 🔮 Potential Future Improvements

Possible next steps for the project include:

- [ ] Integrate query rewriting with the same configurable model backend used for answer generation.
- [ ] Make local Ollama and cloud inference selectable through configuration.
- [ ] Add page-level citations and retrieved-source previews.
- [ ] Improve chunking with token-aware or structure-aware splitting.
- [ ] Add a persistent vector store for reusable document indexing.
- [ ] Add configurable retrieval thresholds and retrieval evaluation.
- [ ] Add automated tests for PDF extraction, OCR fallback, retrieval, and answer generation.
- [ ] Improve caching of the embedding model and processed documents.
- [ ] Add more robust error handling and user-facing configuration checks.
- [ ] Add authentication and appropriate access controls if private multi-user usage is required.

These are potential improvements and are not claimed as completed features.

## 🧪 Testing

The repository includes:

- `test_ollama.py` — a script for testing Ollama connectivity.
- `test_tesseract.py` — a script for checking Tesseract OCR.

The presence of these scripts does not imply that the project has a complete automated test suite. The current implementation should also be manually tested with text-based PDFs, scanned PDFs, questions with known answers, and questions whose answers are absent from the document.

## 📚 Concepts Demonstrated

This project brings together several concepts relevant to AI engineering and software development:

- Python application development and modular code organization.
- PDF parsing and OCR-based text recognition.
- Text preprocessing and overlapping chunking.
- Sentence embeddings and vector representations.
- Cosine similarity and semantic information retrieval.
- Retrieval-Augmented Generation (RAG).
- Prompt construction and context-grounded generation.
- Language model API integration.
- Conversational state management in Streamlit.
- Environment configuration and secret management.
- Docker-based application packaging.
- Deployment of a Python web application.

## 👩‍💻 Author

**Ankita Priyadarshini**

GitHub: [@ap-ctrl](https://github.com/ap-ctrl)

Project repository: [AI-Document-Search](https://github.com/ap-ctrl/AI-Document-Search)

---

<div align="center">

Built with Python, Streamlit, Sentence Transformers, OCR, RAG, and Ollama.

If you find this project interesting, consider starring the repository ⭐

</div>
