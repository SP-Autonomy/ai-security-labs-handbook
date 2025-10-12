package ai.policy

default allow = false

# Rule 1: Employees can process non-sensitive data
allow if {
  input.user.role == "employee"
  not input.request.contains_sensitive
}

# Rule 2: Employees with PII clearance can process sensitive data
allow if {
  input.user.role == "employee"
  input.user.clearance == "pii_approved"
  input.request.contains_sensitive
}

# Rule 3: Contractors are never allowed
deny if { 
  input.user.role == "contractor" 
}