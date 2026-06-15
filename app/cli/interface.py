import sys
from app.harness.harness import SolHarness

BOLD = "\033[1m"
RESET = "\033[0m"

harness = SolHarness()

def handle_command(usr_input):
    sanitized_input = usr_input.strip("/")
    if sanitized_input == "exit":
        sys.exit()

while True:
    prompt = input(f"\n{BOLD}You:{RESET} ")
    if not prompt.strip():
        continue
    elif prompt[0] == "/":
        handle_command(prompt)
    else:
        print(f"\n{BOLD}Qwen:{RESET} ", end="", flush=True)
        harness.call_complete(backend_id="o", prompt=prompt)

