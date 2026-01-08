# Research Tracker

**Project**: x_agent_code - Cross-CLI Agent Middleware
**Started**: 2026-01-06
**Last Updated**: 2026-01-08 (Research restructured)

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
| L1 | Existing cross-agent GitHub projects | `NOT_STARTED` | - | Survey for prior art |
| L2 | MCP/A2A protocols & CLI patterns | `COMPLETE` | [L2_protocols_and_patterns.md](landscape/L2_protocols_and_patterns.md) | MCP foundation, A2A patterns |
| L3 | CLI agent orchestration tools | `NOT_STARTED` | - | Non-UI orchestration |
| L4 | Local LLM middleware options | `NOT_STARTED` | - | Localhost routing assistants |

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

---

## Research Journal

*Narrative history of the research process - the journey, not just the destination*

| Date | Entry | Summary |
|------|-------|---------|
| 2026-01-06 | [Initial Discovery](journal/2026-01-06_initial-discovery.md) | Tavily searches, Codex sandbox problem, OpenCode alternative discovered |
| 2026-01-07 | [Architecture Decisions](journal/2026-01-07_architecture-decisions.md) | D1/D2/D3 decisions, feasibility tests, feature brainstorm |
| 2026-01-08 | [Restructure](journal/2026-01-08_restructure.md) | Split monolith, created journal system |

---

## Findings Index

*Links to detailed research documents*

### Landscape (`research/landscape/`)
- [Discovery Findings](landscape/discovery_findings.md) - Overview and synthesis of initial research
- [L2: Protocols and Patterns](landscape/L2_protocols_and_patterns.md) - MCP, A2A, CLI patterns

### Codex (`research/codex/`)
- [P1: Sandbox Restrictions](codex/P1_sandbox_restrictions.md) - Three-tier sandbox analysis

### OpenCode (`research/opencode/`)
- [P2: Capabilities](opencode/P2_capabilities.md) - HTTP API, modes, feasibility tests

### Architecture (`research/architecture/`)
- [A1: MCP Middleware](architecture/A1_mcp_middleware.md) - Hub-spoke design, capability proxying
- [A2: System Topology](architecture/A2_system_topology.md) - Full architecture diagrams
- [A3: Feature Design](architecture/A3_feature_design.md) - Modes, pipelines, observability

### Feature Ideas (`research/features/`)
- [F1: Newsreel Memory](features/F1_newsreel_memory.md) - Grok-4-fast powered activity narrative

---

## Decision Queue

*Research that requires user decision before proceeding*

| ID | Question | Options | Decision | Date |
|----|----------|---------|----------|------|
| D1 | Interaction model | Model A (invisible) vs Model B (visible) | Model A | 2026-01-07 |
| D2 | Architecture | Hub-spoke vs peer-to-peer | Hub-spoke | 2026-01-07 |
| D3 | GPT-5 harness | Codex vs OpenCode | OpenCode | 2026-01-07 |
| D4 | Vibe scope | Initial scope vs deferred | DEFERRED | 2026-01-07 |

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
| 2026-01-08 | Journal | Created research/journal/ with backfilled narrative entries | Implementation phase |

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
