from app.backends.ollama import OllamaBackend
from app.backends.anthropic import AnthropicBackend
from app.harness.tools.files import glob_files, read_file, create_file, edit_file, rename_file
from app.harness.tools.retrieval import retrieve_context

from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from rich.rule import Rule
import pathlib
import difflib
import time

console = Console()

TOOLS = [read_file, glob_files, create_file, edit_file, retrieve_context, rename_file]
TOOL_MAP = {fn.__name__: fn for fn in TOOLS}

SYSTEM_PROMPT = (pathlib.Path(__file__).parent / "prompts/system.md").read_text()

def preview_tool_call(name, args):
    if name == "create_file":
        console.print(Syntax(args.get("content", ""), "markdown", theme="monokai"))
    elif name == "edit_file":
        path = args.get("path")
        edits = args.get("edits", [])
        try:
            content = pathlib.Path(path).read_text()
            new_content = content
            for edit in edits:
                new_content = new_content.replace(edit["old"], edit["new"])
            diff = "".join(difflib.unified_diff(
                content.splitlines(keepends=True),
                new_content.splitlines(keepends=True),
                fromfile=path,
                tofile=path,
            ))
            console.print(Syntax(diff or "(no changes detected)", "diff", theme="monokai"))
        except Exception as e:
            console.print(f"[dim](preview unavailable: {e})[/]")

class SolHarness():
    def __init__(self):
        self.history = [{"role": "system", "content": SYSTEM_PROMPT}]
        self.backend = None

    def get_backend(self, backend_id):
        if backend_id == "a":
            return AnthropicBackend()
        elif backend_id == "o":
            return OllamaBackend()
        else:
            raise ValueError(f"Unknown backend: {backend_id}")

    def call_complete(self, backend_id, prompt):
        stream_dump = ""
        self.backend = self.get_backend(backend_id)

        self.history.append({"role": "user", "content": prompt})
        messages = list(self.history)

        start = time.time()

        # Tool loop
        while True:
            start_per_tool = time.time()
            with console.status("[dim]Thinking...[/]"):
                response = self.backend.complete(messages, tools=TOOLS)
            elapsed_per_tool = time.time() - start_per_tool
            if not response.tool_calls:
                break
            messages.append(response)
            for tool_call in response.tool_calls:
                fn = TOOL_MAP.get(tool_call.function.name)
                if fn:
                    args_text = "\n".join(f"[dim]{k}:[/] {v}" for k, v in tool_call.function.arguments.items())
                    console.print(Panel(
                        args_text,
                        title=f"[bold cyan]{tool_call.function.name}[/] [dim]({elapsed_per_tool:.1f}s)[/]",
                        border_style="yellow",
                        padding=(0, 1),
                    ))
                    preview_tool_call(tool_call.function.name, tool_call.function.arguments)
                    approval = input("  Run? [y/n]: ")
                    if approval.strip().lower() != "y":
                        messages.append({"role": "tool", "content": "Tool call rejected by user. Do not retry this tool call. Ask the user for clarification or what they'd like to do instead."})
                        continue
                    result = fn(**tool_call.function.arguments)
                    messages.append({"role": "tool", "content": str(result)})

        elapsed = time.time() - start
        console.print(f"\n[dim]thought for {elapsed:.1f}s[/]")
        console.rule("[bold]Sol[/]", style="bright_blue")
        for chunk in self.backend.chat(messages, tools=TOOLS):
            print(chunk, end="", flush=True)
            stream_dump += chunk
        print()
        console.rule(style="dim")

        self.history.append({"role": "assistant", "content": stream_dump})
