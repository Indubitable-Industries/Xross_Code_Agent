# x_agent_code

**Cross-CLI Agent Middleware** - Enabling AI coding assistants to communicate, share context, and orchestrate each other.

> **Status: RESEARCH PHASE** - This project contains documentation and plans, but no functional code yet.

---

## Vision

AI coding assistants (Claude Code, GPT5 Codex, OpenCode, Vibe) currently operate in isolation. Switching between them loses context, orchestrating them is impossible, and their combined potential goes untapped.

**x_agent_code** aims to be middleware that enables:
- **Cross-agent communication** - Models exchanging context and collaborating
- **Sub-agent instantiation** - Any agent spawning another as a subordinate worker
- **Runtime configuration** - Temporarily modify prompts/settings, auto-revert after execution
- **Unified context** - Share relevant information across agent boundaries

---

## Current State

### What Exists

| Component | Status | Location |
|-----------|--------|----------|
| Project structure | ✅ Done | Root |
| Agent workflow documentation | ✅ Done | `claudedocs/arch-design/` |
| Research plan | ✅ Done | `claudedocs/plans/` |
| Research tracker | ✅ Done | `research/TRACKER.md` |
| Research findings | ❌ None | `research/*/` |
| Functional code | ❌ None | - |
| Prototype | ❌ None | - |

### What's Documented

The `claudedocs/arch-design/` folder contains workflow guides for AI agents working on this project:

- **BaseResearchInstructions.md** - Tool usage (Tavily, Context7, Morph, Serena, Sequential Thinking)
- **TODOWRITECREATION.md** - Task management and tracking conventions
- **TROUBLESHOOTING_STEP_GUIDE.md** - Systematic investigation workflow
- **ISSUE_FIXING_STEP_GUIDE.md** - Implementation, testing, and fix iteration rules

These exist because this project will largely be built *by* AI agents, and they need clear operating procedures.

---

## Research Questions (Unanswered)

### Feasibility
- [ ] Can CLI agents communicate bidirectionally at all?
- [ ] What sandbox restrictions does Codex CLI impose?
- [ ] Is OpenCode a viable alternative harness for GPT-5?
- [ ] Do existing tools already solve this? (GitHub survey needed)

### Architecture
- [ ] MCP server? Separate service? Plugin system?
- [ ] What protocol for agent-to-agent messages?
- [ ] How to share context without overwhelming token limits?
- [ ] How to handle prompt injection securely?

### Sub-Agent Control
- [ ] Can we spawn Codex/OpenCode as subprocess from Claude Code?
- [ ] Bidirectional? (Claude spawns Codex, Codex spawns Claude)
- [ ] How to modify runtime configuration and auto-revert?

---

## Proposed Interaction Modes

*Theoretical - not implemented*

| Mode | Description | Use Case |
|------|-------------|----------|
| `challenge` | Adversarial review, full context | Code review, security audit |
| `agree` | Confirmatory analysis, summary context | Validation, sanity check |
| `collaborate` | Joint problem solving, incremental sharing | Complex tasks |
| `deduce` | Inference from partial context | Hypothesis testing |

---

## Tech Stack (Planned)

- **Python** - Primary language, agent orchestration
- **Rust** - Performance-critical middleware (if needed)
- **JavaScript/Node** - Integration with JS-based tools

---

## Project Structure

```
x_agent_code/
├── README.md                 # You are here
├── LICENSE                   # MIT
├── .gitignore               # Python/Rust/JS patterns
├── research/                # Research findings (public-facing)
│   ├── TRACKER.md           # Master research tracker
│   ├── landscape/           # Existing tools survey
│   ├── codex/               # Codex CLI research
│   ├── opencode/            # OpenCode research
│   └── architecture/        # Design options
└── claudedocs/
    ├── arch-design/         # Agent workflow documentation
    │   ├── BaseResearchInstructions.md
    │   ├── TODOWRITECREATION.md
    │   ├── TROUBLESHOOTING_STEP_GUIDE.md
    │   └── ISSUE_FIXING_STEP_GUIDE.md
    ├── plans/               # Research and implementation plans
    │   └── 20260106_cross_cli_agent_control.md
    ├── features/            # Feature proposals
    ├── guides/              # How-to documentation
    └── issues/              # Problem tracking
```

---

## Contributing

This project is public from day one. Contributions welcome, but note:

1. **Branch protection** - Work on feature branches, PR to main
2. **AI-assisted development** - Much of this will be built by AI agents following the `arch-design/` guides
3. **Research first** - We're in discovery phase; code comes after we know what to build

---

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-01-06 | Project created | Need cross-agent communication tooling |
| 2026-01-06 | Codex vs OpenCode threshold: 50% | If Codex sandbox adds >50% complexity, pivot to OpenCode |
| 2026-01-06 | CLI-first design | Plugin/MCP/Skill, not replacement for existing tools |

---

## Next Steps

1. **Landscape survey** - Find existing cross-agent projects on GitHub
2. **Codex sandbox audit** - Document what's blocked/restricted
3. **OpenCode capability review** - Assess as alternative GPT-5 harness
4. **Architecture decision** - MCP vs service vs plugin

---

## License

MIT - See [LICENSE](LICENSE)

---

*This project is maintained by [Indubitable Industries](https://github.com/Indubitable-Industries)*
