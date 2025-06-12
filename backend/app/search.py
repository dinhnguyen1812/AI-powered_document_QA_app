from sqlalchemy import text
from .db import engine
from .preprocess import preprocess_japanese_query
from .utils import get_embedding

def search_chunks_any_doc(query: str, top_k: int = 3):
    clean_query = preprocess_japanese_query(query)
    query_embedding = get_embedding(clean_query)

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT c.content, c.doc_id, c.chunk_id, d.filename
                FROM doc_chunks c
                JOIN documents d ON c.doc_id = d.id
                ORDER BY c.embedding <-> CAST(:query_embedding AS vector)
                LIMIT :top_k
            """),
            {"query_embedding": query_embedding, "top_k": top_k}
        )
        return result.fetchall()

def search_chunks_same_doc(query: str, top_k: int = 3):
    clean_query = preprocess_japanese_query(query)
    query_embedding = get_embedding(clean_query)

    with engine.connect() as conn:
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

        result = conn.execute(
            text("""
                SELECT c.content, c.doc_id, c.chunk_id, d.filename
                FROM doc_chunks c
                JOIN documents d ON c.doc_id = d.id
                WHERE c.doc_id = :doc_id
                ORDER BY c.embedding <-> CAST(:query_embedding AS vector)
                LIMIT :top_k
            """),
            {"doc_id": doc_id, "query_embedding": query_embedding, "top_k": top_k}
        )

        return result.fetchall()