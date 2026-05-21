# 📚 Local RAG Document Assistant

A full-stack Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and chat with them in real-time. 

This project prioritizes data privacy and speed by utilizing a **100% local Large Language Model (LLM)** via Ollama, combined with real-time text streaming and a scalable Supabase vector database.

## ✨ Features
* **Completely Private AI:** Text generation is handled entirely on your local hardware using Ollama—no data is sent to OpenAI or third-party cloud providers.
* **Real-Time Streaming:** Responses are streamed word-by-word to the frontend, providing a native, instant chatbot experience.
* **Smart Chunking & Filtering:** Automatically parses PDFs, chunks text intelligently, and filters out low-relevance database hits to prevent AI hallucinations.
* **Source Citation:** Automatically provides exact page numbers for the document chunks used to answer the query.
* **Modern UI:** Clean, responsive split-pane interface built with React and the newly released Tailwind CSS v4.

## 🛠️ Tech Stack & Architecture

### Frontend
* **Framework:** React + Vite
* **Styling:** Tailwind CSS v4
* **State Management:** React Hooks (`useState`, `useEffect`)

### Backend
* **Server:** Python + FastAPI
* **PDF Parsing:** PyMuPDF (`fitz`)
* **Vector Database:** Supabase (PostgreSQL + `pgvector`)
* **Embeddings:** `SentenceTransformers` (`mixedbread-ai/mxbai-embed-large-v1`)
* **LLM Integration:** Ollama (Local text generation) + Python `requests` (Streaming)

---

## 💻 System Requirements
To run this application smoothly on your local machine, you will need:
* **OS:** Windows, macOS, or Linux
* **RAM:** Minimum 8GB (16GB recommended for local LLM processing)
* **Software:**
  * [Python 3.9+](https://www.python.org/downloads/)
  * [Node.js v18+](https://nodejs.org/)
  * [Ollama](https://ollama.com/)
* **Accounts:** A free [Supabase](https://supabase.com/) account for the vector database.

## 🧠 AI Models Used
Before starting the application, ensure you have the required models available:
1. **Embedding Model:** `mixedbread-ai/mxbai-embed-large-v1` (Downloaded automatically by Python on first run).
2. **Local LLM:** `llama3.2:1b` (A blazing-fast, 1-billion parameter model). 
   * *To install, open your terminal and run:*
     ```bash
     ollama run llama3.2:1b
     ```

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
https://github.com/DVenkatY/RAGFromScratch.git
cd RAGFromScratch

Navigate to the backend folder and install the Python dependencies:
cd backend
pip install -r requirements.txt

Create a .env file inside the backend folder and add your Supabase credentials:
SUPABASE_URL="your_supabase_project_url"
SUPABASE_KEY="your_supabase_anon_key"
DATABASE_URL="your_supabase_postgresql_connection_string"

Open a new terminal, navigate to the frontend folder, and install the Node dependencies:
cd frontend
npm install

Running the Application
You need three services running simultaneously for the application to work.

1. Start the Ollama Engine
Make sure the Ollama application is running in the background of your operating system (check your system tray).

2. Start the FastAPI Backend
In your backend terminal, start the Python server:

Bash
cd backend
python main.py
(The server will run at http://localhost:8000)

3. Start the React Frontend
In your frontend terminal, start the Vite development server:

Bash
cd frontend
npm run dev
(The UI will run at http://localhost:5173)
