run-api:
	uvicorn labs.01-pii-safe-summarizer.app.main:app --reload --port 8000
run-opa:
	opa run --server labs/01-pii-safe-summarizer/security/policy.rego
test-malicious-contractor:
	@echo "=== Test 1: Malicious content + contractor (should be BLOCKED) ==="
	@curl -s -X POST -F "file=@tests/malicious-contractor.txt" -F "user_role=contractor" http://localhost:8000/summarize | python -m json.tool
	@echo ""
test-benign-employee:
	@echo "=== Test 2: Benign content + employee (should SUCCEED) ==="
	@curl -s -X POST -F "file=@tests/benign-employee.txt" -F "user_role=employee" http://localhost:8000/summarize | python -m json.tool
	@echo ""
test-sensitive-employee-denied:
	@echo "=== Test 3: Sensitive content + regular employee (should be BLOCKED) ==="
	@curl -s -X POST -F "file=@tests/sensitive-employee.txt" -F "user_role=employee" http://localhost:8000/summarize | python -m json.tool
	@echo ""
test-sensitive-employee-approved:
	@echo "=== Test 4: Sensitive content + PII-approved employee (should SUCCEED with masking) ==="
	@curl -s -X POST -F "file=@tests/sensitive-employee.txt" -F "user_role=employee" -F "user_clearance=pii_approved" http://localhost:8000/summarize | python -m json.tool
	@echo ""
test-all:
	@make test-malicious-contractor
	@make test-benign-employee
	@make test-sensitive-employee-denied
	@make test-sensitive-employee-approved