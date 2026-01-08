# F1: Newsreel Memory Plugin

**Status**: IDEA
**Priority**: TBD
**Dependencies**: Core middleware operational

---

## Concept

A claude-mem inspired plugin for the middleware that maintains a running narrative of project activity - what's been completed, what's being worked on, current states - presented as a "newsreel" style log.

## Key Differentiator

Uses **Grok-4-fast** (via OpenRouter) as the summarization engine:
- Extremely cheap (~$0.05/1M input, $0.10/1M output)
- Fast response times
- Good enough for summarization tasks
- Keeps expensive models (GPT-5, Claude) for actual work

## Trigger

**Optional feature** - only activates if user provides OpenRouter API key in middleware config.

## Proposed Functionality

### What Gets Recorded

| Event Type | Example |
|------------|---------|
| Agent requests | "Asked GPT-5 to review auth.py in challenge mode" |
| Agent responses | "GPT-5 identified 3 security concerns" |
| Mode switches | "Switched to collaborate mode for implementation" |
| File operations | "Modified src/auth.py based on GPT feedback" |
| Session boundaries | "Session started/ended" |
| Decisions | "Chose approach B per GPT recommendation" |

### Newsreel Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📰 x_agent_code NEWSREEL | 2026-01-08 14:32
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔄 SESSION RESUMED
   Continuing auth refactor from yesterday's session.

⚔️ CHALLENGE MODE ENGAGED
   Asked GPT-5 to critique the JWT implementation.
   GPT-5 raised concerns about token expiration handling.

🤝 COLLABORATION INITIATED
   Claude and GPT-5 jointly designing refresh token flow.
   Consensus reached on sliding window approach.

✅ MILESTONE: Auth middleware complete
   Files modified: auth.py, middleware.py, config.yaml
   Tests passing: 12/12

📊 SESSION STATS
   Agents consulted: 2 (GPT-5, Claude)
   Modes used: challenge → collaborate
   Tokens: ~8.2k across agents
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Summarization Strategy

Raw events are verbose. Grok-4-fast periodically summarizes:

```
Every N events OR every M minutes:
  1. Collect raw event buffer
  2. Send to Grok-4-fast: "Summarize these middleware events as a brief newsreel entry"
  3. Append summary to newsreel.md
  4. Clear buffer
```

### Storage

```
~/.x_agent_code/
├── newsreel.md           # Human-readable narrative log
├── events.jsonl          # Raw events (append-only)
└── sessions/
    └── {session_id}.json # Per-session detailed state
```

## User Interactions

### Commands

| Command | Action |
|---------|--------|
| `/newsreel` | Display recent newsreel entries |
| `/newsreel today` | Today's activity |
| `/newsreel --full` | Complete history |
| `/newsreel search "auth"` | Search newsreel |

### Automatic Context

On session start, middleware can inject recent newsreel as context:
```
"Yesterday you were working on auth refactor. GPT-5 had concerns about
token expiration. You decided on sliding window refresh tokens."
```

This gives agents continuity without full context replay.

## Cost Analysis

Assuming Grok-4-fast via OpenRouter:
- Input: $0.05 / 1M tokens
- Output: $0.10 / 1M tokens

**Example session:**
- 50 events × ~100 tokens each = 5k tokens input
- Newsreel output ~500 tokens
- Cost: ~$0.0003 per summarization

Even aggressive summarization (every 10 events) would cost < $0.01 per session.

## Integration Points

### With Cross-Session Memory (P1)

Newsreel complements token-based memory:
- Memory: Raw context preservation
- Newsreel: Narrative summary for humans and context injection

### With YAML Pipelines (P1)

Pipeline execution could auto-log to newsreel:
```yaml
pipeline: code_review
newsreel: true  # Enable newsreel logging for this pipeline
```

### With Observability (P0)

Newsreel is essentially observability for humans:
- Token tracking → appears in session stats
- Audit trail → newsreel IS the human-readable audit

## Open Questions

1. **Summarization trigger**: Event count vs time interval vs hybrid?
2. **Newsreel length**: Rolling window or full history?
3. **Privacy**: Should newsreel include code snippets or just descriptions?
4. **Multi-project**: One newsreel per project or global?

## Implementation Notes

### Grok-4-fast Prompt

```
You are a project activity summarizer. Convert these raw middleware events
into a brief, engaging newsreel entry. Use these symbols:
- 🔄 Session events
- ⚔️ Challenge mode
- 🤝 Collaboration
- 💡 Insights/decisions
- ✅ Completions
- ⚠️ Issues/concerns

Keep it concise but informative. Write for a developer resuming work tomorrow.
```

### Fallback

If no OpenRouter key provided:
- Raw events still logged to `events.jsonl`
- Newsreel generation disabled
- User can manually summarize or use other tools

---

## References

- [claude-mem](https://github.com/anthropics/claude-mem) - Inspiration for memory patterns
- [A3: Feature Design](../architecture/A3_feature_design.md) - Related P1 cross-session memory
- Grok-4-fast pricing: OpenRouter
