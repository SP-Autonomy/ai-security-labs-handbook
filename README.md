# AI Security Labs Handbook 🛡️

A comprehensive hands-on laboratory series demonstrating production-grade AI security patterns across different AI architectures: simple LLMs, RAG systems, and agentic AI.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Labs](https://img.shields.io/badge/labs-3-green.svg)

## 🎯 Overview

This handbook provides **practical, runnable examples** of AI security implementations that work across different deployment models - whether you're using local models (Ollama), cloud APIs (OpenAI, Anthropic), or proprietary in-house models.

### 🔑 Key Concepts

**Defense-in-Depth Architecture**: Multiple independent security layers that work regardless of your LLM provider.

┌──────────────────────────────────────────────────────┐
│              Your Application Layer                   │
└───────────────────┬──────────────────────────────────┘
│
┌───────────────────▼──────────────────────────────────┐
│           Security Gateway (Provider-Agnostic)        │
├──────────────────────────────────────────────────────┤
│  Pre-Processing:                                      │
│  • DLP (PII Detection/Masking)                       │
│  • Prompt Injection Detection                        │
│  • Policy Enforcement (OPA)                          │
│  • Input Validation                                  │
├──────────────────────────────────────────────────────┤
│  LLM Provider Abstraction                            │
│  ├─ Ollama (Local)                                   │
│  ├─ OpenAI API                                       │
│  ├─ Anthropic API                                    │
│  ├─ Azure OpenAI                                     │
│  └─ Custom In-House Models                           │
├──────────────────────────────────────────────────────┤
│  Post-Processing:                                    │
│  • Output Sanitization                               │
│  • DLP (Response Filtering)                          │
│  • Provenance Tracking                               │
└──────────────────────────────────────────────────────┘

**The key insight**: Security processors operate on requests/responses as data structures - they don't care where the LLM lives or how it's called. Only the thin provider layer changes.

## 🧪 Laboratory Series

### Lab 01: PII-Safe Summarizer ✅ Complete
**Focus**: Simple LLM + Security Fundamentals

A document summarization service with comprehensive security controls.

**Security Features**:
- Data Loss Prevention (PII masking)
- Prompt injection detection
- Role-based and Attribute-based access control (RBAC/ABAC)
- Performance monitoring

**[👉 Go to Lab 01](labs/01-pii-safe-summarizer/README.md)**

**Learn**: Foundation security patterns that apply to all AI systems

---

### Lab 02: Secure RAG Copilot 🚧 Coming Soon
**Focus**: Retrieval-Augmented Generation + Context Security
**Learn**: RAG-specific threats and how to mitigate them

---

### Lab 03: Observability and Governance in Agentic AI 🚧 Coming Soon
**Focus**: Agentic AI + Observability, Governance and Context
**Learn**: Controlling autonomous AI systems safely without slowing adoption

---

## 🏗️ Architecture Philosophy

### Provider-Agnostic Security
The security architecture is **completely decoupled** from your provider choice, regardless whether the deployment model is on-prem, cloud hosted, cloud API, or hybrid.

## 🚀 Quick Start
### Prerequisites
* Python 3.11+
* One of:
- Ollama (for local models)
- OpenAI API key (for cloud models)
- Any other LLM provider

## Installation
**Clone the repository**
git clone https://github.com/yourusername/ai-security-labs-handbook.git
cd ai-security-labs-handbook

**Create virtual environment**
python3.11 -m venv .venv
source .venv/bin/activate

**Install dependencies**
pip install -r requirements.txt

**Start with Lab 01**
cd labs/01-pii-safe-summarizer#

## 🧪 Test Scenarios
**Test 1: Malicious Content (Contractor)**
Expected: ❌ BLOCKED by injection detection and policy
**Test 2: Benign Content (Employee)**
Expected: ✅ SUCCESS - generates summary
**Test 3: Sensitive Data (Regular Employee)**
Expected: ❌ BLOCKED by policy (no PII clearance)
**Test 4: Sensitive Data (PII-Approved Employee)**
Expected: ✅ SUCCESS - PII masked in both request and response

## 📊 Test Results
<details>
<summary><b>Click to see detailed test outputs</b></summary>
❌ Blocked Request: Malicious Content (Contractor)
{
    "blocked": true,
    "reason": "prompt_injection_suspected",
    "meta": {
        "stages": [
            {
                "name": "dlp_pre",
                "latency_ms": 0.0
            },
            {
                "name": "injection_guard",
                "latency_ms": 0.1
            }
        ],
    }
}

✅ Successful Request: Benign content + employee
json {
    "prompt": "Please create 5 bullets and 3 action items without exposing any private data.",
    "user": {
        "role": "employee"
    },
    "contains_sensitive": false,
    "answer": "XYZ
 "provenance": {
        "policy": "OPA v1",
        "dlp": "basic_masks_v1"
    },
    "meta": {
        "stages": [
            {
                "name": "dlp_pre",
                "latency_ms": 0.0
            },
            {
                "name": "injection_guard",
                "latency_ms": 0.2
            },
            {
                "name": "policy_gate",
                "latency_ms": 12.4
            },
            {
                "name": "llm_call",
                "latency_ms": 16253.8
            },
            {
                "name": "dlp_post",
                "latency_ms": 0.6
            },
            {
                "name": "add_provenance",
                "latency_ms": 0.0
            }
        ],
    }
}

❌ Blocked Request: Sensitive Content + Regular Employee
json{
  "blocked": true,
  "reason": "policy_denied",
  "meta": {
    "stages": [
      {"name": "dlp_pre", "latency_ms": 0.0},
      {"name": "injection_guard", "latency_ms": 0.1},
      {"name": "policy_gate", "latency_ms": 12.6}
    ]
  }
}

✅Successful Request: Sensitive Data (PII-Approved Employee)
json {
    "prompt": "Customer John Smith (SSN: ***-**-****) requested a refund.\nHis card ending in ****-****-****-**** was charged twice.\nContact: <email>\nPlease summarize this case for our records.",
    "user": {
        "role": "employee",
        "clearance": "pii_approved"
    },
    "contains_sensitive": true,
    "answer": "Here is a summary of the case in 5 bullets and 3 action items:\n\n\u2022 Customer John Smith (SSN: ***-**-****) requested a refund due to his card being charged twice.\n\u2022 The transaction was made through a credit/debit card with an ending in ****-****-****-****, which is not the usual format for most cards.\n\u2022 Our team will investigate this request and contact the customer via email.\n\u2022 Action items:\n\n1. Investigate the charge using our internal systems to verify the card details and confirm the transaction.\n2. Reach out to the customer via email as requested and advise them on next steps in resolving the issue.\n3. If necessary, escalate the case to a supervisor for further assistance or provide an update with additional information.",
    "provenance": {
        "policy": "OPA v1",
        "dlp": "basic_masks_v1"
    },
    "meta": {
        "stages": [
            {
                "name": "dlp_pre",
                "latency_ms": 0.0
            },
            {
                "name": "injection_guard",
                "latency_ms": 0.1
            },
            {
                "name": "policy_gate",
                "latency_ms": 13.6
            },
            {
                "name": "llm_call",
                "latency_ms": 7096.4
            },
            {
                "name": "dlp_post",
                "latency_ms": 0.1
            },
            {
                "name": "add_provenance",
                "latency_ms": 0.0
            }
        ],
    }
}
</details>

See individual lab READMEs for specific setup instructions.#

## 🎓 What You'll Learn
**Security Fundamentals (Lab01)**

* Defense-in-depth architecture: Multiple independent security layers
* Input validation & sanitization, output filtering: Handling sensitive vs non-sensitive data
* Output filtering:
* Policy-based access control: Declarative access control with OPA/Rego
* Audit trails & observability: Performance monitoring and audit trails

## 📚 Further Reading

* OWASP Top 10 for LLMs
* NIST AI Risk Management Framework
* Anthropic's Claude Safety Best Practices

## 🙏 Acknowledgments
Built to demonstrate enterprise-grade AI security patterns for educational purposes.