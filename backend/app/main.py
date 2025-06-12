from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from .embeddings import generate_and_save_embeddings
from .search import search_chunks_any_doc, search_chunks_same_doc
from .db_init import init_db
from .answer import get_answer

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    print("🔄 Initializing DB and running embedding generation...")
    init_db()  # ensure tables exist
    print("✅ Database is initialized.")
    print("🔄 Running embedding generation at startup...")
    generate_and_save_embeddings()
    print("✅ Embedding generation complete.")

@app.get("/search")
def search_endpoint(query: str = Query(...)):
    results = search_chunks_same_doc(query)
    return [{"doc_id": r.doc_id, "chunk_id": r.chunk_id, "text": r.content} for r in results]

@app.get("/answer")
def answer_endpoint(question: str = Query(...)):
    answer, chunks = get_answer(question)
    return {
        "answer": answer,
        "sources": [
            {
                "doc_id": c.doc_id,
                "chunk_id": c.chunk_id,
                "content": c.content,
                "filename": c.filename
            } for c in chunks
        ]
    }