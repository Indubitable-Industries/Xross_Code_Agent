# Journal: Research Restructure

**Date**: 2026-01-08
**Session**: Documentation Cleanup
**Duration**: ~30 minutes

---

## The Problem

Reviewed project state with user. Found a significant issue:

**Designed Structure (from README):**
```
research/
├── TRACKER.md           # Master tracker
├── landscape/           # Existing tools survey
├── codex/               # Codex CLI research
├── opencode/            # OpenCode research
└── architecture/        # Design options
```

**Actual State:**
```
research/
├── TRACKER.md
├── HARNESS.md           # ✅ Good
├── landscape/
│   └── discovery_findings.md   # ← 852 lines, EVERYTHING here
├── codex/
│   └── .gitkeep         # ❌ Empty
├── opencode/
│   └── .gitkeep         # ❌ Empty
└── architecture/
    └── .gitkeep         # ❌ Empty
```

The monolithic `discovery_findings.md` contained:
- Codex sandbox analysis (belongs in `codex/`)
- OpenCode capabilities and API (belongs in `opencode/`)
- MCP middleware design (belongs in `architecture/`)
- System topology diagrams (belongs in `architecture/`)
- A2A/MCP protocol patterns (belongs in `landscape/`)
- Feature brainstorm (belongs in `architecture/`)
- Feasibility test results (mixed)

**Why this matters:** The "research publicly" goal means someone browsing the repo should be able to navigate to specific findings by category. An 852-line dump defeats that purpose.

---

## The Solution

Split the monolith into topic-specific documents following the designed structure.

### Split Plan

| Content | New Location | New File |
|---------|--------------|----------|
| Codex sandbox restrictions | `research/codex/` | `P1_sandbox_restrictions.md` |
| OpenCode capabilities, modes, HTTP API | `research/opencode/` | `P2_capabilities.md` |
| MCP middleware design, hub-spoke | `research/architecture/` | `A1_mcp_middleware.md` |
| System topology diagrams | `research/architecture/` | `A2_system_topology.md` |
| Feature brainstorm, priorities | `research/architecture/` | `A3_feature_design.md` |
| A2A protocol, CLI patterns | `research/landscape/` | `L2_protocols_and_patterns.md` |
| Original file | `research/landscape/` | Reduced to synthesis-only |

### Execution

Created 6 new documents:
1. `codex/P1_sandbox_restrictions.md` - Three-tier sandbox analysis, workarounds, decision to use OpenCode instead
2. `opencode/P2_capabilities.md` - HTTP API, invocation modes, all feasibility test results
3. `architecture/A1_mcp_middleware.md` - Hub-spoke design, capability proxying, request flows
4. `architecture/A2_system_topology.md` - Full system diagrams, component breakdown, data flows
5. `architecture/A3_feature_design.md` - All feature categories, priority matrix, implementation details
6. `landscape/L2_protocols_and_patterns.md` - MCP/A2A protocols, CLI patterns, interaction modes

Reduced `discovery_findings.md`:
- 852 lines → 113 lines (87% reduction)
- Now contains: overview, document index, key conclusions, decisions summary, feasibility results summary
- Acts as synthesis + navigation hub to detailed docs

Updated `TRACKER.md`:
- Added links to all new documents
- Updated research topic statuses
- Added session log entry

Cleanup:
- Removed `.gitkeep` files from `codex/`, `opencode/`, `architecture/` (now have real content)

---

## New Problem Identified

User raised a valid concern: If we commit now, the research *process* is invisible. Git history technically has it, but nobody browses `git log` to understand a project's evolution.

The journey of discovery - what we searched, what failed, why we pivoted - is valuable context that gets lost in polished final documents.

**Solution:** Create `research/journal/` folder with dated narrative entries.

This is that journal.

---

## Final Structure

```
research/
├── TRACKER.md                           # Master tracker with all links
├── HARNESS.md                           # Operational doc
├── journal/                             # NEW - Process history
│   ├── 2026-01-06_initial-discovery.md
│   ├── 2026-01-07_architecture-decisions.md
│   └── 2026-01-08_restructure.md
├── landscape/
│   ├── discovery_findings.md            # Synthesis only (113 lines)
│   └── L2_protocols_and_patterns.md     # Protocols doc
├── codex/
│   └── P1_sandbox_restrictions.md       # Sandbox analysis
├── opencode/
│   └── P2_capabilities.md               # Capabilities + tests
└── architecture/
    ├── A1_mcp_middleware.md             # Middleware design
    ├── A2_system_topology.md            # System diagrams
    └── A3_feature_design.md             # Feature design
```

---

## Lessons Learned

1. **Structure matters from day one.** It's easier to maintain organization than to retrofit it.

2. **Monolithic dumps are tempting but harmful.** Fast to write, hard to navigate.

3. **Process is as valuable as results.** For a "research publicly" project, showing the journey matters.

4. **Journal > Git log.** Git history is complete but invisible. Narrative journals are browsable.

---

## Next Steps

1. Update README to mention journal folder
2. Commit all restructured research
3. Begin implementation phase (middleware skeleton)

---

## Mood Check

Satisfied. The research folder now reflects what was actually researched:
- Codex → evaluated, rejected
- OpenCode → evaluated, selected, tested
- Architecture → designed, documented
- Features → brainstormed, prioritized

And now there's a journal showing *why* we made those choices.

Ready to build.
