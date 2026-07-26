# Phase 2 — Loop Engineering

## What It Is & Why It Matters

Strip away every framework, and an agent is a `while` loop: the model receives the goal plus accumulated context, decides to reason, act, or answer, a tool call executes in real code, the result goes back into context, and the loop repeats. Perceive → reason → act → observe. This loop is the atomic unit of every agentic system you will build — including the multi-agent routing layer of your SaaS ERP. Every orchestrator-worker graph is a composition of these loops, so without a mental model of the loop you'll be debugging framework abstractions blind.

Just as important as *how* to loop is *when not to*. Anthropic's canonical taxonomy splits agentic systems into workflows — prompt chaining, routing, parallelization (sectioning or voting), orchestrator-workers, and evaluator-optimizer — versus true agents, where the model drives the loop itself. Their rule, now industry consensus: find the simplest solution possible, and add agentic autonomy only when it is *measurably* better. If you can pre-specify the steps, write a workflow — cheaper, deterministic, debuggable. Reach for a loop only when the number or shape of steps can't be known upfront, the task needs environment interaction, and occasional errors are tolerable. In your ERP, most request handling will be workflow-shaped routing; the loop earns its place in open-ended tasks like reconciliation. Signs you're over-looping: wildly varying token costs, frequent mid-task failures, inconsistent output structures.

## Core Concepts (Learn in This Order)

1. **ReAct (Reason + Act).** The foundational loop pattern from Yao et al.: interleave Thought → Action → Observation so reasoning traces let the model plan and recover, while actions ground it in the environment and fight hallucination. Learn the text-parsing flavor first (the model emits `Thought: ... Action: name: input`, your code regex-matches and executes), then the native tool-calling flavor (structured JSON function calls, possibly parallel per turn). The loop shape is identical; only the wire format changes.

2. **Tool-use loops and the tool-call contract.** Tools are structured outputs: the model emits JSON, deterministic code executes it, and a text observation comes back. Tool names, docstrings, and error strings are prompt engineering — Anthropic calls this surface the "agent-computer interface." The critical discipline: return errors *as observations*, never raise them, so the loop sees what went wrong and self-corrects on the next iteration.

3. **Retry and self-correction loops.** Feeding failure context back into the loop changes the model's next action — but only if you force it to think first. Before any retry, require a short reflection: "What specifically failed? What one change would fix it?" Without that gate, loops repeat the same failing call. Classify errors before deciding: retry 429/5xx with backoff; bail immediately on 401/403/422.

4. **Reflection (Reflexion).** Shinn et al. formalized self-correction as verbal reinforcement learning: generate → evaluate against *critical* criteria (not "is this good?") → write a structured lesson to an episodic memory buffer → regenerate. Measured results: 91% pass@1 on HumanEval versus GPT-4's 80% baseline, and production replications report roughly +34% output quality for about 1.6x token cost, with most tasks converging in two iterations.

5. **Loop guards — non-negotiable.** Defense in depth, four layers: **max iterations** (production values typically 15–25) with an "early stopping generate" — on hitting the cap, make one final no-tools call asking for the best answer so far; **wall-clock timeouts and per-step token/cost budgets**, watching for quadratic context growth; **stuck detection via fingerprinting** — hash the tool name plus a result preview, and three identical iterations means the loop is spinning; and **human-in-the-loop checkpoints** for irreversible actions like writing to your ERP's production tables.

6. **Evaluator-optimizer.** Anthropic's workflow version of reflection: a generator LLM and an evaluator LLM iterate against *explicit acceptance criteria* ("must pass all unit tests," "must cite tool evidence"). Two things separate this from aimless self-critique: concrete criteria and a loop guard. This pattern is your bridge from single loops to the structured workflows of later phases — the shape of quality control in any serious ERP agent.

## Study Resources

### YouTube

| Resource | What you get |
|---|---|
| [Building AI Agents in Pure Python — Beginner Course](https://www.youtube.com/watch?v=bZzyPscbtI8) (Dave Ebbelaar) | The best video companion to Anthropic's guide: ~47 minutes of raw-Python tools, prompt chaining, routing, and parallelization, ending in a working calendar agent. Build the loop yourself before touching any framework. |
| [What's next for AI agentic workflows ft. Andrew Ng](https://www.youtube.com/watch?v=sal78ACtGTc) (Sequoia Capital) | The ~14-minute talk that defined the four agentic patterns (reflection, tool use, planning, multi-agent) and argued an iterative loop around a weaker model beats a one-shot stronger model. |
| [What Anthropic Learned Building AI Agents in 2025](https://www.youtube.com/watch?v=TledrLrVUQI) (Cal Rueb, AWS re:Invent AIM277) | The most current update from Anthropic's Applied AI team: tool-design lessons for the loop, context engineering, and failure stories from Claude Code. |
| [You Can't Run AI Agents Without This](https://www.youtube.com/watch?v=rh_PcL26zls) (Matthew Berman) | Agent evaluation — the piece that closes the evaluator-optimizer loop. Measure whether your loop works instead of shipping on vibes. |
| [Learn to build effective Agentic AI systems](https://www.youtube.com/watch?v=w7vqXL4PWEE) (DeepLearning.AI, bonus) | Entry point to Andrew Ng's Agentic AI course (course page: https://www.deeplearning.ai/courses/agentic-ai) — the four patterns built from first principles in raw Python. |

Two AI Bites tutorials are excellent companions to the build gate but lack verifiable watch URLs: search YouTube for "Build an AI Agent from Scratch in Raw Python" and "Build a Reflection AI Agent from Scratch — Raw Python Implementation". Anthropic's "Vibe Coding in Prod | Code w/ Claude" video is assigned to Phase 1 — revisit it for its lessons on where humans must stay inside production agentic loops.

### X (Twitter)

| Account | Why follow |
|---|---|
| [@dexhorthy](https://x.com/dexhorthy) (Dex Horthy) | HumanLayer founder, author of 12-Factor Agents. The strongest production voice on loop discipline: own your control flow, keep agents under ~20 steps. |
| [@ShunyuYao12](https://x.com/ShunyuYao12) (Shunyu Yao) | Author of ReAct, co-author of Reflexion, Tree of Thoughts, and SWE-bench. Follow the source of the loop patterns themselves. |
| [@lilianweng](https://x.com/lilianweng) (Lilian Weng) | Author of the canonical agent survey; ex-OpenAI safety. Low posting frequency, high signal on agent and reasoning research. |
| [@swyx](https://x.com/swyx) (Shawn Wang) | Latent Space editor and "AI Engineer" movement founder. Curates harness engineering and talks from the people building the loops. |
| [@hwchase17](https://x.com/hwchase17) (Harrison Chase) | LangChain/LangGraph co-founder. Posts on agent harnesses, context engineering, and evaluators for long-horizon agents. |

### Docs & Blogs

| Resource | Why read it |
|---|---|
| [Building effective agents — Anthropic](https://www.anthropic.com/engineering/building-effective-agents) | The core reference: workflows vs. agents, the five patterns, and the "simplest solution first" rule. Read first. |
| [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) (code: https://github.com/ysymyth/ReAct) | The paper behind the loop. Study the Thought/Action/Observation traces. |
| [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366) | Reflection loops with episodic memory; the basis for your evaluator-optimizer build. |
| [LLM Powered Autonomous Agents — Lilian Weng](https://lilianweng.github.io/posts/2023-06-23-agent/) | Definitive survey of planning (including self-reflection), memory, and tool use. |
| [Agents — Chip Huyen](https://huyenchip.com/2025/01/07/agents.html) | Tools taxonomy, planning patterns, and agent failure modes. |
| [12-Factor Agents — HumanLayer](https://github.com/humanlayer/12-factor-agents) | The anti-framework manifesto: own your control flow and context window. |
| [The Anatomy of an Agent Loop — Steve Kinney](https://stevekinney.com/writing/agent-loops) | The best single write-up of loop guards: budgets, fingerprinting, error classification. |
| [A practical guide to building agents — OpenAI](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/) | When single- vs. multi-agent, guardrails, and orchestration decisions. |
| [Let's Build an AI Agent from Scratch in Raw Python — AI Bites](https://www.ai-bites.net/lets-build-an-ai-agent-from-scratch-in-raw-python/) | Full ReAct implementation with code — the reference for Step 1 of your build gate. |

## Hands-On Build Gate: From ReAct to Reflection in ~100 Lines

Do not advance to Phase 3 until this works. Stack: Python 3.12, one LLM API key (OpenAI or Anthropic SDK), `httpx`. No frameworks.

**Step 1 — ReAct loop from scratch (~80–100 lines).** Write a `ChatBot` class holding `messages` with a `__call__` that appends and queries the LLM. Add three plain-function tools: `wikipedia(q)` (MediaWiki API), `calculate(expr)`, and `arxiv_search(q)`. Write the ReAct system prompt ("You run in a loop of Thought, Action, PAUSE, Observation…") with one few-shot example and the tool list. Then `Agent.run(question)`: loop up to `max_turns`, regex-match `Action: name: input`, execute, feed back `"Observation: …"`, return when no action is emitted.

**Step 2 — Add loop guards.** Set `max_turns = 10`, a wall-clock budget, and a token counter; on hitting the cap, make one final no-tools call: "Give your best answer so far." Log every Thought/Action/Observation to a trace file. Now deliberately try to get the agent stuck — give it a tool that always errors — and watch the trace. Then add identical-action detection (fingerprint the last three tool calls) and a forced reflection prompt before each retry.

**Step 3 — Wrap it in an evaluator-optimizer.** Pair a generator with a critic: generate an answer, have the critic score it against explicit criteria (correctness, completeness, cites tool evidence), and if below threshold, append the critique and regenerate — max three iterations. Run ~10 questions through both the single-pass and reflection versions and record the quality improvement and token multiplier. You've now measured this phase's central tradeoff with your own numbers.

**Deliverable:** one file, ~150–200 lines with comments, plus a short write-up: what made the loop fail, and which guard fixed it?

## Common Pitfalls

- **Infinite loops.** An agent with no `max_turns` cap will happily call the same failing tool forever — especially text-parsing ReAct agents whose regex silently fails to match. Every loop you ever ship needs a hard iteration ceiling and an early-stopping-generate fallback.
- **Runaway cost.** Each iteration re-sends the entire conversation, so token usage grows quadratically with loop length. A 25-turn agent can cost 20x a single call. Set per-run token and dollar budgets, and treat wildly varying costs across runs as a signal that the task wants a workflow, not a loop.
- **No observability.** If you can't answer "why did the agent do that?" from a trace, you don't have an agent — you have a slot machine. Log every iteration from day one; when a loop misbehaves, debug the trace, not the prompt by vibes.

## Checkpoint for Phase 3

You're ready for multi-agent orchestration when you can: (1) implement the perceive-reason-act-observe loop from scratch without a framework; (2) articulate when a structured workflow beats an agentic loop, with cost/failure evidence to back the call; (3) show your guarded ReAct agent surviving a deliberately broken tool; and (4) present measured quality-vs-token numbers from your evaluator-optimizer wrapper. Next up: Phase 3 composes your loops into explicit, checkpointable graphs — the state machines your ERP's multi-agent architecture (and its Phase 6 routing layer) will be built on.
