# Research Tracker

**Project**: x_agent_code - Cross-CLI Agent Middleware
**Started**: 2026-01-06
**Last Updated**: 2026-01-08 (L1a deep-dive complete)

---

## Status Legend

| Status | Meaning |
|--------|---------|
| `NOT_STARTED` | Identified but no work done |
| `IN_PROGRESS` | Active research |
| `BLOCKED` | Waiting on dependency or decision |
| `COMPLETE` | Findings documented |
| `ABANDONED` | Determined not worth pursuing |

---

## Research Topics

### Phase 1: Landscape Survey

| ID | Topic | Status | Findings | Notes |
|----|-------|--------|----------|-------|
| L1 | Existing cross-agent GitHub projects | `COMPLETE` | [L1_github_survey.md](landscape/L1_github_survey.md) | 25+ projects surveyed, niche validated |
| L1a | Deep-dive: claude-code-mcp & oh-my-opencode | `COMPLETE` | [L1a_deep_dive_key_projects.md](landscape/L1a_deep_dive_key_projects.md) | Patterns adopted, hybrid approach recommended |
| L2 | MCP/A2A protocols & CLI patterns | `COMPLETE` | [L2_protocols_and_patterns.md](landscape/L2_protocols_and_patterns.md) | MCP foundation, A2A patterns |
| L3 | CLI agent orchestration tools | `NOT_STARTED` | - | Non-UI orchestration |
| L4 | Local LLM middleware options | `NOT_STARTED` | - | Localhost routing assistants |
| L5 | P2P agent communication patterns | `COMPLETE` | [L5_p2p_patterns.md](landscape/L5_p2p_patterns.md) | SQLite + MCP notifications, Agent Cards pattern |

### Phase 2: Platform Capabilities

| ID | Topic | Status | Findings | Notes |
|----|-------|--------|----------|-------|
| P1 | Codex CLI sandbox restrictions | `COMPLETE` | [P1_sandbox_restrictions.md](codex/P1_sandbox_restrictions.md) | Network blocked, workarounds documented |
| P2 | OpenCode capabilities & API | `COMPLETE` | [P2_capabilities.md](opencode/P2_capabilities.md) | HTTP API, multi-model confirmed |
| P3 | Claude Code extensibility | `COMPLETE` | [L2_protocols_and_patterns.md](landscape/L2_protocols_and_patterns.md) | MCP, hooks, skills |
| P4 | Vibe integration options | `NOT_STARTED` | - | Lower priority |

### Phase 3: Architecture Options

| ID | Topic | Status | Findings | Notes |
|----|-------|--------|----------|-------|
| A1 | MCP middleware design | `COMPLETE` | [A1_mcp_middleware.md](architecture/A1_mcp_middleware.md) | Hub-spoke, tool exposure |
| A2 | System topology | `COMPLETE` | [A2_system_topology.md](architecture/A2_system_topology.md) | Full architecture diagrams |
| A3 | Feature design | `COMPLETE` | [A3_feature_design.md](architecture/A3_feature_design.md) | Modes, pipelines, observability |
| A4 | Protocol design | `COMPLETE` | [L2_protocols_and_patterns.md](landscape/L2_protocols_and_patterns.md) | Message format, context sharing |

### Phase 4: Feasibility Tests

| ID | Topic | Status | Findings | Notes |
|----|-------|--------|----------|-------|
| F1 | Claude Code spawning subprocess | `COMPLETE` | PASSED | `opencode run` works from Claude Code |
| F2 | Codex subprocess spawning | `ABANDONED` | - | Using OpenCode instead |
| F3 | Bidirectional communication test | `COMPLETE` | PASSED | Context sent, structured JSON returned |
| F4 | Context size limits | `NOT_STARTED` | - | How much can we share? |
| F5 | Multi-model support | `COMPLETE` | PASSED | GPT-5, Grok-4-fast confirmed |
| F6 | HTTP API per-request model | `COMPLETE` | PASSED | Single serve, multi-model via API |
| F7 | OpenCode CLI invocation from Claude | `COMPLETE` | [F7_invocation_tests.md](opencode/F7_invocation_tests.md) | `opencode run` works, model selection works |
| F8 | Push notification feasibility | `COMPLETE` | [F8_notification_feasibility.md](feasibility/F8_notification_feasibility.md) | NEGATIVE - push/poll don't work for CLI agents |
| F9 | Long-polling keep-alive pattern | `TESTING` | [F9_long_polling_keepalive.md](features/F9_long_polling_keepalive.md) | Research done, PoC built, [test harness](feasibility/F9_poc_test_harness.md) ready |

---

## Research Journal

*Narrative history of the research process - the journey, not just the destination*

| Date | Entry | Summary |
|------|-------|---------|
| 2026-01-06 | [Initial Discovery](journal/2026-01-06_initial-discovery.md) | Tavily searches, Codex sandbox problem, OpenCode alternative discovered |
| 2026-01-07 | [Architecture Decisions](journal/2026-01-07_architecture-decisions.md) | D1/D2/D3 decisions, feasibility tests, feature brainstorm |
| 2026-01-08 | [Restructure](journal/2026-01-08_restructure.md) | Split monolith, created journal system |
| 2026-01-08 | [GitHub Survey](journal/2026-01-08_github-survey.md) | L1 complete - 25+ projects, niche validated |
| 2026-01-08 | [Deep-Dive Key Projects](journal/2026-01-08_deep-dive.md) | L1a complete - patterns extracted, hybrid approach recommended |

---

## Findings Index

*Links to detailed research documents*

### Landscape (`research/landscape/`)
- [Discovery Findings](landscape/discovery_findings.md) - Overview and synthesis of initial research
- [L1: GitHub Survey](landscape/L1_github_survey.md) - 25+ projects surveyed, niche validated
- [L1a: Deep-Dive Key Projects](landscape/L1a_deep_dive_key_projects.md) - claude-code-mcp & oh-my-opencode analysis
- [L2: Protocols and Patterns](landscape/L2_protocols_and_patterns.md) - MCP, A2A, CLI patterns

### Codex (`research/codex/`)
- [P1: Sandbox Restrictions](codex/P1_sandbox_restrictions.md) - Three-tier sandbox analysis

### OpenCode (`research/opencode/`)
- [P2: Capabilities](opencode/P2_capabilities.md) - HTTP API, modes, feasibility tests
- [F7: Invocation Tests](opencode/F7_invocation_tests.md) - CLI invocation from Claude Code validated

### Architecture (`research/architecture/`)
- [A1: MCP Middleware](architecture/A1_mcp_middleware.md) - Hub-spoke design, capability proxying
- [A2: System Topology](architecture/A2_system_topology.md) - Full architecture diagrams
- [A3: Feature Design](architecture/A3_feature_design.md) - Modes, pipelines, observability

### Feasibility Tests (`research/feasibility/`)
- [F8: Notification Feasibility](feasibility/F8_notification_feasibility.md) - Push notification support for Claude Code, Codex, OpenCode
- [F9: PoC Test Harness](feasibility/F9_poc_test_harness.md) - Long-polling validation tests

### Feature Ideas (`research/features/`)
- [F1: Newsreel Memory](features/F1_newsreel_memory.md) - Grok-4-fast powered activity narrative
- [F2: Peer Agent Messaging](features/F2_peer_agent_messaging.md) - Live P2P communication between concurrent agent sessions
- [F9: Long-Polling Keep-Alive](features/F9_long_polling_keepalive.md) - Child agents wait in open tool calls for work

---

## Decision Queue

*Research that requires user decision before proceeding*

| ID | Question | Options | Decision | Date |
|----|----------|---------|----------|------|
| D1 | Interaction model | Model A (invisible) vs Model B (visible) | Model A | 2026-01-07 |
| D2 | Architecture | Hub-spoke vs peer-to-peer | Hub-spoke | 2026-01-07 |
| D3 | GPT-5 harness | Codex vs OpenCode | OpenCode | 2026-01-07 |
| D4 | Vibe scope | Initial scope vs deferred | DEFERRED | 2026-01-07 |
| D5 | P2P messaging | Add peer messaging to hub-spoke? | YES - F2 proposed | 2026-01-08 |

---

## Session Log

*Brief notes on research sessions*

| Date | Session | Work Done | Next |
|------|---------|-----------|------|
| 2026-01-06 | Setup | Created project structure, arch-design docs, tracker | Begin L1: GitHub survey |
| 2026-01-06 | Discovery | Ran 6 Tavily searches, synthesized findings on Codex sandbox, MCP, OpenCode, A2A | User decisions on D1, D2 |
| 2026-01-07 | Architecture | Model A selected, hub-spoke design, OpenCode invocation modes documented | Feasibility tests |
| 2026-01-07 | Feasibility | F1, F3, F5, F6 passed - subprocess spawn, multi-model, HTTP API confirmed | Build middleware |
| 2026-01-07 | Feature Design | Feature brainstorm with user decisions, LLM Context Arena modes reviewed | Resolve open questions |
| 2026-01-08 | Restructure | Split monolithic discovery_findings.md into categorized documents | Journal setup |
| 2026-01-08 | Journal | Created research/journal/ with backfilled narrative entries | L1 survey |
| 2026-01-08 | L1 Survey | GitHub landscape survey - 25+ projects, niche validated, key projects identified | Deep-dive phase |
| 2026-01-08 | L1a Deep-Dive | Analyzed claude-code-mcp and oh-my-opencode in detail, documented patterns to adopt | Implementation phase |
| 2026-01-08 | F7 Testing | Validated `opencode run` CLI invocation with multiple models (GPT-5, Grok) | Ready to build |
| 2026-01-08 | L5 Research | P2P agent communication patterns - SQLite + MCP notifications architecture | Implementation ready |
| 2026-01-08 | F8 Feasibility | Push notification tests - NEGATIVE, push/poll don't work for CLI agents | F9 proposed |
| 2026-01-08 | F9 Proposed | Long-polling keep-alive pattern - child agents wait in open tool calls | Needs research |
| 2026-01-08 | F9 Research | MCP spec analysis - SSE streaming, progress notifications, timeout config | VIABLE - needs PoC |
| 2026-01-08 | F9 PoC | Built MCP server with register_and_wait, heartbeats, message delivery | Ready to test |
| 2026-01-08 | F9 Harness | Created formal test harness with 7 test cases | Testing phase |

---

## How to Use This Tracker

### Starting Research
1. Pick a `NOT_STARTED` topic
2. Update status to `IN_PROGRESS`
3. Create findings doc in appropriate subfolder
4. Follow `arch-design/TROUBLESHOOTING_STEP_GUIDE.md` workflow

### Completing Research
1. Finalize findings document
2. Update status to `COMPLETE`
3. Add link to Findings Index
4. Log session in Session Log
5. Commit changes

### Picking Up Mid-Session
1. Check Session Log for last state
2. Find `IN_PROGRESS` topics
3. Read linked findings doc
4. Continue from documented point
