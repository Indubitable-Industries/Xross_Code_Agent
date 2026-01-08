#!/usr/bin/env python3
"""
Helper script to send a message to a waiting agent.

Usage:
    uv run send_message.py "Your message content" [mode]

Modes: challenge, agree, collaborate, deduce, info (default: info)

Example:
    uv run send_message.py "Review this code for security issues" challenge
"""

import json
import sys
from datetime import datetime
from pathlib import Path

MESSAGE_FILE = Path(__file__).parent / "pending_message.json"


def send_message(content: str, mode: str = "info"):
    """Write a message to the pending message file."""
    message = {
        "content": content,
        "mode": mode,
        "timestamp": datetime.now().isoformat(),
        "from": "cli_sender"
    }

    with open(MESSAGE_FILE, 'w') as f:
        json.dump(message, f, indent=2)

    print(f"Message queued:")
    print(f"  Content: {content[:80]}{'...' if len(content) > 80 else ''}")
    print(f"  Mode: {mode}")
    print(f"  File: {MESSAGE_FILE}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    content = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "info"

    valid_modes = ["challenge", "agree", "collaborate", "deduce", "info"]
    if mode not in valid_modes:
        print(f"Invalid mode: {mode}")
        print(f"Valid modes: {', '.join(valid_modes)}")
        sys.exit(1)

    send_message(content, mode)


if __name__ == "__main__":
    main()
