# NexusAI 🧠
### Multi-Agent Autonomous Research & Decision Intelligence System

> **"From raw data to actionable decisions — fully autonomous."**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Status: Active](https://img.shields.io/badge/status-active-green.svg)]()

---

## The Problem

Every organization drowns in data but starves for decisions.

Current AI tools answer single questions. They don't:
- Connect dots across 50 sources simultaneously
- Reason through multi-step problems autonomously
- Collaborate between specialized agents to cross-validate findings
- Deliver a final decision with full reasoning trace

**NexusAI solves this.** It deploys a coordinated swarm of specialized AI agents that research, reason, debate, and converge on high-confidence decisions — without human hand-holding.

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   ORCHESTRATOR AGENT                 │
│         (Task decomposition + agent routing)         │
└──────────┬──────────┬──────────┬────────────────────┘
           │          │          │
    ┌──────▼──┐ ┌─────▼───┐ ┌───▼──────┐
    │RESEARCH │ │ANALYST  │ │VALIDATOR │
    │ AGENT   │ │ AGENT   │ │  AGENT   │
    │(web+RAG)│ │(reason) │ │(critique)│
    └──────┬──┘ └─────┬───┘ └───┬──────┘
           └──────────┴──────────┘
                      │
           ┌──────────▼──────────┐
           │   SYNTHESIS AGENT   │
           │ (final report + CoT)│
           └─────────────────────┘
```

### Agent Roles

| Agent | Role | Capability |
|-------|------|------------|
| **Orchestrator** | Task decomposition | Breaks complex goals into parallel subtasks |
| **Research Agent** | Data gathering | Web search, RAG, document parsing |
| **Analyst Agent** | Chain-of-thought reasoning | Multi-step inference, pattern detection |
| **Validator Agent** | Critique & fact-check | Cross-validates claims, flags contradictions |
| **Synthesis Agent** | Final output | Merges findings into structured decision report |

---

## Key Features

- **Long-chain reasoning** — Analyst agent uses CoT (Chain-of-Thought) with up to 32 reasoning steps
- **Multi-agent debate** — Validator challenges Analyst findings before synthesis
- **Persistent memory** — Vector store (ChromaDB) for cross-session context retention
- **Tool use** — Web search, code execution, file parsing, API calls
- **Streaming output** — Real-time reasoning trace visible to user
- **REST API** — Drop-in integration for any product

---

## Quickstart

```bash
git clone https://github.com/Sicanbt/NexusAI.git
cd NexusAI
pip install -r requirements.txt
cp .env.example .env  # add your API keys
python -m nexus run "Analyze the top 5 AI infrastructure companies and recommend the best investment target"
```

---

## Example Output

```
[ORCHESTRATOR] Breaking task into 3 subtasks...
[RESEARCH]     Fetching data on NVIDIA, CoreWeave, Lambda Labs, Together AI, Groq...
[ANALYST]      Step 1: Revenue growth analysis...
               Step 2: Moat assessment...
               Step 8: Risk-adjusted scoring...
[VALIDATOR]    Challenging claim: "CoreWeave has strongest moat"...
               Counter-evidence found. Flagging for re-analysis.
[ANALYST]      Revising conclusion based on validator feedback...
[SYNTHESIS]    Final recommendation: [NVIDIA] — confidence 87%
               Full reasoning trace: 847 tokens
```

---

## Tech Stack

- **LLM Backend**: OpenAI GPT-4o / Anthropic Claude / local via Ollama
- **Agent Framework**: Custom orchestration (no LangChain overhead)
- **Memory**: ChromaDB (vector) + Redis (session)
- **API**: FastAPI + WebSocket for streaming
- **Frontend**: Next.js dashboard with real-time agent trace visualization

---

## Roadmap

- [x] Core multi-agent orchestration
- [x] Chain-of-thought reasoning engine
- [x] REST API + streaming
- [ ] Web UI dashboard
- [ ] Plugin marketplace for custom tools
- [ ] Enterprise SSO + audit logs
- [ ] On-premise deployment (Docker + K8s)

---

## License

MIT — free to use, modify, and deploy.
