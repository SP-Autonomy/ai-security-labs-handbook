"""
Agent Tool Guard helpers used by the orchestrator and tools.
"""
import uuid, time
from shared.evidence.logger import append_evidence

def new_run_id():
    return f"run-{uuid.uuid4().hex[:8]}"

def log_agent_event(run_id, agent_id, event_type, details):
    append_evidence({
        "type": "agent_event",
        "run_id": run_id,
        "agent_id": agent_id,
        "event": event_type,
        "details": details,
        "ts": time.time()
    })