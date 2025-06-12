# backend/app/embeddings.py

import os
import json
import openai
from pathlib import Path
from typing import List, Dict

from .preprocess import load_documents, clean_japanese_text
from .chunking import chunk_text

# Set your OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

VEC_PATH = Path(__file__).parent / "vector_store.json"


def get_embedding(text: str, model: str = "text-embedding-3-small") -> List[float]:
    """
    Call OpenAI to get embedding for a given text.
    """
    response = openai.embeddings.create(
        model=model,
        input=text
    )
    return response.data[0].embedding


def generate_and_save_embeddings():
    """
    Load preprocessed docs, chunk them, get embeddings, and save results.
    """
    docs = load_documents()
    vector_data = []

    for doc_id, doc in enumerate(docs):
        tokens = doc.split()  # Already tokenized Japanese text
        chunks = chunk_text(tokens)

        for idx, chunk in enumerate(chunks):
            embedding = get_embedding(chunk)
            vector_data.append({
                "doc_id": doc_id,
                "chunk_id": idx,
                "text": chunk,
                "embedding": embedding
            })

    with open(VEC_PATH, "w", encoding="utf-8") as f:
        json.dump(vector_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved {len(vector_data)} embeddings to {VEC_PATH}")

