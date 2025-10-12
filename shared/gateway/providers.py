import os, requests

def call_llm(prompt: str) -> str:
    prov = os.getenv("MODEL_PROVIDER", "ollama")
    if prov == "ollama":
        model = os.getenv("GEN_MODEL", "llama3.2:3b")
        
        # Check if OLLAMA_HOST is explicitly set in .env
        ollama_host = os.getenv("OLLAMA_HOST")
        
        # Only auto-detect if OLLAMA_HOST is not set
        if not ollama_host:
            ollama_host = "http://localhost:11434"
            
            # If running in WSL and no explicit host, try to find Windows host
            if "WSL" in os.uname().release:
                try:
                    with open("/etc/resolv.conf", "r") as f:
                        for line in f:
                            if line.startswith("nameserver"):
                                windows_host = line.split()[1]
                                ollama_host = f"http://{windows_host}:11434"
                                break
                except:
                    pass
        
        r = requests.post(f"{ollama_host}/api/generate",
                          json={"model": model, "prompt": prompt, "stream": False}, timeout=120)
        r.raise_for_status()
        return r.json().get("response","")
    raise RuntimeError("Only ollama provider is configured for now")