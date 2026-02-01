# Journal: Architecture Decisions & Feasibility Tests

**Date**: 2026-01-07
**Sessions**: Architecture Design, Feasibility Testing, Feature Brainstorm
**Duration**: ~4 hours across multiple sessions

---

## Morning: Architecture Decisions

### Decision D1: Interaction Model

**Question:** How does the user see other agents working?

**Options explored:**

**Model A - Invisible Subprocess:**
- Claude Code spawns other agents as subprocesses (no visible window)
- Passes context + mode-specific prompt
- Waits for response, displays inline
- User sees: `GPT-5 Review (challenge mode): ...`

**Model B - Visible Parallel Windows:**
- Separate terminal windows for each agent
- User SEES the other agent working
- Push-based injection into running sessions
- More complex implementation

**Discussion with user:**
- User asked about seeing "thinking" from other agents
- Clarified: visibility of thinking is nice-to-have, not required
- Logging acceptable if real-time visibility is hard

**DECIDED: Model A (Invisible Subprocess)**

*Rationale:* Simpler to implement, user gets results inline, thinking can be logged. Model B is cool but adds significant complexity. Can always add later.

---

### Decision D2: Architecture Topology

**Question:** Hub-spoke or peer-to-peer?

**Hub-Spoke:**
```
        Claude Code (HUB)
              │
    ┌─────────┼─────────┐
    ▼         ▼         ▼
 OpenCode   Vibe    Future N
```

**Peer-to-Peer:**
```
Claude Code ⟷ OpenCode
     ⟷         ⟷
      Vibe ⟷ Future N
```

**Analysis:**
- Peer-to-peer: Every agent talks to every other. N² connections. Complexity explosion.
- Hub-spoke: Claude Code orchestrates. Other agents are spokes. N connections. Extensible.

**DECIDED: Hub-Spoke with Claude Code as Hub**

*Rationale:* User interacts with Claude Code already. Single point of orchestration. Adding new spoke = 1 integration, not N.

---

### Decision D3: GPT-5 Harness

**Question:** Codex or OpenCode?

Already seeded yesterday but made official today.

| Factor | Codex | OpenCode |
|--------|-------|----------|
| Network | Blocked by default | No restrictions |
| Sandbox | Three-tier, complex | None |
| MCP support | 3/5 | Via Claude compat |
| Providers | OpenAI only | 75+ via OpenRouter |
| Open source | No | Yes |

**DECIDED: OpenCode**

*Rationale:* Avoids sandbox complexity entirely. 75+ providers is bonus. Open source means we can debug issues.

---

## Afternoon: Feasibility Testing

Time to stop theorizing and actually test things.

### F1: Claude Code Spawning Subprocess

**Hypothesis:** Claude Code can spawn `opencode run` and get a response.

**Test:**
```bash
opencode run "Reply with exactly: TEST_SUCCESS_12345" --print-logs
```

**Result:** ✅ SUCCESS

Response received in ~4 seconds. Some non-fatal `Bad file descriptor` errors in logs but operation completed cleanly.

**Learning:** Subprocess spawning works. The errors are noise, not blockers.

---

### F3: Bidirectional Communication

**Hypothesis:** We can send context and get structured responses back.

**Test:**
```bash
opencode run "Analyze this Python function and respond with ONLY a JSON object: {'issues': [...], 'rating': 1-5}

def divide(x, y):
    return x / y
"
```

**Result:** ✅ SUCCESS

```json
{
  "issues": ["Potential ZeroDivisionError if y is 0", ...],
  "rating": 4
}
```

**Learning:** Structured output works. JSON parsing reliable. Context passing functional.

---

### F5: Multi-Model Support

**Hypothesis:** OpenCode can route to different models via flags.

**Tests:**
```bash
opencode run "Reply TEST_GPT5" -m "openrouter/openai/gpt-5"
opencode run "Reply TEST_GROK" -m "openrouter/x-ai/grok-4-fast"
```

**Results:** ✅ BOTH SUCCESS

| Model | Response |
|-------|----------|
| GPT-5 | `GPT5_TEST` |
| Grok-4-fast | `GROK_TEST` |

**Learning:** Multi-model routing works via `-m` flag. OpenRouter handles the actual API calls.

---

### F6: HTTP API Per-Request Model Selection

**Hypothesis:** `opencode serve` can accept different models per HTTP request.

**Test:**
```bash
# Terminal 1
opencode serve --port 3001

# Terminal 2
curl -X POST http://127.0.0.1:3001/session -d '{}'
# Returns session ID

curl -X POST http://127.0.0.1:3001/session/{id}/message \
  -H "Content-Type: application/json" \
  -d '{"model": "openrouter/openai/gpt-5", "parts": [{"type": "text", "text": "Hello"}]}'
```

**Result:** ✅ SUCCESS

Single serve instance, multiple models per request. This simplifies architecture - no need for one server per model.

**Learning:** The API is cleaner than expected. Session-based, model-per-request, structured responses with token counts and costs.

---

## Evening: Feature Brainstorm

User wanted to discuss what the middleware should actually DO beyond basic routing.

### Reference: LLM Context Arena

Looked at `/home/(folders)/llm-council-rag` for inspiration.

Found 6 deliberation modes:
- **Council**: All answer → Peer review → Synthesize
- **Round Robin**: Sequential refinement
- **Fight**: Answer → Critique → Defend
- **Stacks**: Merge → Attack → Judge → Defend
- **Complex Iterative**: Extract ⇄ Expand cycles
- **Complex Questioning**: Socratic with muse round

These are more sophisticated than simple challenge/agree/collaborate. Worth considering.

---

### Feature Discussion Highlights

**KV Store for Shared State:**
- User: "most interesting, why use it though"
- Brainstormed use cases: intermediate results, shared artifacts, conversation state
- Deferred to P3 priority - needs more design

**Context Compression:**
- User: "When should it kick in, what should it do to summarize, what kind of information loss is possible"
- Proposed: 70%/85% thresholds, lossless/lossy/hybrid strategies
- Key insight: Keep original accessible, compression is reversible via `@expand`

**YAML Pipeline Config:**
- User: "yes! and I want to be able to config graph them out"
- Big excitement here. User wants routing playbooks as YAML DAGs
- This becomes P1 priority

**Cross-Session Memory:**
- User: "yes actually... keep the last X tokens of context cross-session"
- Approved. Token-based retention window.

**Rate Limiting + Budgeting:**
- User: "should be together"
- Unified implementation approved

**Sanitization:**
- User: "Why would we worry about sanitizing what was inside of the tool already"
- Clarified scope: Not internal sanitization, but preventing context payloads being misread as prompts
- Solution: XML delimiter framing (`<context>` vs `<instruction>`)

---

## Priority Matrix (End of Day)

| Priority | Feature |
|----------|---------|
| P0 | Agent registry, routing, mode system, logging |
| P1 | YAML pipelines, cross-session memory, rate limiting + budgeting |
| P2 | Token tracking, context compression |
| P3 | KV store, validation layer |

---

## Artifacts Updated

- `research/landscape/discovery_findings.md` - Added decisions, feasibility results, feature brainstorm (became monolithic)
- `research/TRACKER.md` - Updated with F1, F3, F5, F6 status

---

## Mood Check

Very confident now. Theory validated:
- Subprocess spawning works ✅
- Multi-model works ✅
- HTTP API works ✅
- Structured responses work ✅

User engaged and making decisions. Feature scope is clarifying.

**Concern:** discovery_findings.md is getting unwieldy. Everything dumped in one file. Should probably restructure... (foreshadowing tomorrow)
