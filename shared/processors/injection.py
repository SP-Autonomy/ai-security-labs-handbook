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
    - Context: Multiple patterns = BLOCK (reduce false positives)
    """
    prompt = req.get("prompt", "")
    context = req.get("context", "")
    
    # Check user prompt first (strict - single pattern blocks)
    # This ensures Lab 01 tests still work!
    for pattern in BAD_HINTS:
        if re.search(pattern, prompt, re.IGNORECASE):
            return {"blocked": True, "reason": "prompt_injection_suspected"}
    
    # Check retrieved context (lenient - requires 2+ patterns)
    # This reduces false positives from documents discussing attacks
    if context:
        context_lower = context.lower()
        suspicious_count = sum(
            1 for pattern in BAD_HINTS 
            if re.search(pattern, context_lower)
        )
        
        # Block if multiple suspicious patterns (likely actual attack)
        if suspicious_count >= 2:
            return {"blocked": True, "reason": "prompt_injection_suspected"}
    
    return req