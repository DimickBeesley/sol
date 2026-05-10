# Sol

LLM harness and agent automation orchestrator. Combines local Ollama models, the Anthropic API, and RAG over a local Obsidian vault to power automated homelab workflows — primarily keeping the portfolio site (blu3mlab.com) in sync with lab documentation.

---

## Project Structure

```
app/
  harness/          # LLM abstraction layer — unified interface over Ollama and Anthropic
  ingestion/        # Obsidian vault indexing and RAG retrieval
  blu3mlab-pipeline/ # Portfolio site diff/update agent
  interface/        # Click CLI for headless/cron invocation
main.py             # Entry point
```

All local repos live under `/home/blu3m/Code/`.

---

## Key Paths

| Resource | Path |
|---|---|
| Obsidian vault | `/home/blu3m/Code/blu3mlab-vault/` |
| Portfolio site (local) | `/home/blu3m/Code/portfolio/` |
| Portfolio site (GitHub) | https://github.com/DimickBeesley/portfolio |

---

## Tech Stack

**Language:** Python

**LLM backends:**
- Local: Ollama (`ollama` Python library) — Qwen for generation, `nomic-embed-text` for embeddings
- Cloud: Anthropic API (`anthropic` SDK) — reserved for complex reasoning tasks

**RAG pipeline:**
- LlamaIndex with ObsidianReader (handles wikilinks + frontmatter)
- PostgreSQL + pgvector as vector store (`llama-index-vector-stores-postgres`)
- Embeddings via Ollama (`nomic-embed-text`)
- Same Postgres instance can store structured data (pipeline run history, approval states, etc.)

**Portfolio pipeline:**
- PyGithub for PR creation from a dedicated agent GitHub account
- GitHub email notifications for review — no additional notification layer needed

**Interface:**
- Click for CLI entrypoints
- Rich for terminal output formatting
- No TUI — Claude Code is the primary interactive interface

---

## Harness Design

The harness uses a shared `Protocol` or ABC so pipelines don't care whether they're talking to Ollama or Anthropic. New backends slot in without touching pipeline code. Avoid LangChain — use raw SDKs for control and clarity.

---

## blu3mlab Pipeline Flow

1. Index/update vault RAG from `/home/blu3m/Code/blu3mlab-vault/`
2. Read current portfolio site HTML from `/home/blu3m/Code/portfolio/`
3. Use LLM to compare vault content against site content and propose additions
4. Agent GitHub account opens a PR on `DimickBeesley/portfolio`
5. User reviews and merges or closes — no auto-merge

---

## Ollama Setup (Arch)

Still needs to be installed. Required models:
- `qwen2.5` (or whichever Qwen variant) — generation
- `nomic-embed-text` — embeddings for RAG

---

## Environment

Secrets go in `.env` (gitignored). Expected keys:
- `ANTHROPIC_API_KEY`
- `GITHUB_AGENT_TOKEN` — PAT for the agent GitHub account used to open PRs
