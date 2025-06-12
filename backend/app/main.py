from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.preprocess import load_documents
from .embeddings import generate_and_save_embeddings

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Document Search App Backend is running."}

@app.get("/test-docs")
def test_docs():
    docs = load_documents()
    return {
        "count": len(docs),
        "preview": docs[1][:200] if docs else "No documents loaded"
    }

@app.on_event("startup")
async def startup_event():
    print("🔄 Running embedding generation at startup...")
    generate_and_save_embeddings()
    print("✅ Embedding generation complete.")