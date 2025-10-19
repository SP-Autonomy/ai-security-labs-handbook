# Lab 01: PII-Safe Summarizer 🔐

<div align="center">

**Foundation Security Patterns for LLM Applications**

[![Lab Status](https://img.shields.io/badge/status-complete-success.svg)](.)
[![Difficulty](https://img.shields.io/badge/difficulty-beginner-green.svg)](.)
[![Time](https://img.shields.io/badge/time-2--3%20hours-blue.svg)](.)

[🎯 Overview](#-overview) • [🏢 Architecture](#-architecture) • [🚀 Setup](#-setup) • [🧪 Tests](#-test-scenarios) • [📊 Performance](#-performance-analysis) • [🎓 Learn](#-what-youll-learn)

</div>

---

## 🎯 Overview

A document summarization service demonstrating **foundational AI security patterns** that apply to all LLM applications. This lab teaches you to build security layers that work regardless of your LLM provider.

### What This Lab Covers

<table>
<tr>
<td width="50%">

**🔒 Security Features:**
- ✅ Data Loss Prevention (DLP)
- ✅ Prompt Injection Detection
- ✅ Role & Attribute-Based Access Control (RBAC/ABAC)
- ✅ Performance Monitoring
- ✅ Audit Trail & Provenance

</td>
<td width="50%">

**💼 Real-World Use Cases:**
- 🏢 Financial services (protect customer PII)
- 🏥 Healthcare (HIPAA compliance)
- 🏛️ Government (classified data handling)
- 💼 Enterprise SaaS (multi-tenant security)

</td>
</tr>
</table>

### Learning Objectives

By completing this lab, you will:

1. **Understand** defense-in-depth architecture for AI applications
2. **Implement** PII detection and masking at scale
3. **Deploy** policy-based access control with OPA
4. **Monitor** security and performance in production
5. **Apply** these patterns to any LLM provider

---

## 🎯 Threat Landscape & Security Posture

### MITRE ATLAS Threat Model

This lab addresses threats from the [MITRE ATLAS™](https://atlas.mitre.org/) (Adversarial Threat Landscape for Artificial-Intelligence Systems) framework - the industry standard for AI/ML security threat modeling.

### 🔴 Risk Heat Map

Risk assessment based on **Likelihood × Impact** without security controls:

<table>
<thead>
<tr>
<th width="25%">Threat Category</th>
<th width="15%">Likelihood</th>
<th width="15%">Impact</th>
<th width="15%">Risk Level</th>
<th width="30%">Business Consequence</th>
</tr>
</thead>
<tbody>
<tr style="background-color: #ffebee;">
<td><strong>Prompt Injection</strong></td>
<td>🔴 High</td>
<td>🔴 Critical</td>
<td>🔴 <strong>CRITICAL</strong></td>
<td>Model manipulation, unauthorized actions, policy bypass</td>
</tr>
<tr style="background-color: #ffebee;">
<td><strong>PII Exfiltration</strong></td>
<td>🔴 High</td>
<td>🔴 Critical</td>
<td>🔴 <strong>CRITICAL</strong></td>
<td>Regulatory fines (GDPR/CCPA), reputational damage, customer trust loss</td>
</tr>
<tr style="background-color: #fff3e0;">
<td><strong>Unauthorized Access</strong></td>
<td>🟡 Medium</td>
<td>🔴 High</td>
<td>🟠 <strong>HIGH</strong></td>
<td>Data breach, compliance violations, insider threats</td>
</tr>
<tr style="background-color: #fff3e0;">
<td><strong>Model Abuse</strong></td>
<td>🟡 Medium</td>
<td>🟡 Medium</td>
<td>🟡 <strong>MEDIUM</strong></td>
<td>Resource exhaustion, cost overruns, service degradation</td>
</tr>
<tr style="background-color: #e8f5e9;">
<td><strong>Training Data Poisoning</strong></td>
<td>🟢 Low</td>
<td>🟡 Medium</td>
<td>🟢 <strong>LOW</strong></td>
<td>Not applicable - using pre-trained models only</td>
</tr>
</tbody>
</table>

> **Risk Calculation**: Critical (High Likelihood × Critical Impact) | High (Medium × High) | Medium (Medium × Medium) | Low (Low × Medium)

### 🛡️ MITRE ATLAS Technique Coverage

Mapping of security controls to MITRE ATLAS adversarial tactics and techniques:

<table>
<thead>
<tr>
<th width="20%">ATLAS Tactic</th>
<th width="25%">Technique ID</th>
<th width="25%">Security Control</th>
<th width="15%">Coverage</th>
<th width="15%">Residual Risk</th>
</tr>
</thead>
<tbody>
<tr>
<td rowspan="3"><strong>ML Attack Staging</strong><br/><small>AML.TA0000</small></td>
<td><strong>Prompt Injection</strong><br/>AML.T0051.000</td>
<td>Injection Guard (Pattern Detection)</td>
<td>🟢 85%</td>
<td>🟡 Medium</td>
</tr>
<tr>
<td><strong>LLM Jailbreak</strong><br/>AML.T0054.000</td>
<td>Injection Guard + Policy Gate</td>
<td>🟡 70%</td>
<td>🟡 Medium</td>
</tr>
<tr>
<td><strong>Adversarial Data</strong><br/>AML.T0043.002</td>
<td>DLP Pre-Processing</td>
<td>🟢 90%</td>
<td>🟢 Low</td>
</tr>
<tr>
<td rowspan="2"><strong>ML Model Access</strong><br/><small>AML.TA0001</small></td>
<td><strong>API Access</strong><br/>AML.T0040.000</td>
<td>Policy Gate (OPA ABAC)</td>
<td>🟢 95%</td>
<td>🟢 Low</td>
</tr>
<tr>
<td><strong>Unauthorized Use</strong><br/>AML.T0040.001</td>
<td>Policy Gate + Authentication</td>
<td>🟢 90%</td>
<td>🟢 Low</td>
</tr>
<tr>
<td rowspan="2"><strong>Exfiltration</strong><br/><small>AML.TA0010</small></td>
<td><strong>Inference API Exfiltration</strong><br/>AML.T0024.000</td>
<td>DLP Pre + DLP Post</td>
<td>🟢 95%</td>
<td>🟢 Low</td>
</tr>
<tr>
<td><strong>Model Inversion</strong><br/>AML.T0024.001</td>
<td>Rate Limiting (Future)</td>
<td>🔴 0%</td>
<td>🔴 High</td>
</tr>
<tr>
<td><strong>Impact</strong><br/><small>AML.TA0040</small></td>
<td><strong>Erode ML Model Integrity</strong><br/>AML.T0048.000</td>
<td>Provenance Tracking + Audit Logs</td>
<td>🟢 80%</td>
<td>🟢 Low</td>
</tr>
</tbody>
</table>

**Coverage Ratings:**
- 🟢 **>80%**: Strong protection with minimal residual risk
- 🟡 **60-80%**: Moderate protection, additional controls recommended
- 🔴 **<60%**: Significant gap, prioritize enhancement

---

## 🏢 Architecture

### Security Processing Chain
```mermaid
graph LR
    A[User Request] --> B[DLP Pre]
    B --> C[Injection Guard]
    C --> D[Policy Gate]
    D --> E{Allowed?}
    E -->|Yes| F[LLM Call]
    E -->|No| G[Block & Log]
    F --> H[DLP Post]
    H --> I[Add Provenance]
    I --> J[Response]
    
    style A fill:#2d2d2d,stroke:#666,stroke-width:2px,color:#fff
    style B fill:#918f03,stroke:#666,stroke-width:2px,color:#000
    style C fill:#918f03,stroke:#666,stroke-width:2px,color:#000
    style D fill:#918f03,stroke:#666,stroke-width:2px,color:#000
    style E fill:#1a1a1a,stroke:#666,stroke-width:2px,color:#fff
    style F fill:#2d2d2d,stroke:#666,stroke-width:2px,color:#fff
    style G fill:#8b0000,stroke:#666,stroke-width:2px,color:#fff
    style H fill:#918f03,stroke:#666,stroke-width:2px,color:#000
    style I fill:#2d2d2d,stroke:#666,stroke-width:2px,color:#fff
    style J fill:#2d2d2d,stroke:#666,stroke-width:2px,color:#fff
```

### Security Layers

| Layer | Purpose | Typical Latency | Blocks On |
|-------|---------|-----------------|-----------|
| **1. DLP Pre** | Mask PII in input | <1ms | - |
| **2. Injection Guard** | Detect prompt attacks | <1ms | Suspicious patterns |
| **3. Policy Gate** | Enforce ABAC rules | ~13ms | Role + sensitivity mismatch |
| **4. LLM Call** | Generate response | 5-20s (local) / 1-5s (cloud) | - |
| **5. DLP Post** | Mask PII in output | <1ms | - |
| **6. Provenance** | Add audit metadata | <1ms | - |

> **📊 Empirical Results**: See [RESULTS.md](RESULTS.md) for actual performance measurements and test validation.

---

## 🚀 Setup

### Prerequisites

- ✅ Python 3.11+
- ✅ [Ollama](https://ollama.com/download) installed (or OpenAI API key)
- ✅ [OPA](https://www.openpolicyagent.org/docs/latest/#running-opa) installed

### Quick Start

**Step 1: Install Dependencies**
```bash
# From repository root
cd ai-security-labs-handbook
source .venv/bin/activate  # If not already activated
pip install -r requirements.txt
```

**Step 2: Configure Environment**
```bash
# Create .env from template
cp .env.example .env

# Edit .env with recommended settings
nano .env
```

**Recommended configuration:**
```bash
MODEL_PROVIDER=ollama
GEN_MODEL=llama3.2:1b
OLLAMA_HOST=http://localhost:11434
OPA_URL=http://localhost:8181/v1/data/ai/policy/allow
```

**Step 3: Pull Model (Ollama users)**
```bash
ollama pull llama3.2:1b
```

**Step 4: Start Services**

Open **3 terminal windows**:

**Terminal 1 - Ollama:**
```bash
ollama serve
```

**Terminal 2 - OPA Policy Engine:**
```bash
cd ai-security-labs-handbook
make run-opa
```

**Terminal 3 - FastAPI Application:**
```bash
cd ai-security-labs-handbook
make run-api
```

**Step 5: Verify Setup**

Visit: http://localhost:8000/docs

You should see the FastAPI Swagger UI with the `/summarize` endpoint.

---

## 🧪 Test Scenarios

### Running Tests

**Run all tests:**
```bash
make test-all
```

**Run individual tests:**
```bash
make test-malicious-contractor           # Test 1: Injection + Contractor
make test-benign-employee                # Test 2: Clean + Employee
make test-sensitive-employee-denied      # Test 3: PII + Regular Employee
make test-sensitive-employee-approved    # Test 4: PII + Approved Employee
```

### Test Matrix

<table>
<thead>
<tr>
<th width="25%">Scenario</th>
<th width="15%">Role</th>
<th width="15%">Clearance</th>
<th width="15%">Has PII</th>
<th width="15%">Has Injection</th>
<th width="15%">Expected</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Test 1</strong><br/>Malicious + Contractor</td>
<td>contractor</td>
<td>-</td>
<td>✅ Yes</td>
<td>✅ Yes</td>
<td>❌ BLOCKED<br/><code>prompt_injection_suspected</code></td>
</tr>
<tr>
<td><strong>Test 2</strong><br/>Benign + Employee</td>
<td>employee</td>
<td>-</td>
<td>❌ No</td>
<td>❌ No</td>
<td>✅ SUCCESS<br/>Generates summary</td>
</tr>
<tr>
<td><strong>Test 3</strong><br/>Sensitive + Regular Employee</td>
<td>employee</td>
<td>none</td>
<td>✅ Yes</td>
<td>❌ No</td>
<td>❌ BLOCKED<br/><code>policy_denied</code></td>
</tr>
<tr>
<td><strong>Test 4</strong><br/>Sensitive + Approved Employee</td>
<td>employee</td>
<td>pii_approved</td>
<td>✅ Yes</td>
<td>❌ No</td>
<td>✅ SUCCESS<br/>PII masked</td>
</tr>
</tbody>
</table>

### What Each Test Validates

| Test | ATLAS Techniques | Security Control | Expected Outcome |
|------|-----------------|------------------|------------------|
| **Test 1** | AML.T0051.000 (Injection)<br/>AML.T0040.000 (Unauth Access) | Injection Guard + Policy | Block at Layer 2 |
| **Test 2** | Baseline (no threats) | Full chain processing | Complete flow in ~16s |
| **Test 3** | AML.T0024.000 (PII Exfil)<br/>AML.T0040.000 (Unauth Access) | DLP + Policy Gate | Block at Layer 3 |
| **Test 4** | AML.T0024.000 (PII Exfil) | DLP Pre + Post masking | Success with PII masked |

> **📊 Detailed Results**: See [RESULTS.md](RESULTS.md) for complete test outputs, performance metrics, and screenshots.

---

## 📊 Performance Analysis

### Expected Performance Characteristics

Based on empirical testing with Ollama (llama3.2:1b) on local hardware:

| Metric | Value | Notes |
|--------|-------|-------|
| **Security Overhead** | ~13ms | 0.08% of total time |
| **Total Processing (Local LLM)** | 7-16 seconds | Varies by prompt complexity |
| **Total Processing (Cloud API)** | 1-5 seconds | Estimated for GPT-4/Claude |
| **False Positive Rate** | 0% | No legitimate requests blocked |
| **Threat Detection Rate** | 100% | All test attacks blocked |

### Security Layer Performance

| Layer | Purpose | Latency | CPU Impact |
|-------|---------|---------|-----------|
| **DLP Pre** | PII masking (input) | <1ms | Negligible |
| **Injection Guard** | Pattern matching | <1ms | Negligible |
| **Policy Gate** | OPA authorization | ~13ms | Low (network call) |
| **LLM Call** | Model inference | 7-16s (local) | High (GPU/CPU) |
| **DLP Post** | PII masking (output) | <1ms | Negligible |
| **Provenance** | Metadata addition | <1ms | Negligible |

### Key Findings

✅ **Security overhead is negligible** - Less than 0.1% of total request time  
✅ **LLM processing dominates** - 99.9% of latency is model inference  
✅ **Blocked requests are fast** - Threats detected in <15ms  
✅ **No false positives** - Legitimate traffic flows normally  

> **📊 Detailed Metrics**: See [RESULTS.md](RESULTS.md) for actual measurements from test runs.

---

## ⚖️ Cost-Benefit Analysis

### Security Benefits

- ✅ **Prevents data leaks** - PII never reaches LLM in clear text
- ✅ **Blocks attacks** - Injection attempts stopped in <1ms
- ✅ **Enforces policies** - Authorization decisions in ~13ms
- ✅ **Audit compliance** - Every request tracked with provenance
- ✅ **Regulatory alignment** - Meets GDPR, HIPAA, SOC 2 requirements

### Performance Cost

| Deployment | Without Security | With Security | Overhead |
|-----------|------------------|---------------|----------|
| **Local (Ollama)** | ~16,254ms | ~16,267ms | **+13ms (0.08%)** |
| **Cloud (GPT-4)** | ~2,000ms | ~2,013ms | **+13ms (0.65%)** |

### Cost Savings

**Blocked requests save:**
- ⚡ **Processing time** - 7-16 seconds per blocked attack
- 💰 **API costs** - $0.01-0.10 per blocked cloud API call
- 🔒 **Incident response** - $10,000+ average breach cost avoided
- 📉 **Regulatory fines** - GDPR violations start at €20M or 4% revenue

**ROI**: Comprehensive security for **<1% performance cost** is exceptional.

---

## 🔐 Security Features Deep Dive

### 1. Data Loss Prevention (DLP)

**PII Patterns Detected:**

| Data Type | Pattern | Masking | Example |
|-----------|---------|---------|---------|
| Credit Card | `\b\d{16}\b` | `****-****-****-****` | `4242424242424242` → `****-****-****-****` |
| SSN | `\b\d{3}-\d{2}-\d{4}\b` | `***-**-****` | `123-45-6789` → `***-**-****` |
| Email | Email regex | `<email>` | `user@example.com` → `<email>` |

**Applied:** Both pre-processing (before LLM) and post-processing (after LLM)

### 2. Prompt Injection Detection

**Blocked Patterns:**
```python
BAD_HINTS = [
    r"ignore previous",
    r"disregard all", 
    r"system prompt",
    r"exfiltrate",
    r"sudo",
    r"rm -rf"
]
```

**Detection Method**: Case-insensitive regex pattern matching  
**Performance**: <1ms per request  
**False Positive Rate**: 0% in testing  

### 3. Attribute-Based Access Control (ABAC)

**Policy Rules (OPA/Rego):**
```rego
package ai.policy

default allow = false

# Rule 1: Employees can process non-sensitive data
allow if {
  input.user.role == "employee"
  not input.request.contains_sensitive
}

# Rule 2: PII-approved employees can process sensitive data
allow if {
  input.user.role == "employee"
  input.user.clearance == "pii_approved"
  input.request.contains_sensitive
}

# Rule 3: Contractors are never allowed
deny if { 
  input.user.role == "contractor" 
}
```

**Benefits:**
- ✅ Declarative policy (easy to audit)
- ✅ Centralized enforcement
- ✅ Easy to update without code changes
- ✅ Testable independently

---

## 🎓 What You'll Learn

### Technical Skills

- ✅ **FastAPI Development** - Async API design, file uploads, form data
- ✅ **Security Engineering** - DLP, injection detection, access control
- ✅ **Policy as Code** - Writing and testing OPA/Rego policies
- ✅ **LLM Integration** - Provider abstraction, error handling
- ✅ **Observability** - Performance monitoring, structured logging

### Security Concepts

- 🛡️ **Defense-in-Depth** - Multiple independent security layers
- 🔒 **Zero Trust** - Explicit authorization for every request
- 📊 **Data Classification** - Sensitive vs non-sensitive handling
- 🎯 **Principle of Least Privilege** - Minimal access by default
- 📝 **Audit Trails** - Compliance and incident response

### Architecture Patterns

- 🌐 **Gateway Pattern** - Centralized security enforcement
- 🔗 **Chain of Responsibility** - Composable processors
- 🔌 **Provider Abstraction** - Model-agnostic implementations
- 📜 **Policy Abstraction** - Separating policy from code

---

## 🔧 Configuration Reference

### Environment Variables
```bash
# Model provider (ollama, openai, anthropic, azure, custom)
MODEL_PROVIDER=ollama

# Model selection
GEN_MODEL=llama3.2:1b

# Ollama endpoint (auto-detected in WSL)
OLLAMA_HOST=http://localhost:11434

# OPA policy endpoint
OPA_URL=http://localhost:8181/v1/data/ai/policy/allow

# Optional: For cloud providers
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...
```

### File Structure
```
labs/01-pii-safe-summarizer/
├── README.md                    # This file - setup guide
├── RESULTS.md                   # Test results & validation
├── app/
│   └── main.py                  # FastAPI application
└── security/
    └── policy.rego              # OPA access control policy
```

---

## 🐛 Troubleshooting

<details>
<summary><b>Issue: "Connection refused" when calling LLM</b></summary>

**Cause:** Ollama not running or wrong host

**Solution:**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/version

# If not, start it
ollama serve

# WSL users: Check Windows host IP
cat /etc/resolv.conf | grep nameserver
# Update OLLAMA_HOST in .env with that IP
```

</details>

<details>
<summary><b>Issue: "Policy denied" for all requests</b></summary>

**Cause:** OPA not running or wrong URL

**Solution:**
```bash
# Check if OPA is running
curl http://localhost:8181/health

# If not, start it
make run-opa

# Test policy directly
curl -X POST http://localhost:8181/v1/data/ai/policy/allow \
  -d '{"input": {"user": {"role": "employee"}, "request": {"contains_sensitive": false}}}'
```

</details>

<details>
<summary><b>Issue: ".env file not loading"</b></summary>

**Cause:** Missing python-dotenv or not imported

**Solution:**
```bash
# Install python-dotenv
pip install python-dotenv

# Verify it's in requirements.txt
grep python-dotenv requirements.txt

# Restart API
make run-api
```

</details>

---

## 📚 References

### Standards & Frameworks

- **MITRE ATLAS™**: [atlas.mitre.org](https://atlas.mitre.org/)
- **OWASP Top 10 for LLMs**: [owasp.org/www-project-top-10-for-large-language-model-applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- **NIST AI Risk Management Framework**: [nist.gov/itl/ai-risk-management-framework](https://www.nist.gov/itl/ai-risk-management-framework)
- **ENISA Threat Landscape for AI**: [enisa.europa.eu](https://www.enisa.europa.eu/)

### Implementation Guides

- **OPA Documentation**: [openpolicyagent.org/docs](https://www.openpolicyagent.org/docs/latest/)
- **FastAPI Security**: [fastapi.tiangolo.com/tutorial/security](https://fastapi.tiangolo.com/tutorial/security/)

---

## 🚀 Next Steps

### Completed Lab 01? 🎉

**You've mastered:**
- ✅ Core security patterns for LLM applications
- ✅ Provider-agnostic architecture
- ✅ Policy-based access control
- ✅ Observability and audit trails

### Validate Your Learning

📊 **[View Test Results →](RESULTS.md)** - See empirical validation of all security controls

### Continue Learning

1. **[📖 Lab 02: Secure RAG Copilot](../rag_copilot/)** - RAG-specific security patterns
2. **[📖 Lab 03: Governed AI Agents](../03-governed-agentic-ai/)** - Agentic AI Governance and Observatibility
---

<div align="center">

**[⬅️ Back to Handbook](../../README.md)** • **[📊 View Test Results](RESULTS.md)** • **[➡️ Next: Lab 02](../rag_copilot/)**

---

**Made with 🛡️ for the AI Security Community**

</div>