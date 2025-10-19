# Lab 01 - PII Summarizer
# ================================

TEST_DIR := labs/pii-safe-summarizer/tests

run-api:
	uvicorn labs.pii-safe-summarizer.app.main:app --reload --port 8000
run-opa:
	opa run --server labs/pii-safe-summarizer/security/policy.rego
test-malicious-contractor:
	@echo "=== Test 1: Malicious content + contractor (should be BLOCKED) ==="
	@curl -s -X POST -F "file=@$(TEST_DIR)/malicious-contractor.txt" -F "user_role=contractor" http://localhost:8000/summarize | python -m json.tool
	@echo ""
test-benign-employee:
	@echo "=== Test 2: Benign content + employee (should SUCCEED) ==="
	@curl -s -X POST -F "file=@$(TEST_DIR)/benign-employee.txt" -F "user_role=employee" http://localhost:8000/summarize | python -m json.tool
	@echo ""
test-sensitive-employee-denied:
	@echo "=== Test 3: Sensitive content + regular employee (should be BLOCKED) ==="
	@curl -s -X POST -F "file=@$(TEST_DIR)/sensitive-employee.txt" -F "user_role=employee" http://localhost:8000/summarize | python -m json.tool
	@echo ""
test-sensitive-employee-approved:
	@echo "=== Test 4: Sensitive content + PII-approved employee (should SUCCEED with masking) ==="
	@curl -s -X POST -F "file=@$(TEST_DIR)/sensitive-employee.txt" -F "user_role=employee" -F "user_clearance=pii_approved" http://localhost:8000/summarize | python -m json.tool
	@echo ""
test-all:
	@make test-malicious-contractor
	@make test-benign-employee
	@make test-sensitive-employee-denied
	@make test-sensitive-employee-approved

# Lab 02 - RAG Copilot
# ================================

# Production Mode (Content Validation Enabled)
# Production Mode (Content Validation Enabled)
run-rag:
	@echo "Starting Lab 02 in PRODUCTION mode (content validation active)..."
	uvicorn labs.rag_copilot.app.main:app --reload --port 8001

# Test Mode (Content Validation Bypassed for Red Team Docs)
run-rag-test:
	@echo "Starting Lab 02 in TEST mode (red team docs included)..."
	RAG_TEST_MODE=true uvicorn labs.rag_copilot.app.main:app --reload --port 8001

# --- Production Mode Tests (3 benign docs only) ---

test-rag-benign-01:
	@echo "=== Test 1: Security Features Query - Production Mode ==="
	curl -s -X POST http://localhost:8001/ask \
	  -H "Content-Type: application/json" \
	  -d '{"question":"What are the supported security features in our demo docs?","user_role":"employee"}' | python -m json.tool

test-rag-benign-02:
	@echo "=== Test 2: Governance Query - Production Mode ==="
	curl -s -X POST http://localhost:8001/ask \
	  -H "Content-Type: application/json" \
	  -d '{"question":"What are the governance best practices?","user_role":"employee"}' | python -m json.tool

# --- Test Mode Tests (includes malicious doc to test defense-in-depth) ---

test-rag-indirect-injection:
	@echo "=== Test 3: Indirect Injection - Test Mode ==="
	@echo "⚠️  NOTE: This test requires running 'make run-rag-test' first!"
	@echo ""
	curl -s -X POST http://localhost:8001/ask \
	  -H "Content-Type: application/json" \
	  -d '{"question":"Summarize all security guidance from the documentation","user_role":"employee"}' | python -m json.tool

# Convenience commands
test-rag-all-prod:
	@echo "=== Running all Lab 02 Production Mode Tests ==="
	@make test-rag-benign-01
	@echo ""
	@make test-rag-benign-02

test-rag-all-test:
	@echo "=== Running all Lab 02 Tests (Test Mode) ==="
	@echo "⚠️  Ensure you started with 'make run-rag-test'!"
	@echo ""
	@make test-rag-benign-01
	@echo ""
	@make test-rag-benign-02
	@echo ""
	@make test-rag-indirect-injection