"""
F9 PoC: Long-Polling Keep-Alive MCP Server

Tests whether CLI agents (Claude Code) can wait in an open tool call
while the server holds the connection and sends heartbeat progress notifications.

Usage:
    uv run server.py

Then add to Claude Code:
    claude mcp add --transport http f9-poc http://localhost:8765/mcp
"""

import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession

# Configuration
HEARTBEAT_INTERVAL = 30  # seconds between heartbeats
DEFAULT_TIMEOUT = 120    # seconds before returning "no_work"
MESSAGE_FILE = Path(__file__).parent / "pending_message.json"

mcp = FastMCP("F9-LongPolling-PoC")


def log(msg: str):
    """Simple timestamped logging."""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def check_for_message() -> dict | None:
    """Check if there's a pending message in the file."""
    if MESSAGE_FILE.exists():
        try:
            with open(MESSAGE_FILE) as f:
                message = json.load(f)
            # Remove the file after reading (message consumed)
            MESSAGE_FILE.unlink()
            log(f"Message found and consumed: {message.get('content', '')[:50]}...")
            return message
        except (json.JSONDecodeError, IOError) as e:
            log(f"Error reading message file: {e}")
    return None


@mcp.tool()
async def register_and_wait(
    agent_name: str,
    ctx: Context[ServerSession, None],
    timeout_seconds: int = DEFAULT_TIMEOUT
) -> dict[str, Any]:
    """
    Register as a child agent and wait for work.

    This tool holds the connection open, sending heartbeat progress notifications
    every 30 seconds until either:
    - A message arrives (returns the message)
    - Timeout is reached (returns no_work: true)

    Args:
        agent_name: Name to register this agent as
        timeout_seconds: How long to wait before returning no_work (default 120s)

    Returns:
        Either a message dict or {"no_work": true}
    """
    log(f"Agent '{agent_name}' registered, waiting for work (timeout: {timeout_seconds}s)")

    start_time = asyncio.get_event_loop().time()
    heartbeat_count = 0

    while True:
        elapsed = asyncio.get_event_loop().time() - start_time

        # Check for timeout
        if elapsed >= timeout_seconds:
            log(f"Timeout reached for agent '{agent_name}' after {heartbeat_count} heartbeats")
            return {
                "no_work": True,
                "agent_name": agent_name,
                "waited_seconds": int(elapsed),
                "heartbeats_sent": heartbeat_count
            }

        # Check for pending message
        message = check_for_message()
        if message:
            log(f"Delivering message to agent '{agent_name}'")
            return {
                "no_work": False,
                "agent_name": agent_name,
                "message": message,
                "waited_seconds": int(elapsed),
                "heartbeats_sent": heartbeat_count
            }

        # Send heartbeat progress notification
        heartbeat_count += 1
        progress = elapsed / timeout_seconds
        await ctx.report_progress(
            progress=progress,
            total=1.0,
            message=f"Heartbeat #{heartbeat_count} - waiting for work ({int(elapsed)}s/{timeout_seconds}s)"
        )
        log(f"Heartbeat #{heartbeat_count} sent for agent '{agent_name}' ({int(elapsed)}s elapsed)")

        # Wait for next check (check every second, but only heartbeat every HEARTBEAT_INTERVAL)
        # This allows faster message detection while keeping heartbeats at 30s intervals
        next_heartbeat = heartbeat_count * HEARTBEAT_INTERVAL
        while asyncio.get_event_loop().time() - start_time < min(next_heartbeat, timeout_seconds):
            # Quick poll for messages (every 1 second)
            await asyncio.sleep(1)
            message = check_for_message()
            if message:
                log(f"Delivering message to agent '{agent_name}' (between heartbeats)")
                return {
                    "no_work": False,
                    "agent_name": agent_name,
                    "message": message,
                    "waited_seconds": int(asyncio.get_event_loop().time() - start_time),
                    "heartbeats_sent": heartbeat_count
                }


@mcp.tool()
async def send_message(content: str, mode: str = "info") -> dict[str, Any]:
    """
    Send a message to a waiting agent.

    This is a helper tool for testing - in production, messages would come
    from other agents or external systems.

    Args:
        content: The message content
        mode: Message mode (challenge, agree, collaborate, info)

    Returns:
        Confirmation of message queued
    """
    message = {
        "content": content,
        "mode": mode,
        "timestamp": datetime.now().isoformat(),
        "from": "test_sender"
    }

    with open(MESSAGE_FILE, 'w') as f:
        json.dump(message, f)

    log(f"Message queued: {content[:50]}...")
    return {
        "status": "queued",
        "message": message
    }


@mcp.tool()
async def check_status() -> dict[str, Any]:
    """
    Check server status and whether any message is pending.

    Returns:
        Server status information
    """
    return {
        "server": "F9-LongPolling-PoC",
        "status": "running",
        "message_pending": MESSAGE_FILE.exists(),
        "heartbeat_interval": HEARTBEAT_INTERVAL,
        "default_timeout": DEFAULT_TIMEOUT
    }


if __name__ == "__main__":
    print("=" * 60)
    print("F9 Long-Polling PoC Server")
    print("=" * 60)
    print(f"Heartbeat interval: {HEARTBEAT_INTERVAL}s")
    print(f"Default timeout: {DEFAULT_TIMEOUT}s")
    print(f"Message file: {MESSAGE_FILE}")
    print()
    print("To test:")
    print("  1. Add to Claude Code:")
    print("     claude mcp add --transport http f9-poc http://localhost:8000/mcp")
    print()
    print("  2. In Claude Code, call:")
    print("     register_and_wait(agent_name='test')")
    print()
    print("  3. Send a message (in another terminal):")
    print("     uv run send_message.py 'Hello from test!' info")
    print()
    print("=" * 60)
    print()

    # Run with streamable-http transport (default port 8000)
    mcp.run(transport="streamable-http")
