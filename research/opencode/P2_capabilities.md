# P2: OpenCode Capabilities & API

**Research ID**: P2
**Status**: COMPLETE
**Source**: Discovery research + Feasibility tests (2026-01-06/07)

---

## Overview

OpenCode is an open-source terminal assistant supporting 75+ AI providers, selected as the GPT-5 harness for x_agent_code.

## Core Features

| Feature | Description |
|---------|-------------|
| Provider support | 75+ models via OpenRouter |
| Multi-session | Run multiple agents in parallel on same project |
| Plugin hooks | Extensibility via GitHub issue #5305 |
| Custom commands | Markdown files for workflow customization |
| Privacy-first | No code storage |
| Claude compat | "Oh My OpenCode" compatibility layer |

## Command Types

| Type | Description | Example |
|------|-------------|---------|
| TUI Commands | Instant execution | Interactive terminal |
| Slash Commands | Agent-driven | `/command` syntax |

## Invocation Modes

### Mode Comparison

| Mode | Command | Use Case |
|------|---------|----------|
| Direct run | `opencode run "prompt"` | One-shot subprocess, non-interactive |
| HTTP serve | `opencode serve --port 3000` | Persistent API server |
| Attach | `opencode run --attach "prompt"` | CLI attaches to running serve instance |

### Recommended for x_agent_code

Run `opencode serve` as persistent background process:
- Middleware makes HTTP API calls to localhost:PORT
- Avoids cold boot overhead on each request
- Fast response times

### HTTP Server Flags

```
--port      Port to listen on
--hostname  Hostname to bind
--mdns      Enable mDNS discovery
--cors      Additional CORS origins
```

---

## HTTP API Reference

### Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/session` | POST | Create new session |
| `/session/{id}/message` | POST | Send message to session |
| `/session/{id}/command` | POST | Execute command in session |
| `/session/{id}/shell` | POST | Execute shell command |
| `/event` | GET | Server-sent events (streaming) |
| `/config` | GET | Get configuration |
| `/doc` | GET | OpenAPI specification |

### Message Format

```bash
POST /session/{id}/message
Content-Type: application/json

{
  "model": "openrouter/openai/gpt-5",
  "agent": "build",
  "parts": [{"type": "text", "text": "Your prompt here"}]
}
```

### Per-Request Model Selection

**Key finding**: Single `opencode serve` instance can handle multiple models dynamically.

```
                    ┌─────────────────────────────────────┐
                    │     opencode serve --port 3001      │
                    │   (single instance, multi-model)    │
                    └─────────────────────────────────────┘
                                     │
              ┌──────────────────────┼──────────────────────┐
              │                      │                      │
    { model: "gpt-5" }    { model: "grok-4-fast" }   { model: "gemini-3" }
              │                      │                      │
              ▼                      ▼                      ▼
         OpenRouter            OpenRouter             OpenRouter
              │                      │                      │
              ▼                      ▼                      ▼
           OpenAI                  xAI                  Google
```

---

## Available Models

All models route through **OpenRouter** for credits/billing.

| Model | Command Flag | Notes |
|-------|--------------|-------|
| GPT-5 | `-m "openrouter/openai/gpt-5"` | Primary target |
| GPT-5 Pro | `-m "openrouter/openai/gpt-5-pro"` | Higher capability |
| Grok-4-fast | `-m "openrouter/x-ai/grok-4-fast"` | Cheap/fast option |
| Gemini-3-Pro | `-m "openrouter/google/gemini-3-pro-preview"` | Default |
| Claude models | `-m "openrouter/anthropic/claude-*"` | Various |

---

## Feasibility Test Results

### F1: Subprocess Spawning - PASSED

**Test**: Can Claude Code spawn OpenCode as a subprocess?

```bash
opencode run "Reply with exactly: TEST_SUCCESS_12345" --print-logs
```

**Result**: SUCCESS
- Response received in ~4 seconds
- OpenCode spawned cleanly from Claude Code session
- Some non-fatal errors (`Bad file descriptor`) but operation completed

### F3: Bidirectional Communication - PASSED

**Test**: Can we send context and receive structured responses?

```bash
opencode run "Analyze this Python function and respond with ONLY a JSON object..."
```

**Result**: SUCCESS - Structured JSON returned
```json
{
  "issues": ["Potential ZeroDivisionError if y is 0", ...],
  "rating": 4
}
```

### F5: Multi-Model Support - PASSED

| Model | Command | Result |
|-------|---------|--------|
| GPT-5 | `-m "openrouter/openai/gpt-5"` | Returned `GPT5_TEST` |
| Grok-4-fast | `-m "openrouter/x-ai/grok-4-fast"` | Returned `GROK_TEST` |

### F6: HTTP API Per-Request Model - PASSED

**Test**: Does HTTP API support per-request model selection?

```bash
opencode serve --port 3001
curl -X POST http://127.0.0.1:3001/session -d '{}'
curl -X POST http://127.0.0.1:3001/session/{id}/message -d '{"model": "...", "parts": [...]}'
```

**Result**: SUCCESS
- Server starts on specified port
- Session creation via `POST /session`
- Per-request model selection confirmed

---

## Comparison with Codex

| Aspect | OpenCode | Codex |
|--------|----------|-------|
| Open source | Yes | No |
| Provider support | 75+ | Limited |
| Network sandbox | None | Blocked by default |
| MCP rating | Via Claude compat | 3/5 |
| Multi-session | Yes | No |
| Plugin system | Yes | Limited |

**Decision**: OpenCode selected over Codex for x_agent_code.

---

## References

- OpenCode documentation: [opencode.ai/docs/server/](https://opencode.ai/docs/server/)
- Tavily search: "OpenCode CLI" (2026-01-06)
- Feasibility tests (2026-01-07)
