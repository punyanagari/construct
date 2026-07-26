# Phase 5 — Token Optimization

## What it is and why it matters

In an agentic system, token spend **compounds**: a 10-iteration tool-calling loop resends its full context — system prompt, tool schemas, accumulated tool outputs — on every step, so one 50K-token context costs 50K input tokens *per iteration*, not per task. For a SaaS ERP with multi-agent routing, that compounding happens once per agent per query, 24/7. Token optimization attacks this in a fixed order: **measure → cache → compress → right-size models → structural changes** — measure first because you can't optimize what you can't see, cache and compress next because they're cheap config-level wins, structural surgery last. Cross-provider evaluation of 500+ agent sessions shows this stack delivers 45–80% cost cuts (arXiv:2601.06007), and practitioners report 78–91% total reductions when routing, pre-filtering, and compression are layered on top.

## Core concepts, in learning order

### 1. Measurement: count tokens before you spend them

Tokens are the unit of price, context limits, and truncation — count them locally *before* calling the API. Use **tiktoken** (https://github.com/openai/tiktoken) for offline counting and cost forecasting; the Cookbook notebook (https://cookbook.openai.com/examples/How_to_count_tokens_with_tiktoken.ipynb) covers tool calls and structured-output schema overhead too. On the response side, read the `usage` object on every call: `input_tokens`, `output_tokens`, and crucially `cached_tokens` / `cache_read_input_tokens` — only `cached_tokens > 0` proves a cache hit. Know your pricing tiers: on Anthropic, cache reads cost ~0.1× input and writes ~1.25×; OpenAI cache reads are ~50% off. Track cost per agent run, per step, per model (LangSmith, Helicone, or a 20-line callback). **Cache hit rate** is the single most important cost metric for agents — the Claude Code team monitors it like uptime and declares SEVs when it drops.

### 2. Prompt caching: the biggest single lever

Caching reuses KV computations for an *exact prefix match*: one changed character near the top invalidates everything after it. A 2026 cross-provider evaluation measured 45–80% input-cost reduction on long-horizon agent tasks (https://arxiv.org/abs/2601.06007). The mechanics differ per provider:

- **Anthropic (explicit):** mark blocks with `cache_control: {"type": "ephemeral"}`, up to 4 breakpoints, minimum 1,024 tokens (2,048 for Haiku), 5-minute TTL (1-hour option). Write ≈1.25× input price, read ≈0.1×. On newer models, cache reads don't count against your input-tokens-per-minute rate limit. Docs: https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
- **OpenAI (automatic):** no code changes for prompts ≥1,024 tokens; hits come in 128-token increments. Use `prompt_cache_key` to improve cache routing. Guide: https://developers.openai.com/api/docs/guides/prompt-caching and Cookbook "Prompt Caching 201" (https://developers.openai.com/cookbook/examples/prompt_caching_201).
- **Gemini (implicit + explicit):** implicit caching auto-applies on Gemini 2.5+ with a 75% discount (min ~1,024–2,048 tokens); the explicit `cachedContents` API guarantees savings but bills TTL-based *storage* — don't leave caches open. Docs: https://ai.google.dev/gemini-api/docs/caching and https://developers.googleblog.com/gemini-2-5-models-now-support-implicit-caching/

### 3. Cache-safe context layout

Because caching is prefix-exact, the layout rule is: **static decision context first, dynamic operational context last** — Phase 4's context engineering applied to token economics. System prompt, tool definitions, and reference docs go at the front; the user turn, timestamps, and volatile state go at the tail. The Claude Code team's operational rules (from Thariq Shihipar's thread): never edit the system prompt mid-session — pass updates via `<system-reminder>` messages; don't swap models or tool sets mid-session — use subagents or `defer_loading` tool stubs; compaction/fork calls must reuse the parent's exact prefix or you pay full price for the whole history. And beware the 5-minute TTL: stepping away mid-session means the next message reprocesses everything.

### 4. Context compaction

When the window fills, evict in tiers from cheapest to most lossy: (a) prune or replace old tool outputs first, (b) truncate oversized file reads, (c) full LLM summarization of the conversation — most expensive, lossiest. Claude Code's `/compact`, auto-compact (~95% capacity), and microcompact are the reference implementation. Quality degrades after repeated compactions, so compact early, pass focus instructions, and externalize durable state to files (the `plan.md` / `tasks.md` pattern). Deep dive: https://y-agent.github.io/inside-claude-code/04-context-compaction.html; cross-tool comparison: https://gist.github.com/badlogic/cd2ef65b0697c4dbe2d13fbecb0a0a5f.

### 5. Prompt compression

Microsoft's **LLMLingua / LongLLMLingua / LLMLingua-2** (https://github.com/microsoft/LLMLingua) uses a small LM to score token importance and drop low-value tokens — up to 20× compression with minimal quality loss on in-context-learning and summarization prompts. Caveat: reasoning and math tasks degrade at aggressive ratios, so always test against an uncompressed baseline first.

### 6. Tool-output truncation

Tool results are the silent budget-killer. Cap shell/grep/web outputs (a ~1,000-token head+tail cap is a good default), strip boilerplate — Sonnet's "dynamic filtering" does this automatically for web search, saving 24% — and prune unused MCP tool schemas: each connected server can add thousands of tokens *per message*.

### 7. Model right-sizing

Most agent steps — classification, extraction, formatting, routing, simple edits — don't need a frontier model. Route them to Haiku/Flash/mini-class models and reserve the flagship for reasoning-heavy synthesis (your ERP Query Router is the perfect first candidate). Workflow: audit every call, score each task (reasoning complexity, output sensitivity, context length), then test the cheaper model on 30–50 representative inputs before switching. Even 60% of traffic on a cheaper tier produces large savings. Counterintuitive note: a bigger, well-cached model can end up cheaper than a smaller uncached one — cache hit rate beats list price.

### 8. Batching

OpenAI's and Anthropic's Batch APIs give a flat ~50% discount for async workloads: nightly ERP summarization, backfills, bulk classification. Never batch real-time requests.

### 9. Structured outputs and output-side savings

Output tokens cost more than input, so shrink them: tight structured-output schemas, brevity instructions ("write the code without explanation"), `MAX_OUTPUT_TOKENS` caps, and Anthropic's token-efficient tool use beta — up to 70% fewer output tokens on tool calls (https://claude.com/blog/token-saving-updates).

### 10. Claude Code session hygiene

Claude Code is likely your daily driver by now, and cutting its token usage drastically is a discipline of its own — here is the concrete checklist, combining the team's own guidance with reported 77–91% cost-reduction practice (e.g., 87% via input pre-filtering: https://www.youtube.com/watch?v=zAsg3G_iZMw; 78%+ via model cascades, compression, and observability: https://www.ai-jason.com/learning-ai/how-to-reduce-llm-cost):

- **Lean CLAUDE.md (<200 lines).** It is loaded on every single message; every line is a per-turn tax. Keep it to stable, path-agnostic rules.
- **Path-scoped rules.** Move module-specific instructions into scoped rule files so they load only when you touch that part of the repo, instead of inflating every session.
- **`.claudeignore`** for `node_modules`, build output, and logs so they never enter context.
- **Disconnect unused MCP servers** — each one injects its tool schemas into every message.
- **Filter and truncate tool output**: pipe long shell output through `head`/`tail`/`grep` before it lands in context; use subagents for large file reads so contents stay out of your main context.
- **One session per task.** Context cost compounds every turn, so `/clear` between unrelated tasks; use plan mode first, because wrong-path rewrites are the biggest token sink; be surgically specific ("check `verifyUser` in `auth.js`", not "find the bug").
- **Use `--print` headless mode** for one-shot/CI tasks, route mechanical work to Haiku, and monitor with `/context` and `/usage`. Reference: https://code.claude.com/docs/en/context-window and https://ryandoser.com/claude-code-usage-tips/.

## Study resources

### YouTube

| Video | Channel | Length | Why watch it | Link |
|---|---|---|---|---|
| "Give Me 10 Mins and I'll Save You Millions of Claude Tokens" | Nate Herk \| AI Automation | 10:43 | Practical Claude Code token-saving habits and where caching kicks in automatically. Best first watch. | https://www.youtube.com/watch?v=6cEQEba0i2A |
| "What is Prompt Caching? Optimize LLM Latency with AI Transformers" | IBM Technology | 9:06 | The prefill/KV-pair mechanics behind caching — the conceptual foundation before touching provider APIs. | https://www.youtube.com/watch?v=u57EnkQaUTY |
| "Your AI credits are vanishing — here's the fix" | Burke Holland (+2 co-creators) | 13:20 | Chaptered demo of prompt caching live in GitHub Copilot, including "what breaks the cache." | https://www.youtube.com/watch?v=TYOhNRp5n7Y |
| "How to Save Tokens in Codex & Claude Code (Prompt Caching)" | Rachel noCode | 8:02 | Cross-tool comparison (Codex, Claude Code, Cursor, OpenCode) — shows the technique generalizes beyond one vendor. | https://www.youtube.com/watch?v=Ip5fsigtcR8 |
| "How I cut token costs by 90%: AI cost optimization guide" | PropTech Founder | 19:51 | Production case study (~$1M/yr claimed saved) walking the full optimization stack end-to-end. | https://www.youtube.com/watch?v=4x4nM0uPmg0 |
| "Token Cost Reduction through LLMLingua's Prompt Compression" | AI Anytime | 37:45 | Hands-on LLMLingua walkthrough with code — your go-to for the compression stage. | https://www.youtube.com/watch?v=xLNL6hSCPhc |

### X (Twitter)

| Account | Why follow | Link |
|---|---|---|
| Thariq Shihipar (@trq212) | Claude Code team at Anthropic. His verified thread "Lessons from Building Claude Code: Prompt Caching Is Everything" (prefix ordering, `<system-reminder>` updates, `defer_loading`, cache-safe compaction, "monitor cache hit rate like uptime") is the most-cited primary source on agent token economics. | https://x.com/trq212 · thread: https://x.com/trq212/status/2024574133011673516 |
| Boris Cherny (@bcherny) | Creator/head of Claude Code; posts his own setup and context/token-efficiency patterns (plan mode, subagents, CLAUDE.md discipline). | https://x.com/bcherny |
| Simon Willison (@simonw) | Amplified and annotated the prompt-caching lessons; relentless practical experiments on LLM tooling and token costs. | https://x.com/simonw |
| Numman Ali (@nummanali) | Viral compaction-survival thread (97K+ views): start sessions in Plan Mode + request a persistent To-Do list so plans survive compaction. | https://x.com/nummanali/status/2010042788566720955 |

### Docs & blogs

| Resource | What you get | Link |
|---|---|---|
| Anthropic — Prompt caching | cache_control, breakpoints, TTLs, minimums, pricing | https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching |
| OpenAI — Prompt caching guide | Automatic caching, `prompt_cache_key`, explicit breakpoints | https://developers.openai.com/api/docs/guides/prompt-caching |
| OpenAI Cookbook — Prompt Caching 201 | Measurement and cache-hit optimization strategies | https://developers.openai.com/cookbook/examples/prompt_caching_201 |
| Gemini API — Context caching | Implicit vs explicit caching, storage billing | https://ai.google.dev/gemini-api/docs/caching |
| Claude Code — Explore the context window | What loads into context, what survives compaction, `/context` & `/compact` | https://code.claude.com/docs/en/context-window |
| tiktoken repo | Offline token counting for cost forecasting | https://github.com/openai/tiktoken |
| microsoft/LLMLingua | Prompt compression framework (up to 20×) | https://github.com/microsoft/LLMLingua |
| awesome-llm-token-optimization | Curated strategies with a savings/effort table | https://github.com/pleasedodisturb/awesome-llm-token-optimization |
| "Prompt Caching Is Everything" (summary) | Faithful write-up of Thariq's thread — the best single read here | https://blog.devaubree.fr/en/blog/prompt-caching-claude-code/ |
| "How prompt caching actually works" (mager.co) | The "[stable prefix][new tail]" mental model and silent invalidators | https://mager.co/blog/2026-04-29-claude-prompt-caching/ |
| arXiv:2601.06007 | 500+ agent sessions across three providers: 45–80% cuts; strategic cache boundaries beat naive full-context caching | https://arxiv.org/abs/2601.06007 |
| Lance Martin — Agent design patterns | Cache context vs isolate context; hit rate as the top production metric | http://rlancemartin.github.io/2026/01/09/agent_design/ |

## Hands-on build gate: "Cut My Agent's Token Bill in Half"

Take the tool-calling agent you built in earlier phases (or build a ~100-line research/Q&A agent: ~1,500-token system prompt, 2–3 tools, loop capped at 10 iterations, mid-tier model) and cut its cost per task by **≥50%** with measurement at every step.

1. **Instrument.** Log per-call `input_tokens`, `output_tokens`, `cached_tokens`; count prompts locally with tiktoken; compute cost per task from a pricing table. Run 20 fixed benchmark tasks and record the baseline.
2. **Pass 1 — Cache.** Move all static content to the front; add `cache_control` breakpoints (Anthropic) or `prompt_cache_key` (OpenAI); strip timestamps from the prefix. Verify hits via `cached_tokens > 0`. Expect 40–80% input-cost reduction on multi-turn runs.
3. **Pass 2 — Truncate & compact.** Cap every tool result at ~1,000 tokens (keep head+tail); replace tool outputs older than 3 turns with a placeholder; summarize history past a budget. Confirm no quality regression >2 points on your benchmark.
4. **Pass 3 — Right-size.** Route classification/extraction/formatting steps to Haiku/mini after testing on 30 representative subtask inputs; keep the flagship for final synthesis.
5. **Pass 4 — Structured outputs.** Tight schemas, "output only the result" instructions, token-efficient tool use where available.

**Deliverable:** a before/after table — cost/task, tokens/task (in/out/cached), iterations/task, quality score — plus a short write-up naming which lever contributed most. Gate: ≥50% cost cut with ≤2-point quality drop. Stretch: move the nightly summary job to a Batch API for another 50% off that workload.

## Common pitfalls

- **Cache-busting layouts.** A timestamp, random ID, or edited system prompt near the top silently invalidates everything after it — you pay full price and only notice if you watch `cached_tokens`. Verify hits on every run, not just the first.
- **Premature compression.** LLMLingua at aggressive ratios and repeated full-history summarization both erode reasoning quality. Prune tool outputs first, truncate second, summarize last, and always test against an uncompressed baseline. Small projects where everything fits in context can actually get *worse* with compression overhead.
- **Right-sizing without testing.** Swapping in a cheap model without a 30–50-input comparison trades invisible quality loss for visible savings.
- **Retrofitting late.** Cache-aware layout is an architectural constraint, not a bolt-on — design your ERP's agent harness cache-first now and avoid a painful rewrite later.

## Checkpoint for Phase 6

You pass this phase when your benchmark table shows a ≥50% cost reduction, `cached_tokens` is consistently non-zero across multi-turn runs, and you can explain with numbers which lever contributed most. In Phase 6, this cost discipline becomes a routing decision: picking the cheapest capable model for every request your ERP serves is the biggest structural lever of all — and you'll keep watching cache hit rate with the same SEV-style discipline the Claude Code team runs internally.
