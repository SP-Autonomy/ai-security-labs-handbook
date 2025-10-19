<div align="center">

# 🛡️ AI Security Labs Handbook

**Production-Grade AI Security Patterns for LLM Applications**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![OPA](https://img.shields.io/badge/OPA-Policy-7B68EE.svg)](https://www.openpolicyagent.org/)

**[🧪 Labs](#-laboratory-series) • [🚀 Quick Start](#-quick-start) • [📚 Learn](#-learning-path)**

---

### 🎯 **Hands-on laboratories demonstrating AI security across different architectures**

**Simple LLMs • RAG Systems • Agentic AI**

</div>

---

## 📖 Overview

This handbook provides **practical, runnable examples** of AI security implementations that work across different deployment models - whether you're using **local open-source models** (Ollama), **cloud APIs** (OpenAI, Anthropic), or **proprietary in-house models**.

### Why This Handbook?

- ✅ **Learn by doing** - Real, working code you can run locally
- ✅ **Provider-agnostic** - Security patterns work with any LLM
- ✅ **Enterprise-ready** - Patterns used in production systems
- ✅ **Comprehensive** - Covers LLMs, RAG, and Agentic AI
- ✅ **Open source** - MIT licensed, free to use and modify

---

## 🔑 Core Concept: Provider-Agnostic Security

Security layers operate **independently of your LLM provider**, making your security investment portable and future-proof.

### Architecture Overview

<table>
<tr>
<td colspan="2" align="center"><strong>🎯 Your Application Layer</strong></td>
</tr>
<tr>
<td colspan="2" align="center">⬇️</td>
</tr>
<tr>
<td colspan="2" align="center" bgcolor="#fff4e6"><strong>🛡️ Security Gateway (Provider-Agnostic)</strong></td>
</tr>
<tr>
<td width="50%" valign="top">
<strong>📥 Pre-Processing</strong>
<ul>
<li>✓ PII Detection & Masking</li>
<li>✓ Prompt Injection Detection</li>
<li>✓ Policy Enforcement (OPA)</li>
<li>✓ Input Validation</li>
</ul>
</td>
<td width="50%" valign="top">
<strong>📤 Post-Processing</strong>
<ul>
<li>✓ Output Sanitization</li>
<li>✓ Response DLP</li>
<li>✓ Provenance Tracking</li>
</ul>
</td>
</tr>
<tr>
<td colspan="2" align="center">⬇️</td>
</tr>
<tr>
<td colspan="2" align="center" bgcolor="#e8f5e9">
<strong>🔌 LLM Provider (Interchangeable)</strong><br/>
Ollama (Local) • OpenAI/Anthropic (Cloud) • Azure OpenAI (Enterprise) • Custom In-House
</td>
</tr>
</table>

> **💡 Key Insight**: Security processors work with data structures, not API calls. Write security logic once, use everywhere.

### Multi-Provider Support

| Deployment Model | Example | Code Change Required | Security Processors |
|-----------------|---------|---------------------|-------------------|
| **🏠 Local/On-Prem** | Ollama, vLLM, TGI | Update `providers.py` (30 lines) | ✅ No change |
| **☁️ Cloud API** | OpenAI, Anthropic, Cohere | Update `providers.py` (30 lines) | ✅ No change |
| **🏢 Enterprise** | Azure OpenAI, AWS Bedrock | Update `providers.py` (30 lines) | ✅ No change |
| **🔧 In-House** | Custom fine-tuned models | Update `providers.py` (30 lines) | ✅ No change |

---

## 🧪 Laboratory Series

<table>
<tr>
<td width="33%" align="center">

### 🔐 Lab 01
**PII-Safe Summarizer**

✅ **COMPLETE**

Foundation security patterns for LLM applications

**Features:**
- PII Detection & Masking
- Prompt Injection Guards
- RBAC/ABAC Policies
- Performance Monitoring

[**📖 Enter Lab 01 →**](labs/pii-safe-summarizer/)

**Time:** 2-3 hours  
**Difficulty:** 🟢 Beginner

</td>
<td width="33%" align="center">

### 🔍 Lab 02
**Secure RAG Copilot**

✅ **COMPLETE**

RAG-specific security patterns

**Features:**
- Indirect Prompt Injection Defense
- Content Validation (Pre-Ingestion) and Sanitization
- Embedding Security
- DLP + Policy Gate + Provenance

[**🔮 Preview Lab 02 →**](labs/rag_copilot/)

**Time:** 3-4 hours  
**Difficulty:** 🟡 Intermediate

</td>
<td width="33%" align="center">

### 🤖 Lab 03
**Governed Agentic AI**

🚧 **COMING SOON**

Autonomous system governance

**Features:**
- Tool Authorization
- Action Approval Workflows
- Sandboxing & Limits
- Decision Audit Trails

[**🔮 Preview Lab 03 →**](labs/governed-agentic-ai/)

**Time:** 4-5 hours  
**Difficulty:** 🔴 Advanced

</td>
</tr>
</table>

### 🗺️ Learning Path

| Step | Action |
|------|--------|
| 1️⃣ | 📚 Start Here → Lab 01 (Fundamentals) |
| 2️⃣ | ↓ Lab 02 (RAG Security) |
| 3️⃣ | ↓ Lab 03 (Agentic AI) |

> **💡 Recommended**: Complete labs in order. Each builds on concepts from the previous.

### Lab-Specific Learning

| Lab | You'll Master |
|-----|--------------|
| **Lab 01** | PII masking, injection detection, ABAC policies, performance monitoring |
| **Lab 02** | Context security, retrieval auth, citation tracking, embedding safety |
| **Lab 03** | Tool authorization, sandboxing, decision auditing, governance frameworks |

---
## 🚀 Quick Start

### Prerequisites

- ✅ **Python 3.11+**
- ✅ **LLM Provider** (choose one):
  - 🦙 [Ollama](https://ollama.com/download) - Recommended for local development
  - 🤖 OpenAI API key - For cloud deployment  
  - ⚡ Any other LLM provider
- ✅ **[OPA](https://www.openpolicyagent.org/docs/latest/#running-opa)** - Open Policy Agent

### Installation
```bash
# 1. Clone repository
git clone https://github.com/SP-authonomy/ai-security-labs-handbook.git
cd ai-security-labs-handbook

# 2. Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables. E.g.
MODEL_PROVIDER=ollama
GEN_MODEL=llama3.2:1b
OLLAMA_HOST=http://localhost:11434
OPA_URL=http://localhost:8181/v1/data/ai/policy/allow
```
