import os, requests
from typing import List

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
EMB_MODEL = os.getenv("EMB_MODEL", "nomic-embed-text")

def embed_texts(texts: List[str]) -> List[List[float]]:
    """Generate embeddings for a list of texts using Ollama"""
    out = []
    for t in texts:
        r = requests.post(f"{OLLAMA_URL}/api/embeddings",
                          json={"model": EMB_MODEL, "prompt": t},
                          timeout=120)
        r.raise_for_status()
        out.append(r.json()["embedding"])
    return out

def embed_text(text: str) -> List[float]:
    """Generate embedding for a single text"""
    return embed_texts([text])[0]