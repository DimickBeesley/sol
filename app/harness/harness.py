from app.backends.ollama import OllamaBackend
from app.backends.anthropic import AnthropicBackend
from app.harness.tools.files import glob_files, read_file, create_file, edit_file
from app.harness.tools.retrieval import retrieve_context

TOOLS = [read_file, glob_files, create_file, edit_file, retrieve_context]
TOOL_MAP = {fn.__name__: fn for fn in TOOLS}

class SolHarness():
    def __init__(self):
        self.history = []
        self.backend = None

    def get_backend(self, backend_id):
        if backend_id == "a":
            return AnthropicBackend()
        elif backend_id == "o":
            return OllamaBackend()
        else:
            raise ValueError(f"Unknown backend: {backend_id}")


    def call_chat(self, backend_id, prompt):
        call_context = ""
        stream_dump = ""
        self.backend = self.get_backend(backend_id)

        self.history.append({"role": "user", "content": prompt})
        
        

        messages = list(self.history)

        for chunk in self.backend.chat(messages, tools=TOOLS, tool_map=TOOL_MAP):
            print(chunk, end="", flush=True)
            stream_dump += chunk
        print()

        self.history.append({"role": "assistant", "content": stream_dump})
        
