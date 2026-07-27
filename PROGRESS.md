# PROGRESS

> State file — read this first in any new session. Update it after every work session.

**Current phase:** 0 — scaffolded; roadmap revised to v2, not started
**Mode:** v4 — concept tutor. The owner learns concepts from examples and never writes code; Claude is the hands (writes/runs all demos, commits them under `phases/XX/demo/`). Every lesson = concept → worked example (annotated trace, demo run, Auto-MB scenario) → a prediction/decision question the owner answers. A phase closes on an understanding gate: checkpoint quiz + defended design call + seeded-failure trace diagnosis, in the owner's own words.
**Last updated:** 2026-07-26

## v2 migration checklist (apply once)

- [x] Commit v2 `ROADMAP.md`, `PROGRESS.md`, `README.md` (this change set)
- [x] Rename `phases/08-ai-organization` → `phases/09-ai-organization`
- [x] Create `phases/08-evals-observability/` and open its phase issue (#9)
- [x] Slim `phases/01-setup` guide (LangGraph rebuild + MCP server → move into `phases/03-graph-engineering`)

## Phase status

| Phase | Status | Understanding gate passed | Notes |
| --- | --- | --- | --- |
| 1. Setting Up AI Agents | not started | — | Issue #3 |
| 2. Loop Engineering | not started | — | Issue #2 |
| 3. Graph Engineering (+ MCP) | not started | — | Issue #7 |
| 4. Context Engineering | not started | — | Issue #1 |
| 5. Token Optimization | not started | — | Issue #5 |
| 6. AI Routing | not started | — | Issue #8 |
| 7. Agent Roles Assignment | not started | — | Issue #6 |
| 8. Evals & Observability *(new)* | not started | — | Issue #9 |
| 9. AI Organization (capstone) | not started | — | Issue #4 |

## Session log

| Date | Session summary | Commits |
| --- | --- | --- |
| 2026-07-26 | Repo scaffolded: roadmap, 8 phase guides, issue board (8 phase issues); mode set to full delegation | initial scaffold |
| 2026-07-26 | Roadmap v2 final: cloned + diffed repo vs generated files; kept repo's corrected ordering, Mermaid ladder, orientation & X/channel tables; added 9-phase structure (Evals P8, capstone → P9), slimmed P1, security thread, protocol v2, per-phase gates, canonical-link fix; README synced | v2 roadmap + progress + readme |
| 2026-07-26 | v2 migration finished (Claude Code): capstone folder → 09, Phase 8 guide + issue #9 opened, P1 guide slimmed to raw Python, P3 guide absorbed LangGraph rebuild + MCP + framework survey, stale Phase-8/9 cross-refs swept, issue #4 retitled to Phase 9 | v2 judgment edits |
| 2026-07-26 | Phase 1 kickoff per protocol v2: `phases/01-setup/LEARNINGS.md` delivered (design decisions D1–D6 with falsifiers, gotchas, empty break-log/challenge sections). Ball is with the owner: run the gate, break it once, challenge a D in issue #3 | P1 LEARNINGS.md |
| 2026-07-26 | Protocol rearranged to **v3 — hybrid tutor mode** (owner got their involvement wrong in v2): Claude learns each phase and teaches with explanations + step-by-step actions/decisions; owner types, runs, decides, and answers the checkpoint quiz. ROADMAP/README/PROGRESS/LEARNINGS updated; L1 (workflow vs agent, loop anatomy, setup) taught in session | protocol v3 |
| 2026-07-27 | Protocol re-architected to **v4 — concept tutor mode** (owner: learn concepts from examples, no coding tasks): Claude is the hands, owner is trained as architect/auditor — reads traces, makes design calls, never writes code. Understanding gates (quiz + design call + trace diagnosis) replace build gates; Claude commits annotated demos under `phases/XX/demo/`. Under v3 the owner had hands-on-built through L4 (working calculator agent loop — artifacts kept in `phases/01-setup/pocket_agent/`); P1 closes under v4 rules from here | protocol v4 |

## How to resume (for any AI session)

1. Read `PROGRESS.md` (this file) → find current phase and status.
2. Read `ROADMAP.md` for the phase's mission, gate, and pass criteria; read the phase folder's `README.md` and `LEARNINGS.md` (if it exists).
3. Check the phase's open GitHub issue for the owner's pending challenge or decisions.
4. Continue work; commit code + update `LEARNINGS.md`; update this file's phase table and session log before ending.

## Working agreements (v4)

- One phase at a time, in order — no skipping ahead.
- Claude teaches from examples; the owner never writes code. Every lesson ends with a prediction or decision question the owner answers before the next lesson.
- Claude writes, runs, and commits each phase's demo artifact under `phases/XX/demo/` — annotated to be read. The owner runs at most a single command to reproduce a demo.
- Decision points are explicit: Claude lays out options + tradeoffs and recommends one; the owner decides; the choice and reason go in LEARNINGS.md under `## Decisions`.
- A phase closes on its understanding gate, logged in LEARNINGS.md: `## Checkpoint quiz` (concepts explained cold) + a defended Auto-MB design call (under `## Decisions`) + a seeded-failure trace diagnosis (under `## Diagnoses`).
- When a gate passes, mark the table above and close the phase issue.
- Security lines in P6–P9 gates remain pass criteria — they surface as design-call and diagnosis material.
