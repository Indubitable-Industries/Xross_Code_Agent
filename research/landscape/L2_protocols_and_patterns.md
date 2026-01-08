# L2: Protocols and Patterns

**Research ID**: L2
**Status**: COMPLETE
**Source**: Discovery research (2026-01-06)

---

## MCP (Model Context Protocol)

### Overview

MCP provides the **vertical integration layer** between agents and tools/data.

### Transport Modes

| Transport | Use Case | Characteristics |
|-----------|----------|-----------------|
| **stdio** | Local subprocess | Single client, stdout=MCP messages, stderr=logging |
| **HTTP** | Remote/multi-client | Multiple clients, network-accessible |

### Key Finding

**Claude Code can act as MCP SERVER** via `claude mcp serve`.

This enables:
- Exposing Claude Code tools (view, edit, bash, grep) to other agents
- Native protocol for cross-agent tool sharing
- No custom protocol implementation needed

### Architecture Pattern

Central MCP server that all CLI agents connect to as message broker/context hub.

### Configuration Scopes

| Scope | Location | Use Case |
|-------|----------|----------|
| Project | Git repository | Project-specific tools |
| Local | User directory | User preferences |
| Global | Machine-wide | Shared infrastructure |

### Message Format

- JSON-RPC over newline-delimited streams
- Each server registers in service registry
- Host application instantiates dedicated client instances per server

---

## A2A Protocol (Agent-to-Agent)

### Overview

Google's open standard for **horizontal agent interoperability** (complements MCP's vertical integration).

### Status

| Milestone | Date | Status |
|-----------|------|--------|
| Initial release | 2025 | Complete |
| Linux Foundation donation | June 2025 | Complete |
| Production-ready | End 2025 | Target |
| Company backing | - | 100+ companies |

**Recommendation**: Don't depend on A2A yet, but adopt compatible design patterns.

### Core Concepts

| Concept | Description |
|---------|-------------|
| Client agent | Initiates requests |
| Remote agent | Receives delegated tasks |
| `agent_card` / `agent.json` | Capability advertisement |
| Capability negotiation | Dynamic discovery |

### Relationship to MCP

| Protocol | Direction | Purpose |
|----------|-----------|---------|
| MCP | Vertical | Agent ↔ Tools/Data |
| A2A | Horizontal | Agent ↔ Agent |

### ADK Integration

Agent Development Kit (ADK) supports `to_a2a()` conversion for interoperability.

---

## CLI Agent Communication Patterns

### Pattern 1: Subprocess Spawning

```
Parent Agent → spawn → Child Agent → response
```

**Characteristics**:
- Simple, synchronous
- No persistent connection
- Cold boot per request

### Pattern 2: HTTP Server

```
Agent A → HTTP → Agent B Server → response
```

**Characteristics**:
- Persistent service
- Multiple clients
- Warm connection

### Pattern 3: MCP Server

```
Agent A → MCP protocol → MCP Server → tools/data
```

**Characteristics**:
- Native Claude Code support
- Tool/capability sharing
- Registry-based discovery

---

## Claude Code Extensibility

### Hooks

Custom shell scripts for workflow customization.

### Skills System

| Location | Scope |
|----------|-------|
| `~/.claude/skills/` | User global |
| `.claude/skills/` | Project local |

Format: YAML/Markdown files

### MCP Support Rating

| Tool | MCP Rating |
|------|------------|
| Claude Code | 5/5 |
| Codex | 3/5 |

### Sub-agents

Claude Code supports spawning specialized worker agents.

### CCC (Custom Launcher)

Supports agents, MCPs, plugins with FastMCP integration.

---

## Design Patterns for x_agent_code

### Adopted from A2A (without dependency)

1. **Agent registry with capability cards**
   - Each spoke agent advertises capabilities
   - Middleware maintains registry
   - Dynamic discovery on startup

2. **Client→Remote task delegation**
   - Claude Code as client/hub
   - Spoke agents as remote workers
   - Middleware routes requests

3. **Capability negotiation**
   - Query available tools per agent
   - Route requests to capable agents
   - Fallback handling

### Adopted from MCP

1. **Tool exposure**
   - Middleware exposes tools to Claude Code
   - `ask_gpt()`, `ask_agent()`, `list_agents()`

2. **Capability proxying**
   - Claude's tools exposed to spoke agents
   - Bidirectional tool access

3. **Registry pattern**
   - Service discovery
   - Health checking
   - Capability enumeration

---

## Interaction Modes

User's proposed modes achievable via middleware controlling:

### Context Sharing Strategies

| Strategy | Description | Use Case |
|----------|-------------|----------|
| Full | Complete context passed | Deep collaboration |
| Summary | Compressed context | Token efficiency |
| Incremental | Delta updates only | Ongoing conversation |
| Partial | Relevant subset | Focused query |

### System Prompt Injection

| Mode | Prompt Style | Behavior |
|------|--------------|----------|
| Challenge | Adversarial | Find flaws, critique |
| Agree | Confirmatory | Build on, support |
| Collaborate | Cooperative | Joint problem-solving |
| Deduce | Inferential | Reason from evidence |

---

## Runtime Prompt Modification

Achievable through:

1. **Claude Code skills**
   - Automatic context injection
   - YAML/Markdown configuration

2. **OpenCode custom commands**
   - Markdown files
   - Per-command behavior

3. **Middleware injection**
   - Temporary instruction files
   - Cleanup after execution
   - Mode-specific prompt wrapping

---

## References

- MCP specification
- A2A protocol documentation
- Tavily searches (2026-01-06):
  - "CLI agent communication patterns"
  - "MCP server architecture"
  - "Claude Code extensibility"
  - "A2A protocol"
