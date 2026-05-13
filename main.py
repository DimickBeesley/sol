from app.harness.ollama import OllamaBackend
from app.harness.anthropic import AnthropicBackend

if __name__ == "__main__":
    ollama = OllamaBackend()
    anthropic = AnthropicBackend()

    print(anthropic.generate("Hello Claude!"))
