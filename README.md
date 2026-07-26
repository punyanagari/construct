# Construct

**Learning in public: from a first AI agent loop to a fully automated AI organization.**

This repo documents a structured journey through AI agent engineering — setup, loop engineering, graph engineering, context engineering, token optimization, AI routing, agent role assignment, evals & observability, and a capstone "AI organization" for full business automation (the end goal: a SaaS ERP with multi-agent routing).

## How this repo works

- **[ROADMAP.md](ROADMAP.md)** — the single source of truth: sequence rationale, per-phase missions, build gates + pass criteria, curated resources, and the 24-week timeline.
- **[PROGRESS.md](PROGRESS.md)** — the state file. Current phase, what's done, what's next. Any AI session starts by reading this.
- **`phases/`** — one folder per phase: the full study guide, the owner's build-gate code, and `LEARNINGS.md` (Claude's distilled notes + design decisions, the owner's break log, and the challenge resolution).
- **GitHub Issues** — one issue per phase = the task board. Challenges, decisions, and review happen there.

**Protocol (v2 — owner in the loop):** Claude writes each phase's `LEARNINGS.md` before the phase starts; the owner runs the build gate, breaks it once on purpose, and challenges one design decision in the phase issue. A phase is done when the gate passes its criteria *and* the challenge is resolved.

## The 9 phases

| # | Phase | Folder | Build gate |
| --- | --- | --- | --- |
| 1 | Setting Up AI Agents | `phases/01-setup` | Pocket Research Agent — raw Python, no framework |
| 2 | Loop Engineering | `phases/02-loop-engineering` | ReAct loop from scratch + loop guards + evaluator-optimizer, measured |
| 3 | Graph Engineering (+ MCP) | `phases/03-graph-engineering` | Support-triage agent (approval gate, crash-resume, time travel) + P1 rebuilt in LangGraph + one MCP server |
| 4 | Context Engineering | `phases/04-context-engineering` | The Context Gauntlet — naive vs engineered agent, measured |
| 5 | Token Optimization | `phases/05-token-optimization` | Cut an agent's token spend ≥50% in 4 measured passes |
| 6 | AI Routing | `phases/06-ai-routing` | ERP Query Router — intent → specialist agents → cost-aware model routing |
| 7 | Agent Roles Assignment | `phases/07-agent-roles` | Planner/executor/reviewer crew with a seeded trap the reviewer must catch |
| 8 | Evals & Observability | `phases/08-evals-observability` | Eval harness on the P7 crew that catches a seeded regression |
| 9 | AI Organization (capstone) | `phases/09-ai-organization` | Mini ERP, Inc. — CEO → departments → workers, approval gates, full tracing, red-team pass |

## Rules of the road

1. **Workflow first, agents only when necessary** — restraint is a core skill.
2. **Build from scratch before reaching for a framework.**
3. **A phase is done when its build gate passes its criteria and the issue challenge is resolved** — not when the material is read.
4. **Security lines in P6–P9 gates are pass criteria**, not suggestions.
5. Every learning, decision, and improvement gets committed — the repo is the memory.
