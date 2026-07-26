# Construct

**Learning in public: from a first AI agent loop to a fully automated AI organization.**

This repo documents a structured journey through AI agent engineering — setup, loop engineering, graph engineering, context engineering, token optimization, AI routing, agent role assignment, and finally a capstone "AI organization" for full business automation (the end goal: a SaaS ERP with multi-agent routing).

## How this repo works

- **[ROADMAP.md](ROADMAP.md)** — the map: why the 8 phases are sequenced this way, the master resource index (YouTube, X, docs), and a 24-week timeline.
- **[PROGRESS.md](PROGRESS.md)** — the state file. Current phase, what's done, what's next. Any AI session starts by reading this.
- **`phases/`** — one folder per phase with the full study guide (concepts in learning order, curated verified resources, pitfalls) and a **build gate**: a hands-on project that must work before advancing.
- **GitHub Issues** — one issue per phase = the task board. Discussion, decisions, and review happen there.

## The 8 phases

| # | Phase | Folder | Build gate |
|---|-------|--------|-----------|
| 1 | Setting Up AI Agents | `phases/01-setup` | Pocket Research Agent — same agent built 3 ways (raw Python → LangGraph → MCP) |
| 2 | Loop Engineering | `phases/02-loop-engineering` | ReAct loop from scratch + loop guards + evaluator-optimizer |
| 3 | Graph Engineering | `phases/03-graph-engineering` | Support-triage agent: conditional edges, retry cycle, human approval, checkpointing |
| 4 | Context Engineering | `phases/04-context-engineering` | The Context Gauntlet — naive vs engineered agent, measured |
| 5 | Token Optimization | `phases/05-token-optimization` | Cut an agent's token spend ≥50% in 4 measured passes |
| 6 | AI Routing | `phases/06-ai-routing` | ERP Query Router — intent → specialist agents → cost-aware model routing |
| 7 | Agent Roles Assignment | `phases/07-agent-roles` | Planner/executor/reviewer crew with a seeded trap the reviewer must catch |
| 8 | AI Organization (capstone) | `phases/08-ai-organization` | Mini ERP, Inc. — CEO → departments → workers, approval gates, full tracing |

## Rules of the road

1. **Workflow first, agents only when necessary** — restraint is a core skill.
2. **Build from scratch before reaching for a framework.**
3. **A phase is done when its build gate works**, not when its material is read.
4. Every learning, decision, and improvement gets committed — the repo is the memory.
