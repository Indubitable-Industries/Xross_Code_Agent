# A2: System Topology

**Research ID**: A2
**Status**: COMPLETE
**Source**: Architecture design (2026-01-07)

---

## Full System Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        x_agent_code Architecture                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   USER                                                                  │
│     │                                                                   │
│     ▼                                                                   │
│   ┌──────────────────────────────────────────────────────────────────┐  │
│   │  Claude Code (HUB)                                               │  │
│   │  - Interactive terminal you're using                             │  │
│   │  - Has MCP tools: Claude-Mem, Serena, Chrome, Playwright, etc.   │  │
│   │  - Middleware runs as MCP server attached to Claude Code         │  │
│   └────────────────────────┬─────────────────────────────────────────┘  │
│                            │                                            │
│                            │ MCP protocol                               │
│                            ▼                                            │
│   ┌──────────────────────────────────────────────────────────────────┐  │
│   │  x_agent_code Middleware (MCP Server)                            │  │
│   │  - Runs locally, Claude Code connects via MCP                    │  │
│   │  - Exposes tools: ask_gpt(), ask_agent(), list_agents()          │  │
│   │  - Auto-generates capability proxies from Claude's MCP tools     │  │
│   │  - Manages mode (challenge/agree/collaborate/deduce)             │  │
│   └────────────────────────┬─────────────────────────────────────────┘  │
│                            │                                            │
│                            │ HTTP API                                   │
│                            ▼                                            │
│   ┌──────────────────────────────────────────────────────────────────┐  │
│   │  opencode serve (background process)                             │  │
│   │  - Started on middleware init: `opencode serve --port 3001`      │  │
│   │  - Middleware calls HTTP endpoints                               │  │
│   │  - GPT-5 via OpenCode's provider system                          │  │
│   │  - Can call BACK to Claude via proxied capabilities              │  │
│   └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│   Future: Additional spoke agents on different ports                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Component Breakdown

### Layer 1: User Interface

| Component | Description |
|-----------|-------------|
| Claude Code | Terminal interface user interacts with |
| User commands | Natural language requests ("ask GPT to...") |

### Layer 2: Hub (Claude Code)

| Component | Description |
|-----------|-------------|
| Claude Code runtime | Interactive AI assistant |
| Native MCP tools | Claude-Mem, Serena, Chrome, Playwright, etc. |
| MCP client | Connects to middleware MCP server |

### Layer 3: Middleware

| Component | Description |
|-----------|-------------|
| MCP Server | Protocol interface for Claude Code |
| Agent Registry | Tracks available spoke agents |
| Mode Manager | Handles interaction modes |
| Capability Proxy | Exposes Claude's tools to spokes |
| HTTP Client | Communicates with OpenCode serve |

### Layer 4: Spoke Agents

| Component | Description |
|-----------|-------------|
| OpenCode serve | Background HTTP server |
| OpenRouter | Model routing layer |
| GPT-5 / Grok / etc. | Actual AI models |

---

## Communication Protocols

### Claude Code ↔ Middleware

**Protocol**: MCP (Model Context Protocol)
**Transport**: stdio (local subprocess)
**Format**: JSON-RPC over newline-delimited streams

### Middleware ↔ OpenCode

**Protocol**: HTTP REST
**Transport**: TCP localhost:3001
**Format**: JSON request/response

### OpenCode ↔ Models

**Protocol**: OpenRouter API
**Transport**: HTTPS
**Format**: OpenAI-compatible API

---

## Data Flow Diagrams

### Forward Request (Claude → GPT)

```
User: "Ask GPT to review this code"
        │
        ▼
┌─────────────────┐
│   Claude Code   │
│ (parse request) │
└────────┬────────┘
         │ MCP call: ask_gpt(context, mode)
         ▼
┌─────────────────┐
│   Middleware    │
│ (format prompt) │
└────────┬────────┘
         │ HTTP POST /session/{id}/message
         ▼
┌─────────────────┐
│ OpenCode serve  │
│ (route to GPT)  │
└────────┬────────┘
         │ OpenRouter API
         ▼
┌─────────────────┐
│     GPT-5       │
│  (generate)     │
└────────┬────────┘
         │ Response
         ▼
    [Back up chain]
         │
         ▼
User sees: "GPT-5 Review: ..."
```

### Reverse Request (GPT → Claude tools)

```
GPT: "Need to read /logs/training.log"
        │
        ▼
┌─────────────────┐
│ OpenCode serve  │
│(intercept tool) │
└────────┬────────┘
         │ HTTP callback to middleware
         ▼
┌─────────────────┐
│   Middleware    │
│ (proxy request) │
└────────┬────────┘
         │ MCP call to Claude's Read tool
         ▼
┌─────────────────┐
│   Claude Code   │
│ (execute tool)  │
└────────┬────────┘
         │ File contents
         ▼
    [Back up chain]
         │
         ▼
GPT receives file contents
```

---

## Port Allocation

| Service | Port | Purpose |
|---------|------|---------|
| OpenCode serve | 3001 | Primary GPT-5 harness |
| Future agent 2 | 3002 | Reserved |
| Future agent 3 | 3003 | Reserved |

---

## Process Lifecycle

### Startup

```
1. claude (user command)
2. └── x_agent_code MCP server (spawned by Claude Code)
3.     └── opencode serve --port 3001 (spawned by middleware)
```

### Shutdown

```
1. User exits Claude Code
2. Claude Code terminates MCP servers
3. Middleware receives SIGTERM
4. Middleware kills opencode serve child process
5. Clean exit
```

---

## Extensibility Points

### Adding New Spoke Agent

1. Implement HTTP server on new port
2. Register in middleware agent registry
3. Map capabilities to proxy interface
4. Configure routing rules

### Adding New Capability

1. Define tool schema in middleware
2. Implement handler (forward to spoke or proxy Claude tool)
3. Register in capability registry
4. Test bidirectional flow

---

## References

- [MCP Middleware Design](A1_mcp_middleware.md)
- [Feature Design](A3_feature_design.md)
