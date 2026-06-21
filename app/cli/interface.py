import sys
from app.harness.harness import SolHarness
from rich.console import Console

console = Console()
harness = SolHarness()

def handle_command(usr_input):
    sanitized_input = usr_input.strip("/")
    if sanitized_input == "exit":
        sys.exit()

while True:
    prompt = input("\n\033[1mYou:\033[0m ")
    if not prompt.strip():
        continue
    elif prompt[0] == "/":
        handle_command(prompt)
    else:
        harness.call_complete(backend_id="o", prompt=prompt)
