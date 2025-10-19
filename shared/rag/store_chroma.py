import os, uuid, glob
from typing import List, Dict, Optional, Any
import chromadb
from .ollama_embed import embed_texts

# Chroma client with persistent storage
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_data")
_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
_collection_name = os.getenv("RAG_COLLECTION", "lab02_docs")
_collection: Optional[Any] = None

# Content validation patterns (same as injection guard)
SUSPICIOUS_PATTERNS = [
    r"ignore previous instructions",
    r"disregard all",
    r"reveal.*system prompt",
    r"exfiltrate",
    r"ignore all previous",
    r"disregard.*safety",
]

def get_collection():
    """Get or create the collection"""
    global _collection
    if _collection is None:
        _collection = _client.get_or_create_collection(name=_collection_name)
    return _collection

def reset_collection():
    """Reset the collection - delete and recreate"""
    global _collection
    try:
        _client.delete_collection(_collection_name)
    except Exception:
        pass
    _collection = _client.get_or_create_collection(name=_collection_name)
    return _collection

def validate_document(text: str, source_path: str) -> tuple[bool, str]:
    """
    Validate document before ingestion.
    Returns (is_valid, reason)
    """
    import re
    
    # Count suspicious patterns
    suspicious_count = sum(
        1 for pattern in SUSPICIOUS_PATTERNS 
        if re.search(pattern, text, re.IGNORECASE)
    )
    
    # Allow documents from redteam folder (for testing)
    if "redteam" in source_path or "ipi_pages" in source_path:
        return True, "redteam_document"
    
    # Block if 2+ malicious patterns (likely attack)
    if suspicious_count >= 2:
        return False, f"rejected_suspicious_content ({suspicious_count} patterns)"
    
    return True, "accepted"

def add_docs_from_folder(folder: str, validate: bool = True) -> int:
    """
    Add documents from folder with optional validation.
    
    Args:
        folder: Path to folder containing documents
        validate: If True, validate documents before ingestion (default: True)
    
    Returns:
        Number of documents successfully added
    """
    paths = sorted(glob.glob(os.path.join(folder, "*.md"))) + \
            sorted(glob.glob(os.path.join(folder, "*.txt")))
    
    if not paths:
        return 0
    
    ids, docs, meta = [], [], []
    rejected = []
    
    for p in paths:
        with open(p, "r", encoding="utf-8") as f:
            txt = f.read()
        
        # Validate if enabled
        if validate:
            is_valid, reason = validate_document(txt, p)
            if not is_valid:
                rejected.append((p, reason))
                print(f"⚠️  Rejected: {p} ({reason})")
                continue
        
        did = str(uuid.uuid4())
        ids.append(did)
        docs.append(txt)
        meta.append({
            "source_path": p,
            "trust_level": "redteam" if "redteam" in p else "internal"
        })
    
    if not docs:
        return 0
    
    embeddings = embed_texts(docs)
    
    collection = get_collection()
    collection.add(
        documents=docs, 
        metadatas=meta, 
        embeddings=embeddings,  # type: ignore
        ids=ids
    )
    
    if rejected:
        print(f"⚠️  Total rejected: {len(rejected)} documents")
    
    return len(ids)

def query(question: str, k: int = 3) -> List[Dict[str, Any]]:
    qemb = embed_texts([question])[0]
    
    collection = get_collection()
    res: Any = collection.query(
        query_embeddings=[qemb], 
        n_results=k, 
        include=["documents", "metadatas", "distances"]
    )
    
    hits: List[Dict[str, Any]] = []
    
    if res and res.get("ids") and len(res["ids"]) > 0:
        for i in range(len(res["ids"][0])):
            hits.append({
                "id": res["ids"][0][i],
                "text": res["documents"][0][i],
                "source": res["metadatas"][0][i]["source_path"],
                "distance": res["distances"][0][i],
            })
    
    return hits