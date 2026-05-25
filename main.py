import sys
import time
import argparse
from app.harness.harness import SolHarness

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", choices=["o", "a"], default="o", help="Backend: o=Ollama, a=Anthropic")
    parser.add_argument("prompt", help="The prompt to send")
    args = parser.parse_args()

    harness = SolHarness()
    start = time.time()

    if args.b == "o":
        harness.call_stream(backend_id="o", prompt=args.prompt)
    else:
        print(harness.call_generate(backend_id="a", prompt=args.prompt))

    elapsed = time.time() - start
    print(f"\n[{elapsed:.2f}s]")
