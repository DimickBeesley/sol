from app.harness.ollama import OllamaBackend

if __name__ == "__main__":
    ollama = OllamaBackend()

    print(ollama.generate("Hello Gemma!"))
