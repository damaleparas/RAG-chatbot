# 🤖 AI Agent: PDF-RAG System Workflow

This project is a Full-Stack **Retrieval-Augmented Generation (RAG)** application. It allows users to upload a PDF and "chat" with its contents using an AI agent powered by Google Gemini.

---

## 🏗️ System Architecture

The application follows a decoupled architecture where the Backend handles heavy computation and AI logic, while the Frontend provides a real-time chat interface.



### 1. The Backend (FastAPI + LangChain)
* **API Layer (`main.py`):** Acts as the entry point. It receives user questions and sends back AI responses.
* **RAG Logic (`rag/`):** A modular pipeline that processes documents and queries the LLM.
* **Vector Database (FAISS):** Stores text embeddings for high-speed semantic search.

### 2. The Frontend (React + Vite)
* **UI Component (`ChatWidget.jsx`):** A responsive chat interface.
* **State Management:** Tracks chat history and loading states.
* **API Client (Axios):** Communicates with the FastAPI server.

---

## 🔄 Detailed Workflow

### Phase 1: Knowledge Ingestion (The "Learning" Phase)
Before the agent can answer, it must process the PDF.

1.  **Text Extraction:** `pdf_to_text.py` uses `pypdf` to convert the PDF into raw text.
2.  **Recursive Chunking:** `chunking.py` breaks text into 1000-character pieces with a 200-character overlap. This ensures no context is lost at the "cuts."
3.  **Embedding Generation:** `embed_store.py` sends chunks to `models/embedding-001`. (We use **batching and sleep timers** here to avoid `429 Resource Exhausted` errors).
4.  **Indexing:** The vectors are saved in `data/faiss_index` for offline use.



### Phase 2: Retrieval & Generation (The "Chatting" Phase)
When you type a message in the UI:

1.  **Search:** The system searches the `faiss_index` for the top 3 most relevant text chunks related to your question.
2.  **Context Injection:** Those chunks are pasted into a hidden prompt (Context).
3.  **LLM Reasoning:** The prompt is sent to `gemini-1.5-flash`.
4.  **Answer:** The AI returns a response strictly based on the provided PDF data.



---

## 📁 Project Structure

```text
.
├───backend
│   │   main.py             # FastAPI Server
│   │   .env                # GOOGLE_API_KEY
│   ├───data
│   │       knowledge.pdf   # Your PDF source
│   │       chunks.json     # Intermediate storage
│   │       faiss_index/    # Vector DB files
│   └───rag
│           chunking.py     # Splitter logic
│           embed_store.py  # Embedding logic (with Rate Limit handling)
│           pdf_to_text.py  # PDF Parser
│           rag_answer.py   # RAG Chain logic
│
└───frontend
    └───src
            App.jsx         # Root Component
            ChatWidget.jsx  # Chat UI Logic