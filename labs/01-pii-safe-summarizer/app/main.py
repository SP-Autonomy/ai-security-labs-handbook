from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, Form
from shared.gateway.gateway import Chain
from shared.gateway.providers import call_llm
from shared.processors.injection import injection_guard
from shared.processors.dlp import dlp_pre, dlp_post
from shared.processors.policy_opa import policy_gate
from shared.processors.provenance import add_provenance

app = FastAPI(title="PII-Safe Summarizer")

def llm_call(req):
    prompt = f"Summarize into 5 bullets and 3 short action items. Be concise.\n\n{req['prompt']}"
    return {"answer": call_llm(prompt)}

chain = Chain(pre=[dlp_pre, injection_guard, policy_gate],
              post=[dlp_post, add_provenance],
              llm_call=llm_call)

@app.post("/summarize")
async def summarize(
    file: UploadFile, 
    user_role: str = Form("contractor"),
    user_clearance: str = Form(None)  # ← NEW: optional clearance level
):
    text = (await file.read()).decode("utf-8")[:100_000]
    user = {"role": user_role}
    if user_clearance:
        user["clearance"] = user_clearance
    req = {"prompt": text, "user": user}
    return chain.run(req)