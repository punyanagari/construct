# Phase 1 — Setting Up AI Agents

## What it is & why it matters

Before you touch a framework, you need one distinction burned into your mental model. A **workflow** is an LLM (or several) orchestrated by predefined code paths — you write the control flow, the model fills in the intelligence. An **agent** is an LLM dynamically directing its own process and tool usage in a loop — the model decides what happens next. This is the core taxonomy from Anthropic's "Building effective agents," and it carries a sharp edge: most tasks you think need an agent are better served by a workflow, and most workflows are better served by a single well-prompted LLM call. For your SaaS ERP, the query-routing layer you're planning is likely a *workflow* (a router pattern), while the specialist agents behind it are *agents*. Knowing which is which saves you weeks.

Here's the encouraging part: a working agent is about 60–100 lines of plain Python. An LLM client, a list of tool schemas, a `while` loop that sends messages, executes whatever tool the model asks for, appends the result, and repeats until the model stops asking. That's the whole trick — everything LangGraph, CrewAI, or the OpenAI Agents SDK does is scaffolding around that loop.

You build it from scratch first for one reason: frameworks hide the loop, and the loop is where every production bug lives. When your ERP agent loops forever, calls the wrong tool, or blows your token budget, you'll debug it at the message-history level. If you've only ever called `graph.invoke()`, you're stuck. Every serious curriculum on this topic converges on the same advice — raw loop first, framework second. Treat it as a gate, not a suggestion.

## Core concepts, in learning order

Work through these in sequence; each one assumes the previous:

1. **Agent vs. workflow, and when NOT to build an agent.** Learn the taxonomy and the "simplest thing that works" principle before writing code.
2. **LLM API fundamentals.** Messages format (system/user/assistant/tool roles), temperature, max tokens, structured output, and cost/latency tradeoffs between model tiers. You can't build an agent before you can make one well-controlled LLM call.
3. **Tool calling (function calling).** Declaring a tool schema (name, description, JSON parameters), reading the model's tool-call response, executing it, and feeding the result back. Tool description quality determines agent reliability more than anything else — you are prompt-engineering your tools.
4. **The agent loop in raw Python.** The `while` loop: messages in → text or tool call out → execute → append → repeat, with a stopping condition (max iterations, human checkpoint). This is the single most important exercise in the entire roadmap.
5. **The five canonical workflow patterns.** Prompt chaining, routing, parallelization (sectioning/voting), orchestrator-workers, evaluator-optimizer. Your ERP's multi-agent routing is pattern #2 — learn to pick the simplest one that solves the problem.
6. **Reliability basics.** Tracing every LLM call and tool invocation, human-in-the-loop approval gates, hard stopping conditions, and first-pass evaluation — enough to keep a demo from becoming a runaway bill.

> **Moved in roadmap v2:** LangGraph, the framework survey (OpenAI Agents SDK, CrewAI, Claude Agent SDK, AutoGen), and MCP now live in Phase 3 (`phases/03-graph-engineering`). Phase 1 is raw Python only.

## Study resources

### YouTube

| Title | Channel | URL | Why watch |
|---|---|---|---|
| Building AI Agents in Pure Python | Dave Ebbelaar | https://www.youtube.com/watch?v=bZzyPscbtI8 | The raw-Python build this phase is about — API calls, tool calling, and the loop with zero framework. The video companion to the build gate. |
| Advice for Building Agents | OpenAI | https://www.youtube.com/watch?v=js4HRqmsDQE | OpenAI's own practical agent-design guidance — when to agent at all, tool design, guardrails. |
| Vibe Coding in Prod \| Code w/ Claude | Anthropic | https://www.youtube.com/watch?v=fHWFF_pnqDk | An Anthropic coding-agent researcher (co-author of "Building effective agents") on running agents in production: stress-testing, I/O verification, context compaction, human oversight — concept 6 in practice. |

### X (Twitter)

| Handle | URL | Why follow |
|---|---|---|
| Harrison Chase — @hwchase17 | https://x.com/hwchase17 | LangChain/LangGraph founder and CEO. Framework releases, agent architecture threads, production lessons. The single most important account for the LangGraph ecosystem. |
| Anthropic — @AnthropicAI | https://x.com/AnthropicAI | Agent SDK and Claude Code releases, MCP ecosystem news, and links to the engineering blog posts you're reading this phase. |
| Logan Kilpatrick — @OfficialLoganK | https://x.com/OfficialLoganK | Leads Google AI Studio/Gemini API (ex-OpenAI DevRel). Insider view of agent tooling and ecosystem shifts from both OpenAI and Google. |
| Peter Steinberger — @steipete | https://x.com/steipete | Open-source agentic builder; candid, technically grounded posts on agentic engineering workflows. |

### Docs, blogs & repos

| Resource | URL | Why use it |
|---|---|---|
| Anthropic — "Building effective agents" | https://www.anthropic.com/engineering/building-effective-agents | THE canonical taxonomy: workflows vs. agents, the five workflow patterns, the "simplest possible solution" principle. Read before writing any agent code. |
| OpenAI — "A practical guide to building agents" | https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/ | OpenAI's written playbook: when to build an agent, tool design, guardrails, and human oversight — the second opinion next to Anthropic's taxonomy. |
| Microsoft — "AI Agents for Beginners" (GitHub course) | https://github.com/microsoft/ai-agents-for-beginners | Free 18-lesson curriculum: design patterns, tool use, agentic RAG, multi-agent, MCP/A2A protocols, with code samples. Use it as your self-study backbone. |

## Hands-on build gate: the Pocket Research Agent

You don't advance to Phase 2 until this works. **From scratch, ~100 lines, no framework**, over one or two evenings:

A CLI agent with a `while` loop and three tools you write yourself: `web_search` (Tavily, Serper, or DuckDuckGo), `read_notes`/`write_notes` against a local markdown file, and `calculator`. Give it a system prompt ("You are a research assistant; always cite sources; save findings to notes"), a max-iterations stopping condition (10 is fine), and print every tool call. Task it with: *"Research the current state of small language models for on-device agents and save a 5-bullet summary with sources."*

*(In roadmap v2 the LangGraph rebuild and the MCP server moved into Phase 3's build gate — you'll rebuild this exact agent there and feel what the framework adds.)*

**Stretch:** add a second "critic" agent (the evaluator-optimizer pattern, still raw Python) that reviews the summary before it's saved.

## Common pitfalls

1. **Reaching for a framework before writing the raw loop.** Frameworks abstract away the message history — which is exactly where you'll debug every production failure. Do step 1 of the build gate first, no exceptions.
2. **Building an agent where a workflow (or one LLM call) suffices.** Anthropic's golden rule: a well-prompted single call beats a workflow, a workflow beats an agent, and one agent with good tools usually beats a crew. Complexity must earn its place.
3. **Sloppy tool descriptions.** The model chooses tools based on their names and descriptions, not their code. Vague schemas cause wrong-tool calls more reliably than any model limitation does.
4. **No stopping condition.** An agent loop without max iterations, a human approval gate, or tracing is a runaway API bill waiting to happen. Instrument from day one.

## Checkpoint — you're ready for Phase 2 when you can

- Explain, without notes, the difference between a workflow and an agent — and name a task in your ERP that should stay a workflow.
- Write a ~100-line agent loop in raw Python with tool calling, a system prompt, and a max-iterations stop, from memory.
- Name all five canonical workflow patterns and justify the simplest one for a given problem — including which pattern your ERP query router will use.
