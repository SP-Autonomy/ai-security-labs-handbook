<div align="center">

# 🛡️ AI Security Labs Handbook

**Production-Grade Security Patterns for Modern AI Systems**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![OPA](https://img.shields.io/badge/OPA-Policy-7B68EE.svg)](https://www.openpolicyagent.org/)
[![Labs](https://img.shields.io/badge/labs-3%2F3%20complete-success.svg)](.)

**[🧪 Labs](#-laboratory-series) • [🚀 Quick Start](#-quick-start) • [📚 Security Frameworks](#-security-frameworks) • [🎓 Learn](#-what-youll-learn)**

---

### 🎯 **Hands-on security laboratories covering the full AI application spectrum**

**Simple LLMs → RAG Systems → Multi-Agent AI**

**100% Complete** • **Provider-Agnostic** • **Production-Ready**

</div>

---

## 📖 Overview

A comprehensive, **hands-on security handbook** with 3 progressive laboratories demonstrating AI security implementations that work across **any LLM provider** - from local Ollama to OpenAI, Anthropic, Azure OpenAI, or custom in-house models.

### Why This Handbook?

<table>
<tr>
<td width="50%">

**🎯 Practical Learning**
- ✅ Real, working code you can run locally
- ✅ Complete test suites with expected results
- ✅ Evidence-based validation
- ✅ Step-by-step documentation

</td>
<td width="50%">

**🏢 Enterprise-Ready**
- ✅ Patterns from production systems
- ✅ Defense-in-depth architectures
- ✅ Comprehensive audit trails
- ✅ Policy-driven governance

</td>
</tr>
<tr>
<td width="50%">

**🔧 Provider-Agnostic**
- ✅ Works with any LLM (local or cloud)
- ✅ Portable security investment
- ✅ Future-proof implementations
- ✅ No vendor lock-in

</td>
<td width="50%">

**📚 Progressive Curriculum**
- ✅ Beginner to advanced difficulty
- ✅ Builds on previous concepts
- ✅ Covers all AI architectures
- ✅ Industry-standard frameworks

</td>
</tr>
</table>

---

## 🎓 What You'll Learn

### Security Skills Across All Labs

| Skill Area | Lab 01 | Lab 02 | Lab 03 |
|------------|--------|--------|--------|
| **Input Validation** | ✅ Prompt injection detection | ✅ Context injection detection | ✅ Tool parameter validation |
| **Output Sanitization** | ✅ PII masking | ✅ Citation tracking | ✅ Exfiltration detection |
| **Access Control** | ✅ RBAC/ABAC policies | ✅ Document-level filtering | ✅ Per-agent tool allowlists |
| **Audit & Compliance** | ✅ Provenance metadata | ✅ Source attribution | ✅ Immutable evidence logs |
| **Defense-in-Depth** | ✅ 5-layer chain | ✅ 9-layer chain | ✅ Context-aware risk scoring |
| **Threat Detection** | ✅ Pattern matching | ✅ Content validation | ✅ Behavioral anomalies |

### By the End of This Handbook

You'll be able to:

✅ **Secure traditional LLM applications** with PII protection, injection detection, and policy enforcement  
✅ **Defend RAG systems** against indirect injection, content poisoning, and information leakage  
✅ **Govern autonomous agents** with tool authorization, sandboxing, and comprehensive monitoring  
✅ **Implement defense-in-depth** security architectures for any AI system  
✅ **Build provider-agnostic** security that works across all LLM platforms  
✅ **Create audit trails** that meet enterprise compliance requirements

---

## 🔑 Core Concept: Provider-Agnostic Security

Security layers operate **independently of your LLM provider**, making your security investment **portable** and **future-proof**.

### Architecture Pattern
```
┌─────────────────────────────────────────────────────────┐
│                  Your Application                       │
│          (Summarizer / RAG / Agentic AI )               │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│          🛡️ Security Gateway (Provider-Agnostic)        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Pre-Processing              Post-Processing            │
│  ├─ DLP (PII Detection)      ├─ Output Sanitization     │
│  ├─ Injection Detection      ├─ Response DLP            │
│  ├─ Policy Enforcement       ├─ Provenance Tracking     │
│  ├─ Context Validation       └─ Citation Verification   │
│  └─ Tool Authorization                                   │
│                                                          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│      🔌 LLM Provider Interface (30-line adapter)        │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┬────────────┐
        │            │            │            │
        ↓            ↓            ↓            ↓
    ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐
    │ Ollama │  │ OpenAI │  │ Azure  │  │ Custom │
    │ (Local)│  │ (Cloud)│  │  OpenAI│  │In-House│
    └────────┘  └────────┘  └────────┘  └────────┘
```

> **💡 Key Insight**: Security operates on **data structures**, not API calls. Write security logic **once**, use **everywhere**.

### Switching Providers

All security remains **unchanged** when switching LLM providers:
```python
# Only this file changes (30 lines):
# shared/gateway/providers.py

def call_llm(prompt: str) -> str:
    if PROVIDER == "ollama":
        return ollama.generate(...)      # Local
    elif PROVIDER == "openai":
        return openai.chat.completions.create(...)  # Cloud
    elif PROVIDER == "azure":
        return azure_openai.chat.completions.create(...)  # Enterprise
    elif PROVIDER == "custom":
        return your_model.predict(...)   # In-house
```

**Security processors (`dlp.py`, `injection.py`, `policy_opa.py`, etc.):** ✅ **No changes required**

---

## 🧪 Laboratory Series

<table>
<thead>
<tr>
<th width="33%">Lab 01: Foundation</th>
<th width="33%">Lab 02: RAG Security</th>
<th width="33%">Lab 03: Agentic AI</th>
</tr>
</thead>
<tbody>
<tr>
<td valign="top">

### 🔐 PII-Safe Summarizer

**✅ COMPLETE**

Foundational security patterns for LLM applications

**Security Controls:**
- ✅ PII Detection & Masking
- ✅ Prompt Injection Guards
- ✅ RBAC/ABAC Policies (OPA)
- ✅ Provenance Tracking
- ✅ Performance Monitoring

**Threat Coverage:**
- OWASP LLM01 (Injection)
- OWASP LLM06 (Sensitive Info)
- OWASP LLM08 (Excessive Agency)

**What You'll Build:**  
Secure summarization service with 5-layer defense-in-depth

[**📖 Start Lab 01 →**](labs/pii-safe-summarizer/)

⏱️ **2-3 hours**  
🎯 **Beginner**

</td>
<td valign="top">

### 🔍 Secure RAG Copilot

**✅ COMPLETE**

RAG-specific security patterns and retrieval safety

**Security Controls:**
- ✅ Indirect Injection Defense
- ✅ Content Validation (Pre-Ingestion)
- ✅ Context Sanitization
- ✅ Source Attribution
- ✅ Vector Search Security

**Threat Coverage:**
- OWASP LLM01 (Indirect Injection)
- OWASP LLM03 (Corpus Poisoning)
- OWASP LLM06 (Info Disclosure)

**What You'll Build:**  
RAG copilot with 9-layer security chain and test/prod separation

[**📖 Start Lab 02 →**](labs/rag_copilot/)

⏱️ **2-3 hours**  
🎯 **Intermediate**

</td>
<td valign="top">

### 🤖 Governed Agentic AI

**✅ COMPLETE**

Multi-agent governance with MCP-style tool control

**Security Controls:**
- ✅ OPA Tool Authorization
- ✅ Context-Aware Risk Scoring
- ✅ Budget Enforcement
- ✅ Sandbox Path Protection
- ✅ Evidence-Based Auditing

**Threat Coverage:**
- MAESTRO (11/12 categories)
- OWASP LLM01, 06, 08, 10
- Tool misuse, exfiltration, goal misalignment

**What You'll Build:**  
3-agent orchestration system with comprehensive governance

[**📖 Start Lab 03 →**](labs/governed_agentic_ai/)

⏱️ **3-4 hours**  
🎯 **Advanced**

</td>
</tr>
</tbody>
</table>

### 🗺️ Recommended Learning Path
```
Start Here
    ↓
┌────────────────────────────────────────────┐
│  Lab 01: PII-Safe Summarizer (2-3 hours)  │  ← Foundation
│  • Input validation                        │
│  • Output sanitization                     │
│  • Policy enforcement                      │
└────────────────┬───────────────────────────┘
                 ↓
┌────────────────────────────────────────────┐
│  Lab 02: Secure RAG Copilot (2-3 hours)   │  ← RAG-Specific
│  • Retrieval security                      │
│  • Indirect injection defense              │
│  • Content validation                      │
└────────────────┬───────────────────────────┘
                 ↓
┌────────────────────────────────────────────┐
│  Lab 03: Governed Agentic AI (3-4 hours)  │  ← Autonomous Systems
│  • Tool authorization                      │
│  • Behavioral monitoring                   │
│  • Context-aware risk scoring              │
└────────────────────────────────────────────┘
                 ↓
         Production Ready! 🎉
```

**Total Time:** ~8-10 hours for complete mastery

---

## 📊 Security Frameworks

This handbook maps to industry-standard security frameworks:

### OWASP LLM Top 10 Coverage

| Threat | Lab 01 | Lab 02 | Lab 03 | Mitigation |
|--------|--------|--------|--------|------------|
| **LLM01: Prompt Injection** | ✅ | ✅ | ✅ | Pattern detection + context analysis |
| **LLM03: Training/Corpus Poisoning** | - | ✅ | - | Pre-ingestion validation |
| **LLM06: Sensitive Info Disclosure** | ✅ | ✅ | ✅ | DLP + PII masking |
| **LLM08: Excessive Agency** | ✅ | - | ✅ | Policy gates + tool allowlists |
| **LLM10: Model DoS** | ✅ | - | ✅ | Budget enforcement + rate limits |

### MAESTRO Framework (Agentic AI)

Lab 03 provides comprehensive coverage of the **MAESTRO** threat ontology:

| Category | Coverage | Controls |
|----------|----------|----------|
| Tool Misuse | 100% | OPA allowlists + budget enforcement |
| Information Leakage | 100% | Pattern detection + evidence logging |
| Goal Misalignment | 100% | Context-aware risk scoring |
| Environmental Manipulation | 100% | Sandbox + path validation |
| A2A Trust | 100% | Per-agent identity + authorization |
| Schema Violations | 100% | JSON Schema validation |

**Total:** 11/12 MAESTRO categories addressed ✅

---

## 🚀 Quick Start

### Prerequisites

<table>
<tr>
<td width="50%">

**Required:**
- ✅ Python 3.11+
- ✅ Git
- ✅ 8GB RAM minimum

</td>
<td width="50%">

**Choose One LLM Provider:**
- 🦙 [Ollama](https://ollama.com/download) (Recommended - free, local)
- 🤖 OpenAI API key
- ⚡ Anthropic API key
- 🏢 Azure OpenAI credentials

</td>
</tr>
<tr>
<td colspan="2">

**Additional Tools:**
- ✅ [OPA](https://www.openpolicyagent.org/docs/latest/#running-opa) - Open Policy Agent (for policy enforcement)
- ✅ curl or httpie (for testing)
- ✅ jq (optional - for JSON parsing)

</td>
</tr>
</table>

### Installation (5 Minutes)
```bash
# 1. Clone repository
git clone https://github.com/SP-authonomy/ai-security-labs-handbook.git
cd ai-security-labs-handbook

# 2. Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up Ollama (if using local models)
ollama pull llama3.2:1b           # For Labs 1, 2, 3
ollama pull nomic-embed-text      # For Lab 2, 3 (embeddings)

# 5. Configure environment
cp .env.example .env
# Edit .env with your settings (or keep defaults for Ollama)

# 6. Start OPA (separate terminal)
opa run --server --log-level error
```

### Quick Test (Verify Setup)
```bash
# Start OPA policies (terminal 1)
make run-opa

# Test Lab 01 (terminal 2)
make run-api
# In terminal 3:
make test-benign-employee
# Expected: ✅ SUCCESS

# You're ready! 🎉
```

---

## 📚 Documentation Structure

Each lab includes comprehensive documentation:
```
labs/
├── pii-safe-summarizer/
│   ├── README.md              # Setup, architecture, tests
│   ├── RESULTS.md             # Empirical test results
│   ├── app/                   # FastAPI application
│   ├── policies/              # OPA policies
│   └── redteam/               # Attack simulations
│
├── rag_copilot/
│   ├── README.md              # RAG-specific security
│   ├── RESULTS.md             # Validation results
│   ├── app/                   # RAG application
│   ├── data/corpus/           # Trusted documents
│   ├── redteam/ipi_pages/     # Malicious docs for testing
│   └── policies/              # Content validation
│
└── governed_agentic_ai/
    ├── README.md              # Multi-agent governance
    ├── RESULTS.md             # MAESTRO validation
    ├── app/                   # Agent orchestrator
    ├── agent/                 # Agent implementations
    ├── tools/                 # Tool registry
    ├── policies/              # OPA tool policies
    └── security/              # Context analyzer
```

---

## 🛠️ Technology Stack

<table>
<tr>
<td width="50%">

**Core Framework**
- Python 3.11+
- FastAPI (async web framework)
- Pydantic (data validation)
- asyncio (concurrent processing)

**Security**
- OPA (policy enforcement)
- JSON Schema (validation)
- Regex (pattern matching)
- Custom security processors

</td>
<td width="50%">

**LLM Integration**
- Ollama (local models)
- OpenAI SDK (cloud)
- Anthropic SDK (cloud)
- ChromaDB (vector storage - Lab 02)

**Testing & Monitoring**
- pytest (unit tests)
- curl (integration tests)
- Evidence logging (JSONL)
- Performance metrics

</td>
</tr>
</table>

---

## 🎯 Use Cases

This handbook is for:

| Role | Use Case |
|------|----------|
| **🔒 Security Engineers** | Learn AI-specific security patterns and threat models |
| **👨‍💻 AI/ML Engineers** | Add production-grade security to AI applications |
| **🏢 Enterprise Architects** | Design secure, compliant AI systems |
| **🎓 Students & Researchers** | Study practical AI security implementations |
| **🚀 Startup Founders** | Build secure AI products from day one |
| **📊 Compliance Teams** | Understand AI audit and governance requirements |

### Real-World Applications

- ✅ **Customer Support Bots** with PII protection (Lab 01)
- ✅ **Enterprise Knowledge Bases** with RAG security (Lab 02)
- ✅ **AI Research Assistants** with tool governance (Lab 03)
- ✅ **Document Processing Pipelines** with content validation
- ✅ **Automated Workflow Systems** with decision auditing

---

## 📈 Performance Benchmarks

Security overhead across all labs:

| Lab | Security Layers | Overhead | Impact |
|-----|----------------|----------|--------|
| **Lab 01** | 5 layers | <15ms (<1%) | ✅ Minimal |
| **Lab 02** | 9 layers | <100ms (<1%) | ✅ Minimal |
| **Lab 03** | Context-aware | <4ms (<0.02%) | ✅ Negligible |

**Key Finding:** Security adds **<1% latency** in all scenarios. LLM call time (10-30s) dominates.

---


## 📄 License

MIT License - Free to use, modify, and distribute.

See [LICENSE](LICENSE) for full details.

---

## 🙏 Acknowledgments

Built with insights from:

- **OWASP LLM Top 10** - AI security threat taxonomy
- **MAESTRO Framework** - Multi-agent security research
- **Anthropic's Research** - Constitutional AI and safety
- **OpenAI's Best Practices** - Prompt engineering and safety
- **Production systems** - Real-world security patterns

---


<div align="center">

## 🎓 Ready to Master AI Security?

**Start with Lab 01 and build production-ready security in less than 10 hours**

**[🚀 Begin Lab 01: PII-Safe Summarizer →](labs/pii-safe-summarizer/)**

---

*Last Updated: October 2025*

</div>