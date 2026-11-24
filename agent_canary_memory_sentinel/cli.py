"""CLI for Canary Memory Sentinel."""
import argparse
from .core import CanaryMemorySentinel

def main():
    parser = argparse.ArgumentParser(description="Agent Canary Memory Sentinel CLI")
    parser.add_argument("--demo", action="store_true", help="Run canary test demo")
    args = parser.parse_args()

    sentinel = CanaryMemorySentinel()
    canary = sentinel.plant_canary("conversation_history")
    memory = f"User said hello. System state normal. {canary}"

    res = sentinel.inspect_memory(memory)
    print(f"Memory check intact={res['intact']}, found={res['found_canaries']}")

if __name__ == "__main__":
    main()
