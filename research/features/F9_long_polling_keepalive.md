# F9: Long-Polling Keep-Alive Pattern

**Feature ID**: F9
**Proposed**: 2026-01-08
**Status**: COMPLETE (Research) - Needs PoC Implementation
**Priority**: HIGH (Blocking P2P if F8 approaches fail)
**Depends On**: F8 (Push Notification Feasibility - found limitations)

---

## Problem Statement

F8 research determined that:
- Push notifications don't reach model context
- Polling doesn't work (agents aren't daemons, can't autonomously check)
- There's no interrupt mechanism for CLI agents

**The gap**: How do we deliver messages to an agent that only acts on user input or tool calls?

---

## Proposed Solution: Long-Polling Keep-Alive

### Core Concept

Instead of the agent polling the server, **the agent stays in an open tool call** that the server holds until there's work to do.

```
┌─────────────────┐                    ┌─────────────────┐
│   Child Agent   │                    │   MCP Server    │
│  (Claude Code)  │                    │  (x_agent_code) │
└────────┬────────┘                    └────────┬────────┘
         │                                      │
         │  1. register_and_wait()              │
         │─────────────────────────────────────►│
         │                                      │
         │     [Server holds connection open]   │
         │                                      │
         │                    2. Message arrives│
         │                    from another agent│
         │                                      │
         │  3. Response: {message: "..."}       │
         │◄─────────────────────────────────────│
         │                                      │
         │  4. Agent processes message          │
         │                                      │
         │  5. register_and_wait() [loop]       │
         │─────────────────────────────────────►│
         │                                      │
```

### Hierarchy Implication

This creates a real parent-child hierarchy:
- **Parent Agent**: The one orchestrating (e.g., Claude Code in main window)
- **Child Agents**: Register with MCP, wait for commands
- **MCP Server**: Broker that holds connections and routes messages

---

## Technical Questions (Need Research)

### Q1: MCP Tool Call Timeouts

Do MCP tool calls have timeouts? If so, what are they?

**If timeout exists**:
- Server returns "no work, re-poll" before timeout
- Agent loops back with another `register_and_wait()`
- This is classic long-polling

**If no timeout**:
- Server can hold indefinitely until work arrives
- Simpler but may have other issues (connection drops, etc.)

### Q2: Agent Behavior in Long Tool Calls

Will the agent actually wait for a long-running tool call to complete?

**Concerns**:
- Does the agent timeout internally?
- Does the user interface become unresponsive?
- Can the agent be interrupted by user input?

### Q3: Token Usage

What's the token cost of:
- The initial `register_and_wait()` call?
- A "no work" response that triggers re-poll?
- The loop overhead?

**Goal**: Minimize tokens for idle waiting, only use tokens for real work.

### Q4: Re-entrancy

When agent receives a message and processes it, can it:
- Call other tools while processing?
- Send responses back?
- Then re-enter the wait state?

### Q5: Multiple Children

Can multiple child agents be waiting simultaneously?
- Server needs to track multiple open connections
- Route messages to correct waiting agent
- Handle agent disconnects gracefully

---

## Proposed MCP Tool Interface

### `register_and_wait()`

```python
@mcp_tool
def register_and_wait(
    agent_name: str,
    agent_type: str,  # "claude-code" | "codex" | "opencode"
    capabilities: list[str],
    timeout_seconds: int = 30  # Return "no work" before this
) -> dict:
    """
    Register as a child agent and wait for work.

    Returns when:
    - A message arrives for this agent
    - Timeout reached (returns no_work: true)
    - Server shutting down

    Response:
    {
        "agent_id": "uuid",
        "no_work": false,
        "message": {
            "from": "parent-agent-id",
            "mode": "challenge",
            "content": "Review this code...",
            "context": {...}
        }
    }

    Or if timeout:
    {
        "agent_id": "uuid",
        "no_work": true,
        "pending_count": 0
    }
    """
```

### `respond_and_wait()`

```python
@mcp_tool
def respond_and_wait(
    agent_id: str,
    response_to: str,  # message_id being responded to
    response: str,
    timeout_seconds: int = 30
) -> dict:
    """
    Send response to previous message and wait for next work.
    Combines response + re-registration in single call.
    """
```

---

## Token Optimization Strategies

### Strategy 1: Minimal Response Schema

```json
// Instead of verbose response:
{"status": "no_work", "agent_id": "...", "timestamp": "...", "queue_depth": 0}

// Use minimal:
{"nw": true}  // no work
{"m": "..."}  // message content only
```

### Strategy 2: Adaptive Timeout

- Start with short timeout (5s) when activity is expected
- Increase timeout (30s, 60s) during idle periods
- Decrease when messages start flowing

### Strategy 3: Batch Heartbeats

- Server tracks multiple waiting agents
- Single "tick" response to all idle agents
- Reduces round-trips

### Strategy 4: Delta Encoding

- Only send changes, not full state
- Agent maintains local state
- Server sends diffs

---

## Implementation Phases

### Phase 1: Proof of Concept
- Implement basic `register_and_wait()` with fixed timeout
- Test with Claude Code as child agent
- Measure token usage and latency

### Phase 2: Optimization
- Implement minimal response schema
- Add adaptive timeout
- Test with multiple children

### Phase 3: Production
- Add error handling and reconnection
- Implement `respond_and_wait()` for efficiency
- Add monitoring and metrics

---

## Research Tasks

| ID | Question | Method |
|----|----------|--------|
| F9.1 | MCP tool call timeout limits | Test with Claude Code, check MCP spec |
| F9.2 | Agent behavior during long calls | Test with real agents |
| F9.3 | Token usage baseline | Measure with minimal payloads |
| F9.4 | User experience impact | Test responsiveness during wait |
| F9.5 | Multi-agent scaling | Test with 3+ waiting agents |

---

## Success Criteria

1. Child agent can wait for work without user prompting
2. Messages delivered within 5 seconds of arrival
3. Token overhead < 100 tokens per minute while idle
4. User can still interrupt waiting agent if needed
5. Pattern works for Claude Code, Codex, and OpenCode

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| MCP timeout too short | Medium | High | Implement re-poll loop |
| High token usage | Medium | Medium | Minimal response schema |
| Agent becomes unresponsive | Low | High | Test interruptibility |
| Connection drops | Medium | Low | Auto-reconnect logic |
| Doesn't work with all agents | Medium | High | Test each agent type |

---

## Alternative Approaches (If This Fails)

1. **User-prompted checking**: Accept manual "check messages" workflow
2. **Scheduled check**: Agent checks at start of each user interaction
3. **Out-of-band notification**: Desktop notification prompts user to tell agent
4. **Different architecture**: Abandon P2P, use purely synchronous patterns

---

---

## Raw Results - Web Search

### Search: "MCP tool call timeout limits"

**Key Findings**:
- MCP spec says implementations SHOULD establish timeouts to prevent hung connections
- Timeouts SHOULD be configurable on a per-request basis
- Progress notifications CAN reset the timeout clock (implies work is happening)
- Maximum timeout SHOULD always be enforced regardless of progress notifications

### Search: "long-polling LLM agents patterns"

**Key Findings**:
- [AsyncLM Paper](https://arxiv.org/abs/2412.07017): Proposes interrupt mechanism to notify LLM in-flight when functions return
- [MCP Issue #982](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/982): Discusses long-running/async tools with polling mechanisms
- Proposed workflow: CallToolAsyncRequest → CallToolAsyncResult with taskId → Poll with CheckToolAsyncStatusRequest
- Pattern: Tool returns immediately with taskId, widget/client polls, displays results
- Temporal/Forge patterns: Offload to queue, stream results back via pub/sub

### Search: "MCP streaming SSE long-running tools"

**Key Findings**:
- MCP supports Streamable HTTP transport with SSE for long-running operations
- Server can return standard JSON OR upgrade to SSE stream for progressive results
- Progress notifications sent during processing, main result still single response
- HTTP/1.1 proxies may close idle connections after 60 seconds - send heartbeats every 30s
- SSE streams are resumable - server can replay messages after disconnection
- Client sends Accept header with both `application/json` and `text/event-stream`

### Search: "Claude Code tool call timeout configuration"

**Key Findings**:
- Default bash timeout: 2 minutes (120 seconds)
- Configurable via `~/.claude/settings.json`:
  - `BASH_DEFAULT_TIMEOUT_MS`: default 120000ms
  - `BASH_MAX_TIMEOUT_MS`: up to 7200000ms (2 hours)
  - `MCP_TIMEOUT`: MCP server startup timeout
- Hardcoded max may exist: ~612 seconds (10min 12sec) reported by users
- Codex: Configure in `~/.codex/config.toml` with `timeout = <seconds>`
- Full restart required after changing settings

---

## Raw Results - Context7

### MCP Specification: Timeouts

```
Implementations SHOULD establish timeouts for all sent requests.
When timeout expires, sender SHOULD issue cancellation notification.
SDKs SHOULD allow timeouts to be configured per-request.
Progress notifications MAY reset timeout clock.
Maximum timeout SHOULD always be enforced.
```

### MCP Specification: Progress Notifications

```json
{
  "method": "notifications/progress",
  "params": {
    "progressToken": "abc123",
    "progress": 50,
    "total": 100,
    "message": "Processing..."
  }
}
```
- Progress notifications keep connection alive during long operations
- Server sends these out-of-band to inform client of status
- Client can use these to reset timeout clock

### MCP Specification: SSE Streams (GET /mcp)

```
Clients establish SSE stream via GET request to /mcp endpoint.
Server can send messages proactively to client.
Accept header must include text/event-stream.
Server sends JSON-RPC requests and notifications on this stream.
```

---

---

## Synthesis (20 Sequential Thoughts)

### Research Question Answers

**Q1: MCP Tool Call Timeouts**
- MCP spec: implementations SHOULD establish configurable timeouts
- Progress notifications MAY reset timeout clock
- Maximum timeout SHOULD always be enforced regardless of progress
- **Claude Code**: Default 2 minutes, configurable up to 2 hours via `~/.claude/settings.json`
- **Codex**: Configure in `~/.codex/config.toml` with `timeout = <seconds>`
- **Verdict**: ✅ Timeouts exist but are configurable and can be extended via progress notifications

**Q2: Agent Behavior in Long Tool Calls**
- MCP supports SSE upgrade for Streamable HTTP - server can progressively send results
- User interruptibility: Unclear from spec, needs empirical testing
- UI responsiveness: Likely maintained if using non-blocking transport
- **Verdict**: ⚠️ NEEDS EMPIRICAL TESTING - spec supports it, behavior unknown

**Q3: Token Usage**
- Not directly addressed in searches
- Minimal response schema (`{"nw": true}`) should minimize tokens
- Progress notifications are out-of-band, don't add to model context
- **Verdict**: ⚠️ NEEDS EMPIRICAL TESTING - measure with PoC

**Q4: Re-entrancy**
- MCP sessions persist across multiple tool calls
- Agent maintains session ID, can call other tools
- `respond_and_wait()` pattern combines response + re-registration
- **Verdict**: ✅ YES - MCP session management supports re-entrancy

**Q5: Multiple Children**
- MCP servers act as multiplexers for concurrent connections
- HTTP+SSE best for high concurrency (HTTP/2 multiplexing)
- Server tracks multiple open connections, routes to correct agent
- **Verdict**: ✅ YES - MCP architecture supports multiple concurrent waiting agents

### Viability Assessment

**THEORETICALLY VIABLE** based on MCP spec support for:

1. **Streamable HTTP with SSE** - Server can upgrade to SSE stream for long-running tools
2. **Progress Notifications** - Keep connection alive, reset timeout clock
3. **Configurable Timeouts** - Up to 2 hours in Claude Code
4. **HTTP/2 Multiplexing** - Multiple concurrent waiting agents supported
5. **30-Second Heartbeats** - Prevent HTTP proxy disconnection

### Critical Gap

All findings are **spec-based, not empirically validated**. Phase 1 PoC required to test:
- Does Claude Code's MCP client handle SSE tool responses correctly?
- Do progress notifications actually reset Claude Code's internal timeout?
- Can user interrupt a waiting agent?
- What is actual token usage for minimal heartbeat responses?

---

## Conclusions

### Pattern Viability: ✅ THEORETICALLY VIABLE

The long-polling keep-alive pattern CAN work based on MCP specification support. Key requirements:

1. **Use Streamable HTTP transport** (not STDIO) for SSE capability
2. **Send progress notifications every 30 seconds** as heartbeats
3. **Configure agent timeout** appropriately (extend from default 2 min)
4. **Implement graceful timeout/re-registration loop**
5. **Use minimal response schema** to minimize token usage

### Implementation Path

| Phase | Work | Validates |
|-------|------|-----------|
| Phase 1 | Basic `register_and_wait()` PoC | Agent waits, receives message |
| Phase 2 | Heartbeat + timeout handling | Connection stays alive |
| Phase 3 | Multi-agent + `respond_and_wait()` | Full production pattern |

### Remaining Uncertainties (Need Empirical Testing)

| Uncertainty | Test Method |
|-------------|-------------|
| Claude Code SSE handling | Create test MCP server with SSE tool |
| Progress notification timeout reset | Long-running tool with periodic notifications |
| User interruptibility | Try Ctrl+C during wait |
| Token usage | Measure with minimal responses |
| OpenCode/Codex behavior | Test same pattern with each agent |

---

## Success Criteria - Assessment

| Criteria | Status | Evidence |
|----------|--------|----------|
| Child agent can wait for work | ⚠️ NEEDS PoC | Spec supports via SSE, not tested |
| Messages delivered within 5s | ✅ LIKELY | SSE provides real-time delivery |
| Token overhead < 100/min idle | ⚠️ NEEDS PoC | Progress notifications out-of-band |
| User can interrupt | ⚠️ NEEDS PoC | Unclear from spec |
| Works for all agents | ⚠️ PARTIAL | Depends on each agent's MCP client |

---

## Next Actions

1. ~~**Create Phase 1 PoC MCP server**~~ - ✅ DONE: [`poc/f9_long_polling/`](../../poc/f9_long_polling/)
2. **Test with Claude Code** first (best documented timeout config)
3. **Measure token usage** of heartbeat loop
4. **Test user interruptibility** (Ctrl+C, new message)
5. **If successful**: Proceed to Phase 2 optimization
6. **If fails**: Document specific failure mode, consider alternatives

---

## PoC Implementation

**Location**: [`poc/f9_long_polling/`](../../poc/f9_long_polling/)

### Quick Start

```bash
cd poc/f9_long_polling
uv sync
uv run server.py
```

Server runs at `http://localhost:8000/mcp`

### Add to Claude Code

```bash
claude mcp add --transport http f9-poc http://localhost:8000/mcp
```

### Tools

| Tool | Purpose |
|------|---------|
| `register_and_wait(agent_name, timeout_seconds)` | Wait for work, receive heartbeats |
| `send_message(content, mode)` | Queue a message for waiting agent |
| `check_status()` | Server status and pending messages |

### Test Procedure

See formal test harness: [`feasibility/F9_poc_test_harness.md`](../feasibility/F9_poc_test_harness.md)

Quick reference: [`poc/f9_long_polling/README.md`](../../poc/f9_long_polling/README.md)

---

## References

- F8: Push Notification Feasibility (found the limitations)
- F2: Peer Agent Messaging (original feature proposal)
- L5: P2P Agent Communication Patterns (architecture research)
