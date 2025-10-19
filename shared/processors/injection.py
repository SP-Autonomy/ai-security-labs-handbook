import re

BAD_HINTS = [
    r"ignore previous instructions",
    r"disregard all",
    r"reveal.*system prompt",
    r"exfiltrate",
    r"ignore all previous",
    r"disregard.*safety",
]

def injection_guard(req):
    """
    Detects prompt injection in user input and retrieved context.
    
    - Prompt: Single malicious pattern = BLOCK (strict)
    - Context: Single pattern = BLOCK (changed from 2+ for RAG defense)
    """
    prompt = req.get("prompt", "")
    context = req.get("context", "")
    
    # Check user prompt first (strict - single pattern blocks)
    for pattern in BAD_HINTS:
        if re.search(pattern, prompt, re.IGNORECASE):
            return {"blocked": True, "reason": "prompt_injection_suspected"}
    
    # Check retrieved context (also strict for indirect injection)
    if context:
        context_lower = context.lower()
        suspicious_count = sum(
            1 for pattern in BAD_HINTS 
            if re.search(pattern, context_lower)
        )
        
        # Block if ANY suspicious pattern in retrieved context (indirect injection!)
        if suspicious_count >= 1:  # ← Changed from >= 2
            return {"blocked": True, "reason": "prompt_injection_suspected"}
    
    return req