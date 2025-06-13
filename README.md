# 📄 AI-Powered Document QA Assistant

This is a prototype web application that helps users search and understand document content by leveraging AI and Large Language Models (LLMs). The user can ask a question in natural Japanese, and the system will retrieve relevant documents, summarize them, and answer the question using an LLM.

---

## 🚀 Features

- Preprocess and split documents into chunks
- Embed document chunks using OpenAI Embeddings and store in PostgreSQL + pgvector
- Perform similarity search based on user question
- Summarize and answer questions using OpenAI GPT models
- Simple and clean frontend built with React + TypeScript + React-Bootstrap

---

## 🛠️ Tech Stack

| Layer        | Technology                            | Why Chosen                                              |
|--------------|----------------------------------------|----------------------------------------------------------|
| Backend      | Python 3.9 + FastAPI                   | Fast, async-ready, modern Python web framework          |
| LLM API      | OpenAI GPT-4o           | High-quality summarization and QA in Japanese           |
| Embedding    | OpenAI text-embedding-3-small          | High-dimensional dense embeddings for vector search     |
| Vector DB    | PostgreSQL + pgvector                  | SQL-native, production-friendly vector search            |
| Frontend     | React + TypeScript + React-Bootstrap   | Simple and modular UI development with good UX          |
| Container    | Docker + Docker Compose                | Easy deployment and local development                   |

---
## 📁 Project Structure (Major Files Only)
```
document_search_app/
├── README.md
├── docker-compose.yml
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── data/
│   │   └── docs/                # Place for PDF files
│   └── app/
│       ├── main.py              # FastAPI entrypoint
│       ├── db.py                # PostgreSQL & pgvector connection
│       ├── db_init.py           # DB schema setup
│       ├── preprocess.py        # Load + clean documents
│       ├── embeddings.py        # Chunk + embed + save
│       ├── search.py            # Vector search logic
│       ├── answer.py            # LLM-based summarization
│       ├── utils.py             # Helper functions
│       ├── chunking.py          # Text chunking
│       └── vector_store.json    # (legacy) vector store file
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── public/
│   └── src/
│       ├── App.tsx              # Main React component
│       ├── index.tsx            # Entry point
│       └── components/          # UI parts like AnswerBox
```
---

## 📦 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/dinhnguyen1812/document-qa-assistant.git
cd document-qa-assistant
```
### 2. Backend Setup
Set up your .env:
```
OPENAI_API_KEY=your-api-key-here
DATABASE_URL=postgresql://postgres:password@db:5432/mydatabase
```
### 3. Run the app with Docker Compose:
```
docker compose up --build -d
```
- Backend: http://localhost:8001
- Frontend: http://localhost:5173

## 🚀 Deployments

### 1. 🔗 Frontend
The React frontend is deployed on Render:

**URL:** [https://ai-powered-document-qa-app-frontend.onrender.com/](https://ai-powered-document-qa-app-frontend.onrender.com/)

### 2. 🔗 Backend
The FastAPI backend is deployed on Render:

**URL:** [https://ai-poswered-document-qa-app.onrender.com/docs](https://ai-poswered-document-qa-app.onrender.com/docs)

### 3. 🗃️ Database
PostgreSQL with pgvector is hosted on Supabase

## 🛠️ Development Stages
| Stage                         | Description                                                                 |
|------------------------------|-----------------------------------------------------------------------------|
| 🔧 Initial Setup              | Set up project structure, Docker, FastAPI backend, and React+TypeScript UI |
| 🧹 Japanese Text Preprocessing| Loaded Japanese PDFs, cleaned text, removed noise, tokenized               |
| 🔪 Chunk & Embed              | Split text into chunks and generated embeddings with OpenAI API            |
| 🗄️ Vector DB Integration      | Used PostgreSQL + pgvector to store vectors for efficient search           |
| 🔍 Semantic Search API        | Built `/search` endpoint to fetch relevant chunks using vector similarity  |
| ✍️ LLM-based Summarization    | Created `/answer` endpoint to summarize search results with LLM            |
| 🖥️ Frontend Integration       | Implemented UI with React + Bootstrap for query input and result display   |

## 🧠 How it Works
- User inputs a natural language question in Japanese.
- The system generates an embedding for the question using OpenAI Embeddings.
- It searches the vector database for the most similar document chunks.
- It builds a prompt with the context and sends it to the OpenAI GPT API.
- GPT returns a concise answer in Japanese.
- The frontend displays the answer and referenced document excerpts.

### ✅ Key Implementation Highlights
- Japanese Text Processing: Used fugashi to tokenize Japanese text accurately.
- Vector Search Optimization: Stored chunk vectors using pgvector to enable fast similarity search.
- LLM Prompt Engineering: Constructed dynamic prompts with document context to ensure accurate and concise responses.
- Separation of Concerns: Clear division between document parsing, vector indexing, search, and answer generation.

### 😅 Challenges Faced
- Japanese Text Preprocessing: It was important to clean and organize the Japanese text from PDFs carefully. This included removing extra characters, fixing spaces between words, and making the text consistent so the search works better.
- TypeScript Debugging: Fixing problems in the React + TypeScript frontend took time, especially to make sure everything works well and talks correctly with the backend.
- Vector Setup & Similarity: Setting up the database to store and compare vectors was tricky, and making sure the similarity search finds the right matches took some testing.

### 📌 Future Improvements
- Create a frontend where users can upload PDF files or paste a download link.
- Combine keyword search (TF-IDF) with AI search for better results.
- Summarize information from multiple documents together.
- Deploy to a cloud platform like GCP or AWS with SSL.
- Use Kubernetes for easier scaling, management, and cloud deployment.
- Add user register/login to save search history and personalize results.

### ✨ Author

**Dinh Nguyen Duc**  
*Software Engineer (AI Infrastructure, MLOps, DevOps)*  

🇯🇵 Based in Tokyo | 🌐 English, Japanese, Vietnamese