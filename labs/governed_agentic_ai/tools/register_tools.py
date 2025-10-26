"""
Register all tools with the MCP stub with proper schemas and constraints.
"""
from shared.agent.mcp_stub import mcp, Tool
from .tool_implementations import (
    search_docs_tool,
    summarize_findings_tool,
    check_policy_tool,
    generate_report_tool,
    write_to_file_tool,
    read_file_tool,
    list_files_tool,
    send_email_tool
)

def register_all_tools():
    """Register all tools with schemas and budgets"""
    
    # Search docs - safe, read-only
    mcp.register_tool(Tool(
        name="search_docs",
        func=search_docs_tool,
        schema={
            "type": "object",
            "properties": {
                "query": {"type": "string"}
            },
            "required": ["query"]
        },
        owner="system",
        side_effect=False,
        max_calls=10,
        max_seconds=180
    ))
    
    # Summarize findings - uses LLM, read-only
    mcp.register_tool(Tool(
        name="summarize_findings",
        func=summarize_findings_tool,
        schema={
            "type": "object",
            "properties": {
                "text": {"type": "string"}
            },
            "required": ["text"]
        },
        owner="system",
        side_effect=False,
        max_calls=5,
        max_seconds=180
    ))
    
    # Check policy - safe, read-only
    mcp.register_tool(Tool(
        name="check_policy",
        func=check_policy_tool,
        schema={
            "type": "object",
            "properties": {
                "policy": {"type": "string"}
            },
            "required": ["policy"]
        },
        owner="system",
        side_effect=False,
        max_calls=10,
        max_seconds=180
    ))
    
    # Generate report - uses LLM, read-only
    mcp.register_tool(Tool(
        name="generate_report",
        func=generate_report_tool,
        schema={
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "body": {"type": "string"}
            },
            "required": ["title", "body"]
        },
        owner="system",
        side_effect=False,
        max_calls=5,
        max_seconds=180
    ))
    
    # Write to file - has side effects, restricted
    mcp.register_tool(Tool(
        name="write_to_file",
        func=write_to_file_tool,
        schema={
            "type": "object",
            "properties": {
                "filename": {"type": "string"},
                "content": {"type": "string"}
            },
            "required": ["filename", "content"]
        },
        owner="admin",
        side_effect=True,  # Has side effects!
        max_calls=3,
        max_seconds=180
    ))
    
    # Read file - read-only
    mcp.register_tool(Tool(
        name="read_file",
        func=read_file_tool,
        schema={
            "type": "object",
            "properties": {
                "filename": {"type": "string"}
            },
            "required": ["filename"]
        },
        owner="system",
        side_effect=False,
        max_calls=10,
        max_seconds=180
    ))
    
    # List files - read-only
    mcp.register_tool(Tool(
        name="list_files",
        func=list_files_tool,
        schema={"type": "object"},
        owner="system",
        side_effect=False,
        max_calls=10,
        max_seconds=180
    ))
    
    # Send email - DANGEROUS, has side effects
    mcp.register_tool(Tool(
        name="send_email",
        func=send_email_tool,
        schema={
            "type": "object",
            "properties": {
                "to": {"type": "string"},
                "subject": {"type": "string"},
                "body": {"type": "string"}
            },
            "required": ["to", "subject", "body"]
        },
        owner="admin",
        side_effect=True,  # Has side effects!
        max_calls=1,
        max_seconds=180
    ))