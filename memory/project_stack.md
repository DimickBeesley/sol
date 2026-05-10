---
name: Sol Project Stack
description: Technology choices and infrastructure for the Sol project
type: project
---

Sol is a Python-based LLM orchestration layer.

- **Local LLMs**: Ollama (needs installation on Arch) + Qwen model (needs install) + nomic-embed-text for embeddings
- **Cloud LLM**: Anthropic API
- **Obsidian vault**: /home/blu3m/Code/blu3mlab-vault/ — full vector RAG planned
- **Portfolio site**: Flask app behind Cloudflare proxy. GitHub: https://github.com/DimickBeesley/portfolio, local path: /home/blu3m/Code/portfolio. HTML edited manually in the past.
- **Approval workflow**: Agent GitHub user creates PRs on the portfolio site repo; user gets notified and reviews

**Why:** Homelab-focused, privacy-conscious setup. Local-first where possible, API for heavier reasoning.
**How to apply:** Prefer local-first solutions (Ollama embeddings, Postgres/pgvector for storage). Anthropic API reserved for complex reasoning tasks. User wants to build Postgres familiarity — use it for both vector and structured data rather than introducing a separate store.

**Agreed library choices:**
- Harness: raw `ollama` + `anthropic` SDKs behind a shared Protocol/ABC (no LangChain)
- RAG: LlamaIndex (ObsidianReader) + PostgreSQL/pgvector (`llama-index-vector-stores-postgres`) + nomic-embed-text via Ollama
- Pipeline: PyGithub for PR creation from agent GitHub account
- Interface: Click CLI + Rich (no TUI)
