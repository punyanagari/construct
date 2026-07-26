# PROGRESS

> State file — read this first in any new session. Update it after every work session.

**Current phase:** 0 — scaffolded; roadmap revised to v2, not started
**Mode:** v2 — owner in the loop. Claude writes each phase's `LEARNINGS.md` (concepts, design decisions with rationale, gotchas) and answers challenges; the owner runs the build gate, breaks it once on purpose, and challenges one design decision in the phase issue. A phase is done when the gate passes its criteria AND the challenge is resolved.
**Last updated:** 2026-07-26

## v2 migration checklist (apply once)

- [ ] Commit v2 `ROADMAP.md`, `PROGRESS.md`, `README.md` (this change set)
- [ ] Rename `phases/08-ai-organization` → `phases/09-ai-organization`
- [ ] Create `phases/08-evals-observability/` and open its phase issue
- [ ] Slim `phases/01-setup` guide (LangGraph rebuild + MCP server → move into `phases/03-graph-engineering`)

## Phase status

| Phase | Status | Build gate passed | Notes |
| --- | --- | --- | --- |
| 1. Setting Up AI Agents | not started | — | Issue #3 |
| 2. Loop Engineering | not started | — | Issue #2 |
| 3. Graph Engineering (+ MCP) | not started | — | Issue #7 |
| 4. Context Engineering | not started | — | Issue #1 |
| 5. Token Optimization | not started | — | Issue #5 |
| 6. AI Routing | not started | — | Issue #8 |
| 7. Agent Roles Assignment | not started | — | Issue #6 |
| 8. Evals & Observability *(new)* | not started | — | Issue: open one |
| 9. AI Organization (capstone) | not started | — | Issue #4 |

## Session log

| Date | Session summary | Commits |
| --- | --- | --- |
| 2026-07-26 | Repo scaffolded: roadmap, 8 phase guides, issue board (8 phase issues); mode set to full delegation | initial scaffold |
| 2026-07-26 | Roadmap v2 final: cloned + diffed repo vs generated files; kept repo's corrected ordering, Mermaid ladder, orientation & X/channel tables; added 9-phase structure (Evals P8, capstone → P9), slimmed P1, security thread, protocol v2, per-phase gates, canonical-link fix; README synced | v2 roadmap + progress + readme |

## How to resume (for any AI session)

1. Read `PROGRESS.md` (this file) → find current phase and status.
2. Read `ROADMAP.md` for the phase's mission, gate, and pass criteria; read the phase folder's `README.md` and `LEARNINGS.md` (if it exists).
3. Check the phase's open GitHub issue for the owner's pending challenge or decisions.
4. Continue work; commit code + update `LEARNINGS.md`; update this file's phase table and session log before ending.

## Working agreements (v2)

- One phase at a time, in order — no skipping ahead.
- Kickoff: Claude delivers `phases/XX/LEARNINGS.md` before the phase starts, with design decisions labeled D1, D2, … so each has a challenge target.
- Owner's three per phase: run the build gate · break it once and log it under `## Break log` in LEARNINGS.md · challenge one design decision in the phase issue.
- Challenge resolution goes in LEARNINGS.md under `## Challenge & resolution` — either the doc changes or the defense is written down.
- Code lives in the phase folder; when a gate passes, mark the table above and close the phase issue.
- Security lines in P6–P9 gates are pass criteria, not suggestions.
