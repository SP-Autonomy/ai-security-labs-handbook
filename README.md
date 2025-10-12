<div align="center"># AI Security Labs Handbook 🛡️

A comprehensive hands-on laboratory series demonstrating production-grade AI security patterns across different AI architectures: simple LLMs, RAG systems, and agentic AI.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Labs](https://img.shields.io/badge/labs-3-green.svg)
</div>
## 🎯 Overview

This handbook provides **practical, runnable examples** of AI security implementations that work across different deployment models - whether you're using local open-source models (with Ollama), cloud APIs (OpenAI, Anthropic), or proprietary in-house models.

### 🔑 Core Concept: Provider-Agnostic Security
Security layers operate independently of your LLM provider, making your security investment portable and future-proof.

**Defense-in-Depth Architecture**: Multiple independent security layers that work regardless of your LLM provider.

```mermaid
flowchart TB
    subgraph app["🎯 Your Application Layer"]
    A[FastAPI Endpoint]
    end
    
    subgraph gateway["🛡️ Security Gateway - Provider Agnostic"]
        subgraph pre["📥 Pre-Processing"]
        B1[PII Detection & Masking]
        B2[Prompt Injection Detection]
        B3[Policy Enforcement OPA]
        B4[Input Validation]
        end
        
        subgraph llm["🔌 LLM Provider - Interchangeable"]
        C1[Ollama Local]
        C2[OpenAI / Anthropic]
        C3[Azure OpenAI]
        C4[Custom In-House]
        end
        
        subgraph post["📤 Post-Processing"]
        D1[Output Sanitization]
        D2[Response DLP]
        D3[Provenance Tracking]
        end
    end
    
    A --> B1 --> B2 --> B3 --> B4
    B4 --> C1 & C2 & C3 & C4
    C1 & C2 & C3 & C4 --> D1 --> D2 --> D3
    
    style app fill:#e1f5ff
    style gateway fill:#fff4e6
    style pre fill:#f3e5f5
    style llm fill:#e8f5e9
    style post fill:#fce4ec

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
<img width="1029" height="620" alt="Malicious Contractor Prompt" src="https://github.com/user-attachments/assets/b427b043-cb01-4805-8da3-ac62e6f30a93" />

✅ Successful Request: Benign content + employee
<img width="1360" height="1707" alt="Benign Employee Prompt" src="https://github.com/user-attachments/assets/cc363204-0218-422b-b451-8fcdcad0a2fd" />

❌ Blocked Request: Sensitive Content + Regular Employee
<img width="1119" height="752" alt="Regular Employee Sensitive Content Prompt" src="https://github.com/user-attachments/assets/f2bc56e1-0dc6-4f88-95ce-5afc425f5c5f" />

✅Successful Request: Sensitive Data (PII-Approved Employee)
<img width="1360" height="1771" alt="Approved Employee Sensitive Content Prompt" src="https://github.com/user-attachments/assets/234545cc-c279-4d4c-93d3-03be74069b1e" />

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
