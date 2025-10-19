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
from labs.lab02_rag_copilot.security.sanitize import sanitize
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="RAG Copilot (Lab 02)")

# ---- Initialize collection on startup (small corpus) ----
CORPUS_DIR = "labs/lab02_rag_copilot/data/corpus"

@app.on_event("startup")
def _startup():
    reset_collection()
    added = add_docs_from_folder(CORPUS_DIR)
    print(f"[Lab02] Ingested {added} docs from {CORPUS_DIR}")

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
    # Retrieve
    hits = query(body.question, k=5)
    # Sanitize retrieved text to reduce indirect injection risk
    for h in hits:
        h["text"] = sanitize(h["text"])
    # Build request; we pass retrieved context into req["context"] so the injection guard can scan it
    req = {
        "prompt": body.question,
        "user": {"role": body.user_role},
        "context": "\n\n".join([h["text"] for h in hits]),
        "chunks": hits,
    }
    return chain.run(req)