from typing import List


def chunk_text(tokens: List[str], chunk_size: int = 200, overlap: int = 20) -> List[str]:
    """
    Split a list of tokens into overlapping chunks.
    Each chunk contains 'chunk_size' tokens with 'overlap' tokens overlap.
    """
    chunks = []
    for i in range(0, len(tokens), chunk_size - overlap):
        chunk = tokens[i:i + chunk_size]
        # if chunk:
        #     chunks.append(" ".join(chunk))
        chunks.append(chunk)
    return chunks

