<div align="center">

# 📄 AI Document Chat

### AI-Powered PDF Question Answering using RAG, OCR, Ollama and Docker

An AI-powered application that allows users to upload PDF documents and ask questions about their content.

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-red.svg)]()
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue.svg)]()
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-black.svg)]()
[![Qwen](https://img.shields.io/badge/Qwen-2.5%201.5B-purple.svg)]()

</div>

---

## 📌 Overview

**AI Document Chat** is an AI-powered PDF question-answering application that allows users to upload a PDF and ask questions about its contents.

The application uses **local AI with Ollama**, meaning the AI model runs locally instead of relying on a cloud-based AI API.

Users can upload a PDF, process the document, and ask questions through a simple Streamlit chat interface.

---

# 🚀 Features

| Feature              | Description                                                  |
| -------------------- | ------------------------------------------------------------ |
| 📄 PDF Upload        | Upload PDF documents directly through the application        |
| 🔍 Text Extraction   | Extract and process text from PDF files                      |
| 🧠 Document Q&A      | Ask natural-language questions about uploaded documents      |
| 🔎 Context Retrieval | Retrieve relevant document content before generating answers |
| 🤖 Local AI          | Generate answers using Ollama and Qwen 2.5                   |
| 💬 Chat Interface    | Simple Streamlit-based conversational interface              |
| 🐳 Docker Support    | Containerized environment for easier setup and deployment    |
| 🔒 Local Processing  | No external AI API required                                  |

---

# 🛠️ Technology Stack

### Frontend

- Streamlit

### Backend

- Python

### AI Model

- Ollama
- Qwen 2.5 1.5B

### PDF Processing

- Python PDF processing libraries
- Tesseract OCR support

### Containerization

- Docker
- Docker Compose

---

# 🧠 How It Works

The application follows a **Retrieval-Augmented Generation (RAG)** workflow.

```text
                ┌──────────────────┐
                │   Upload PDF     │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Process PDF      │
                │ Extract Text     │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Store / Prepare  │
                │ Document Data    │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ User Question    │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Retrieve Relevant│
                │ Document Content │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Ollama + Qwen    │
                │ Generate Answer  │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Display Answer   │
                │ in Streamlit     │
                └──────────────────┘
```

---

# 📂 Project Structure

```text
AI-Document-Search/
│
├── 📄 app.py
├── 📄 main.py
├── 📄 pdf_processor.py
├── 📄 rag.py
├── 📄 search.py
├── 📄 search_app.py
├── 📄 rewrite.py
│
├── 🐳 Dockerfile
├── 🐳 docker-compose.yml
│
├── 📦 requirements.txt
├── ⚙️ .dockerignore
├── ⚙️ .gitignore
│
├── 📄 sample.pdf
├── 📄 data.pkl
│
├── 🧪 test_ollama.py
└── 🧪 test_tesseract.py
```

---

# 🐳 Running the Project with Docker

## Prerequisites

Make sure the following are installed:

- Docker Desktop
- Docker Compose

Verify your installation:

```bash
docker --version
```

```bash
docker compose version
```

---

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/ap-ctrl/AI-Document-Search.git
```

Move into the project directory:

```bash
cd AI-Document-Search
```

---

## 2️⃣ Build and Start the Application

```bash
docker compose up --build
```

This command will:

- Build the Python application container
- Start the Streamlit application
- Start the Ollama container
- Create the required Docker network
- Create the Ollama data volume

---

# 🤖 Download the AI Model

Check available Ollama models:

```bash
docker exec -it ai-document-chat-ollama ollama list
```

If the model is not available, download it using:

```bash
docker exec -it ai-document-chat-ollama ollama pull qwen2.5:1.5b
```

Verify the installation:

```bash
docker exec -it ai-document-chat-ollama ollama list
```

You should see:

```text
qwen2.5:1.5b
```

---

# 🧪 Test the AI Model

You can test whether Ollama and the model are working correctly:

```bash
docker exec -it ai-document-chat-ollama ollama run qwen2.5:1.5b "Say hello"
```

Example response:

```text
Hello! How can I help you today?
```

---

# 💻 Using the Application

After the containers are running, open:

```text
http://localhost:8501
```

Then:

1. 📄 Upload a PDF document.
2. ⏳ Wait for the document to be processed.
3. 💬 Enter a question.
4. 🔎 Relevant document content is retrieved.
5. 🤖 Ollama generates an answer.
6. ✅ The answer is displayed in the Streamlit interface.

---

# 📸 Application Workflow

### 1️⃣ Upload a PDF

Upload a PDF document through the Streamlit interface.

⬇️

### 2️⃣ Process the Document

The application extracts text from the PDF and prepares the document for searching and retrieval.

⬇️

### 3️⃣ Ask a Question

For example:

```text
What is the patient's name?
```

⬇️

### 4️⃣ Retrieve Relevant Information

The application searches the processed PDF for relevant information.

⬇️

### 5️⃣ Generate an Answer

The relevant document context is sent to the local Ollama model.

⬇️

### 6️⃣ Display the Answer

The AI-generated answer is displayed in the Streamlit interface.

---

# 🐳 Docker Architecture

The project uses two main containers.

## 📦 Application Container

**Container Name:**

```text
ai-document-chat-app
```

### Responsibilities

- Run the Streamlit application
- Handle PDF uploads
- Process documents
- Retrieve relevant information
- Communicate with Ollama

**Port:**

```text
8501
```

---

## 🤖 Ollama Container

**Container Name:**

```text
ai-document-chat-ollama
```

### Responsibilities

- Run the Ollama server
- Store downloaded AI models
- Process prompts
- Generate AI responses

**Port:**

```text
11434
```

---

# 📦 Useful Docker Commands

<details>
<summary><b>Check Running Containers</b></summary>

```bash
docker ps
```

</details>

<details>
<summary><b>Check Available Ollama Models</b></summary>

```bash
docker exec -it ai-document-chat-ollama ollama list
```

</details>

<details>
<summary><b>View Application Logs</b></summary>

```bash
docker compose logs
```

For live logs:

```bash
docker compose logs -f
```

</details>

<details>
<summary><b>Stop the Application</b></summary>

```bash
docker compose down
```

</details>

<details>
<summary><b>Start the Application Again</b></summary>

```bash
docker compose up
```

</details>

<details>
<summary><b>Rebuild After Code Changes</b></summary>

```bash
docker compose up --build
```

</details>

---

# 🔐 Local AI

This project uses a locally running Ollama model.

### Advantages

- 🔑 No external AI API key required
- 💻 AI processing can run locally
- ☁️ Reduced dependency on cloud AI services
- 🎛️ Greater control over the AI model and environment

---

# 🔮 Future Improvements

Potential improvements include:

- 📚 Support multiple PDF uploads
- 💬 Add chat history
- 📂 Add document history
- 🔎 Improve document chunking
- 🗄️ Add vector database support
- 📄 Support DOCX files
- 🖼️ Improve support for image-based PDFs
- 🔤 Improve OCR functionality
- 📍 Add source citations for answers
- 🌐 Deploy the application publicly
- 🔐 Add authentication and user accounts

---

# ⭐ Project Status

> 🟢 **Active — Successfully Running Locally**

The application has been tested locally with:

- ✅ Docker
- ✅ Docker Compose
- ✅ Ollama
- ✅ Qwen 2.5 1.5B
- ✅ PDF Upload
- ✅ Document Processing
- ✅ OCR Support
- ✅ Retrieval-Based Question Answering
- ✅ Streamlit

---

<div align="center">

## 👩‍💻 Author

### Ankita Priyadarshini

Built using **Python · Streamlit · RAG · Ollama · Qwen · Docker**

⭐ If you found this project interesting, consider giving it a star!

</div>
