# Research Tracker

**Project**: x_agent_code - Cross-CLI Agent Middleware
**Started**: 2026-01-06
**Last Updated**: 2026-01-06

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
| L2 | MCP multi-agent patterns | `NOT_STARTED` | - | How others extend MCP |
| L3 | CLI agent orchestration tools | `NOT_STARTED` | - | Non-UI orchestration |
| L4 | Local LLM middleware options | `NOT_STARTED` | - | Localhost routing assistants |

### Phase 2: Platform Capabilities

| ID | Topic | Status | Findings | Notes |
|----|-------|--------|----------|-------|
| P1 | Codex CLI sandbox restrictions | `NOT_STARTED` | - | What's blocked? |
| P2 | OpenCode capabilities & API | `NOT_STARTED` | - | GPT-5 alternative harness |
| P3 | Claude Code extensibility | `NOT_STARTED` | - | MCP, hooks, skills |
| P4 | Vibe integration options | `NOT_STARTED` | - | Lower priority |

### Phase 3: Architecture Options

| ID | Topic | Status | Findings | Notes |
|----|-------|--------|----------|-------|
| A1 | MCP server approach | `NOT_STARTED` | - | Native integration |
| A2 | Standalone service approach | `NOT_STARTED` | - | Decoupled middleware |
| A3 | Plugin/skill hybrid | `NOT_STARTED` | - | Per-tool plugins + shared service |
| A4 | Protocol design | `NOT_STARTED` | - | Message format, context sharing |

### Phase 4: Feasibility Tests

| ID | Topic | Status | Findings | Notes |
|----|-------|--------|----------|-------|
| F1 | Claude Code spawning subprocess | `NOT_STARTED` | - | Can we launch other CLIs? |
| F2 | Codex subprocess spawning | `NOT_STARTED` | - | Sandbox may block |
| F3 | Bidirectional communication test | `NOT_STARTED` | - | Both directions work? |
| F4 | Context size limits | `NOT_STARTED` | - | How much can we share? |

---

## Findings Index

*Links to detailed research documents*

### Landscape (`research/landscape/`)
- *(none yet)*

### Codex (`research/codex/`)
- *(none yet)*

### OpenCode (`research/opencode/`)
- *(none yet)*

### Architecture (`research/architecture/`)
- *(none yet)*

---

## Decision Queue

*Research that requires user decision before proceeding*

| ID | Question | Options | Decision | Date |
|----|----------|---------|----------|------|
| - | - | - | - | - |

---

## Session Log

*Brief notes on research sessions*

| Date | Session | Work Done | Next |
|------|---------|-----------|------|
| 2026-01-06 | Setup | Created project structure, arch-design docs, tracker | Begin L1: GitHub survey |

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
