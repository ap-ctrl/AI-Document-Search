📄 AI Document Chat

An AI-powered PDF question-answering application that allows users to upload a PDF and ask questions about its contents.

The application uses local AI with Ollama, meaning the AI model runs locally instead of relying on a cloud-based AI API.

Users can upload a PDF, process the document, and ask questions through a simple Streamlit chat interface.

🚀 Features
📄 Upload PDF documents
🔍 Extract and process text from PDFs
🧠 Ask questions about the uploaded document
🤖 Local AI using Ollama
💬 Chat-style user interface
🐳 Dockerized application
🔎 Document retrieval before generating answers
🔒 No external AI API required


🛠️ Technologies Used
Frontend
Streamlit
Backend
Python
AI Model
Ollama
Qwen 2.5 1.5B
PDF Processing
Python PDF processing libraries
Tesseract OCR support
Containerization
Docker
Docker Compose

📂 Project Structure
AI-Document-Search
│
├── app.py
├── main.py
├── pdf_processor.py
├── rag.py
├── search.py
├── search_app.py
├── rewrite.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
├── .gitignore
│
├── sample.pdf
│
├── data.pkl
│
├── test_ollama.py
└── test_tesseract.py

🧠 How It Works

The application follows a simple Retrieval-Augmented Generation workflow.

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
🐳 Running the Project Using Docker
Prerequisites

Make sure the following are installed:

Docker Desktop
Docker Compose

You can verify Docker installation using:
docker --version

and:

docker compose version

Step 1: Clone the Repository

After uploading the project to GitHub:

git clone YOUR_REPOSITORY_URL

Move into the project folder:

cd AI-Document-Search

Step 2: Build and Start the Application

Run:
docker compose up --build

This command will:

Build the Python application container.
Start the Streamlit application.
Start the Ollama container.
Create the required Docker network.
Create the Ollama data volume.

🤖 Download the AI Model

After the Docker containers are running, check the available Ollama models:
docker exec -it ai-document-chat-ollama ollama list

If the Qwen model is not available, download it using:
docker exec -it ai-document-chat-ollama ollama pull qwen2.5:1.5b

Verify the installation:
docker exec -it ai-document-chat-ollama ollama list

You should see:
qwen2.5:1.5b

🧪 Test the AI Model

You can test whether Ollama and the model are working correctly:

docker exec -it ai-document-chat-ollama ollama run qwen2.5:1.5b "Say hello"

Example response:

Hello! How can I help you today?

💻 Run the Application

After the containers are running, open your browser and access the Streamlit application on port:

8501

The application allows you to:

Upload a PDF.
Wait for the PDF to be processed.
Enter a question.
Retrieve information from the PDF.
Receive an AI-generated answer.

📸 Application Workflow
1. Upload a PDF

The user uploads a PDF document through the Streamlit interface.

2. Process the Document

The application extracts text from the PDF and prepares the document for searching and retrieval.

3. Ask a Question

The user enters a question related to the uploaded document.

Example:

What is the patient's name?
4. Retrieve Relevant Information

The application searches the processed PDF for relevant information.

5. Generate an Answer

The retrieved information is sent to the local Ollama model.

6. Display the Answer

The answer is displayed in the Streamlit chat interface.

🐳 Docker Containers

The project uses two main containers.

Application Container

Container name:

ai-document-chat-app

Responsibilities:

Run the Streamlit application.
Handle PDF uploads.
Process documents.
Retrieve relevant information.
Communicate with Ollama.

Ollama Container

Container name:

ai-document-chat-ollama

Responsibilities:

Run the Ollama server.
Store downloaded AI models.
Process prompts.
Generate AI responses.

📦 Useful Docker Commands
Check Running Containers
docker ps
Check Ollama Models
docker exec -it ai-document-chat-ollama ollama list
View Application Logs
docker compose logs

For live logs:

docker compose logs -f
Stop the Application

Press:

CTRL + C

Or run:

docker compose down
Start the Application Again
docker compose up
Rebuild After Code Changes

If you make changes to the Python code or Docker configuration:

docker compose up --build

🔮 Future Improvements

Possible improvements for the project include:

Support multiple PDF uploads.
Add document history.
Add chat history.
Improve document chunking.
Add vector database support.
Add support for DOCX files.
Add support for image-based PDFs.
Improve OCR functionality.
Add source citations for answers.
Deploy the application publicly.
Add authentication and user accounts.
🔐 Local AI

This project uses a locally running Ollama model.

Advantages include:

No external AI API key required.
AI processing can run locally.
Reduced dependency on cloud AI services.
Greater control over the AI model and environment.
👩‍💻 Author

Ankita Priyadarshini

AI Document Chat is a local AI-powered document question-answering project built using Python, Streamlit, Docker, Ollama, and the Qwen language model.

⭐ Project Status

🚧 Active / Working Locally

The application has been successfully tested locally with:

Docker
Docker Compose
Ollama
Qwen 2.5 1.5B
PDF Upload
Document Processing
Question Answering
Streamlit


