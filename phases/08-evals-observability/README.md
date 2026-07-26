# Phase 8 — Evals & Observability *(new in roadmap v2)*

## What it is & why it matters

Every gate so far demanded measurement — the Context Gauntlet's accuracy curves, the token bill's before/after table, the Query Router's 60-query eval. This phase turns those one-off measurements into a discipline before the capstone multiplies agents, because an organization multiplies every *unmeasured* weakness: one loopy agent is annoying, twenty are a budget incident you can't see. The capstone's own #1 pitfall is "automating before evals exist" — so the harness gets built here, on the Phase 7 crew, and reused as-is in Mini ERP, Inc. For the SaaS ERP this is also product infrastructure: the regression harness you build this week is the same machinery that will stop a prompt tweak from silently breaking a customer's invoice flow.

## Core concepts, in learning order

1. **Eval-set construction.** Scripted scenarios with expected outcomes and labeled difficulty, sourced from real failure cases (your break logs from earlier phases are the seed corpus). Small and real beats large and synthetic.
2. **Exact-match vs LLM-as-judge.** Use exact-match wherever an answer is checkable; use a judge with an explicit rubric (factual accuracy, criteria compliance, source quality, tool efficiency) everywhere else. Judge the **end state, not the path** — multi-agent runs are non-deterministic by design, so two valid runs may use different tools in different orders.
3. **Judge calibration.** Hand-label ~20 samples yourself first, then measure judge agreement against your labels. An uncalibrated judge is vibes with extra steps.
4. **Tracing.** LangSmith or Langfuse with one shared trace ID across every agent in a run (OpenTelemetry-style), so a whole org run reads as one story. Per-agent cost and latency dashboards.
5. **The regression harness.** One command re-runs the full eval set and posts a scoreboard; it runs after *any* prompt or topology change. Without it, every tweak across N agents is a coin flip.
6. **Benchmark literacy.** When quoting SWE-bench/AutoGenBench-style numbers, always name the split, scaffold, and date — scores are meaningless without them.

## Study resources

### YouTube

| Title | Channel | URL | Why watch |
|---|---|---|---|
| You Can't Run AI Agents Without This | Matthew Berman | https://www.youtube.com/watch?v=rh_PcL26zls | Agent evaluation end-to-end — measure whether your loop works instead of shipping on vibes. |

### X (Twitter)

| Handle | URL | Why follow |
|---|---|---|
| @simonw | https://x.com/simonw | Relentless practical LLM experiments; consistently honest about what evals do and don't show. |
| @omarsar0 | https://x.com/omarsar0 | DAIR.AI founder; curates agent-evaluation papers and orchestration research weekly. |

### Docs & blogs

| Resource | URL | Why use it |
|---|---|---|
| Langfuse — AI agent observability | https://langfuse.com/blog/2024-07-ai-agent-observability-with-langfuse | Debugging thousand-observation traces; assembling multi-agent distributed traces via shared trace IDs. |
| LangChain Academy (LangSmith courses) | https://academy.langchain.com/ | Framework-author courses on evals, tracing, and deployment with LangSmith. |
| Anthropic — How we built our multi-agent research system | https://www.anthropic.com/engineering/built-multi-agent-research-system | The LLM-as-judge rubric and end-state-not-path evaluation lessons, from a production multi-agent system. |

## Hands-on build gate: the harness that catches a seeded regression

Build the eval harness **on your Phase 7 crew** (planner → executor → reviewer):

1. **Eval set.** 15–20 scripted scenarios with expected outcomes and difficulty labels — at least five drawn from your own break logs.
2. **Scoring.** Exact-match where checkable; LLM-as-judge with an explicit rubric elsewhere. Calibrate: hand-label 20 samples, report judge agreement.
3. **Tracing.** Langfuse or LangSmith on every run, one shared trace ID per crew run, per-agent cost and step counts on a dashboard.
4. **One-command regression run** that re-executes the full set and prints a scoreboard (pass rate, cost, p95 latency, per-scenario diffs vs last run).
5. **Prove it:** deliberately weaken one prompt (e.g., soften the reviewer's acceptance criteria) and show the harness flags the regression **before you can spot it in the outputs yourself**.

**Deliverable:** the harness code, the calibration numbers, and one scoreboard showing the seeded regression caught.

## Common pitfalls

- **Vibes-based judging.** No rubric + no calibration = a judge that agrees with whoever wrote the prompt.
- **Path-based evals on non-deterministic systems.** Scoring "did it call tool X then Y" fails by design; score the end state.
- **Building the harness after the org exists.** Retrofitting evals onto twenty agents means twenty times the instrumentation debt — this phase exists to prevent exactly that.

## Checkpoint — ready for Phase 9 when

- The harness catches the seeded regression, and you can show the scoreboard that proves it.
- Judge agreement with your own 20 hand-labeled samples is measured and reported.
- One command re-runs the whole suite; traces show one shared ID per crew run with per-agent costs.
