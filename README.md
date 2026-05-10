# Sol

Personal LLM harness and agent automation orchestrator. Runs local models via Ollama alongside the Anthropic API, indexes a local Obsidian vault for RAG, and automates homelab workflows — starting with keeping [blu3mlab.com](https://blu3mlab.com) in sync with lab documentation.

---

## What it does

- **Harness** — unified interface over Ollama (local) and Anthropic (cloud), so pipelines don't care which backend they're using
- **Ingestion** — indexes an Obsidian vault into PostgreSQL (pgvector) for semantic retrieval
- **blu3mlab pipeline** — compares vault documentation against the portfolio site, proposes additions as GitHub PRs for human review
- **CLI** — Click-based entrypoints for headless/cron invocation

---

## Architecture

```
Obsidian Vault ──► LlamaIndex + pgvector (RAG)
                         │
                         ▼
              Harness (Ollama / Anthropic)
                         │
                         ▼
            blu3mlab-pipeline agent
                         │
                         ▼
         GitHub PR on DimickBeesley/portfolio
                         │
                         ▼
                  Human review & merge
```

---

## Setup

### 1. Install Ollama (Arch Linux)

```bash
yay -S ollama
systemctl enable --now ollama
ollama pull qwen2.5
ollama pull nomic-embed-text
```

### 2. Python environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Environment variables

Copy `.env.example` to `.env` and fill in:

```
ANTHROPIC_API_KEY=...
GITHUB_AGENT_TOKEN=...   # PAT for the agent GitHub account
```

### 4. Index the vault

```bash
python main.py ingest
```

---

## Usage

```bash
# Index / re-index the Obsidian vault
python main.py ingest

# Run the portfolio sync pipeline
python main.py pipeline blu3mlab

# Interactive chat with a model (debug/dev)
python main.py chat --backend ollama
```

---

## Project layout

```
app/
  harness/            # LLM backend abstraction
  ingestion/          # Vault indexing and RAG
  blu3mlab-pipeline/  # Portfolio diff and PR agent
  interface/          # Click CLI definitions
main.py
```

---

## Key paths (local)

| Resource | Path |
|---|---|
| Obsidian vault | `/home/blu3m/Code/blu3mlab-vault/` |
| Portfolio site | `/home/blu3m/Code/portfolio/` |
