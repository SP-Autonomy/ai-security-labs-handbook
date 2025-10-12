import re
BAD_HINTS = [r"ignore previous", r"disregard all", r"system prompt", r"exfiltrate", r"sudo", r"rm -rf"]
def injection_guard(req):
    text = (req.get("prompt") or "") + " " + (req.get("context") or "")
    for pat in BAD_HINTS:
        if re.search(pat, text, re.I):
            req["_blocked"] = True
            req["_reason"] = "prompt_injection_suspected"
            break
    return req