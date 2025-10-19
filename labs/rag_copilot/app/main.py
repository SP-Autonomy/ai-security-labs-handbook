from dotenv import load_dotenv
load_dotenv()

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from shared.gateway.gateway import Chain
from shared.gateway.providers import call_llm
from shared.processors.injection import injection_guard
from shared.processors.dlp import dlp_pre, dlp_post
from shared.processors.policy_opa import policy_gate
from shared.processors.provenance import add_provenance
from shared.rag.store_chroma import reset_collection, add_docs_from_folder, query
from labs.rag_copilot.security.sanitize import sanitize

# Configuration
CORPUS_DIR = "labs/rag_copilot/data/corpus"
REDTEAM_DIR = "labs/rag_copilot/redteam/ipi_pages"
TEST_MODE = os.getenv("RAG_TEST_MODE", "false").lower() == "true"

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    Replaces deprecated @app.on_event("startup")
    """
    # Startup: Ingest documents
    reset_collection()
    
    # Ingest trusted corpus (with validation)
    added = add_docs_from_folder(CORPUS_DIR, validate=True)
    print(f"[Lab02] Ingested {added} trusted docs from {CORPUS_DIR}")
    
    # In test mode, ingest red team docs WITHOUT validation
    if TEST_MODE:
        print(f"[Lab02] 🔴 TEST MODE ACTIVE: Including red team documents")
        redteam_added = add_docs_from_folder(REDTEAM_DIR, validate=False)
        print(f"[Lab02] 🔴 TEST MODE: Ingested {redteam_added} red team docs (unvalidated)")
        print(f"[Lab02] Total: {added + redteam_added} docs")
    else:
        print(f"[Lab02] Production mode: Red team docs excluded")
    
    yield  # Application runs here
    
    # Shutdown: Cleanup if needed
    print("[Lab02] Shutting down...")

# Initialize FastAPI with lifespan
app = FastAPI(title="RAG Copilot (Lab 02)", lifespan=lifespan)

class AskBody(BaseModel):
    question: str
    user_role: str = "employee"

def llm_call(req):
    # Build a grounded prompt with citations
    ctx_lines = []
    for i, c in enumerate(req.get("chunks", []), start=1):
        ctx_lines.append(f"[{i}] {c['text']}\n(Source: {c['source']})")
    context = "\n\n".join(ctx_lines)
    prompt = (
        "You are a concise security copilot. Answer using only the provided context. "
        "Cite sources like [1], [2]. If the answer is not in the context, say 'Not found in provided context.'\n\n"
        f"Question: {req['prompt']}\n\nContext:\n{context}\n\nAnswer:"
    )
    return {"answer": call_llm(prompt), "source_ids": [c["source"] for c in req.get("chunks", [])]}

# Chain: reuse existing processors. injection_guard inspects both prompt & context.
chain = Chain(pre=[dlp_pre, injection_guard, policy_gate],
              post=[dlp_post, add_provenance],
              llm_call=llm_call)

@app.post("/ask")
def ask(body: AskBody):
    # Retrieve documents
    hits = query(body.question, k=3)
    
    # Build request with UNSANITIZED context for security checks
    req = {
        "prompt": body.question,
        "user": {"role": body.user_role},
        "context": "\n\n".join([h["text"] for h in hits]),  # ← RAW content
        "chunks": hits,
    }
    
    # Run security checks on raw content
    req = dlp_pre(req)
    if req.get("blocked"):
        return req
    
    req = injection_guard(req)
    if req.get("blocked"):
        return req
    
    req = policy_gate(req)
    if req.get("blocked"):
        return req
    
    # NOW sanitize before LLM call
    for h in hits:
        h["text"] = sanitize(h["text"])
    req["context"] = "\n\n".join([h["text"] for h in hits])
    req["chunks"] = hits
    
    # Call LLM with sanitized content
    result = llm_call(req)
    req.update(result)
    
    # Post-processing
    req = dlp_post(req)
    req = add_provenance(req)
    
    return req