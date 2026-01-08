# L5: P2P Agent Communication Patterns

**Task ID**: L5
**Started**: 2026-01-08
**Status**: COMPLETE

---

## Research Questions

1. How do multi-agent systems handle peer discovery?
2. What message broker patterns exist for agent communication?
3. Does MCP protocol support multi-client scenarios?
4. What MIT-licensed implementations can we learn from?
5. What's the simplest approach for local-only P2P?

---

## Raw Results - Tavily

### Search: "multi-agent message broker LLM orchestration pub/sub pattern"

- [OpenAI Agents SDK - Orchestrating multiple agents](https://openai.github.io/openai-agents-python/multi_agent/) - Multi-agent orchestration patterns
- [LlamaIndex Multi-Agent Patterns](https://developers.llamaindex.ai/python/framework/understanding/agent/multi_agent/) - Framework patterns for multi-agent
- [Pub/Sub Message Brokers for GenAI](https://arxiv.org/html/2312.14647v1) - Neural Publish/Subscribe Paradigm for AI
- [Flink + Kafka Multi-Agent Orchestrator](https://www.confluent.io/blog/multi-agent-orchestrator-using-flink-and-kafka/) - Event-driven agent orchestration
- [Google ADK Multi-Agent Systems](https://google.github.io/adk-docs/agents/multi-agents/) - ADK patterns including SequentialAgent, ParallelAgent
- [IBM LLM Agent Orchestration](https://www.ibm.com/think/tutorials/llm-agent-orchestration-with-langchain-and-granite) - Orchestration with LangChain
- [ZenML Best LLM Orchestration Frameworks](https://www.zenml.io/blog/best-llm-orchestration-frameworks) - Framework comparison
- [AWS Strands Agents](https://aws.amazon.com/blogs/machine-learning/customize-agent-workflows-with-advanced-orchestration-techniques-using-strands-agents/) - AWS agent workflow techniques

**Key Insight**: "Agents are essentially stateful microservices with a brain, and the same event-driven principles that scale microservices apply to multi-agent systems." Kafka serves as messaging backbone, Flink as processing engine for routing.

### Search: "agent registry discovery protocol AI agents peer-to-peer"

- [ACDP - Agent Communication & Discovery Protocol](https://www.cmdzero.io/blog-posts/introducing-the-agent-communication-discovery-protocol-acdp-a-proposal-for-ai-agents-to-discover-and-collaborate-with-each-other) - DNS-based discovery + P2P awareness
- [A2A Protocol - Agent Discovery](https://a2a-protocol.org/latest/topics/agent-discovery/) - Agent Cards for self-description
- [MCP Gateway & Registry](https://github.com/agentic-community/mcp-gateway-registry) - **License**: Unknown - Enterprise MCP registry with OAuth
- [IBM AI Agent Protocols](https://www.ibm.com/think/topics/ai-agent-protocols) - Overview of agent protocols
- [A2A Agent Registry Proposal](https://github.com/a2aproject/A2A/discussions/741) - Community discussion on registry design
- [arXiv: Evolution of AI Agent Registry Solutions](https://arxiv.org/abs/2508.03095) - Centralized vs distributed registries
- [IETF Draft: HTTP-Based AI Agent Discovery](https://www.ietf.org/archive/id/draft-cui-ai-agent-discovery-invocation-00.html) - Standards proposal
- [Microsoft Entra Agent ID](https://learn.microsoft.com/en-us/entra/agent-id/identity-platform/agent-registry-collections) - Enterprise agent registry
- [arXiv: Agent Discovery in Internet of Agents](https://arxiv.org/html/2511.19113) - IoA framework challenges

**Key Protocols**:
- **ACDP**: DNS for discovery (SRV/TXT records), HTTPS for communication, hybrid central+P2P
- **A2A**: Agent Cards (JSON self-description), Linux Foundation managed
- **MCP Gateway**: Agents discover via registry, communicate P2P directly

### Search: "MCP server multiple clients shared state agent communication"

- [MCPcat: Configure MCP Servers for Multiple Connections](https://mcpcat.io/guides/configuring-mcp-servers-multiple-simultaneous-connections/) - Connection pooling, session management
- [Microsoft: Build A2A Communication on MCP](https://developer.microsoft.com/blog/can-you-build-agent2agent-communication-on-mcp-yes) - MCP as A2A foundation
- [MCP Official: Understanding MCP Clients](https://modelcontextprotocol.io/docs/learn/client-concepts) - Host manages multiple clients
- [AWS: Inter-Agent Communication on MCP](https://aws.amazon.com/blogs/opensource/open-protocols-for-agent-interoperability-part-1-inter-agent-communication-on-mcp/) - MCP for agent interoperability
- [Multi-MCP Proxy Server](https://itnext.io/multi-mcp-exposing-multiple-mcp-servers-as-one-5732ebe3ba20) - Single proxy to multiple backends
- [MCP-Use: Easiest way to interact with MCP servers](https://github.com/mcp-use/mcp-use) - Custom agent MCP interaction

**Key Findings**:
- MCP servers act as **multiplexers** - serialize access while maintaining per-client illusion
- HTTP + SSE best for high concurrency (HTTP/2 multiplexing)
- **Redis/DynamoDB** for shared state across instances
- MCP now supports: resumable streams, elicitation, sampling, notifications
- Resources enable agents to share context (files, state, memory)
- Resource subscriptions enable inter-agent workflows with dependencies

---

## Raw Results - Context7

### MCP Specification: Session Management

**Session IDs**: Globally unique, cryptographically secure, ASCII characters (0x21-0x7E)

**Lifecycle**:
1. Initialize: POST /mcp/initialize → Server returns Mcp-Session-Id
2. Maintain: All subsequent requests include Mcp-Session-Id header
3. Terminate: DELETE /mcp/ or server-initiated (client gets 404)

**Notifications**:
- `notifications/resources/list_changed` - Resource list updated
- `notifications/resources/updated` - Specific resource changed

**Multi-client support**: Host application manages multiple clients, each client connects to specific MCP server.

---

## Raw Results - GitHub

From searches above:
- [agentic-community/mcp-gateway-registry](https://github.com/agentic-community/mcp-gateway-registry) - Enterprise MCP gateway (License: check)
- [mcp-use/mcp-use](https://github.com/mcp-use/mcp-use) - Custom agent MCP interaction
- [a2aproject/A2A](https://github.com/a2aproject/A2A) - A2A protocol reference

---

## Synthesis

### Cross-Source Pattern Analysis (18 thoughts)

**Common Architecture Across All Sources**:
All sources converge on a three-component architecture: REGISTRY + ROUTER + PERSISTENCE.
- Enterprise: Kafka (persistence) + Flink (routing) + Registry service
- Local adaptation: SQLite (persistence) + MCP server (routing) + agents table (registry)

**Discovery Mechanism Comparison**:
| Approach | Source | Our Adaptation |
|----------|--------|----------------|
| DNS (SRV/TXT) | ACDP | ❌ Overkill for local |
| Agent Cards (JSON) | A2A | ✅ Perfect - register with JSON schema |
| Registry + P2P | MCP Gateway | ✅ SQLite query replaces network discovery |

**MCP Multi-Client Solution**:
- MCP stdio is 1:1 with host process (limitation)
- Solutions: HTTP+SSE for concurrency, shared state via external store
- Our approach: SQLite replaces Redis/DynamoDB, MCP server acts as multiplexer

**Message Patterns**:
| Pattern | Use Case | Implementation |
|---------|----------|----------------|
| Direct | Code review handoff | `to_agent = specific_id` |
| Broadcast | "Who has context on X?" | `to_agent = NULL` |

**Session Lifecycle (from MCP spec)**:
- Initialize → maintain with heartbeat → terminate (graceful or timeout)
- 90-second timeout aligns with MCP notification patterns
- Agent registry mirrors MCP session management

**Notification Mechanism**:
- Leverage MCP's existing notifications/resources/updated pattern
- No custom polling needed - server pushes on message arrival

### Architecture Decision

**Hub-Spoke with P2P Messaging Overlay**:
- D2 decision (hub-spoke) remains valid
- F2 adds peer awareness through the hub
- Hub facilitates P2P by being message broker
- Microsoft's "Build A2A on MCP" validates this pattern

---

## Conclusions

### Research Questions Answered

| # | Question | Answer |
|---|----------|--------|
| 1 | How do multi-agent systems handle peer discovery? | Agent Cards pattern (JSON self-description), registry-based lookup |
| 2 | What message broker patterns exist? | Pub/sub (broadcast) + point-to-point (direct) - both needed |
| 3 | Does MCP support multi-client? | Yes - multiplexer pattern, shared state, resource subscriptions |
| 4 | MIT-licensed implementations? | MCP protocol (MIT), A2A spec (open), patterns > code |
| 5 | Simplest local-only P2P? | SQLite shared state + MCP notifications |

### Recommended Architecture for x_agent_code

```
┌─────────────────────────────────────────────────┐
│         x_agent_code MCP Server                 │
│  ┌───────────────┐  ┌───────────────────────┐  │
│  │ Agent Registry │  │   Message Router      │  │
│  │ (list_agents) │  │ (send/broadcast/get)  │  │
│  └───────┬───────┘  └───────────┬───────────┘  │
│          │                      │               │
│  ┌───────┴──────────────────────┴───────────┐  │
│  │         SQLite Shared State              │  │
│  │  ~/.x_agent_code/state.db                │  │
│  │  ┌─────────┐  ┌──────────┐               │  │
│  │  │ agents  │  │ messages │               │  │
│  │  └─────────┘  └──────────┘               │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
        │              │              │
   ┌────┴────┐    ┌────┴────┐   ┌────┴────┐
   │ Claude  │    │  Codex  │   │OpenCode │
   │  Code   │    │         │   │         │
   └─────────┘    └─────────┘   └─────────┘
```

### Key Implementation Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Persistence | SQLite | Simple, file-based, handles concurrency |
| Discovery | Agent Cards | JSON schema, local query, no network |
| Messaging | Direct + Broadcast | Both patterns needed per use cases |
| Notifications | MCP native | Leverage existing spec, no polling |
| Timeout | 90 seconds | 3 missed heartbeats (30s interval) |
| Security | File permissions | Local-only, no auth needed initially |
| Scale | 2-10 agents | Local development use case |

### Open Questions Resolved

| Question | Resolution |
|----------|------------|
| Persistence | SQLite at `~/.x_agent_code/state.db` |
| Security | File permissions for local-only |
| Ordering | SQLite auto-increment, best-effort delivery |
| Scale | 2-10 concurrent agents max |
| Cross-machine | DEFERRED - start local-only |

---

## Next Actions

### Immediate (L5 → Implementation)

1. **Update F2 document** with architecture decisions from this research
2. **Design SQLite schema** for agents and messages tables
3. **Define MCP tools API** based on validated patterns
4. **Add to implementation backlog** with priority

### Blocking Feasibility Test

**F8: Push Notification Feasibility** - [F8_notification_feasibility.md](../feasibility/F8_notification_feasibility.md)

The architecture above assumes heartbeats and push notifications work. However, CLI agents are not daemons - they only act on user input or tool decisions. F8 must validate:
- Can Claude Code receive MCP server-pushed notifications?
- Can Codex receive notifications?
- Can OpenCode (one-shot) receive any notification?
- What hacky workarounds exist?

**If F8 shows push doesn't work**: Fall back to polling + activity-based model (mailbox pattern).

### Future Research (if needed)

- L6: Network-capable P2P (when cross-machine needed)
- L7: Authentication/authorization for multi-user scenarios
- L8: Message persistence and history management

### Implementation Priority

| Priority | Feature | Dependency |
|----------|---------|------------|
| P1 | Agent registration/discovery | None |
| P2 | Direct messaging | P1 |
| P3 | Broadcast messaging | P1 |
| P4 | Capability querying | P1 |
| P5 | Resource subscriptions | P2, P3 |
