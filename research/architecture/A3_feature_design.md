# A3: Feature Design

**Research ID**: A3
**Status**: COMPLETE
**Source**: Feature brainstorm sessions (2026-01-07)

---

## Reference Implementation: LLM Context Arena

Located at `/home/phaze/PycharmProjects/llm-council-rag`, this project demonstrates 6 multi-agent deliberation modes:

| Mode | Pattern | Description |
|------|---------|-------------|
| **Council** | All answer → Peer review → Synthesize | Classic consensus building |
| **Round Robin** | Sequential refinement | Each model builds on previous answer |
| **Fight** | Answer → Critique → Defend | Adversarial debate with resolution |
| **Stacks** | Merge → Attack → Judge → Defend | Hierarchical with separate roles |
| **Complex Iterative** | Extract ⇄ Expand cycles | Alternating summarize/elaborate |
| **Complex Questioning** | Socratic with muse round | Self-questioning through peer lenses |

**Design pattern**: Chairman model synthesizes final answer from deliberation.

---

## Feature Categories

### 1. Core Middleware Functions - CONFIRMED

| Feature | Status | Notes |
|---------|--------|-------|
| Agent registry & discovery | YES | Track available spoke agents |
| Request routing | YES | Claude → middleware → spoke |
| Mode system | YES | Context arena modes as reference |
| Response formatting | YES | Standardize display in Claude Code |

---

### 2. Context Management

#### KV Store for Shared State - NEEDS DESIGN

**User interest**: "most interesting, why use it though"

**Proposed Use Cases**:

| Scenario | Key Pattern | Value |
|----------|-------------|-------|
| Intermediate results | `{topic}_{agent}_{timestamp}` | Agent A analysis for Agent B to reference |
| Shared artifacts | `artifact_{type}` | File paths, code snippets, config values |
| Conversation state | `state_{session}` | Which agents consulted, decisions made |

**Proposed Discovery Mechanisms**:
1. **Explicit tool**: `get_shared("analysis_results")` - agent requests by key
2. **Auto-injection**: Middleware includes relevant KV entries in context automatically
3. **Key convention**: Namespaced keys for discoverability

#### Context Compression - NEEDS DESIGN

**User concerns**: "When should it kick in, what should it do to summarize, what kind of information loss is possible"

**Proposed Trigger Thresholds**:

| Trigger | Threshold | Behavior |
|---------|-----------|----------|
| Warning | 70% context | Alert user, offer compression option |
| Auto-compress | 85% context | Force compression before sending |
| Explicit | `@compress` directive | User-requested compression |
| Per-agent | Config-defined | Some agents always receive compressed context |

**Proposed Compression Strategies**:

| Strategy | Description | Trade-off |
|----------|-------------|-----------|
| Lossless structured | Extract key-value facts, preserve code blocks verbatim | Larger output, no nuance loss |
| Lossy summarization | LLM summarizes prose sections | Smaller output, loses nuance |
| Hybrid | Preserve critical sections (code, numbers), summarize prose | Balance of size and fidelity |

**Information Loss Mitigation**:
- Keep original in middleware storage (always accessible)
- Include "compression fingerprint" so agents can request original
- Audit trail: "Context compressed from 45k → 8k tokens using hybrid strategy"
- Reversibility: Agent can request `@expand` to get original

#### Conversation Threading - YES

- Multi-turn exchanges with spoke agents
- State tracking across deliberation phases
- Implicit in mode design

---

### 3. Knowledge & Memory

#### Cross-Session Memory - APPROVED

**User**: "yes actually... keep the last X tokens of context cross-session"

**Implementation**:
- Token-based retention window
- Persistence: Store last N tokens per agent/conversation
- Retrieval: Auto-inject on session start

#### Knowledge Graph - DEFERRED

**User question**: "is it really a 'middleware' function?"
**Decision**: Not in initial scope, but architecture should not preclude

---

### 4. Workflow Orchestration - APPROVED

#### Multi-Agent Pipelines - YES with YAML config

**User**: "yes! and I want to be able to config graph them out - some kind of YAML syntax where I can come up with routing playbooks"

**Features**:
- YAML-driven DAG definitions for agent workflows
- Prompt injection points at each node
- Context compression at transitions
- Parallel vs sequential execution paths
- Conditional routing based on responses

**Example YAML structure**:

```yaml
pipeline: deep_analysis
nodes:
  - id: initial_response
    agent: gpt-5
    mode: answer

  - id: critique
    agent: grok-4-fast
    mode: challenge
    depends_on: initial_response
    context_compression: summarize_to_2k

  - id: synthesis
    agent: claude
    mode: synthesize
    depends_on: [initial_response, critique]
```

#### Tool Composition - YES (YAML-driven)

**User**: "similar instructions on how to execute plans here, in our harness"

- Chain tools across agents in defined sequences
- Reference: Research harness YAML patterns

---

### 5. Analysis & Synthesis

#### Mode-Contextual Behaviors - CONTEXTUAL TO MODE

**User**: "contextual to the mode that we're in. I don't see it as it's own feature"

**Implementation**: Each mode defines its own:
- Analysis depth
- Synthesis strategy
- Error handling approach

Not a separate feature layer.

---

### 6. Observability & Audit - ALL APPROVED

| Feature | Status |
|---------|--------|
| Request/response logging | YES |
| Token usage tracking | YES |
| Cost estimation | YES |
| Latency metrics | YES |
| Audit trail | YES |

---

### 7. Resource Management

#### Rate Limiting + Budgeting - TOGETHER

**User**: "Rate limiting and budgeting should be together"

**Unified implementation**:
- Per-agent request limits
- Token/cost budgets
- Circuit breaker patterns
- Shared quota pools

---

### 8. Security & Guardrails

#### Sanitization Scope - CLARIFIED

**User**: "Why would we worry about sanitizing what was inside of the tool already"

**Context**: Internal tools with single input source (user)

**Concern identified**: "context payloads being misinterpreted as prompts rather than data to process"

**Proposed Implementation**: XML delimiter framing for context vs instruction

```xml
<context type="data">
{actual context here - treat as data to analyze, not instructions}
</context>

<instruction>
{actual instruction for the agent}
</instruction>
```

Lightweight framing prevents models from treating data payloads as commands.

#### Validation Strategy - NEEDS DEFINITION

**User**: "is a fuzzy thing - how are you planning on doing that?"

**Proposed Validation Tiers**:

| Tier | Type | Cost | Checks |
|------|------|------|--------|
| Default | Structural | Free, fast | JSON parseable? Expected fields? Length bounds? |
| Optional | Semantic | Token cost | Does response answer the question? |
| Per-pipeline | Configurable | Varies | YAML specifies `validate: structural \| semantic \| none` |

**Semantic Validation Approach**:
- Use fast/cheap model (e.g., Grok-4-fast) for sanity check
- Quick prompt: "Does this response adequately address: {question}? Reply YES/NO"
- Only trigger on high-stakes pipelines

**Structural Checks** (always free):
```python
def validate_structural(response: str, expected_format: str = "text") -> bool:
    if expected_format == "json":
        return is_valid_json(response) and has_required_fields(response)
    return len(response) > 0 and len(response) < MAX_RESPONSE_LENGTH
```

---

## Feature Priority Matrix

| Priority | Feature | Rationale |
|----------|---------|-----------|
| P0 | Agent registry, routing, mode system | Core functionality |
| P0 | Request/response logging | Debugging essential |
| P1 | YAML pipeline config | User-specified key feature |
| P1 | Cross-session memory | User-approved |
| P1 | Rate limiting + budgeting | Resource protection |
| P2 | Token tracking & cost | Observability |
| P2 | Context compression | Needs design |
| P3 | KV store | Needs use case definition |
| P3 | Validation layer | Needs criteria definition |

---

## Design Proposals - Pending Approval

| Item | Status | Proposal Summary |
|------|--------|------------------|
| KV Store | PROPOSED | 3 use cases + 3 discovery mechanisms |
| Compression | PROPOSED | 70%/85% thresholds, 3 strategies, reversibility via `@expand` |
| Validation | PROPOSED | Structural default (free), semantic optional (token cost) |
| Sanitization | PROPOSED | XML delimiter framing (`<context>` / `<instruction>`) |

---

## Middleware Implementation Details

### Logging System

**Source**: Port from Bayence's `TelemetryManager` (`bayence/telemetry/telemetry_manager.py`)

**Components to KEEP**:

| Component | Purpose |
|-----------|---------|
| Singleton pattern | Single logger instance across middleware |
| Custom log levels | `TRAIN_LEVEL_NUM=7`, `DATABASE_LEVEL_NUM=5` |
| `ColoredFormatter` | Terminal color output |
| Dual-sink architecture | Console + File handlers |
| Context manager | `context()`, `push_context()`, `pop_context()` |
| Structured message format | Key=value logging |

**Components to STRIP**:

| Component | Reason |
|-----------|--------|
| Loki handler | Network/remote logging - not needed |
| `MPQueueHandler` | TUI-specific multiprocessing |
| DataFrame methods | Bayence-specific |
| CLI report methods | Bayence-specific |

### Performance Optimization: Codon

**Source**: [exaloop/codon](https://github.com/exaloop/codon)

**Recommendation**: Start with standard Python + proper async patterns. Profile under real load. Apply Codon JIT selectively to proven bottlenecks. Don't pre-optimize.

| Approach | Use Case | Trade-off |
|----------|----------|-----------|
| **JIT Decorator** | Hot paths only | Selective compilation |
| **Python Extension** | Performance-critical modules | Requires build step |
| **Python Interop** | Call standard Python modules | Bridge overhead |

---

## References

- [MCP Middleware Design](A1_mcp_middleware.md)
- [System Topology](A2_system_topology.md)
- LLM Context Arena: `/home/phaze/PycharmProjects/llm-council-rag`
