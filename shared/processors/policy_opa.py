import os, requests, json
OPA_URL = os.getenv("OPA_URL", "http://localhost:8181/v1/data/ai/policy/allow")

def policy_gate(req):
    payload = {"input": {"user": req.get("user", {}), "request": {"intent": req.get("intent","summarize"),
                                                                  "contains_sensitive": req.get("contains_sensitive", False)}}}
    try:
        resp = requests.post(OPA_URL, json=payload, timeout=2)
        allow = resp.json().get("result", False)
    except Exception:
        allow = False
    if not allow:
        req["_blocked"] = True
        req["_reason"] = "policy_denied"
    return req