import sys
from app.harness.harness import SolHarness

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <prompt>")
        sys.exit(1)

    prompt = sys.argv[1]
    harness = SolHarness()
    print(harness.call_generate("o", prompt))
