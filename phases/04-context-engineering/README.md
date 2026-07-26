# Phase 4 — Context Engineering

## What It Is & Why It Matters

In Phase 2 you learned to control what the model does *inside* the context window — the wording of prompts, instructions, and tool calls; in Phase 3 you made the control flow around those calls explicit. Context engineering is the step above both: deciding what fills the window in the first place. Andrej Karpathy defined it as "the delicate art and science of filling the context window with just the right information for the next step" (June 2025). Shopify CEO Tobi Lütke, whose tweet pushed the term mainstream days earlier, framed it as "the art of providing all the context for the task to be plausibly solvable by the LLM." Prompt engineering is a subset of context engineering — you cannot write a good prompt for a window stuffed with the wrong information.

This phase is the pivot point of the entire roadmap. Everything you built in Phases 1–3 (loops, routing, tools) culminates here, and everything after it depends on it. Phase 5's token optimization techniques all manipulate the context window — caching, compaction, trimming are context-engineering moves. The multi-agent isolation strategies of Phases 6–7 are literally the "Isolate" strategy you'll learn in this phase scaled up. Skip this phase, and later phases become recipe-copying: you'll paste in a multi-agent template without understanding *why* the sub-agents need fresh windows. Timebox this phase to 1–2 weeks and treat it as the "why your agent broke at turn 15 and how to fix it" module of the whole curriculum.

## Core Concepts — Learn in This Order

### Stage 1: The Mental Model — What Fills the Window

"Context" is everything the model sees on each inference call: the system prompt, conversation history, memory, retrieved documents (RAG), tool definitions and tool outputs, and any structured output schema. Karpathy's OS analogy makes the constraint concrete: the LLM is the CPU and the context window is RAM — finite working memory that you must actively curate. Anthropic's framing gives you the objective function: your job is to assemble "the smallest set of high-signal tokens that maximize the likelihood of the desired outcome." Every technique in this phase is a way of moving closer to that smallest set.

### Stage 2: Failure Modes — Why This Discipline Exists

Before techniques, learn what goes wrong. **Context rot**: quality degrades as input length grows, well before the hard token limit. Chroma Research tested 18 frontier models and found every one degrades at every length increment — there is no safe "big window." **Lost in the middle**: models exhibit U-shaped attention, attending to the start and end of context while missing the middle (Liu et al., arXiv:2307.03172) — so *position* matters as much as *presence*. And Drew Breunig's four named failures, popularized by LangChain: **poisoning** (a hallucination enters context and compounds), **distraction** (bloated history over-weights the past and the goal is forgotten), **confusion** (too many tools or schemas degrade decisions), and **clash** (contradictory sources in context). These are the bugs your engineered agent must be immune to.

### Stage 3: Static Context Design

Start with the parts of context that don't change per turn. System prompts should sit at the "right altitude" — specific enough to guide behavior, not so brittle they hard-code heuristics that break on edge cases — and should keep a stable prefix for cacheability. Tool design is context design: prefer fewer, well-scoped, token-efficient tools, because bloated tool lists cause context confusion. Manus's production lesson is counterintuitive: mask tools (hide them from the model) instead of removing them mid-task, because mutating the tool list breaks the KV-cache prefix.

### Stage 4: The Four Strategy Pillars — Write, Select, Compress, Isolate

LangChain's taxonomy is your organizing framework:

- **Write (offload):** persist state *outside* the window — scratchpads, a `todo.md` file, memory stores. Manus's "recitation" trick: having the agent rewrite its todo list keeps goals inside the recent attention span.
- **Select (retrieve):** RAG done well means targeted, reranked retrieval, not naive top-20 dumping. Prefer **just-in-time context**: keep lightweight references (file paths, queries, links) in the window and load the data at runtime via tools.
- **Compress (compact):** summarize or trim old conversation turns, clear stale tool outputs. Dex Horthy's rule for coding agents: practice "frequent intentional compaction," keeping context utilization around 40–60% and splitting work into research → plan → implement phases with compact artifacts passed between them.
- **Isolate:** give sub-agents fresh, scoped context windows that return 1–2k-token summaries. Isolation is excellent for parallel *read*/research tasks and risky for *write* tasks that need one coherent author — the same tradeoff you'll revisit when you design your ERP's multi-agent routing in Phase 6.

### Stage 5: Memory Architecture

Distinguish **short-term memory** (thread-scoped state: checkpoints, sliding windows, summary memory) from **long-term memory** (cross-session persistence, organized by the CoALA taxonomy: semantic facts, episodic experiences, procedural skills). Decide deliberately whether memory writes happen on the hot path or in the background. And learn Manus's "keep the wrong stuff in" principle: preserving error traces in context enables recovery — erasing failure removes the evidence the model needs to avoid repeating it.

### Stage 6: KV-Cache Economics & Evaluation

This is where context engineering meets production cost. Append-only context, no timestamps in prefixes, stable ordering of components — these habits determine your KV-cache hit rate, which Manus calls the single biggest cost and latency lever (they rebuilt their framework four times around it). Finally, evaluate at realistic fill levels: traces are the source of truth for what was actually in context at each step, and benchmark scores measured on nearly-empty windows tell you nothing about production behavior.

## Study Resources

### YouTube (watch in this order)

| # | Video | Channel / Speaker | Why watch it | URL |
|---|-------|-------------------|--------------|-----|
| 1 | How Agents Use Context Engineering | LangChain | Best first watch — offloading, reducing, and isolating context with framework-level framing | https://www.youtube.com/watch?v=XFCkrYHHfpQ |
| 2 | Context Engineering for AI Agents with LangChain and Manus | Lance Martin (LangChain) + Yichao "Peak" Ji (Manus) | The single best deep dive — KV-cache hit rate, tool masking, file-system context, recitation, from the person who wrote the famous post | https://www.youtube.com/watch?v=6_BcCthVvb8 |
| 3 | Advanced Context Engineering for Agents | Dex Horthy, YC Root Access | The "dumb zone" (>40% context use = worse outcomes), frequent intentional compaction, research → plan → implement workflows | https://www.youtube.com/watch?v=IS_y40zY-hc |
| 4 | Context Engineering for Agents | Lance Martin, Latent Space | The five context categories, agentic search vs classical retrieval, and the "bitter lesson" of AI engineering | https://www.youtube.com/watch?v=_IlTcWciEC4 |
| 5 | Tips for building AI agents | Anthropic | Pairs with Anthropic's context-engineering post; strong on tool design and agent-loop context hygiene | https://www.youtube.com/watch?v=LP5OCa20Zpg |

*(Bonus for Mandarin speakers: Hung-yi Lee's rigorous lecture "AI Agent (1/3)：核心技術 Context Engineering" — https://www.youtube.com/watch?v=urwDLyNa9FU)*

### X (Twitter) — Who to Follow

| Handle | Who | Why follow | URL |
|--------|-----|------------|-----|
| @karpathy | Andrej Karpathy | The canonical definition and LLM-as-OS mental model; founding tweet: https://x.com/karpathy/status/1937902205765607626 | https://x.com/karpathy |
| @tobi | Tobi Lütke (Shopify CEO) | Made "context engineering" mainstream; champions DSPy as his tooling | https://x.com/tobi |
| @RLanceMartin (following since Phase 3) | Lance Martin (LangChain) | Author of the Write/Select/Compress/Isolate taxonomy; meetup recap thread: https://x.com/RLanceMartin/status/1948441848978309358 | https://x.com/RLanceMartin |
| @dexhorthy (following since Phase 2) | Dex Horthy (HumanLayer) | The most practice-obsessed voice on compaction, sub-agents, and context budgets | https://x.com/dexhorthy |
| @_philschmid | Philipp Schmid (Google DeepMind) | "5 practical tips" thread: https://x.com/_philschmid/status/1982861526466707477 | https://x.com/_philschmid |

*(Honorable mentions: @simonw — https://x.com/simonw — on why the term sticks, and @hwchase17 — https://x.com/hwchase17, already on your list since Phase 1 — for ecosystem-level takes.)*

### Docs, Blogs, Repos & Papers

| # | Resource | Type | Why read it | URL |
|---|----------|------|-------------|-----|
| 1 | Lance Martin, "Context Engineering for Agents" | Blog (canonical #1) | The original Write/Select/Compress/Isolate taxonomy with diagrams | https://rlancemartin.github.io/2025/06/23/context_engineering/ |
| 2 | Manus, "Context Engineering for AI Agents: Lessons from Building Manus" | Blog (canonical #2) | Production lessons: KV-cache hit rate, tool masking, recitation, keep errors | https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus |
| 3 | Anthropic, "Effective context engineering for AI agents" | Blog (canonical #3) | Attention budget, compaction, structured note-taking, sub-agent architectures, just-in-time retrieval | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents |
| 4 | Chroma, "Context Rot" | Research (canonical #4) | The 18-model empirical study proving degradation at every length | https://research.trychroma.com/context-rot |
| 5 | Simon Willison, "Context engineering" | Blog | Sharp analysis of the term and how it differs from prompt engineering | https://simonwillison.net/2025/Jun/27/context-engineering/ |
| 6 | Drew Breunig, "How Contexts Fail" | Blog | The poisoning / distraction / confusion / clash taxonomy | https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html |
| 7 | LangChain, "Context Engineering for Agents" and "The Rise of Context Engineering" | Blog | Ecosystem framing | https://blog.langchain.com/context-engineering-for-agents/ and https://blog.langchain.com/the-rise-of-context-engineering/ |
| 8 | Philipp Schmid, "The New Skill in AI is Not Prompting, It's Context Engineering" | Blog | Concise practitioner summary | https://www.philschmid.de/context-engineering |
| 9 | LangChain/LangGraph, "Memory overview" | Docs | Short-term vs long-term memory in the framework you'll likely use | https://docs.langchain.com/oss/python/concepts/memory |
| 10 | Anthropic docs, "Context editing" | Docs | API-level clearing of old tool results | https://platform.claude.com/docs/en/build-with-claude/context-editing |
| 11 | microsoft/ai-agents-for-beginners — Lesson 12 | Repo/course | Free structured lesson with video and code; beginner-friendly on-ramp | https://github.com/microsoft/ai-agents-for-beginners/blob/main/12-context-engineering/README.md |
| 12 | langchain-ai/how_to_fix_your_context | Repo | Runnable examples of the four strategies | https://github.com/langchain-ai/how_to_fix_your_context |
| 13 | humanlayer/advanced-context-engineering-for-coding-agents | Repo | Dex Horthy's ace-fca.md with real research/plan/implement prompts | https://github.com/humanlayer/advanced-context-engineering-for-coding-agents |
| 14 | Liu et al., "Lost in the Middle" | Paper | The positional-attention evidence behind failure modes | https://arxiv.org/abs/2307.03172 |
| 15 | Mei et al., "A Survey of Context Engineering for LLMs" | Paper | The full academic map of the field | https://arxiv.org/abs/2507.13334 |
| 16 | Zhang et al., "Agentic Context Engineering (ACE)" | Paper | Incremental "playbook" context updates instead of rewrites | https://arxiv.org/abs/2510.04618 |

## Hands-On Build Gate: The Context Gauntlet

You don't advance to Phase 5 until you've *measured* context rot yourself and fixed it. Build one support agent two ways, in one evening (~150 lines of Python, LangGraph or a raw API loop).

**Setup:** simulate a user with 25+ multi-turn exchanges about an order issue. Plant key facts — "order #A-7742 is a replacement, not a refund" and "the user is allergic to latex" — at the *beginning* and the *middle* of the conversation. Attach 6–8 tools, two of which return needlessly large JSON blobs.

- **Version A (naive):** pass the full history and full tool outputs on every turn.
- **Version B (engineered):** add (1) short-term memory with a checkpointer, (2) a RAG store for order/policy docs retrieving top-3 reranked results rather than top-20, (3) compaction — summarize turns older than the last six into a rolling summary, offload full tool outputs to files and pass back references, (4) a long-term memory store for user facts (write-on-hot-path), and (5) as a stretch, a research sub-agent that returns findings as a summary (isolation).

**Measure — this is the whole point:** score both versions against a fixed 12-question eval set ("Was order #A-7742 a refund or replacement?") by exact match or LLM-judge. Track answer accuracy, input tokens per call, cost, and accuracy *as a function of where the relevant fact sits in context* (start / middle / end). Expected outcome: Version A degrades sharply after ~10 turns and misses middle-planted facts; Version B holds accuracy with 50–80% fewer tokens. Your deliverable is one page with the two accuracy-vs-context-length curves. That curve is your proof you understand this phase — and a template you can reuse when you evaluate your ERP agents later.

## Common Pitfalls

- **Dumping everything in.** Passing full history and full tool outputs "because the window is big enough" is the failure your Gauntlet curves just measured. Every irrelevant token competes for the attention budget; two noisy tools can poison an otherwise well-built agent (confusion). Curate, don't accumulate.
- **The bigger-window fallacy.** A 1M-token window does not buy you 1M tokens of usable attention. Chroma's 18-model study shows degradation at *every* length increment — context rot is a property of attention, not a quota. Engineering for the smallest high-signal token set beats paying for a larger window every time, on both quality and cost.
- **Deleting error traces.** Cleaning up the transcript to look tidy removes the evidence the model needs to recover; Manus keeps failures in deliberately.
- **Mutating the prefix mid-task.** Changing the system prompt or tool list between turns invalidates the KV-cache and silently multiplies your cost and latency — you'll quantify this in Phase 5.

## Checkpoint — You're Ready for Phase 5 When

You can state Karpathy's and Lütke's definitions and explain the OS/RAM analogy without notes; you can name all four context failures (poisoning, distraction, confusion, clash) and the Write/Select/Compress/Isolate strategies, mapping each failure to the strategy that fixes it; your Context Gauntlet report shows Version B holding accuracy across 25+ turns with a 50–80% token reduction; and you've felt, firsthand, why a fact planted mid-conversation gets missed. With that, Phase 5's token optimization — prompt caching, trimming, and cost engineering — will read as applied context engineering rather than a bag of tricks, and the sub-agent isolation of Phases 6–7 will feel like an obvious extension of what you just built.
