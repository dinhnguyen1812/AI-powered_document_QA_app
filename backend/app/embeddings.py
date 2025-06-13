from sqlalchemy import text
from .chunking import chunk_text
from .db import engine
from .preprocess import load_documents, tagger
from .utils import get_embedding

# Load documents, chunk them, generate embeddings, and save to the database
def generate_and_save_embeddings():
    docs = load_documents()  # List of (filename, cleaned_text)

    with engine.begin() as conn:  # Open a database transaction
        for idx, (filename, doc) in enumerate(docs):
            # Insert document metadata and get generated ID
            result = conn.execute(
                text("INSERT INTO documents (filename) VALUES (:filename) RETURNING id"),
                {"filename": filename}
            )
            doc_id = result.scalar_one()

            # Remove all whitespace and tokenize the text (excluding symbols)
            rejoined = "".join(doc.split())
            tokens = [word.surface for word in tagger(rejoined) if word.feature.pos1 != "記号"]
            chunks = chunk_text(tokens)  # Split tokens into text chunks

            for chunk_idx, chunk_tokens in enumerate(chunks):
                chunk = "".join(chunk_tokens).strip()
                if len(chunk) < 10:  # Skip chunks that are too short
                    continue
                chunk = chunk.replace("　", "").replace("\n", "").replace("\u3000", "")  # Clean up

                embedding = get_embedding(chunk)  # Generate vector embedding
                # Insert chunk and embedding into the database
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

    print("✅ Cleaned and saved embeddings to PostgreSQL.")

def is_valid_chunk(text: str) -> bool:
    # Check if chunk contains too many junk tokens and discard if so
    tokens = re.findall(r'\w+', text)
    if not tokens:
        return False

    junk_tokens = [t for t in tokens if re.fullmatch(r"(cid|\d+)", t)]
    junk_ratio = len(junk_tokens) / len(tokens)

    return junk_ratio < 0.3  # Valid if less than 30% junk tokens
