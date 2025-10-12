<div align="center">

# 🛡️ AI Security Labs Handbook

**Production-Grade AI Security Patterns for LLM Applications**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![OPA](https://img.shields.io/badge/OPA-Policy-7B68EE.svg)](https://www.openpolicyagent.org/)

**[🧪 Labs](#-laboratory-series) • [🚀 Quick Start](#-quick-start) • [📚 Learn](#-what-youll-learn) • [🤝 Contributing](#-contributing)**

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

📖 **[Read Provider Integration Guide →](docs/PROVIDERS.md)**

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
- ABAC Policies
- Performance Monitoring

[**📖 Enter Lab 01 →**](labs/01-pii-safe-summarizer/)

**Time:** 2-3 hours  
**Difficulty:** 🟢 Beginner

</td>
<td width="33%" align="center">

### 🔍 Lab 02
**Secure RAG Copilot**

🚧 **COMING SOON**

RAG-specific security patterns

**Features:**
- Context Injection Prevention
- Retrieval Authorization
- Citation Verification
- Embedding Security

[**🔮 Preview Lab 02 →**](labs/02-secure-rag-copilot/)

**Time:** 3-4 hours  
**Difficulty:** 🟡 Intermediate

</td>
<td width="33%" align="center">

### 🤖 Lab 03
**Governed AI Agents**

🚧 **COMING SOON**

Autonomous system governance

**Features:**
- Tool Authorization
- Action Approval Workflows
- Sandboxing & Limits
- Decision Audit Trails

[**🔮 Preview Lab 03 →**](labs/03-governed-ai-agent/)

**Time:** 4-5 hours  
**Difficulty:** 🔴 Advanced

</td>
</tr>
</table>

### 🗺️ Learning Path
