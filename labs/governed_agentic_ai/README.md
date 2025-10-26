# Lab 03: Governed Agentic AI 🤖

<div align="center">

**Multi-Agent Systems with MCP-Style Tool Governance**

[![Lab Status](https://img.shields.io/badge/status-complete-success.svg)](.)
[![Difficulty](https://img.shields.io/badge/difficulty-advanced-red.svg)](.)
[![Time](https://img.shields.io/badge/time-3--4%20hours-blue.svg)](.)

[🎯 Overview](#overview) • [🏢 Architecture](#architecture) • [🚀 Setup](#setup) • [🧪 Tests](#test-scenarios) • [📊 Results](RESULTS.md)

</div>

---

## 🎯 Overview

A multi-agent orchestration system demonstrating **Agent-to-Agent (A2A) governance** with MCP-style tool control, budgets, schema validation, sandboxing, and evidence logging.

### Key Features

| Security | Governance |
|----------|------------|
| ✅ Tool Allowlists per Agent | ✅ Budget Enforcement (calls + time) |
| ✅ JSON Schema Validation | ✅ Sandbox Path Traversal Protection |
| ✅ Side-Effect Detection | ✅ Append-Only Evidence Log |
| ✅ Exfiltration Pattern Detection | ✅ Agent Identity & Authorization |

### Learning Objectives

1. **Understand** agentic AI security challenges (unauthorized tool access, exfiltration)
2. **Implement** MCP-style tool registry with governance controls
3. **Enforce** per-agent tool allowlists and execution budgets
4. **Detect**