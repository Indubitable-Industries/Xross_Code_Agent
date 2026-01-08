# A1: MCP Middleware Design

**Research ID**: A1
**Status**: COMPLETE
**Source**: Discovery research + Architecture decisions (2026-01-06/07)

---

## Overview

The x_agent_code middleware is an **MCP server that Claude Code connects to**, providing the bridge between Claude Code (hub) and spoke agents (OpenCode/GPT-5, future agents).

## Architecture Decision: Hub-Spoke

**DECIDED**: Hub-spoke topology with Claude Code at center (NOT bidirectional peer-to-peer).

```
                    ┌─────────────┐
                    │ Claude Code │  ← User interacts here
                    │   (HUB)     │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
         ┌────────┐  ┌────────┐  ┌────────┐
         │OpenCode│  │ Vibe   │  │Future N│
         │ (GPT)  │  │(defer) │  │ agents │
         └────────┘  └────────┘  └────────┘
```

**Rationale**:
- Claude Code orchestrates all interactions
- Other agents are spokes, not peers
- Extensible to N agents without complexity explosion
- User has single point of interaction

---

## Interaction Model Decision

**DECIDED**: Model A - Invisible Subprocess

### Model A (CHOSEN)

- Claude Code spawns other agents as subprocesses (no visible window)
- Passes context + mode-specific prompt
- Waits for response, displays inline
- Visibility of "thinking": nice-to-have if possible, logging acceptable, not required

### Model B (DEFERRED)

Visible parallel windows where you SEE the other agent working in a separate terminal.
- Requires push-based injection into running sessions
- More complex, defer to later phase

---

## MCP Foundation

### Key Findings

| Finding | Implication |
|---------|-------------|
| MCP operates via stdio (local) and HTTP (remote) transports | Multi-agent requires HTTP transport |
| `claude mcp serve` exposes Claude Code tools to other agents | Capability proxying is native |
| Stdio restricts stdout to MCP messages, logging to stderr | Clean message separation |
| Each MCP server registers in service registry | Discoverable architecture |

### Critical Capability

**Claude Code can act as MCP SERVER** via `claude mcp serve`.

This enables:
- Other agents to call Claude's tools
- Central MCP server as message broker/context hub
- Native protocol without custom implementation

---

## Middleware Responsibilities

### Core Functions

| Function | Description |
|----------|-------------|
| Agent registry | Track available spoke agents and their capabilities |
| Request routing | Claude → middleware → spoke agent |
| Mode system | Implement challenge/agree/collaborate/deduce modes |
| Response formatting | Standardize display in Claude Code |

### Exposed MCP Tools

| Tool | Purpose |
|------|---------|
| `ask_gpt()` | Send request to GPT-5 via OpenCode |
| `ask_agent(agent, prompt)` | Generic agent request |
| `list_agents()` | Enumerate available spoke agents |
| `set_mode(mode)` | Change interaction mode |

---

## Capability Proxying

### Pattern

The middleware should **auto-expose capabilities** from Claude Code's MCP tools up to spoke agents.

```
GPT (via OpenCode) → Middleware → Claude Code's MCP tools
```

### Example Cross-Agent Requests

**GPT → Claude (leveraging Claude's tools)**:
- "Ask Claude to use its Chrome tools to take a screenshot"
- "Tell Claude to update all Serena memories"
- "Have Claude search its memory for previous solutions"
- "Ask Claude to use Playwright to test the login flow"

**Claude → GPT (leveraging GPT's strengths)**:
- "Ask GPT why this model is stuck, here's the training config"
- "Send GPT the model architecture for optimization suggestions"
- "Have GPT review this PyTorch code for DL pitfalls"

### Data Passing

- Claude can pass: code snippets, disk paths, config values, log excerpts
- Middleware handles context serialization and size management

---

## Request Flow Example

**User in Claude Code**:
```
> Ask GPT to review plan.md in challenge mode
```

**Middleware action**:
```
POST localhost:3001/run
{
  "prompt": "[CHALLENGE MODE] Review this plan critically...",
  "context": { ... plan.md contents ... }
}
```

**Response displayed in Claude Code**:
```
─────────────────────────────
GPT-5 Review (challenge mode):
Three concerns with this plan:
1. ...
─────────────────────────────
```

### Reverse Request (GPT → Claude tools)

```
GPT: "I need to see the training logs. Ask Claude to
      use its file tools to read /output/logs/training.log"

[Middleware intercepts → calls Claude's Read tool → passes result back to GPT]
```

---

## Startup Sequence

1. User runs `claude` (normal Claude Code)
2. Claude Code loads x_agent_code MCP server from config
3. MCP server starts `opencode serve --port 3001` as child process
4. MCP server introspects Claude's available tools, builds capability registry
5. Ready - user can now say "ask GPT to review this"

---

## Implementation Phases

### Phase 1: Foundation
1. Create middleware MCP server skeleton
2. Port logging system from TelemetryManager
3. Implement agent registry
4. Basic `ask_agent()` tool

### Phase 2: OpenCode Integration
1. Start `opencode serve` as child process
2. HTTP client for OpenCode API
3. Mode system (challenge/agree/collaborate/deduce)
4. Response formatting and display

### Phase 3: Capability Proxying
1. MCP tool introspection
2. Capability registry generation
3. Proxy tool exposure to spoke agents
4. Bidirectional request handling

### Phase 4: Optimization (if needed)
1. Profile under load
2. Async pattern audit
3. Codon JIT for hot paths
4. Caching layer

---

## References

- MCP specification
- Tavily search: "MCP server architecture" (2026-01-06)
- Architecture decisions D1, D2, D3
