# backend/app/embeddings.py

from sqlalchemy import text
from .chunking import chunk_text
from .db import engine
from .preprocess import load_documents
from .utils import get_embedding

def generate_and_save_embeddings():
    """
    Load preprocessed docs, insert documents, chunk them, get embeddings, 
    and save embeddings to PostgreSQL.
    """

    docs = load_documents()

    with engine.begin() as conn:  # Use begin() for transactional commit
        for idx, doc in enumerate(docs):
            # Insert document first, with filename or some identifier (replace with your actual filename or doc metadata)
            result = conn.execute(
                text("INSERT INTO documents (filename) VALUES (:filename) RETURNING id"),
                {"filename": f"doc_{idx + 1}"}
            )
            doc_id = result.scalar_one()  # Get the generated document ID
            
            tokens = doc.split()  # Already tokenized Japanese text
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
