import re
from pathlib import Path
from typing import List
import pdfplumber

from fugashi import Tagger

# Japanese tokenizer
tagger = Tagger()

# Path to document directory
DOCS_DIR = Path(__file__).resolve().parent.parent / "data" / "docs"


def load_documents() -> List[str]:
    """
    Load and preprocess all documents (TXT or PDF) from the docs directory.
    Returns a list of cleaned Japanese text documents.
    """
    documents = []
    for filepath in DOCS_DIR.iterdir():
        if filepath.suffix == ".txt":
            text = filepath.read_text(encoding="utf-8")
        elif filepath.suffix == ".pdf":
            text = extract_text_from_pdf(filepath)
        else:
            continue

        cleaned = clean_japanese_text(text)
        documents.append(cleaned)
    return documents


def extract_text_from_pdf(path: Path) -> str:
    """
    Extract raw text from all pages of a PDF file using pdfplumber.
    Returns the combined text as a string.
    """
    with pdfplumber.open(str(path)) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)


def clean_japanese_text(text: str) -> str:
    """
    Preprocess Japanese text:
    - Remove excessive whitespace
    - Tokenize using MeCab (fugashi)
    - Remove symbols and punctuation
    Returns a space-separated token string.
    """
    text = re.sub(r"\s+", " ", text)
    tokens = [word.surface for word in tagger(text) if word.feature.pos1 != "記号"]
    return " ".join(tokens)

def preprocess_japanese_query(text: str) -> str:
    """
    Preprocess a Japanese search query using the same logic as documents:
    - Remove whitespace
    - Tokenize using MeCab (fugashi)
    - Remove punctuation
    Returns a space-separated token string.
    """
    text = re.sub(r"\s+", " ", text)
    tokens = [word.surface for word in tagger(text) if word.feature.pos1 != "記号"]
    return " ".join(tokens)
