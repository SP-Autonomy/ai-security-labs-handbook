package ai.agent.tools

default allow_tool := false

# Researcher: Read-only research tools
allow_tool if {
  input.agent == "researcher"
  input.tool == "search_docs"
}

allow_tool if {
  input.agent == "researcher"
  input.tool == "summarize_findings"
}

# Analyst: Policy and report generation
allow_tool if {
  input.agent == "analyst"
  input.tool == "check_policy"
}

allow_tool if {
  input.agent == "analyst"
  input.tool == "generate_report"
}

# Writer: File operations (side effects allowed)
allow_tool if {
  input.agent == "writer"
  input.tool == "write_to_file"
}

allow_tool if {
  input.agent == "writer"
  input.tool == "read_file"
}

allow_tool if {
  input.agent == "writer"
  input.tool == "list_files"
}

# Admin agent: All tools (dangerous!)
allow_tool if {
  input.agent == "admin_agent"
}