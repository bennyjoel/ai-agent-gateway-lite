# 🤖 AI Agent Gateway (Community Edition)

> Lightweight, high-throughput asynchronous multi-provider AI gateway. Route agent calls seamlessly across Google Gemini, Anthropic Claude, and OpenAI with automated failover and Model Context Protocol (MCP) tool integration.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python)](https://python.org)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-8A2BE2)](https://modelcontextprotocol.io)

---

### 🚀 Community vs. Hardened Enterprise Edition

This repository contains the **Community (Open-Source)** edition. If you need a fully hardened, multi-tenant enterprise mesh with Redis semantic token caching, automated secret redaction, SQLite episodic agent memory, and token circuit-breakers that guarantee zero runaway billing explosions, check out the **Enterprise Edition**:

| Capability | Community (Free / Open-Source) | [Enterprise Edition ($49)](https://duskfall847.gumroad.com/l/azbrax) |
|---|---|---|
| **Multi-Provider Routing** | Gemini, Claude, OpenAI | ✅ Gemini, Claude, OpenAI + DeepSeek & Local Ollama |
| **Failover Mechanics** | Sequential fallback | ✅ Exponential backoff + Adaptive latency routing |
| **Token Circuit Breaker** | ❌ None | ✅ Hard spend ceilings + Loop recursion cutoff |
| **Episodic Memory Mesh** | ❌ None | ✅ SQLite / ChromaDB semantic episodic memory |
| **Guardrails & PII Filter** | Basic regex | ✅ Automated secret scrubbing + Prompt injection defense |
| **Containerization** | Dockerfile basic | ✅ Multi-stage Distroless Docker + docker-compose mesh |
| **Commercial License** | MIT | ✅ Perpetual Commercial License + Lifetime Architecture Updates |

👉 **[Get the Full Turnkey Enterprise System on Gumroad ($49)](https://duskfall847.gumroad.com/l/azbrax)**

---

## ⚡ Quickstart

Install dependencies:

```bash
git clone https://github.com/bennyjoel/ai-agent-gateway-lite.git
cd ai-agent-gateway-lite
pip install -r requirements.txt
```

Set your API keys:

```bash
export GEMINI_API_KEY="your_key"
export ANTHROPIC_API_KEY="your_key"
export OPENAI_API_KEY="your_key"
```

Run the gateway:

```python
import asyncio
from gateway import AgentGateway

async def main():
    gateway = AgentGateway()
    response = await gateway.chat("Explain Byzantine Fault Tolerance in 2 sentences.")
    print(response)

asyncio.run(main())
```

---

## 🏗️ Architecture

```text
       [ User / Client Agent ]
                  │
                  ▼
        ┌──────────────────┐
        │   AgentGateway   │
        └─────────┬────────┘
                  │  (Smart Provider Failover)
         ┌────────┼────────┐
         ▼        ▼        ▼
     [ Gemini ] [ Claude ] [ OpenAI ]
```

---

## 📦 Commercial Developer Ecosystem

Browse our production-grade architecture systems:

* 📦 **[Next.js 15 Micro-SaaS Boilerplate ($59)](https://duskfall847.gumroad.com/l/xqkhz)**: Supabase RLS, React 19, Stripe idempotency.
* 📦 **[FastAPI Production Microservice Kit ($39)](https://duskfall847.gumroad.com/l/pnwdbj)**: High-throughput async UVLoop architecture.
* 📦 **[Autonomous eBPF Threat Isolator ($399)](https://duskfall847.gumroad.com/l/jhvpeq)**: Kernel-level syscall interceptor.
* 🌐 **[Full Developer Architecture Storefront](https://benny-hub.pages.dev)**

---

## 📄 License

Community Edition is licensed under the [MIT License](LICENSE).
