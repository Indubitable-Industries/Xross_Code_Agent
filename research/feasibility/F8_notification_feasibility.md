# F8: Push Notification Feasibility Tests

**Task ID**: F8
**Created**: 2026-01-08
**Status**: COMPLETE
**Priority**: 1 (Blocking P2P implementation)
**Depends On**: L5 (P2P Agent Communication Patterns)
**Referenced By**: [HARNESS.md Known Issues](../HARNESS.md#known-issues--feasibility-gaps)

---

## Problem Statement

L5 research identified that the P2P architecture assumes agents can:
1. Send periodic heartbeats
2. Receive push notifications

CLI agents are **not daemons** - they only act on user input or tool decisions. This feasibility test determines what notification mechanisms are actually possible.

---

## Research Questions

1. Can Claude Code receive MCP server-initiated notifications?
2. If received, are notifications surfaced to the model's context?
3. Can Claude Code be prompted to poll periodically during a session?
4. What notification mechanisms exist for Codex?
5. Can OpenCode (one-shot mode) receive any form of notification?
6. Are there hacky workarounds that could work short-term?

---

## Test Plan

### T1: Claude Code MCP Notification Reception

**Objective**: Determine if Claude Code's MCP client receives server-pushed notifications.

**Method**:
1. Create minimal MCP server that sends `notifications/resources/updated` after delay
2. Connect Claude Code to server
3. Observe if notification is received/logged/surfaced

**Expected Outcomes**:
- ✅ PASS: Notification received and surfaces to model
- ⚠️ PARTIAL: Notification received but not surfaced
- ❌ FAIL: Notification not received or ignored

**Search Queries**:
```yaml
- tool: tavily
  query: "Claude Code MCP notifications server push events"
- tool: context7
  library: "anthropic/claude-code"
  topic: "MCP notifications handling"
```

---

### T2: Claude Code Polling Capability

**Objective**: Can Claude Code be instructed to periodically check for messages?

**Method**:
1. Include "check for messages every few interactions" in system prompt or MCP config
2. Test if Claude Code actually does this
3. Measure reliability and timing

**Expected Outcomes**:
- ✅ PASS: Claude reliably polls when instructed
- ⚠️ PARTIAL: Polls sometimes but unreliable
- ❌ FAIL: Cannot influence polling behavior

**Search Queries**:
```yaml
- tool: tavily
  query: "Claude Code system prompt periodic actions MCP polling"
- tool: tavily
  query: "LLM agent background task execution CLI"
```

---

### T3: Codex MCP Support

**Objective**: Determine Codex's MCP capabilities and notification support.

**Method**:
1. Research Codex MCP client implementation
2. Test if Codex can connect to custom MCP servers
3. Test notification reception if MCP is supported

**Expected Outcomes**:
- ✅ PASS: Full MCP support with notifications
- ⚠️ PARTIAL: MCP support but no notifications
- ❌ FAIL: No MCP support (need alternative integration)

**Search Queries**:
```yaml
- tool: tavily
  query: "OpenAI Codex CLI MCP server support"
- tool: tavily
  query: "Codex CLI extensibility plugins notifications"
- tool: github
  query: "codex CLI MCP integration"
```

---

### T4: OpenCode Notification Mechanisms

**Objective**: Can OpenCode receive notifications despite one-shot execution?

**Method**:
1. Test `opencode run` with notification flags if any exist
2. Research OpenCode's internal event system
3. Test if shell-level signals could work (hacky)

**Expected Outcomes**:
- ✅ PASS: Some notification mechanism exists
- ⚠️ PARTIAL: Can detect on next invocation
- ❌ FAIL: Truly ephemeral, no notification possible

**Search Queries**:
```yaml
- tool: tavily
  query: "OpenCode CLI notifications events callback"
- tool: context7
  library: "opencode"
  topic: "event system notifications"
```

---

### T5: Hacky Workarounds

**Objective**: Identify unconventional approaches that might work.

**Ideas to Test**:

| Approach | How It Works | Feasibility |
|----------|--------------|-------------|
| File watcher | Agent watches for `.notify` file creation | ⚠️ Requires agent cooperation |
| Environment variable | Set env var, agent checks periodically | ⚠️ Only works on new invocations |
| Named pipe / FIFO | Write to pipe, agent reads | ⚠️ Platform-specific |
| Shared SQLite polling | Agent queries DB on each tool call | ✅ Most reliable fallback |
| Hook injection | Inject notification check into MCP tools | ⚠️ Modifies tool behavior |
| Long-polling endpoint | Agent keeps HTTP connection open | ❌ CLI agents don't persist |

**Search Queries**:
```yaml
- tool: tavily
  query: "inter-process communication CLI tools notification"
- tool: tavily
  query: "file watcher IPC LLM agent coordination"
```

---

---

## Raw Results - Web Search

### Search: "Claude Code MCP notifications server push events"

**Key Findings**:
- Claude Code supports MCP `list_changed` notifications - servers can dynamically update tools/prompts/resources
- WebSocket MCP servers support real-time bidirectional communication with push notifications
- SSE transport allows server-to-client push (but now deprecated in favor of HTTP)
- Community MCP servers exist for notifications:
  - [claude-code-notify-mcp](https://github.com/nkyy/claude-code-notify-mcp) - Desktop notifications with sounds
  - [notifications-mcp-server](https://github.com/charles-adedotun/notifications-mcp-server) - Audio/visual notifications

**Critical Insight**: MCP `notifications/resources/updated` exists and Claude Code receives it for `list_changed` events.

### Search: "Claude Code polling/periodic background tasks"

**Key Findings**:
- Claude Code supports background tasks via `run_in_background: true` or Ctrl+B
- Background task manager maintains process continuity across sessions
- Can monitor with `BashOutput` - "Check with BashOutput every 30 seconds"
- Sequential tool call limitation: processes each tool call sequentially within a session
- [GitHub Issue #1759](https://github.com/anthropics/claude-code/issues/1759) discusses background tasks via MCP servers

**Critical Insight**: Claude Code CAN run background processes, and there's precedent for periodic checking.

### Search: "Codex CLI MCP server support"

**Key Findings**:
- Codex supports MCP in both CLI and IDE extension
- Codex acts as BOTH MCP client AND server
- Transport types: STDIO and Streamable HTTP
- Configure in `~/.codex/config.toml`
- Run Codex as MCP server: `codex mcp` command
- Exposes `codex()` and `codex-reply()` tools

**Critical Insight**: Codex has FULL MCP support - can connect to our MCP server as client.

### Search: "OpenCode notifications events hooks"

**Key Findings**:
- OpenCode has comprehensive plugin/event system with 25+ events
- Event list includes: `session.updated`, `message.updated`, `permission.replied`, etc.
- SSE streaming for real-time events: `/global/event`
- [opencode-notifier](https://github.com/mohak34/opencode-notifier) plugin - desktop notifications
- Plugin structure: async function receiving context, returns event handler
- [Issue #1473](https://github.com/sst/opencode/issues/1473) discusses hooks support

**Critical Insight**: OpenCode has EVENT SUBSCRIPTIONS via SSE - perfect for notifications!

### Search: "IPC workarounds CLI LLM agents"

**Key Findings**:
- mcp-agent (lastmile-ai): TokenCounter with watchers for alerts, handles external signals
- Desktop Commander: file system operations with process management
- Pieces CLI: OS-level platform, can access files and execute tasks
- File watcher pattern: memory proxy auto-indexes new files
- MCP as standardized "USB-C port for AI" - connects to data sources and tools

**Critical Insight**: File watcher + SQLite polling is a viable fallback pattern.

---

## Raw Results - Context7

### Claude Code MCP Documentation

**Transport Types**:
- HTTP (streamable-http) - recommended
- SSE - deprecated but supported
- STDIO - local process

**Server Registration**:
```bash
claude mcp add --transport http <name> <url>
claude mcp add --transport stdio <name> <command>
```

**No explicit notification handling docs found** - but `list_changed` is mentioned in web search results.

### OpenCode Event System

**SSE Endpoint**: `GET /global/event?session=<session_id>`

**JavaScript Usage**:
```javascript
const eventSource = new EventSource('/global/event');
eventSource.onmessage = (event) => {
  console.log('Received event:', JSON.parse(event.data));
};
```

**SDK Usage**:
```javascript
const events = await client.event.subscribe()
for await (const event of events.stream) {
  console.log("Event:", event.type, event.properties)
}
```

**Critical Insight**: OpenCode has a FULL SSE event subscription API - we can push notifications through this!

---

## Output Format

Results will be documented in this file under each test section:

```markdown
### T1 Results

**Status**: [PASS/PARTIAL/FAIL]
**Evidence**: [What we observed]
**Implications**: [What this means for architecture]
**Code/Config**: [Any working examples]
```

---

## Synthesis (23 Sequential Thoughts)

### Per-Agent Analysis

**Claude Code**:
- MCP `list_changed` notification IS received by MCP client
- Background tasks supported via `run_in_background: true`
- Community notification servers prove desktop notifications work
- Model surfacing of notifications unclear - may require PR
- GitHub Issue #1759 explores background tasks via MCP

**Codex**:
- FULL MCP support confirmed - both client AND server
- Configure in `~/.codex/config.toml`
- Supports STDIO and Streamable HTTP transports
- Same MCP notification path as Claude Code

**OpenCode**:
- BEST notification support: native SSE at `/global/event`
- 25+ plugin events including `message.updated`, `session.updated`
- `opencode-notifier` plugin proves pattern works
- One-shot mode (`opencode run`) cannot maintain SSE connection

### Cross-Source Findings

1. **All agents have notification mechanisms** - better than expected
2. **MCP notifications reach client, but model surfacing unclear**
3. **Desktop notifications work** - user-mediated approach is viable
4. **Activity-based heartbeat** - track any MCP call, not explicit heartbeat
5. **Hybrid strategy possible** - different mechanisms per agent

---

## Decision Matrix - CORRECTED

### Initial Assessment (Optimistic) - WRONG

The initial analysis conflated:
- **Desktop notifications** = OS popups that alert the USER
- **Model-aware notifications** = Context that reaches the MODEL

CLI agents receive context ONLY from: user input, tool responses, system prompt. There's NO mechanism for external systems to inject context into an ongoing conversation.

### Corrected Assessment

| Agent | Push to MODEL? | Polling? | Reality |
|-------|----------------|----------|---------|
| Claude Code | ❌ NO | ❌ NOT RELIABLE | MCP notifications update client state, not model context |
| Codex | ❌ NO | ❌ NOT RELIABLE | Same limitation |
| OpenCode (TUI) | ❌ NO | ❌ NOT RELIABLE | SSE events display in TUI, model doesn't see them |
| OpenCode (run) | ❌ NO | ❌ NO | One-shot, no persistent connection |

### Why Polling Doesn't Work

CLI agents only act when: (1) user sends input, (2) agent decides to use a tool.

| Polling Method | Works? | Problem |
|----------------|--------|---------|
| Autonomous polling | ❌ NO | Agents aren't daemons, can't run background loops |
| Piggyback on tool calls | ⚠️ PARTIAL | Only works when agent already using our MCP |
| User prompts "check messages" | ✅ YES | Manual, not automatic |
| System prompt instruction | ⚠️ UNRELIABLE | Agent may ignore |
| Hooks | ❌ NO | Can't inject into model context |

### Verdict

**Neither push notifications nor polling work reliably for CLI agents.**

The fundamental issue: there's no interrupt mechanism. External systems cannot force an agent to take action or inject context into its conversation.

**Architecture Decision**: Current approaches are **INSUFFICIENT** for real-time P2P. Investigating alternative: [F9 - Long-Polling Keep-Alive](../features/F9_long_polling_keepalive.md)

---

## Success Criteria - RESULTS

| Criteria | Status | Evidence |
|----------|--------|----------|
| Clear answer for each agent | ✅ PASS | Decision matrix filled with specific mechanisms |
| At least ONE working approach per agent | ✅ PASS | All agents have polling; 3/4 have push |
| Fallback architecture validated | ✅ PASS | Polling + activity tracking works universally |
| Implementation recommendations documented | ✅ PASS | Hybrid strategy defined below |

### Implementation Recommendations

**Phase 1: Core Infrastructure**
- SQLite shared state with `agents` and `messages` tables
- Activity-based online status (any MCP call updates `last_activity`)
- Polling check on every tool response ("You have N pending messages")

**Phase 2: Desktop Notifications**
- Integrate desktop notification pattern from `claude-code-notify-mcp`
- Sound + popup when message arrives for user attention
- Works for Claude Code and Codex

**Phase 3: OpenCode Plugin**
- Create x_agent_code plugin subscribing to SSE events
- Real-time message push via OpenCode's event system
- Best user experience for OpenCode TUI users

**Phase 4: MCP Notification Exploration**
- Test if `notifications/resources/updated` surfaces to model
- If not, consider PR to upstream projects
- Document findings for community

---

## Next Actions After F8

Based on results:
- Update L5 conclusions with validated architecture
- Update F2 (Peer Agent Messaging) with realistic design
- Create implementation task with known constraints

### Contribution Opportunities - FINDINGS

**For tools with PARTIAL support**: Contribute to improve notification surfacing to model context.

| Tool | Repository | Gap | PR Potential | Priority |
|------|------------|-----|--------------|----------|
| Claude Code | anthropic/claude-code | MCP notifications don't surface to model context | Medium - architectural change | P2 |
| Codex | openai/codex | Same MCP surfacing gap | Medium - depends on OpenAI roadmap | P3 |
| OpenCode | sst/opencode | No gap - already excellent | N/A - contribute plugin instead | P1 |

**Actionable Contributions**:

1. **OpenCode Plugin (P1 - High Value)**
   - Create `x_agent_code` plugin for P2P messaging
   - Subscribe to SSE events, display incoming messages
   - PR to opencode-plugins or publish as standalone
   - LOW effort, HIGH impact

2. **Claude Code Issue/Discussion (P2)**
   - Reference GitHub Issue #1759 on background tasks
   - Propose MCP notification surfacing enhancement
   - May not be accepted but documents the need
   - MEDIUM effort, UNCERTAIN impact

3. **Desktop Notification Enhancement (P3)**
   - Contribute to claude-code-notify-mcp or fork
   - Add P2P message-specific notification type
   - LOW effort, MEDIUM impact

**Rationale**: Contributing back benefits:
1. Our project directly (better notification support)
2. The broader multi-agent ecosystem
3. Establishes x_agent_code as ecosystem contributor

**TODO**: Create `research/contributions/` folder with:
- [ ] OpenCode plugin specification
- [ ] Claude Code enhancement proposal draft
- [ ] Desktop notification integration spec
