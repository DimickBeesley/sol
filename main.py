from app.harness.ollama import OllamaBackend
from app.harness.anthropic import AnthropicBackend
from app.ingestion.ingestion import ingest

if __name__ == "__main__":
    ingest()
