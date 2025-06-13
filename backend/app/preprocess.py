import re
import unicodedata
from pathlib import Path
from typing import List, Tuple
import pdfplumber
from fugashi import Tagger

# Initialize Japanese tokenizer (MeCab-based)
tagger = Tagger()

# Regex pattern for Japanese punctuation to remove
JAPANESE_PUNCTUATION = r"[●○◆■◇★☆●！？。、．「」〔〕（）『』［］｛｝【】〈〉《》≪≫“”‘’・：；…／＼〜～–—ー‐\-\(\)\[\]{}<>@#$%^&*_+=|~`\"'.,!?]"

# Directory path where document files are stored
DOCS_DIR = Path(__file__).resolve().parent.parent / "data" / "docs"

def load_documents() -> List[Tuple[str, str]]:
    # Load and clean all .txt and .pdf documents from DOCS_DIR
    documents = []
    for filepath in DOCS_DIR.iterdir():
        if filepath.suffix == ".txt":
            text = filepath.read_text(encoding="utf-8")
        elif filepath.suffix == ".pdf":
            text = extract_text_from_pdf(filepath)
        else:
            continue

        cleaned = clean_japanese_text(text)
        documents.append((filepath.name, cleaned))
    return documents

def extract_text_from_pdf(path: Path) -> str:
    # Extract and concatenate all text from each page of the PDF
    with pdfplumber.open(str(path)) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)

def clean_japanese_text(text: str) -> str:
    # Normalize Unicode characters (e.g. full-width to half-width)
    text = unicodedata.normalize("NFKC", text)

    # Remove metadata-like patterns and unwanted tokens
    text = re.sub(r"[a-zA-Z]{4,}", "", text)
    text = re.sub(r"[/:\d]{4,}", "", text)
    text = re.sub(r"cid[\w]*", "", text)
    text = re.sub(r"cid\s*:\s*\d+", "", text)

    # Remove all whitespace characters (including full-width spaces)
    text = re.sub(r"[ \u3000\n\r\t]+", "", text)

    # Remove Japanese punctuation marks
    text = re.sub(JAPANESE_PUNCTUATION, "", text)

    # Deduplicate consecutive kana/kanji characters (e.g., 循循 → 循)
    text = re.sub(r'([ぁ-んァ-ン一-龯々])\1+', r'\1', text)

    # Tokenize text and remove symbol tokens (記号)
    tokens = [word.surface for word in tagger(text) if word.feature.pos1 != "記号"]

    return "".join(tokens)

def preprocess_japanese_query(query: str) -> str:
    # Clean and normalize input query text for consistent searching
    text = unicodedata.normalize("NFKC", query)
    text = re.sub(r"[a-zA-Z]{4,}", "", text)
    text = re.sub(r"[/:\d]{4,}", "", text)
    text = re.sub(r"cid[\w]*", "", text)
    text = re.sub(r"cid\s*:\s*\d+", "", text)
    text = re.sub(r"[ \u3000\n\r\t]+", "", text)
    text = re.sub(JAPANESE_PUNCTUATION, "", text)
    text = re.sub(r'([ぁ-んァ-ン一-龯々])\1+', r'\1', text)
    tokens = [word.surface for word in tagger(text) if word.feature.pos1 != "記号"]
    return "".join(tokens)
