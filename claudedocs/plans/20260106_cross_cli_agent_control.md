# Cross CLI Agent Control/Context Tools

**Date**: 2026-01-06
**Type**: DEEP RESEARCH PROJECT
**Status**: Planning / Discovery Phase
**Author**: Indubitable Industries

---

## Project Classification

```yaml
project_type: deep_research
research_mode: unattended_capable
collaboration: public_from_day_1
branch_strategy: protected_main_with_feature_branches
```

---

## Problem Statement

Current AI coding assistants (Claude Code, GPT5 Codex, OpenCode, Vibe) operate in isolation. Context switching between tools creates friction, separate contexts prevent knowledge sharing, and orchestrating multiple agents is difficult or impossible.

**Core Pain Points:**
- Flipping between tools loses context and momentum
- Separate context windows = duplicated understanding
- Long context operations suffer from error-creep
- Tight agent configurations work but can't be orchestrated
- No bidirectional communication between agent systems

---

## Vision

A middleware/MCP system enabling:
1. **Cross-agent communication** - Models speaking to one another
2. **Sub-agent instantiation** - Any agent can spawn another as subordinate
3. **Runtime prompt injection** - Modify prompts/configs temporarily, auto-revert post-execution
4. **Unified context** - Share relevant context across agent boundaries
5. **CLI-first design** - Plugin/MCP/Skill for existing tools, not replacement

---

## Research Objectives

### Primary Questions

1. **Middleware Architecture**
   - What communication patterns work? (challenge, agree, collaborate, deduce)
   - How much context flows between agents?
   - What triggers inter-agent communication?

2. **Sandbox Constraints**
   - Codex CLI sandbox restrictions - what's blocked?
   - OpenCode as alternative harness for GPT5 - complexity comparison
   - Decision threshold: >50% complexity increase = switch to OpenCode

3. **Sub-Agent Instantiation**
   - Can we spawn Codex/OpenCode as sub-agents from Claude Code?
   - Bidirectional? (Claude spawns Codex, Codex spawns Claude)
   - Specialty declarations for informed spawning

4. **Runtime Configuration**
   - Modify system/backend prompts at runtime
   - Preserve existing/default configurations
   - Auto-revert after execution completes

5. **Existing Solutions**
   - GitHub projects for cross-agent communication
   - CLI-driven orchestration tools (NOT heavy Liner-style systems)
   - MCP/plugin architectures that support multiple agent backends

---

## Technical Constraints

| Constraint | Requirement |
|------------|-------------|
| Architecture | Plugin/MCP/Skill - NOT a replacement for any CLI |
| Complexity | CLI-driven, no heavy agent management UI |
| Languages | Python (primary), Rust (performance), JS/Node (integrations) |
| Deployment | Localhost middleware acceptable (local LLM assist OK) |
| Public | Open source from day 1 |

---

## Research Phases

### Phase 1: Landscape Survey
- [ ] Catalog existing cross-agent communication projects
- [ ] Document Codex sandbox restrictions
- [ ] Document OpenCode capabilities and API surface
- [ ] Identify MCP patterns that could extend to multi-agent
- [ ] Survey local LLM options for middleware assistance

### Phase 2: Architecture Design
- [ ] Define communication protocol between agents
- [ ] Design context sharing mechanism
- [ ] Specify sub-agent lifecycle (spawn, configure, execute, revert)
- [ ] Define specialty/capability declaration format
- [ ] Design prompt injection and reversion system

### Phase 3: Prototype Development
- [ ] Minimal middleware proof-of-concept
- [ ] Claude Code <-> OpenCode bidirectional test
- [ ] Sub-agent spawn/control test
- [ ] Runtime config modification test

### Phase 4: Integration
- [ ] MCP server implementation
- [ ] Claude Code skill/hook integration
- [ ] OpenCode integration patterns
- [ ] Documentation for contributors

---

## Unattended Research Rules

When running in unattended research mode:

```yaml
unattended_research_rules:

  discovery:
    - Use parallel searches for independent queries
    - Document all findings immediately to claudedocs/
    - Create issues/ entries for blockers or open questions
    - Track confidence levels for each finding

  decision_making:
    - Catalog options with trade-offs, don't auto-decide
    - Flag decisions requiring human input
    - Use features/ to propose solutions with rationale
    - Never commit architectural decisions unattended

  documentation:
    - Short blurbs in Serena memory (cross-session reference)
    - Detailed findings in claudedocs/ markdown files
    - Keep memory entries <500 tokens, link to docs

  progress_tracking:
    - Update this plan document with findings
    - Mark completed research items
    - Add discovered sub-questions to appropriate phase

  boundaries:
    - NO code commits without human review
    - NO architectural decisions without discussion
    - NO external API calls without explicit approval
    - Document unknowns rather than guess
```

---

## Interaction Modes (Proposed)

For agent-to-agent communication, proposed modes:

| Mode | Description | Context Flow | Use Case |
|------|-------------|--------------|----------|
| `challenge` | Adversarial review | Full context shared | Code review, security audit |
| `agree` | Confirmatory analysis | Summary context | Validation, sanity check |
| `collaborate` | Joint problem solving | Incremental sharing | Complex tasks, research |
| `deduce` | Inference from partial | Minimal context | Hypothesis testing |

Each mode affects:
- Main prompt modifications
- Level of inter-agent interaction
- What context is available to each agent
- Result synthesis method

---

## Key Decisions Pending

1. **Codex vs OpenCode**: Benchmark sandbox complexity for our use case
2. **Middleware Location**: Pure MCP? Separate service? Hybrid?
3. **Context Protocol**: JSON-RPC? Custom? Existing standard?
4. **Local LLM**: Needed? Which model? What role?
5. **Specialty Format**: How agents declare what they're good at

---

## Success Criteria

- [ ] Two different AI agents can exchange context and collaborate on a task
- [ ] Sub-agent can be spawned with modified configuration
- [ ] Configuration reverts automatically after sub-agent execution
- [ ] Works as plugin/skill for existing tools (no replacement)
- [ ] Complexity remains CLI-manageable (no heavy UI required)

---

## References

- Claude Code MCP documentation
- OpenCode GitHub repository
- Codex CLI documentation
- Existing multi-agent frameworks (for patterns, not wholesale adoption)

---

## Next Actions

1. **Immediate**: Complete landscape survey (Phase 1)
2. **This Session**: Initialize Serena memory with project summary
3. **Near-term**: Research existing GitHub projects for cross-agent tooling
4. **Decision Gate**: Codex sandbox assessment determines OpenCode pivot

---

*This document is the authoritative plan for the x_agent_code project. Update in place; do not create derivative plan documents.*
