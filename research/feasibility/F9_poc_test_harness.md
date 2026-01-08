# F9 PoC Test Harness

**Test ID**: F9-POC
**Created**: 2026-01-08
**Status**: NOT_STARTED
**Depends On**: F9 research, PoC implementation
**PoC Location**: [`poc/f9_long_polling/`](../../poc/f9_long_polling/)

---

## Objective

Empirically validate the long-polling keep-alive pattern with Claude Code to determine if child agents can wait in open tool calls while receiving heartbeat progress notifications.

---

## Test Environment

### Prerequisites

| Requirement | Version/Details | Verified |
|-------------|-----------------|----------|
| Python | >= 3.11 | [ ] |
| uv | Latest | [ ] |
| Claude Code | Latest | [ ] |
| Port 8000 | Available | [ ] |

### Setup Commands

```bash
# 1. Navigate to PoC directory
cd /home/phaze/PycharmProjects/x_agent_code/poc/f9_long_polling

# 2. Install dependencies
uv sync

# 3. Start server (Terminal 1)
uv run server.py

# 4. Register MCP server with Claude Code (Terminal 2)
claude mcp add --transport http f9-poc http://localhost:8000/mcp

# 5. Verify registration
claude mcp list
```

---

## Test Cases

### T1: Basic Tool Registration

**Objective**: Verify MCP server connects and tools are visible.

**Steps**:
1. Start server: `uv run server.py`
2. In Claude Code: "List available MCP tools"

**Expected**:
- `register_and_wait` tool visible
- `send_message` tool visible
- `check_status` tool visible

**Pass Criteria**: All 3 tools listed
**Fail Criteria**: Tools not found or connection error

**Result**: `[ ] PASS  [ ] FAIL  [ ] SKIP`
**Notes**:

---

### T2: Short Wait with Timeout

**Objective**: Verify agent waits for tool completion and receives timeout response.

**Steps**:
1. Start server
2. In Claude Code: "Use register_and_wait with agent_name 'test' and timeout_seconds 30"
3. Wait for response (do NOT send any message)

**Expected**:
- Server logs show heartbeat at ~30s mark
- Tool returns after ~30s with `{"no_work": true}`
- Claude Code displays the response (not an error)

**Pass Criteria**:
- [ ] Tool returns cleanly (not timeout error)
- [ ] Response contains `no_work: true`
- [ ] Server logged at least 1 heartbeat

**Fail Criteria**:
- Claude Code shows "tool timeout" error before server returns
- Connection drops during wait
- No heartbeat logged

**Result**: `[ ] PASS  [ ] FAIL  [ ] SKIP`
**Notes**:

---

### T3: Message Delivery During Wait

**Objective**: Verify message can be delivered to waiting agent.

**Steps**:
1. Start server
2. In Claude Code: "Use register_and_wait with agent_name 'test' and timeout_seconds 120"
3. In Terminal 3 (within 30 seconds):
   ```bash
   cd /home/phaze/PycharmProjects/x_agent_code/poc/f9_long_polling
   uv run send_message.py "Test message from harness" challenge
   ```
4. Observe Claude Code response

**Expected**:
- Server logs "Message found and consumed"
- Tool returns with `no_work: false` and message content
- Claude Code receives and displays the message

**Pass Criteria**:
- [ ] Message delivered to waiting agent
- [ ] Response contains message content
- [ ] Mode is "challenge"
- [ ] Delivery time < 5 seconds after message sent

**Fail Criteria**:
- Message not received
- Timeout before message delivery
- Wrong message content

**Result**: `[ ] PASS  [ ] FAIL  [ ] SKIP`
**Notes**:

---

### T4: Multiple Heartbeats

**Objective**: Verify multiple heartbeats are sent during extended wait.

**Steps**:
1. Start server
2. In Claude Code: "Use register_and_wait with agent_name 'test' and timeout_seconds 90"
3. Wait for full duration (do NOT send message)

**Expected**:
- Server logs 3 heartbeats (at ~30s, ~60s, ~90s)
- Progress notifications visible in server logs
- Tool returns with `heartbeats_sent: 3`

**Pass Criteria**:
- [ ] 3 heartbeats logged
- [ ] No connection drops
- [ ] Response shows correct heartbeat count

**Fail Criteria**:
- Fewer than 3 heartbeats
- Connection drops during wait
- Claude Code timeout error

**Result**: `[ ] PASS  [ ] FAIL  [ ] SKIP`
**Notes**:

---

### T5: User Interrupt (Ctrl+C)

**Objective**: Verify user can interrupt a waiting agent.

**Steps**:
1. Start server
2. In Claude Code: "Use register_and_wait with agent_name 'test' and timeout_seconds 300"
3. After ~15 seconds, press Ctrl+C in Claude Code
4. Attempt to use Claude Code normally

**Expected**:
- Wait is interrupted
- Claude Code remains responsive
- No hung state or error cascade

**Pass Criteria**:
- [ ] Ctrl+C interrupts the wait
- [ ] Claude Code usable after interrupt
- [ ] Server handles disconnection gracefully

**Fail Criteria**:
- Cannot interrupt
- Claude Code becomes unresponsive
- Requires restart

**Result**: `[ ] PASS  [ ] FAIL  [ ] SKIP`
**Notes**:

---

### T6: Token Usage Measurement

**Objective**: Measure token overhead of waiting.

**Steps**:
1. Note Claude Code token count before test
2. In Claude Code: "Use register_and_wait with agent_name 'test' and timeout_seconds 60"
3. Wait for timeout
4. Note Claude Code token count after test
5. Calculate tokens used

**Expected**:
- Minimal token usage (< 100 tokens per minute of waiting)
- Progress notifications don't add to model context

**Pass Criteria**:
- [ ] Token usage < 200 tokens for 60s wait
- [ ] Acceptable overhead for production use

**Fail Criteria**:
- Token usage > 500 tokens for 60s wait
- Exponential token growth with wait time

**Result**: `[ ] PASS  [ ] FAIL  [ ] SKIP`
**Tokens Before**:
**Tokens After**:
**Delta**:
**Notes**:

---

### T7: Extended Duration (Claude Code Timeout Test)

**Objective**: Test if Claude Code's internal timeout can handle longer waits.

**Steps**:
1. Start server
2. In Claude Code: "Use register_and_wait with agent_name 'test' and timeout_seconds 180"
3. At ~150 seconds, send message:
   ```bash
   uv run send_message.py "Extended wait test" info
   ```

**Expected**:
- Claude Code waits full 150 seconds
- Message delivered successfully
- No timeout errors from Claude Code

**Pass Criteria**:
- [ ] Wait exceeds 2 minutes (Claude Code default timeout)
- [ ] Message delivered successfully
- [ ] Progress notifications kept connection alive

**Fail Criteria**:
- Claude Code timeout at 2 minutes
- Connection dropped
- Message not delivered

**Result**: `[ ] PASS  [ ] FAIL  [ ] SKIP`
**Actual Wait Duration**:
**Notes**:

---

## Test Execution Log

| Test | Date | Executor | Result | Notes |
|------|------|----------|--------|-------|
| T1 | | | | |
| T2 | | | | |
| T3 | | | | |
| T4 | | | | |
| T5 | | | | |
| T6 | | | | |
| T7 | | | | |

---

## Environment Capture

Record before testing:

```
Date:
Claude Code Version:
Python Version:
OS:
MCP SDK Version:

Claude Code Settings (if modified):
- MCP_TIMEOUT:
- BASH_DEFAULT_TIMEOUT_MS:
- Other:
```

---

## Summary & Conclusions

### Overall Result

`[ ] PASS - Pattern validated, proceed to implementation`
`[ ] PARTIAL - Some tests failed, needs investigation`
`[ ] FAIL - Pattern does not work as expected`

### Key Findings

1.
2.
3.

### Blockers Identified

1.
2.

### Recommendations

1.
2.

---

## Post-Test Actions

- [ ] Update F9 research doc with results
- [ ] Update TRACKER.md status
- [ ] If PASS: Create implementation task
- [ ] If FAIL: Document failure mode, explore alternatives
- [ ] Commit test results

---

## References

- [F9 Research](../features/F9_long_polling_keepalive.md)
- [F8 Notification Feasibility](F8_notification_feasibility.md) (negative result that led to F9)
- [PoC README](../../poc/f9_long_polling/README.md)
