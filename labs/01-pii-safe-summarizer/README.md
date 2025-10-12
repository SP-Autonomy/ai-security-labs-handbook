# Lab 01: PII-Safe Summarizer 🔐

<div align="center">

**Foundation Security Patterns for LLM Applications**

[![Lab Status](https://img.shields.io/badge/status-complete-success.svg)](.)
[![Difficulty](https://img.shields.io/badge/difficulty-beginner-green.svg)](.)
[![Time](https://img.shields.io/badge/time-2--3%20hours-blue.svg)](.)

[🔒 Security Layers](#security-layers) • [🚀 Setup](#-setup) • [🧪 Test Scenarios](#-test-scenarios) • [📊 Performance](#-performance-analysis) • [⚖️ Cost-Benefit Analysis](#cost-benefit-analysis)

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
- ✅ Attribute-Based Access Control (ABAC)
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

## 🏗️ Architecture

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
    
    style B fill:#f3e5f5
    style C fill:#fff4e6
    style D fill:#e1f5ff
    style F fill:#e8f5e9
    style H fill:#fce4ec
    style G fill:#ffebee
```
### Security Layers

| Layer | Purpose | Latency | Blocks On |
|-------|---------|---------|-----------|
| **1. DLP Pre** | Mask PII in input | <1ms | - |
| **2. Injection Guard** | Detect prompt attacks | <1ms | Suspicious patterns |
| **3. Policy Gate** | Enforce ABAC rules | ~13ms | Role + sensitivity mismatch |
| **4. LLM Call** | Generate response | ~5-20s | - |
| **5. DLP Post** | Mask PII in output | <1ms | - |
| **6. Provenance** | Add audit metadata | <1ms | - |

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
**Step 2: Configure Environment Variables**
```bash
nano .env
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
```bash
ollama serve
make run-opa
make run-api
```

## 🧪 Test Scenarios
### Running Tests
**Run all tests:**
```bash
make test-all
```
**Run individual tests:**
```bash
make test-malicious-contractor           # Test 1
make test-benign-employee                # Test 2
make test-sensitive-employee-denied      # Test 3
make test-sensitive-employee-approved    # Test 4
```

**Test Matrix**
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
<td>✅ SUCCESS</td>
</tr>
<tr>
<td><strong>Test 3</strong><br/>Sensitive Information + Regular Employee</td>
<td>employee</td>
<td>none</td>
<td>✅ Yes</td>
<td>❌ No</td>
<td>❌ BLOCKED<br/><code>policy_denied</code></td>
</tr>
<tr>
<td><strong>Test 4</strong><br/>Sensitive Information + Approved Employee</td>
<td>employee</td>
<td>pii_approved</td>
<td>✅ Yes</td>
<td>❌ No</td>
<td>✅ SUCCESS with PII masked</td>
</tr>
</tbody>
</table>

## 🎯 Expected Results
<details>
<summary><b>❌ Test 1: BLOCKED - Malicious Contractor</b></summary>
  <img width="1029" height="620" alt="Malicious Contractor Prompt" src="https://github.com/user-attachments/assets/5f6bb24d-76cc-4382-88bb-d431c1701db7" />
</details>
<details><summary><b>✅ Test 2: SUCCESS - Benign Employee</b></summary>
  <img width="1360" height="1707" alt="Benign Employee Prompt" src="https://github.com/user-attachments/assets/858f597e-1abb-4a82-95ae-2fdc7e9a61c5" />
</details>
<details><summary><b>❌ Test 3: BLOCKED - Sensitive Information + Regular Employee</b></summary>
  <img width="1119" height="752" alt="Regular Employee Sensitive Content Prompt" src="https://github.com/user-attachments/assets/2b30503d-6048-41ec-aa0e-181ac8fd9fa9" />
</details>
<details><summary><b>✅ Test 4: SUCCESS - Sensitive Information + Approved Employee</b></summary>
  <img width="1360" height="1771" alt="Approved Employee Sensitive Content Prompt" src="https://github.com/user-attachments/assets/5a5ea220-6b08-4c13-a74d-9edc0509fdb8" />
</details>

## 📊 Performance Analysis

### Actual Test Results

Based on real measurements from the running system:

#### Test 2: Complete Request Flow (Success)

| Stage | Latency (ms) | % of Total | Cumulative |
|-------|--------------|------------|------------|
| **dlp_pre** | 0.0 | <0.01% | 0.0ms |
| **injection_guard** | 0.2 | <0.01% | 0.2ms |
| **policy_gate** | 12.4 | 0.08% | 12.6ms |
| **llm_call** | 16,253.8 | 99.91% | 16,266.4ms |
| **dlp_post** | 0.6 | <0.01% | 16,267.0ms |
| **add_provenance** | 0.0 | <0.01% | 16,267.0ms |
| **TOTAL** | **16,267ms** | **100%** | - |

> **💡 Key Finding:** Security overhead is only **13.2ms (0.08%)** of total request time.

### Performance Insights

**Blocked requests never reach the LLM**, saving:
- ⚡ **16+ seconds** of processing time
- 💰 **API costs** (if using cloud LLMs)
- 🔒 **Potential security breaches**

---

## ⚖️ Cost-Benefit Analysis

### Security Benefits

- ✅ **Prevents data leaks** - PII never reaches LLM
- ✅ **Blocks attacks** - Injection attempts stopped in <1ms
- ✅ **Enforces policies** - Authorization in ~13ms
- ✅ **Audit compliance** - Every request tracked

### Performance Cost

| Without Security | With Security | Overhead |
|-----------------|---------------|----------|
| 16,254ms | 16,267ms | **+13ms (0.08%)** |

**ROI:** Comprehensive security for **0.08% performance cost** is exceptional.

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

## 🚀 Next Steps

### Completed Lab 01? 🎉

**You've mastered:**
- ✅ Core security patterns for LLM applications
- ✅ Provider-agnostic architecture
- ✅ Policy-based access control
- ✅ Observability and audit trails

### Continue Learning:

1. **[📖 Lab 02: Secure RAG Copilot](../02-secure-rag-copilot/)** - Learn RAG-specific security
2. **[📖 Lab 03: Agentic AI Governance and Observability](../03-governed-ai-agent/)** - Master agentic AI security
---
