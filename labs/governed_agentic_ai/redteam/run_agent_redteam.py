"""
Simple red-team runner for Lab 03: Governed Agentic AI:
- Runs happy_path (should succeed)
- Runs unauthorized_tool (researcher tries to call write_to_file; should be blocked)
- Runs exfil_attempt (simulate injected exfil string in summary and ensure logs flag it)
"""
import requests, time, json

URL = "http://localhost:8002/run_agent"

def run(scenario):
    r = requests.post(URL, json={"scenario": scenario, "user_role": "employee"})
    print(f"\n{'='*60}")
    print(f"[{scenario}] Status: {r.status_code}")
    print(f"{'='*60}")
    try:
        print(json.dumps(r.json(), indent=2))
    except:
        print(r.text)

if __name__ == "__main__":
    print("\n🔴 RED TEAM: Testing Agent Security Controls\n")
    
    scenarios = [
        ("happy_path", "✅ Normal operation - should succeed"),
        ("unauthorized_tool", "❌ Unauthorized tool access - should block"),
        ("exfil_attempt", "❌ Exfiltration attempt - should detect")
    ]
    
    for scenario, description in scenarios:
        print(f"\n📋 Test: {description}")
        run(scenario)
        time.sleep(1)
    
    print("\n\n🔍 Check evidence log: evidence/evidence.jsonl")