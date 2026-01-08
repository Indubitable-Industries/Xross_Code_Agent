# Journal: Initial Discovery

**Date**: 2026-01-06
**Session**: Discovery (Pre-L1)
**Duration**: ~2 hours

---

## Starting Point

Project concept: Build middleware that lets Claude Code talk to other AI agents (GPT-5 via some harness, potentially others). User wants different "modes" - challenge, agree, collaborate, deduce - where agents interact with different dynamics.

**Key questions going in:**
1. Can Codex CLI be used as a GPT-5 harness? What are the restrictions?
2. How do CLI agents communicate? Is there a standard?
3. What extensibility does Claude Code offer?
4. Are there existing solutions we should know about?

---

## Tavily Search Results

### Search 1: "Codex CLI sandbox restrictions"

**Raw findings:**
- Three-tier sandbox: `read-only`, `workspace-write`, `danger-full-access`
- Network access blocked by default even in workspace-write mode
- Linux uses Landlock LSM + seccomp BPF filters
- macOS uses Seatbelt framework
- Windows support experimental
- Domain whitelisting available for cloud environments
- Execution policy rules support pattern matching

**Reaction:** 😬 This is a problem. Network blocked by default means inter-agent HTTP communication would require `danger-full-access` or explicit whitelisting. Users would have to consciously reduce security.

### Search 2: "CLI agent communication patterns"

**Raw findings:**
- MCP operates through stdio (local) and HTTP (remote) transports
- Stdio restricts stdout to MCP messages, logging to stderr
- `claude mcp serve` exposes Claude Code tools to other agents
- Multi-agent requires HTTP transport since stdio limited to single subprocess
- Claude Agent SDK can wrap stdio→HTTP for bridging

**Reaction:** 💡 Wait - Claude Code can act as an MCP *server*? That's huge. We could build a central MCP server that all agents connect to.

### Search 3: "MCP server architecture"

**Raw findings:**
- Each MCP server registers in service registry
- Scope configuration: project-level, local user-specific, global machine-wide
- Host application instantiates dedicated client instances per server
- JSON-RPC message format over newline-delimited streams

**Reaction:** This is well-structured. Registry pattern, scoped configuration, clean protocol. Good foundation.

### Search 4: "Claude Code extensibility"

**Raw findings:**
- Custom hooks for workflow customization
- Skills system: YAML/Markdown files in `~/.claude/skills/` or `.claude/skills/`
- MCP support rated 5/5 vs Codex 3/5
- Sub-agents capability for spawning specialized workers
- CCC (custom launcher) supports agents, MCPs, plugins with FastMCP

**Reaction:** Claude Code is *very* extensible. 5/5 MCP support. This should be the hub.

### Search 5: "OpenCode CLI"

**Raw findings:**
- Open source terminal assistant, 75+ providers
- Plugin hook system
- TUI Commands (instant) vs Slash Commands (agent-driven)
- Multi-session: run multiple agents in parallel on same project
- Custom commands via Markdown files
- "Oh My OpenCode" has Claude Code compatibility layer
- Privacy-first, no code storage

**Reaction:** 🎯 This could be the GPT-5 harness instead of Codex. Open source, 75+ providers, no restrictive sandbox, multi-session support. Much simpler path.

### Search 6: "A2A protocol"

**Raw findings:**
- Google's open standard for agent interoperability
- Donated to Linux Foundation June 2025, 100+ company backing
- Client agent → Remote agent task delegation
- Agents publicize capabilities via `agent_card`/`agent.json`
- MCP = tools/context access, A2A = agent-to-agent communication
- ADK supports `to_a2a()` conversion
- Production-ready version expected end 2025

**Reaction:** Interesting but not ready. We shouldn't depend on it, but we can steal design patterns: capability cards, client→remote delegation, discovery.

---

## Synthesis & Realizations

### The Codex Problem

Codex's security model works against us. Network blocked by default is a dealbreaker for HTTP-based inter-agent communication. Workarounds exist (domain whitelisting, file-based IPC) but add friction.

**Dead end noted:** Codex as GPT-5 harness is possible but painful.

### The OpenCode Alternative

OpenCode solves the Codex problem:
- No restrictive sandbox
- 75+ providers (including GPT-5 via OpenRouter)
- Open source, hackable
- Multi-session support native

**Decision seed planted:** OpenCode > Codex for this use case.

### MCP as Foundation

MCP provides vertical integration (agent↔tools). The key insight: Claude Code can *serve* MCP, not just consume it. Architecture pattern emerging:

```
Claude Code (hub, MCP server)
    ↓
x_agent_code middleware (MCP client to Claude, HTTP to spokes)
    ↓
OpenCode/GPT-5, other agents (spokes)
```

### Interaction Modes are Achievable

User's proposed modes (challenge, agree, collaborate, deduce) map to:
- **Context sharing strategies**: full, summary, incremental, partial
- **System prompt injection**: adversarial, confirmatory, collaborative, inferential

This is just prompt engineering + context management. Not technically hard.

---

## Open Questions (for next session)

1. How does OpenCode operate when spawned as subprocess? Headless mode?
2. What's the exact invocation pattern?
3. Can we do per-request model selection?
4. Should architecture be hub-spoke or peer-to-peer?
5. Model A (invisible subprocess) vs Model B (visible parallel terminals)?

---

## Artifacts Created

- `research/TRACKER.md` - Research tracking structure
- `research/landscape/discovery_findings.md` - Raw findings dump (later restructured)

---

## Mood Check

Optimistic. The pieces exist:
- Claude Code is extensible ✓
- MCP provides the protocol ✓
- OpenCode solves the Codex sandbox problem ✓
- Interaction modes are just prompt engineering ✓

Main risk: Haven't actually *tested* anything yet. All theoretical.
