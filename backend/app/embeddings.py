from sqlalchemy import text
from .chunking import chunk_text
from .db import engine
from .preprocess import load_documents
from .utils import get_embedding

def generate_and_save_embeddings():
    docs = load_documents()  # List of (filename, cleaned_text)

    with engine.begin() as conn:
        for idx, (filename, doc) in enumerate(docs):
            # Insert document with real filename
            result = conn.execute(
                text("INSERT INTO documents (filename) VALUES (:filename) RETURNING id"),
                {"filename": filename}
            )
            doc_id = result.scalar_one()
            
            tokens = doc.split()
            chunks = chunk_text(tokens)

            for chunk_idx, chunk in enumerate(chunks):
                embedding = get_embedding(chunk)
                conn.execute(
                    text("""
                        INSERT INTO doc_chunks (doc_id, chunk_id, content, embedding)
                        VALUES (:doc_id, :chunk_id, :content, :embedding)
                    """),
                    {
                        "doc_id": doc_id,
                        "chunk_id": chunk_idx,
                        "content": chunk,
                        "embedding": embedding
                    }
                )

    print("✅ Saved embeddings to PostgreSQL with pgvector.")

