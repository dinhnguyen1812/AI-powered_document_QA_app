from sqlalchemy import text
from .db import engine

def init_db():
    with engine.begin() as conn:  # <-- begin() ensures commit
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS documents (
                id SERIAL PRIMARY KEY,
                filename TEXT NOT NULL
            );
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS doc_chunks (
                id SERIAL PRIMARY KEY,
                doc_id INTEGER REFERENCES documents(id),
                chunk_id INTEGER,
                content TEXT,
                embedding VECTOR(1536)
            );
        """))