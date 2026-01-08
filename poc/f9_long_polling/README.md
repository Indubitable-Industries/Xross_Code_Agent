# F9 PoC: Long-Polling Keep-Alive Pattern

**Purpose**: Validate that CLI agents (Claude Code) can wait in an open tool call while the MCP server holds the connection and sends heartbeat progress notifications.

## Research Question

From [F9 research](../../research/features/F9_long_polling_keepalive.md):

> Can child agents stay in an open tool call, receiving periodic heartbeats, until work arrives?

## What This Tests

1. **Claude Code waits for long-running tool** - Does it timeout or wait?
2. **Progress notifications work** - Do heartbeats reset the timeout?
3. **Message delivery works** - Can we deliver work to a waiting agent?
4. **User can interrupt** - Can Ctrl+C stop a waiting agent?
5. **Token usage** - How many tokens does the wait loop consume?

## Setup

```bash
cd poc/f9_long_polling

# Install dependencies
uv sync

# Start the server
uv run server.py
```

Server runs at `http://localhost:8000/mcp`

## Test Procedure

### Test 1: Basic Wait and Timeout

1. Add MCP server to Claude Code:
   ```bash
   claude mcp add --transport http f9-poc http://localhost:8000/mcp
   ```

2. In Claude Code, call the tool:
   ```
   Use the register_and_wait tool with agent_name "test-agent" and timeout_seconds 60
   ```

3. **Expected**:
   - Server logs show heartbeats every 30s
   - After 60s, tool returns `{"no_work": true}`
   - Claude Code receives the response (not a timeout error)

### Test 2: Message Delivery

1. Start Claude Code waiting:
   ```
   Use register_and_wait with agent_name "test-agent" and timeout_seconds 120
   ```

2. In another terminal, send a message:
   ```bash
   echo '{"content": "Hello from test!", "mode": "info"}' > pending_message.json
   ```

   Or use the helper script:
   ```bash
   uv run send_message.py "Review this code for security issues" challenge
   ```

3. **Expected**:
   - Server logs show message consumed
   - Tool returns with `{"no_work": false, "message": {...}}`
   - Claude Code receives and can process the message

### Test 3: User Interrupt

1. Start Claude Code waiting with long timeout:
   ```
   Use register_and_wait with agent_name "test-agent" and timeout_seconds 300
   ```

2. Press Ctrl+C in Claude Code

3. **Expected**:
   - Wait is interrupted
   - Claude Code remains usable
   - No error state

### Test 4: Multiple Heartbeats

1. Start with longer timeout:
   ```
   Use register_and_wait with agent_name "test-agent" and timeout_seconds 180
   ```

2. **Expected**:
   - See 6 heartbeats (one every 30s)
   - Each heartbeat logged on server
   - Progress increases: 0.17, 0.33, 0.50, 0.67, 0.83, 1.0

## Success Criteria

| Criteria | Pass | Fail |
|----------|------|------|
| Agent waits for tool completion | Tool returns after timeout | Claude Code shows timeout error before server returns |
| Heartbeats visible in server logs | See "Heartbeat #N" messages | No heartbeats or connection drops |
| Message delivered to waiting agent | Tool returns message content | Message not received |
| User can interrupt | Ctrl+C works cleanly | Hung state or error |
| Token usage acceptable | < 100 tokens per minute idle | Excessive token consumption |

## Files

- `server.py` - MCP server with `register_and_wait` tool
- `send_message.py` - Helper to send test messages
- `pending_message.json` - File-based message queue (created when message sent)
- `pyproject.toml` - Dependencies

## Configuration

In `server.py`:

```python
HEARTBEAT_INTERVAL = 30  # seconds between progress notifications
DEFAULT_TIMEOUT = 120    # seconds before returning no_work
```

Adjust these for testing different scenarios.

## Troubleshooting

**"Connection refused"**
- Ensure server is running: `uv run server.py`
- Check port 8765 is available

**"Tool not found"**
- Re-add the MCP server: `claude mcp add --transport http f9-poc http://localhost:8000/mcp`
- Restart Claude Code

**"Timeout" error in Claude Code**
- This is the failure case we're testing for
- Check Claude Code's MCP timeout settings in `~/.claude/settings.json`
- Try increasing `MCP_TIMEOUT` or tool-specific timeouts

## Results

Document your test results here:

```
Date:
Claude Code Version:
Test 1 (Wait/Timeout): PASS/FAIL - notes
Test 2 (Message Delivery): PASS/FAIL - notes
Test 3 (User Interrupt): PASS/FAIL - notes
Test 4 (Multiple Heartbeats): PASS/FAIL - notes
Token Usage: X tokens over Y minutes
```
