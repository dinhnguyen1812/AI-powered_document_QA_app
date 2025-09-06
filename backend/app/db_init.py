from sqlalchemy import text
from .db import engine
from .embeddings import generate_and_save_embeddings
# Initialize the database: create required extensions and tables if they don't exist
def init_db():
    with engine.begin() as conn:  # begin() creates a transaction and auto-commits on success
        # Enable the 'vector' extension for embedding support
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))

        # Create 'documents' table to store uploaded document metadata
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS documents (
                id SERIAL PRIMARY KEY,
                filename TEXT NOT NULL
            );
        """))

        # Create 'doc_chunks' table to store text chunks and their vector embeddings
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS doc_chunks (
                id SERIAL PRIMARY KEY,
                doc_id INTEGER REFERENCES documents(id),
                chunk_id INTEGER,
                content TEXT,
                embedding VECTOR(1536)
            );
        """))

if __name__ == "__main__":
    print("🔄 Initializing DB...")
    init_db()
    print("✅ DB initialized")

    print("🔄 Generating embeddings...")
    generate_and_save_embeddings()
    print("✅ Embeddings generated")