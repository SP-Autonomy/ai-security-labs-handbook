<div align="center">
    # AI Security Labs Handbook 🛡️

A comprehensive hands-on laboratory series demonstrating production-grade AI security patterns across different AI architectures: simple LLMs, RAG systems, and agentic AI.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Labs](https://img.shields.io/badge/labs-3-green.svg)
</div>

## 🎯 Overview

This handbook provides **practical, runnable examples** of AI security implementations that work across different deployment models - whether you're using local open-source models (with Ollama), cloud APIs (OpenAI, Anthropic), or proprietary in-house models.

### 🔑 Core Concept: Provider-Agnostic Security
**Defense-in-Depth Architecture**: Multiple independent security layers that work regardless of your LLM provider.

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
See individual lab READMEs for specific setup instructions.#

## 🎓 What You'll Learn
**Security Fundamentals (Lab01)**

* Defense-in-depth architecture: Multiple independent security layers
* Input validation & sanitization, output filtering: Handling sensitive vs non-sensitive data
* Policy-based access control: Declarative access control with OPA/Rego
* Audit trails & observability: Performance monitoring and audit trails

## 📚 Further Reading
* OWASP Top 10 for LLMs
* NIST AI Risk Management Framework
* Anthropic's Claude Safety Best Practices

## 🙏 Acknowledgments
Built to demonstrate enterprise-grade AI security patterns for educational purposes.
