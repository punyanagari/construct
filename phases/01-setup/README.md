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
6. **State and memory.** Conversation state, append/reducer semantics, checkpointing and persistence, short-term working memory vs. long-term cross-session memory.
7. **LangGraph (your primary framework).** StateGraph, nodes, edges, conditional edges, the compile/invoke cycle, human-in-the-loop interrupts, streaming, and LangSmith tracing. It's the industry workhorse for stateful, controllable agents.
8. **Other frameworks — compare, don't marry.** OpenAI Agents SDK (minimal primitives: Agents, Runner, handoffs, guardrails), CrewAI (role-based agents and tasks), Claude Agent SDK (Claude Code's capabilities programmatically, with MCP support). One caution: Microsoft's AutoGen is in maintenance mode and migrating to the Microsoft Agent Framework — learn its conversation-first concepts if you're curious, but don't build new projects on it.
9. **MCP (Model Context Protocol).** The "USB-C port for AI": hosts/clients/servers architecture, JSON-RPC over stdio and HTTP transports, and the three primitives (tools, resources, prompts). Build one small MCP server and connect it to Claude Desktop or Claude Code.
10. **Reliability basics.** Tracing every LLM call and tool invocation, human-in-the-loop approval gates, hard stopping conditions, and first-pass evaluation — enough to keep a demo from becoming a runaway bill.

## Study resources

### YouTube

| Title | Channel | URL | Why watch |
|---|---|---|---|
| LangGraph Complete Course for Beginners – Complex AI Agents with Python | freeCodeCamp.org (Vaibhav Mehra) | https://www.youtube.com/watch?v=jGg_1h0qzaM | The best free LangGraph foundation — 3h 10m, builds five agents ending in a RAG agent, with exercises and a full companion code repo. Your main video for concept 7. |
| Advice for Building Agents | OpenAI | https://www.youtube.com/watch?v=js4HRqmsDQE | OpenAI's own practical agent-design guidance; pairs directly with the OpenAI Agents SDK docs when you compare frameworks (concept 8). |
| Vibe Coding in Prod \| Code w/ Claude | Anthropic | https://www.youtube.com/watch?v=fHWFF_pnqDk | An Anthropic coding-agent researcher (co-author of "Building effective agents") on running agents in production: stress-testing, I/O verification, context compaction, human oversight. The perfect practical companion to the written guide. |
| Build a Multi-Agent System with CrewAI \| Agentic AI Tutorial | Generative AI | https://www.youtube.com/watch?v=qsrl2DHYi1Y | Step-by-step CrewAI walkthrough — a good first taste of role-based multi-agent orchestration for concept 8. |
| Agentic AI with LangGraph and MCP Crash Course – Part 1 | Krish Naik | Search YouTube for "Agentic AI with LangGraph and MCP Crash Course Part 1" | Covers the full arc in one sitting: LangGraph building blocks → ReAct agent → memory, streaming, human-in-the-loop → building an MCP server from scratch. |
| The Ultimate MCP Crash Course – Build From Scratch | Web Dev Simplified | Search YouTube for "The Ultimate MCP Crash Course Build From Scratch" | Builds both an MCP server and an MCP client from scratch — the clearest way to understand what the protocol actually does on the wire. |

*Bonus:* freeCodeCamp's "How to Build Advanced AI Agents – LiveKit, Exa, LangChain" (1h) walks through three mini-projects, including a Perplexity-style research assistant: https://www.freecodecamp.org/news/how-to-build-advanced-ai-agents/

### X (Twitter)

| Handle | URL | Why follow |
|---|---|---|
| Harrison Chase — @hwchase17 | https://x.com/hwchase17 | LangChain/LangGraph founder and CEO. Framework releases, agent architecture threads, production lessons. The single most important account for the LangGraph ecosystem. |
| Anthropic — @AnthropicAI | https://x.com/AnthropicAI | Agent SDK and Claude Code releases, MCP ecosystem news, and links to the engineering blog posts you're reading this phase. |
| João Moura — @joaomdmoura | https://x.com/joaomdmoura | CrewAI founder/CEO. Multi-agent orchestration, enterprise agent deployments, and honest founder notes on building in the agent space. |
| Andrew Ng — @AndrewYNg | https://x.com/AndrewYNg | Announces DeepLearning.AI short courses on agentic design patterns and frames agent concepts for learners. |
| Logan Kilpatrick — @OfficialLoganK | https://x.com/OfficialLoganK | Leads Google AI Studio/Gemini API (ex-OpenAI DevRel). Insider view of agent tooling and ecosystem shifts from both OpenAI and Google. |
| Peter Steinberger — @steipete | https://x.com/steipete | Open-source agentic builder; candid, technically grounded posts on agentic engineering workflows. |

### Docs, blogs & repos

| Resource | URL | Why use it |
|---|---|---|
| Anthropic — "Building effective agents" | https://www.anthropic.com/engineering/building-effective-agents | THE canonical taxonomy: workflows vs. agents, the five workflow patterns, the "simplest possible solution" principle. Read before writing any agent code. |
| Anthropic — "How we built our multi-agent research system" | https://www.anthropic.com/engineering/multi-agent-research-system | Production lessons on orchestrator-worker multi-agent design — a preview of where your ERP routing is headed. |
| Microsoft — "AI Agents for Beginners" (GitHub course) | https://github.com/microsoft/ai-agents-for-beginners | Free 18-lesson curriculum: design patterns, tool use, agentic RAG, multi-agent, MCP/A2A protocols, with code samples. Use it as your self-study backbone. |
| freeCodeCamp — "How to Develop AI Agents Using LangGraph" | https://www.freecodecamp.org/news/how-to-develop-ai-agents-using-langgraph-a-practical-guide/ | Written walkthrough of tools → state → graph → loop, building a real finance agent. |
| LangGraph docs & repo | https://docs.langchain.com/oss/python/langgraph/overview · https://github.com/langchain-ai/langgraph | Official reference for your primary framework. |
| OpenAI Agents SDK | https://developers.openai.com/api/docs/guides/agents · https://github.com/openai/openai-agents-python | Docs hub plus a repo with a quickstart — your second framework for comparison. |
| CrewAI docs & repo | https://docs.crewai.com/ · https://github.com/crewAIInc/crewAI | Role-based agents, tasks, and YAML scaffolding — worth skimming even if you don't adopt it. |
| Claude Agent SDK | https://code.claude.com/docs/en/agent-sdk/overview · https://github.com/anthropics/claude-agent-sdk-typescript | Programmatic access to Claude Code's file editing, command execution, sessions, and MCP support. |
| AutoGen repo + migration guide | https://github.com/microsoft/autogen · https://learn.microsoft.com/en-us/agent-framework/migration-guide/from-autogen/ | Read for concepts only — Microsoft is migrating AutoGen users to the Agent Framework, so check current status before investing time. |
| MCP introduction & reference servers | https://modelcontextprotocol.io/introduction · https://github.com/modelcontextprotocol · https://github.com/modelcontextprotocol/servers | Official spec, SDKs, and a collection of reference servers to learn from. |
| Anthropic — "Introducing the Model Context Protocol" | https://www.anthropic.com/news/model-context-protocol | The original announcement — explains the "why" behind MCP's design. |
| DeployHQ — "Build Your First MCP Server" | https://www.deployhq.com/blog/build-your-first-mcp-server-model-context-protocol-guide | Practical Python walkthrough connecting a custom server to Claude Desktop and Claude Code — follow it for the build gate below. |

## Hands-on build gate: the Pocket Research Agent

You don't advance to Phase 2 until this works. Build the **same agent three times** over 2–3 evenings — the repetition is the point, because each layer teaches you something frameworks hide.

1. **From scratch (~100 lines, no framework).** A CLI agent with a `while` loop and three tools you write yourself: `web_search` (Tavily, Serper, or DuckDuckGo), `read_notes`/`write_notes` against a local markdown file, and `calculator`. Give it a system prompt ("You are a research assistant; always cite sources; save findings to notes"), a max-iterations stopping condition (10 is fine), and print every tool call. Task it with: *"Research the current state of small language models for on-device agents and save a 5-bullet summary with sources."*
2. **Rebuild in LangGraph.** Recreate the identical agent as a StateGraph (agent node + tool node + conditional edge), add a checkpointer so conversation memory survives across runs, and add one human-in-the-loop interrupt requiring your approval before any `write_notes` call. Turn on LangSmith tracing and inspect the run step by step.
3. **Rebuild one tool as an MCP server.** Move `web_search` into a standalone MCP server (Python or TypeScript SDK), register it in Claude Desktop or Claude Code, and verify Claude can call it. Then connect the same server to your LangGraph agent. You now understand the whole stack: loop → framework → protocol.

**Stretch:** add a second "critic" agent (the evaluator-optimizer pattern) that reviews the summary before it's saved.

## Common pitfalls

1. **Reaching for a framework before writing the raw loop.** Frameworks abstract away the message history — which is exactly where you'll debug every production failure. Do step 1 of the build gate first, no exceptions.
2. **Building an agent where a workflow (or one LLM call) suffices.** Anthropic's golden rule: a well-prompted single call beats a workflow, a workflow beats an agent, and one agent with good tools usually beats a crew. Complexity must earn its place.
3. **Sloppy tool descriptions.** The model chooses tools based on their names and descriptions, not their code. Vague schemas cause wrong-tool calls more reliably than any model limitation does.
4. **No stopping condition.** An agent loop without max iterations, a human approval gate, or tracing is a runaway API bill waiting to happen. Instrument from day one.
5. **Building on AutoGen without checking its status.** It's in maintenance mode while Microsoft migrates users to the Agent Framework — learn its ideas, but put new projects on LangGraph, the OpenAI Agents SDK, or CrewAI instead.

## Checkpoint — you're ready for Phase 2 when you can

- Explain, without notes, the difference between a workflow and an agent — and name a task in your ERP that should stay a workflow.
- Write a ~100-line agent loop in raw Python with tool calling, a system prompt, and a max-iterations stop, from memory.
- Rebuild that agent as a LangGraph StateGraph with checkpointed memory and a human-in-the-loop approval interrupt, and read its LangSmith trace.
- Stand up a minimal MCP server, register it in Claude Desktop/Code, and consume it from your own agent.
- Name all five canonical workflow patterns and justify the simplest one for a given problem — including which pattern your ERP query router will use.
