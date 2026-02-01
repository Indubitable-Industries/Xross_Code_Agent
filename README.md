# Xross_Code_Agent

**Cross-CLI Agent Middleware** - Enabling AI coding assistants to communicate, share context, and orchestrate each other.

> **Status: RESEARCH COMPLETE → IMPLEMENTATION PHASE** - Architecture designed, feasibility proven, ready to build.

---
This project was designed to be public, along with agentic research updates - from the get-go.
Live journal, decision making, Claude's "notes" - everything.  
Structure around agents is absolutely critical to an good outcome.  
This is an example of what a decent harness help Claude/other agents do without too much handholding.
Interesting findings on the user side, other harness like structures don't perform as well as these instructions did.
Somehow, using Git, project being public and perhaps some other minor aspects has really increased it's abilities.
A paper will be produced after project v1 is completed.  Development will resume again soon (Message: Jan 31 2026)

---

## Vision

AI coding assistants (Claude Code, GPT5 Codex, OpenCode, Vibe) currently operate in isolation. Switching between them loses context, orchestrating them is impossible, and their combined potential goes untapped.

**Xross_Code_Agent** aims to be middleware that enables:
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
| Research findings | ✅ Done | `research/*/` |
| Architecture design | ✅ Done | `research/architecture/` |
| Feasibility tests | ✅ Done | F1, F3, F5, F6, F7 passed; F8 negative; F9 viable |
| P2P communication | 🔬 PoC needed | F9 long-polling pattern needs validation |
| Functional code | ❌ None | - |
| Prototype | ❌ None | - |

### Explore the Research

| Want to... | Go here |
|------------|---------|
| 📰 **Follow the journey** | [`research/journal/`](research/journal/) - Narrative history of discoveries, decisions, dead ends |
| 💡 **Review feature ideas** | [`research/features/`](research/features/) - Proposed capabilities (F1 Newsreel, F2 P2P, F9 Long-polling) |
| 🏗️ **Understand the architecture** | [`research/architecture/`](research/architecture/) - System design, topology, feature specs |
| 🔍 **See platform research** | [`research/codex/`](research/codex/) / [`research/opencode/`](research/opencode/) - CLI capabilities analysis |
| 🗺️ **Survey the landscape** | [`research/landscape/`](research/landscape/) - Protocols, patterns, P2P communication (L5) |
| 🧪 **Feasibility tests** | [`research/feasibility/`](research/feasibility/) - F8 notification tests (negative result) |
| 📋 **Track progress** | [`research/TRACKER.md`](research/TRACKER.md) - Master research tracker with all links |

### What's Documented

The `claudedocs/arch-design/` folder contains workflow guides for AI agents working on this project:

- **BaseResearchInstructions.md** - Tool usage (Tavily, Context7, Morph, Serena, Sequential Thinking)
- **TODOWRITECREATION.md** - Task management and tracking conventions
- **TROUBLESHOOTING_STEP_GUIDE.md** - Systematic investigation workflow
- **ISSUE_FIXING_STEP_GUIDE.md** - Implementation, testing, and fix iteration rules

These exist because this project will largely be built *by* AI agents, and they need clear operating procedures.

---

## Research Questions

### Feasibility - ANSWERED ✅
- [x] Can CLI agents communicate bidirectionally? **YES** - Structured JSON responses work (F3)
- [x] What sandbox restrictions does Codex CLI impose? **Network blocked by default** - See [P1](research/codex/P1_sandbox_restrictions.md)
- [x] Is OpenCode a viable alternative harness for GPT-5? **YES** - 75+ providers, HTTP API, no sandbox (F1, F5, F6)
- [x] Do existing tools already solve this? **NO** - Niche validated, 25+ projects surveyed (L1)
- [x] Can CLI agents receive push notifications? **NO** - See [F8](research/feasibility/F8_notification_feasibility.md)
- [x] Is there an alternative to push/poll? **YES** - Long-polling keep-alive pattern viable - See [F9](research/features/F9_long_polling_keepalive.md)

### Architecture - DECIDED ✅
- [x] MCP server? Separate service? Plugin system? **MCP middleware server** - See [A1](research/architecture/A1_mcp_middleware.md)
- [x] What protocol for agent-to-agent messages? **MCP + HTTP** - See [L2](research/landscape/L2_protocols_and_patterns.md)
- [x] How to share context without overwhelming token limits? **Compression strategies designed** - See [A3](research/architecture/A3_feature_design.md)
- [x] How to handle prompt injection securely? **XML delimiter framing** - See [A3](research/architecture/A3_feature_design.md)

### Sub-Agent Control - TESTED ✅
- [x] Can we spawn Codex/OpenCode as subprocess from Claude Code? **YES** - OpenCode works, Codex abandoned (F1)
- [x] Bidirectional? **YES via capability proxying** - See [A1](research/architecture/A1_mcp_middleware.md)
- [ ] How to modify runtime configuration and auto-revert? (Implementation phase)

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
│   ├── HARNESS.md           # Operational documentation + known issues
│   ├── journal/             # 📰 Narrative research history
│   ├── features/            # 💡 Feature ideas (F1, F2, F9)
│   ├── feasibility/         # 🧪 Feasibility tests (F8)
│   ├── architecture/        # 🏗️ System design documents
│   ├── landscape/           # 🗺️ Protocols, patterns, P2P (L5)
│   ├── codex/               # Codex CLI research (abandoned)
│   └── opencode/            # OpenCode research (selected)
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
| 2026-01-07 | **D1: Model A (Invisible Subprocess)** | Simpler UX, results inline, defer visible windows |
| 2026-01-07 | **D2: Hub-Spoke Architecture** | Claude Code orchestrates, extensible to N agents |
| 2026-01-07 | **D3: OpenCode over Codex** | Avoids sandbox complexity, 75+ providers |
| 2026-01-08 | **D4: Push/Poll abandoned** | CLI agents can't receive push; polling requires daemon (F8) |
| 2026-01-08 | **D5: Long-polling keep-alive** | Child agents wait in open tool calls; MCP SSE + progress notifications (F9) |

---

## Next Steps

1. ~~Landscape survey~~ - ✅ Done (L1, L1a, L5)
2. ~~Codex sandbox audit~~ - ✅ Done → Decided to use OpenCode instead
3. ~~OpenCode capability review~~ - ✅ Done → HTTP API, multi-model confirmed
4. ~~Architecture decision~~ - ✅ Done → MCP middleware, hub-spoke
5. ~~P2P communication feasibility~~ - ✅ Done → Push/poll fail, long-polling viable (F8, F9)

**Current Phase: PoC Validation**
1. **F9 PoC** - Build test MCP server with SSE `register_and_wait()` tool
2. Validate Claude Code behavior with long-running tool calls
3. Measure token usage of heartbeat loop
4. Test user interruptibility during wait

**After PoC: Implementation**
1. Build middleware MCP server skeleton
2. Port logging system from TelemetryManager
3. Implement basic `ask_agent()` tool
4. Implement `register_and_wait()` for P2P messaging

---

## License

MIT - See [LICENSE](LICENSE)

---

*This project is maintained by [Indubitable Industries](https://github.com/Indubitable-Industries)*
