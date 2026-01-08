# Discovery Research Findings

**Task ID**: Discovery (Pre-L1)
**Started**: 2026-01-06
**Status**: COMPLETE

---

## Overview

This document summarizes the initial discovery research for x_agent_code. Detailed findings have been split into topic-specific documents.

## Document Index

| Topic | Document | Summary |
|-------|----------|---------|
| Codex sandbox | [P1_sandbox_restrictions.md](../codex/P1_sandbox_restrictions.md) | Three-tier sandbox, network blocked by default |
| OpenCode capabilities | [P2_capabilities.md](../opencode/P2_capabilities.md) | HTTP API, multi-model support, feasibility tests |
| MCP middleware | [A1_mcp_middleware.md](../architecture/A1_mcp_middleware.md) | Hub-spoke design, tool exposure pattern |
| System topology | [A2_system_topology.md](../architecture/A2_system_topology.md) | Full architecture diagrams, data flows |
| Feature design | [A3_feature_design.md](../architecture/A3_feature_design.md) | Modes, pipelines, observability features |
| Protocols | [L2_protocols_and_patterns.md](L2_protocols_and_patterns.md) | MCP, A2A, CLI patterns |

---

## Key Conclusions

### Feasibility Assessment

**x_agent_code is FEASIBLE** with the following architecture:

1. **MCP middleware server** running locally that provides:
   - Agent registry (discover available agents)
   - Message routing (agent A → middleware → agent B)
   - Context sharing (shared workspace, session state)
   - Capability negotiation

2. **Claude Code** as primary agent via native MCP support (5/5 rating)

3. **OpenCode** as GPT-5 harness instead of Codex (avoids sandbox complexity)

4. **Interaction modes** implemented as prompt templates + context strategies

5. **File-based fallback** for maximum compatibility

### Key Risks

1. Codex sandbox may block even localhost - needs testing
2. A2A not production-ready - don't depend on it
3. Token limits for context sharing - need compression strategy
4. Prompt injection security between agents
5. Different CLI lifecycle models (spawning vs persistent)

---

## Decisions Made

| ID | Decision | Choice | Rationale |
|----|----------|--------|-----------|
| D1 | Interaction Model | Model A (Invisible Subprocess) | Simpler, user sees inline results |
| D2 | Architecture | Hub-Spoke | Claude Code orchestrates, extensible to N agents |
| D3 | GPT-5 Harness | OpenCode | Avoids Codex sandbox complexity |

---

## Feasibility Test Results

| Test | Status | Summary |
|------|--------|---------|
| F1: Subprocess spawning | PASSED | `opencode run` works from Claude Code |
| F2: Codex spawning | ABANDONED | Using OpenCode instead |
| F3: Bidirectional comms | PASSED | Structured JSON responses work |
| F4: Context limits | NOT_STARTED | Deferred |
| F5: Multi-model | PASSED | GPT-5, Grok-4-fast confirmed |
| F6: HTTP API model select | PASSED | Single serve, multi-model via API |

---

## Research Methods

### Tavily Searches (2026-01-06)

- "Codex CLI sandbox restrictions"
- "CLI agent communication patterns"
- "MCP server architecture"
- "Claude Code extensibility"
- "OpenCode CLI"
- "A2A protocol"

### Hands-on Testing (2026-01-07)

- Subprocess spawning verification
- HTTP API endpoint testing
- Multi-model routing confirmation

---

## Next Steps

See [TRACKER.md](../TRACKER.md) for current research priorities.

**Immediate**:
1. Begin middleware implementation
2. Port logging system from TelemetryManager
3. Implement basic `ask_agent()` tool

---

## References

- Detailed research in linked documents above
- Session logs in [TRACKER.md](../TRACKER.md)
