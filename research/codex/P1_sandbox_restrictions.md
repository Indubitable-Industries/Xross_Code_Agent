# P1: Codex CLI Sandbox Restrictions

**Research ID**: P1
**Status**: COMPLETE
**Source**: Discovery research (2026-01-06)

---

## Overview

Codex CLI implements a three-tier sandbox model that significantly impacts cross-agent communication feasibility.

## Sandbox Tiers

| Tier | Name | Network | Filesystem | Use Case |
|------|------|---------|------------|----------|
| 1 | `read-only` | Blocked | Read only | Safe exploration |
| 2 | `workspace-write` | Blocked | Workspace write | Normal development |
| 3 | `danger-full-access` | Allowed | Full access | Requires explicit opt-in |

## Implementation Details

### Linux
- **Landlock LSM**: Filesystem access control
- **seccomp BPF filters**: System call filtering

### macOS
- **Seatbelt framework**: Application sandboxing

### Windows
- **Status**: Experimental support only

## Network Restrictions

Network access is blocked by default even in `workspace-write` mode. This presents a significant barrier for cross-agent communication.

### Available Configuration Options

| Option | Description |
|--------|-------------|
| Domain whitelisting | Allow specific domains (e.g., localhost:PORT) |
| HTTP method filtering | Available for cloud environments |
| Execution policy rules | Pattern matching to allow/prompt/forbid commands |

## Impact Assessment for x_agent_code

**Challenge**: Any cross-agent communication requiring network would need:
1. `danger-full-access` mode (security reduction), OR
2. Explicit network whitelisting for localhost:PORT

**Users must consciously reduce security to enable inter-agent communication.**

## Workarounds

### Option 1: Domain Whitelisting
Configure Codex to allow `localhost:3001` (middleware port).

### Option 2: Execution Policy Rules
Use pattern matching to allow specific inter-agent commands.

### Option 3: File-Based IPC
Filesystem access is allowed in `workspace-write` mode - could use file-based message passing as fallback.

## Decision

**DECIDED**: Use OpenCode instead of Codex as GPT-5 harness to avoid sandbox complexity.

See [OpenCode Capabilities](../opencode/P2_capabilities.md) for alternative approach.

---

## References

- Codex CLI documentation
- Tavily search: "Codex CLI sandbox restrictions" (2026-01-06)
