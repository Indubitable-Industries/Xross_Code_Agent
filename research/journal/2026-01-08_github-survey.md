# Journal: GitHub Landscape Survey

**Date**: 2026-01-08
**Session**: L1 Research
**Duration**: ~45 minutes

---

## Starting Point

Finally doing the GitHub survey we deferred. Now that we have architecture decisions (hub-spoke, OpenCode, interaction modes), we know exactly what to look for:
- MCP multi-agent patterns
- Claude Code extensions
- OpenCode plugins
- Cross-agent communication tools

**Key question**: Is someone already building what we're building?

---

## Search Strategy

Ran 5 parallel searches:
1. "MCP multi-agent orchestration GitHub"
2. "Claude Code extension multi-agent"
3. "OpenCode plugin integration"
4. "AI agent middleware CLI orchestration"
5. "cross-agent communication LLM tools"

---

## The Finds

### 🎯 Bull's-eye: oh-my-opencode-CLI

**Reaction**: Wait, this exists?!

```
Kevinjulu/oh-my-opencode-CLI
- "#1 OpenCode Plugin"
- ASYNC SUBAGENTS (like Claude Code)
- **Claude Code Compatible Layer**
- Curated MCPs
```

This is directly relevant. Someone already built a Claude Code compatibility layer for OpenCode. Need to study this immediately.

### 🎯 Bull's-eye: claude-code-mcp

```
steipete/claude-code-mcp
- Claude Code as one-shot MCP server
- "Agent in your agent" pattern
- Permissions bypassed automatically
```

This is our hub pattern! Claude Code as MCP server, exactly what we designed.

### Thriving Ecosystem

The MCP multi-agent space is HOT:
- **mcp-agent** (lastmile-ai) - workflow patterns, Temporal engine
- **claude-flow** (ruvnet) - 87 MCP tools, enterprise-grade
- **fast-agent** (evalstate) - routing, parallelization, orchestrator-workers
- **Swarms** (kyegomez) - enterprise multi-agent framework

Also found big players:
- **CrewAI** - 100k+ developers, enterprise-ready
- **Microsoft Agent Framework** - graph workflows, middleware system
- **AWS agent-squad** - intent classification, universal deployment

### Research Corner

Interesting academic/research projects:
- **Langroid** (CMU/UW-Madison) - message exchange, MCP adapter
- **MassGen** - Berkeley Agentic AI Summit 2025
- **Multi-LLM-Agent** (X-PLUG) - small LLMs collaborating

Research papers mention "Cache-to-Cache (C2C)" for direct semantic communication between LLMs using KV-cache. Fascinating but probably not relevant to us yet.

---

## Key Realization

**Our niche is valid and unfilled.**

What exists:
- Claude-only multi-agent (claude-flow, etc.)
- Model-agnostic frameworks (CrewAI, Swarms)
- General orchestration platforms

What DOESN'T exist:
- Specific Claude Code ↔ OpenCode/GPT-5 bridge
- Interaction modes (challenge/agree/collaborate/deduce)
- User-facing simplicity ("ask GPT" just works)
- YAML pipeline config for non-developers

The closest are:
- claude-code-mcp (hub pattern)
- oh-my-opencode (spoke with Claude compat)

But nobody wired them together with interaction modes.

---

## Strategic Assessment

### Should we pivot?
**NO.** Our specific use case isn't solved.

### Should we integrate?
**YES, selectively.** Study claude-code-mcp and oh-my-opencode before building. They might be components we use or patterns we adopt.

### Should we continue?
**YES.** Architecture validated by industry patterns. Our novel contribution is clear.

---

## Projects to Deep-Dive

Before implementation, need to understand:

1. **steipete/claude-code-mcp**
   - How does one-shot work?
   - Permission bypass mechanism
   - Could we use it directly?

2. **Kevinjulu/oh-my-opencode-CLI**
   - What's in the compatibility layer?
   - Async subagent implementation
   - Could this BE our spoke?

---

## Useful Patterns (Pattern only, no clone/copy)

| Source | Pattern |
|--------|---------|
| mcp-agent | Temporal execution for pause/resume |
| claude-code-mcp | One-shot + "Boomerang pattern" for subtasks |
| oh-my-opencode | Claude compat layer architecture |
| Langroid | Message exchange, MCP tool adapter |
| agent-cli | Middleware proxy, Markdown memory |

---

## Risk Check

| Risk | Level | Why |
|------|-------|-----|
| Market | LOW | No direct competitor |
| Technical | LOW | Patterns proven, we can learn |
| Adoption | MEDIUM | Lots of options, need clear differentiator |
| Obsolescence | MEDIUM | Fast space, Anthropic/OpenAI could build this |

Mitigation: Move fast, focus on user value, keep it simple.

---

## Mood Check

Validated and energized.

The survey answered the nagging question: "Are we reinventing the wheel?" Answer: No, but we're surrounded by wheel parts. The assembly is our job.

The existence of claude-code-mcp and oh-my-opencode is actually GOOD news - it means:
1. The patterns are proven
2. There's community interest
3. We can learn from working code
4. Our integration layer is the novel part

---

## Next Steps

1. Clone and study claude-code-mcp
2. Clone and study oh-my-opencode
3. Document patterns to adopt
4. THEN start implementation

Not blocked, but informed. Better to build on proven patterns than invent from scratch.
