from sqlalchemy import text
from .db import engine
from .preprocess import preprocess_japanese_query
from .utils import get_embedding

def search_chunks_any_doc(query: str, top_k: int = 3):
    # Step 1: Preprocess the Japanese query text
    clean_query = preprocess_japanese_query(query)
    
    # Step 2: Get vector from OpenAI
    query_embedding = get_embedding(clean_query)

    # Step 3: Run pgvector similarity search
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT content, doc_id, chunk_id
                FROM doc_chunks
                ORDER BY embedding <-> CAST(:query_embedding AS vector)
                LIMIT :top_k
            """),
            {"query_embedding": query_embedding, "top_k": top_k}
        )
        return result.fetchall()

def search_chunks_same_doc(query: str, top_k: int = 3):
    """
    Search top-k most relevant chunks from the same document based on a Japanese query.
    1. Preprocess the query text (same as document preprocessing).
    2. Embed the query using OpenAI.
    3. Find the most relevant document.
    4. Retrieve top-k matching chunks from that document.
    """
    # Step 1: Preprocess and embed the query
    clean_query = preprocess_japanese_query(query)
    query_embedding = get_embedding(clean_query)

    with engine.connect() as conn:
        # Step 2: Find the most relevant doc_id across all chunks
        best_doc = conn.execute(
            text("""
                WITH top_chunks AS (
                    SELECT doc_id, embedding <-> CAST(:query_embedding AS vector) AS distance
                    FROM doc_chunks
                    ORDER BY embedding <-> CAST(:query_embedding AS vector)
                    LIMIT 20
                )
                SELECT doc_id
                FROM top_chunks
                GROUP BY doc_id
                ORDER BY SUM(distance)
                LIMIT 1
            """),
            {"query_embedding": query_embedding}
        ).fetchone()

        if not best_doc:
            return []

        doc_id = best_doc.doc_id

        # Step 3: Search top-k chunks within the most relevant document
        result = conn.execute(
            text("""
                SELECT content, doc_id, chunk_id
                FROM doc_chunks
                WHERE doc_id = :doc_id
                ORDER BY embedding <-> CAST(:query_embedding AS vector)
                LIMIT :top_k
            """),
            {"doc_id": doc_id, "query_embedding": query_embedding, "top_k": top_k}
        )

        return result.fetchall()
