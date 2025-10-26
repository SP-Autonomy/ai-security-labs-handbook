from dotenv import load_dotenv
load_dotenv()

from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from labs.governed_agentic_ai.agent.agent_runner import orchestrate
from labs.governed_agentic_ai.tools.register_tools import register_all_tools

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: Register all tools with MCP"""
    print("[Lab03] Registering tools with MCP...")
    register_all_tools()
    print("[Lab03] Tools registered. Ready for agent orchestration.")
    yield
    print("[Lab03] Shutting down...")

app = FastAPI(title="Governed Agentic AI (Lab 03)", lifespan=lifespan)

class RunAgentBody(BaseModel):
    scenario: str = "happy_path"  # happy_path, unauthorized_tool, exfil_attempt
    user_role: str = "employee"
    question: str = "Summarize compliance state for project X"

@app.post("/run_agent")
def run_agent_endpoint(body: RunAgentBody):
    """
    Orchestrate multi-agent workflow with security controls.
    
    Scenarios:
    - happy_path: Normal operation (researcher -> analyst -> writer)
    - unauthorized_tool: Researcher attempts unauthorized write_to_file
    - exfil_attempt: Injected exfiltration command in summary
    """
    try:
        result = orchestrate(
            question=body.question,
            scenario=body.scenario,
            user_role=body.user_role
        )
        return result
        
    except ValueError as e:
        # Security block (exfiltration, path traversal, etc.)
        error_msg = str(e)
        
        return {
            "blocked": True,
            "reason": "security_violation",
            "error": error_msg,
            "scenario": body.scenario,
            "status": "blocked",
            "message": "Operation blocked by security controls"
        }
        
    except Exception as e:
        # Other errors
        return {
            "error": str(e),
            "scenario": body.scenario,
            "status": "failed"
        }

@app.get("/health")
def health():
    return {"status": "ok", "lab": "governed_agentic_ai"}