#!/usr/bin/env python3
import argparse

from app.cli.interface import run

BACKEND_IDS = {"ollama": "o", "anthropic": "a"}

def parse_args():
    parser = argparse.ArgumentParser(prog="sol")
    parser.add_argument("backend", nargs="?", choices=BACKEND_IDS.keys(), default="anthropic")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    run(BACKEND_IDS[args.backend])
