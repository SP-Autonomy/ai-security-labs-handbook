"""
Tool implementations for the governed agent system.
Each tool enforces sandboxing and logs to evidence.
"""
import os
import json
import re
from pathlib import Path
from shared.gateway.providers import call_llm
from shared.evidence.logger import append_evidence

# Exfiltration patterns to detect and block
EXFIL_PATTERNS = [
    r"exfiltrat",
    r"attacker@",
    r"send.*to.*@.*\.com",
    r"leak.*data",
    r"steal.*information",
    r"transfer.*to.*external"
]

def check_exfiltration(text: str, tool_name: str) -> None:
    """
    Check text for exfiltration patterns and raise error if found.
    
    Args:
        text: Text to check
        tool_name: Name of tool performing the check
    
    Raises:
        ValueError: If exfiltration pattern detected
    """
    text_lower = text.lower()
    
    for pattern in EXFIL_PATTERNS:
        if re.search(pattern, text_lower):
            # Log detection
            append_evidence({
                "type": "exfil_pattern_blocked",
                "tool": tool_name,
                "pattern": pattern,
                "blocked": True,
                "action": "operation_blocked"
            })
            
            # Block the operation
            raise ValueError(f"exfiltration_detected: Pattern '{pattern}' found in content. Operation blocked for security.")

# ... (keep search_docs_tool and summarize_findings_tool as-is) ...

def search_docs_tool(payload: dict, sandbox_dir: str):
    """Search mock document corpus (simulated RAG)"""
    query = payload.get("query", "")
    
    # Mock document hits
    hits = [
        {
            "text": "Project X compliance status: All regulatory requirements met as of Q4 2024.",
            "source": "compliance_report_q4.pdf",
            "score": 0.95
        },
        {
            "text": "Security audit findings: No critical vulnerabilities detected. Minor issues addressed.",
            "source": "security_audit_2024.pdf",
            "score": 0.88
        },
        {
            "text": "Data governance: All PII handling procedures follow GDPR guidelines.",
            "source": "data_governance_policy.pdf",
            "score": 0.82
        }
    ]
    
    return {"query": query, "hits": hits, "count": len(hits)}

def summarize_findings_tool(payload: dict, sandbox_dir: str):
    """Summarize research findings using LLM"""
    text = payload.get("text", "")
    
    if not text:
        return {"summary": "No content to summarize", "status": "empty"}
    
    # Use LLM to summarize
    prompt = f"Summarize the following findings concisely in 2-3 sentences:\n\n{text}\n\nSummary:"
    
    print(f"[summarize_findings] Calling LLM with prompt length: {len(prompt)}")
    summary = call_llm(prompt)
    print(f"[summarize_findings] LLM returned: {len(summary)} chars")
    
    return {"summary": summary, "input_length": len(text), "status": "success"}

def check_policy_tool(payload: dict, sandbox_dir: str):
    """Check against compliance policy (mock OPA check)"""
    policy = payload.get("policy", "")
    
    # Mock policy check
    policies = {
        "compliance_v1": {"ok": True, "message": "Compliance policy v1 validated"},
        "security_v1": {"ok": True, "message": "Security policy v1 validated"},
        "restricted": {"ok": False, "message": "Access denied by policy"}
    }
    
    result = policies.get(policy, {"ok": False, "message": "Unknown policy"})
    return result

def generate_report_tool(payload: dict, sandbox_dir: str):
    """Generate formatted report using LLM"""
    title = payload.get("title", "Report")
    body = payload.get("body", "")
    
    # Check for exfiltration patterns BEFORE calling LLM
    print(f"[generate_report] Checking for exfiltration patterns...")
    check_exfiltration(body, "generate_report")
    
    prompt = (
        f"Generate a professional business report (3-4 paragraphs) with the following:\n"
        f"Title: {title}\n\n"
        f"Content: {body}\n\n"
        f"Format it as a formal business report with clear sections."
    )
    
    print(f"[generate_report] Calling LLM with prompt length: {len(prompt)}")
    report = call_llm(prompt)
    print(f"[generate_report] LLM returned: {len(report)} chars")
    
    return {"report": report, "title": title, "status": "generated"}

def write_to_file_tool(payload: dict, sandbox_dir: str):
    """Write content to file in sandbox"""
    filename = payload.get("filename", "")
    content = payload.get("content", "")
    
    if not filename:
        raise ValueError("filename_required")
    
    # Check for exfiltration patterns BEFORE writing
    print(f"[write_to_file] Checking for exfiltration patterns...")
    check_exfiltration(content, "write_to_file")
    
    # Enforce sandbox
    sandbox_path = Path(sandbox_dir).resolve()
    target_path = (sandbox_path / filename).resolve()
    
    if not str(target_path).startswith(str(sandbox_path)):
        raise ValueError(f"path_traversal_blocked: {filename}")
    
    # Write file
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    return {
        "path": str(target_path),
        "filename": filename,
        "bytes_written": len(content),
        "status": "written"
    }

def read_file_tool(payload: dict, sandbox_dir: str):
    """Read file from sandbox"""
    filename = payload.get("filename", "")
    
    # Enforce sandbox
    sandbox_path = Path(sandbox_dir).resolve()
    target_path = (sandbox_path / filename).resolve()
    
    if not str(target_path).startswith(str(sandbox_path)):
        raise ValueError(f"path_traversal_blocked: {filename}")
    
    if not target_path.exists():
        return {"error": "file_not_found", "filename": filename}
    
    with open(target_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    return {"filename": filename, "content": content, "size": len(content)}

def list_files_tool(payload: dict, sandbox_dir: str):
    """List files in sandbox"""
    sandbox_path = Path(sandbox_dir)
    
    files = []
    for item in sandbox_path.iterdir():
        if item.is_file():
            files.append({
                "name": item.name,
                "size": item.stat().st_size
            })
    
    return {"files": files, "count": len(files)}

def send_email_tool(payload: dict, sandbox_dir: str):
    """DANGEROUS: Send email (simulated, should trigger alerts)"""
    to = payload.get("to", "")
    subject = payload.get("subject", "")
    body = payload.get("body", "")
    
    # Check for exfiltration patterns
    check_exfiltration(to, "send_email")
    check_exfiltration(body, "send_email")
    
    # Simulate sending
    return {
        "status": "simulated_send",
        "to": to,
        "subject": subject,
        "warning": "This tool has side effects!"
    }