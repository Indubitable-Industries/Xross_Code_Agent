# Research Harness

**Purpose**: Operational instructions for agents executing research tasks.

> **READ THIS FIRST** before any research work. This document defines the loop.

---

## Task Format

Research tasks are defined in YAML blocks within `TASKS.yaml` (or inline in TRACKER.md):

```yaml
- id: L1
  name: "Existing cross-agent GitHub projects"
  status: NOT_STARTED
  priority: 1
  searches:
    - tool: tavily
      query: "multi-agent LLM orchestration github"
      max_results: 10
    - tool: tavily
      query: "cross CLI agent communication tools"
      max_results: 10
    - tool: tavily
      query: "Claude Code OpenCode integration"
      max_results: 5
    - tool: github
      query: "MCP server multi-agent"
      max_results: 10
  context7:
    - library: "anthropic/claude-code"
      topic: "MCP server creation"
  output: research/landscape/L1_github_survey.md
  depends_on: []
```

### Field Definitions

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Matches TRACKER.md ID |
| `name` | Yes | Human-readable description |
| `status` | Yes | `NOT_STARTED`, `IN_PROGRESS`, `COMPLETE`, `BLOCKED` |
| `priority` | No | 1 = highest, execute first |
| `searches` | Yes | List of search operations |
| `context7` | No | Documentation lookups |
| `output` | Yes | Where findings go |
| `depends_on` | No | Task IDs that must complete first |

---

## Research Loop

```
┌─────────────────────────────────────────────────────────┐
│                    RESEARCH LOOP                        │
└─────────────────────────────────────────────────────────┘

1. READ HARNESS.md (this file)
         │
         ▼
2. CHECK TRACKER.md
   - Find highest priority NOT_STARTED task
   - Or continue IN_PROGRESS task
         │
         ▼
3. CREATE TODOWRITE
   - Break task into search operations
   - One item per search/lookup
         │
         ▼
4. UPDATE STATUS → IN_PROGRESS
   - In TRACKER.md
   - In TASKS.yaml (if exists)
         │
         ▼
5. EXECUTE SEARCHES (see Search Execution below)
   - Run searches per task definition
   - Dump raw results immediately
         │
         ▼
6. SYNTHESIZE (see Synthesis below)
   - Sequential thinking over results
   - Write findings document
         │
         ▼
7. UPDATE STATUS → COMPLETE
   - Update TRACKER.md
   - Link findings in Findings Index
   - Log in Session Log
         │
         ▼
8. CHECK FOR MORE TASKS
   - More NOT_STARTED? → Go to step 2
   - All complete? → Report to user
         │
         ▼
9. USER CHECKPOINT
   - Present summary of completed research
   - Ask: Continue with next phase? New tasks? Stop?
```

---

## Search Execution

### Tool: Tavily

```
For each tavily search in task:
    1. Run tavily_search with query
    2. Capture: titles, URLs, snippets
    3. Append to output file under "## Raw Results - Tavily"
    4. Mark search complete in TODOWRITE
```

**Concurrency**: Up to 3 Tavily searches in parallel

### Tool: Context7

```
For each context7 lookup in task:
    1. Resolve library ID
    2. Query documentation
    3. Append to output file under "## Raw Results - Context7"
    4. Mark lookup complete in TODOWRITE
```

**Concurrency**: Up to 3 Context7 lookups in parallel

### Tool: GitHub (via Tavily)

```
For github searches:
    1. Use tavily with "site:github.com" prefix
    2. Capture: repo names, descriptions, stars if visible
    3. Append to output file under "## Raw Results - GitHub"
```

### Output File Format

Create output file immediately when starting task:

```markdown
# [Task Name]

**Task ID**: [ID]
**Started**: [timestamp]
**Status**: IN_PROGRESS

---

## Raw Results - Tavily

### Search: "[query 1]"
- [Result 1 title](url) - snippet
- [Result 2 title](url) - snippet
...

### Search: "[query 2]"
...

## Raw Results - Context7

### Library: [library name]
[Documentation excerpts]

## Raw Results - GitHub

### Search: "[query]"
- [repo/name](url) - description
...

---

## Synthesis

*[Added after Sequential Thinking]*

---

## Conclusions

*[Added after synthesis]*

---

## Next Actions

*[What this research suggests we do next]*
```

---

## Synthesis Process

After ALL searches complete for a task:

### Step 1: Per-Source Sequential (12 thoughts each)

```
For each tool that returned results:
    Run Sequential Thinking (12 thoughts)
    Input: That tool's raw results
    Output: Key findings for that source
    Append to "## Synthesis" section
```

### Step 2: Cross-Source Sequential (18 thoughts)

```
If multiple tools returned results:
    Run Sequential Thinking (18 thoughts)
    Input: All per-source syntheses
    Output: Unified conclusions
    Write to "## Conclusions" section
```

### Step 3: Next Actions

```
Based on conclusions:
    Identify follow-up research needs
    Identify decisions needed from user
    Write to "## Next Actions" section
```

---

## User Checkpoints

**Mandatory checkpoints** (STOP and report to user):

1. After completing a full research phase (L1-L4, P1-P4, etc.)
2. When a task is `BLOCKED`
3. When synthesis reveals conflicting information
4. When next actions require architectural decisions
5. After every 3 completed tasks (batch checkpoint)

**Checkpoint format**:

```markdown
## Research Checkpoint

**Completed**: [list of task IDs]
**Key Findings**: [2-3 bullet summary]
**Decisions Needed**: [if any]
**Recommended Next**: [suggested next tasks]

Awaiting your direction.
```

---

## Error Handling

| Error | Action |
|-------|--------|
| Search returns no results | Note in raw results, try alternate query |
| Search fails (API error) | Retry once, then mark search as failed and continue |
| Context7 library not found | Skip, note in results |
| Synthesis unclear | Mark task BLOCKED, request user guidance |
| Dependency not met | Skip task, move to next available |

---

## File Locations

| File | Purpose |
|------|---------|
| `research/HARNESS.md` | This file - operational instructions |
| `research/TRACKER.md` | Status tracking, session log |
| `research/TASKS.yaml` | Task definitions (optional, can be inline) |
| `research/[category]/[ID]_[name].md` | Findings documents |

---

## Quick Reference

```
LOOP:     Read Harness → Check Tracker → TODOWRITE → Search → Synthesize → Update → Next

SEARCH:   Tavily (3 parallel) | Context7 (3 parallel) | GitHub (via Tavily)

SYNTH:    12 thoughts per source → 18 thoughts cross-source → Conclusions

STOP:     Phase complete | Blocked | Conflict | Decision needed | Every 3 tasks
```

---

## Integration

This document is referenced by:
- `claudedocs/arch-design/BaseResearchInstructions.md`
- `claudedocs/arch-design/TROUBLESHOOTING_STEP_GUIDE.md`
- `claudedocs/plans/*.md`

When starting research work, agent should:
1. Read this file first
2. Read TRACKER.md for current state
3. Follow the loop
