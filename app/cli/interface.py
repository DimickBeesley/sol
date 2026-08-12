import sys
from app.harness.harness import SolHarness
from app.rag.ingestion import ingest
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings

bindings = KeyBindings()

@bindings.add("enter")
def _submit(event):
    event.current_buffer.validate_and_handle()

@bindings.add("escape", "enter")
def _newline(event):
    event.current_buffer.insert_text("\n")

def run(backend_id="a"):
    harness = SolHarness()
    session = PromptSession(key_bindings=bindings, multiline=True)

    print("Reindexing vault...")
    ingest()

    while True:
        try:
            prompt = session.prompt(f"\n[{backend_id}] You: ")
        except (KeyboardInterrupt, EOFError):
            sys.exit()

        if not prompt.strip():
            continue
        elif prompt.strip().startswith("/"):
            sanitized = prompt.strip().strip("/")
            if sanitized == "exit":
                sys.exit()
            elif sanitized in ("a", "o"):
                backend_id = sanitized
                print(f"switched to backend: {backend_id}")
            elif sanitized == "index":
                print("Reindexing vault...")
                ingest()
        else:
            harness.call_complete(backend_id=backend_id, prompt=prompt)
