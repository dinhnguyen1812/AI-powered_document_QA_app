from sqlalchemy import text
from .db import engine
from .utils import get_embedding

def search_similar_chunks(query: str, top_k: int = 3):
    query_embedding = get_embedding(query)

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT content, doc_id, chunk_id
                FROM doc_chunks
                ORDER BY embedding <-> :query_embedding
                LIMIT :top_k
            """),
            {"query_embedding": query_embedding, "top_k": top_k}
        )
        return result.fetchall()

