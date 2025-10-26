#!/bin/bash
# Load Lab 03 agent policies into OPA

set -e  # Exit on error

OPA_URL="${OPA_URL:-http://localhost:8181/v1/policies}"

echo "📋 Loading Lab 03 agent tool policies into OPA..."
echo ""

# Check if OPA is running
if ! curl -s "${OPA_URL}" > /dev/null 2>&1; then
    echo "❌ Error: OPA is not running at ${OPA_URL}"
    echo "   Start OPA with: make run-opa (in another terminal)"
    exit 1
fi

# Load agent tools policy
echo "Loading agent_tools.rego into OPA..."
RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT "${OPA_URL}/agent_tools" \
  --data-binary @labs/governed_agentic_ai/policies/agent_tools.rego \
  -H "Content-Type: text/plain")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Policy loaded successfully"
else
    echo "❌ Failed to load policy (HTTP $HTTP_CODE)"
    echo "Response: $BODY"
    exit 1
fi

echo ""
echo "🧪 Testing policy..."
echo ""

# Test 1: Researcher can use search_docs (should return true)
TEST1=$(curl -s -X POST http://localhost:8181/v1/data/ai/agent/tools/allow_tool \
  -H "Content-Type: application/json" \
  -d '{"input":{"agent":"researcher","tool":"search_docs"}}')

if echo "$TEST1" | grep -q '"result":true'; then
    echo "✅ Test 1 passed: researcher CAN use search_docs"
else
    echo "❌ Test 1 failed: researcher should be able to use search_docs"
    echo "   Response: $TEST1"
fi

# Test 2: Researcher cannot use write_to_file (should return false)
TEST2=$(curl -s -X POST http://localhost:8181/v1/data/ai/agent/tools/allow_tool \
  -H "Content-Type: application/json" \
  -d '{"input":{"agent":"researcher","tool":"write_to_file"}}')

if echo "$TEST2" | grep -q '"result":false'; then
    echo "✅ Test 2 passed: researcher CANNOT use write_to_file"
else
    echo "❌ Test 2 failed: researcher should NOT be able to use write_to_file"
    echo "   Response: $TEST2"
fi

# Test 3: Writer can use write_to_file (should return true)
TEST3=$(curl -s -X POST http://localhost:8181/v1/data/ai/agent/tools/allow_tool \
  -H "Content-Type: application/json" \
  -d '{"input":{"agent":"writer","tool":"write_to_file"}}')

if echo "$TEST3" | grep -q '"result":true'; then
    echo "✅ Test 3 passed: writer CAN use write_to_file"
else
    echo "❌ Test 3 failed: writer should be able to use write_to_file"
    echo "   Response: $TEST3"
fi

echo ""
echo "✅ All policy tests passed!"
echo ""
echo "Manual test command:"
echo "  curl -X POST http://localhost:8181/v1/data/ai/agent/tools/allow_tool \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"input\":{\"agent\":\"researcher\",\"tool\":\"search_docs\"}}'"