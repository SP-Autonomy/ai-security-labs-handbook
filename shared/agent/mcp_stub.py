"""
A local MCP-like tool registry & enforcement layer.
- Register tools with name, schema, owner, side_effects flag.
- Enforce allowlist, JSON Schema validation, budgets, and sandbox constraints.
- Provide ephemeral token stubs (not real cryptography) for demo traceability.
"""
import time, uuid, os, json, requests
from jsonschema import validate, ValidationError
from pathlib import Path
from shared.evidence.logger import append_evidence

class ToolError(Exception):
    pass

class BudgetExceeded(ToolError):
    pass

class UnauthorizedTool(ToolError):
    pass

class Tool:
    def __init__(self, name, func, schema=None, owner="admin", side_effect=False, max_calls=5, max_seconds=30):
        self.name = name
        self.func = func
        self.schema = schema or {}
        self.owner = owner
        self.side_effect = side_effect
        self.max_calls = max_calls
        self.max_seconds = max_seconds

class MCP:
    def __init__(self, sandbox_dir="labs/governed_agentic_ai/sandbox_outputs"):
        self.tools = {}
        self.calls = {}  # run_id -> {tool_name: count}
        self.times = {}  # run_id -> total seconds
        self.sandbox_dir = Path(sandbox_dir)
        self.sandbox_dir.mkdir(parents=True, exist_ok=True)
        self.opa_url = os.getenv("AGENT_OPA_URL", "http://localhost:8181/v1/data/ai/agent/tools/allow_tool")

    def register_tool(self, tool: Tool):
        self.tools[tool.name] = tool

    def mint_token(self):
        return f"token-{uuid.uuid4().hex[:8]}"

    def check_allowed(self, tool_name, agent_id, run_id):
        """Check if agent is allowed to use this tool via OPA"""
        if tool_name not in self.tools:
            raise ToolError(f"unknown_tool:{tool_name}")
        
        # Call OPA for authorization
        try:
            response = requests.post(
                self.opa_url,
                json={"input": {"agent": agent_id, "tool": tool_name}},
                timeout=2
            )
            
            if response.status_code == 200:
                result = response.json()
                allowed = result.get("result", False)
                
                if not allowed:
                    # Log unauthorized attempt
                    append_evidence({
                        "type": "unauthorized_tool_attempt",
                        "run_id": run_id,
                        "agent_id": agent_id,
                        "tool": tool_name,
                        "blocked": True,
                        "reason": "opa_policy_denied"
                    })
                    raise UnauthorizedTool(f"agent '{agent_id}' not allowed to use tool '{tool_name}'")
                
                return True
            else:
                # OPA error - fail closed
                append_evidence({
                    "type": "opa_error",
                    "run_id": run_id,
                    "status_code": response.status_code,
                    "tool": tool_name,
                    "agent": agent_id
                })
                raise ToolError(f"opa_check_failed: {response.status_code}")
        
        except requests.exceptions.RequestException as e:
            # OPA unavailable - fail closed for security
            append_evidence({
                "type": "opa_unavailable",
                "run_id": run_id,
                "error": str(e),
                "tool": tool_name,
                "agent": agent_id
            })
            raise ToolError(f"opa_unavailable: {str(e)}")

    def enforce_schema(self, tool: Tool, payload: dict):
        if tool.schema:
            try:
                validate(instance=payload, schema=tool.schema)
            except ValidationError as e:
                raise ToolError(f"schema_violation:{e.message}")

    def enforce_budget(self, tool: Tool, run_id: str):
        """Enforce per-tool call limits and per-run time limits"""
        # Per-tool call limit
        self.calls.setdefault(run_id, {})
        self.calls[run_id].setdefault(tool.name, 0)
        if self.calls[run_id][tool.name] >= tool.max_calls:
            raise BudgetExceeded(f"max_calls_exceeded:{tool.name} (limit: {tool.max_calls})")
    
        # Per-run time budget (cumulative across all tools)
        self.times.setdefault(run_id, 0)
        # Use the highest max_seconds among all tools for the total run budget
        max_run_time = 300  # 5 minutes total for entire workflow
        if self.times[run_id] >= max_run_time:
            raise BudgetExceeded(f"max_run_time_exceeded (spent: {self.times[run_id]:.1f}s, limit: {max_run_time}s)")

    def record_call(self, tool: Tool, run_id: str, elapsed: float):
        self.calls.setdefault(run_id, {})
        self.calls[run_id].setdefault(tool.name, 0)
        self.calls[run_id][tool.name] += 1
        self.times.setdefault(run_id, 0)
        self.times[run_id] += elapsed

    def call_tool(self, tool_name: str, agent_id: str, run_id: str, payload: dict):
        if tool_name not in self.tools:
            raise ToolError("tool_not_found")
        tool = self.tools[tool_name]
        
        # 1. Authorization check (OPA)
        self.check_allowed(tool_name, agent_id, run_id)
        
        # 2. Schema validation
        self.enforce_schema(tool, payload)
        
        # 3. Budget enforcement
        self.enforce_budget(tool, run_id)
        
        # 4. Execute tool
        t0 = time.time()
        result = tool.func(payload, sandbox_dir=str(self.sandbox_dir))
        elapsed = time.time() - t0
        
        # 5. Record metrics
        self.record_call(tool, run_id, elapsed)
        
        # 6. Log to evidence
        append_evidence({
            "type": "tool_call",
            "run_id": run_id,
            "agent_id": agent_id,
            "tool": tool_name,
            "payload": payload,
            "result": result,
            "elapsed": elapsed,
            "authorized": True
        })
        
        return result

mcp = MCP()