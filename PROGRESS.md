# PROGRESS

> State file — read this first in any new session. Update it after every work session.

**Current phase:** 0 — scaffolded; roadmap revised to v2, not started
**Mode:** v3 — hybrid tutor. Claude learns each phase and teaches it: plain-language lessons plus a step-by-step guided build (action → why → what you should see), with explicit decision points where Claude presents tradeoffs and the owner decides. The owner types, runs, and commits; Claude reviews output, answers every "why", and quizzes at the checkpoint. A phase is done when the gate passes its criteria AND the owner passes the checkpoint quiz in their own words.
**Last updated:** 2026-07-26

## v2 migration checklist (apply once)

- [x] Commit v2 `ROADMAP.md`, `PROGRESS.md`, `README.md` (this change set)
- [x] Rename `phases/08-ai-organization` → `phases/09-ai-organization`
- [x] Create `phases/08-evals-observability/` and open its phase issue (#9)
- [x] Slim `phases/01-setup` guide (LangGraph rebuild + MCP server → move into `phases/03-graph-engineering`)

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

## How to resume (for any AI session)

1. Read `PROGRESS.md` (this file) → find current phase and status.
2. Read `ROADMAP.md` for the phase's mission, gate, and pass criteria; read the phase folder's `README.md` and `LEARNINGS.md` (if it exists).
3. Check the phase's open GitHub issue for the owner's pending challenge or decisions.
4. Continue work; commit code + update `LEARNINGS.md`; update this file's phase table and session log before ending.

## Working agreements (v3)

- One phase at a time, in order — no skipping ahead.
- Claude teaches, the owner builds: lessons first, then a step-by-step guided build — every step with the action, the why, and what you should see. Claude never pastes a finished gate solution.
- Decision points are explicit: Claude lays out options + tradeoffs and recommends one; the owner decides; the choice and reason go in LEARNINGS.md under `## Decisions`.
- Owner breaks the passing gate once on purpose and logs it under `## Break log`.
- A phase closes with the checkpoint quiz — Claude asks, the owner answers in their own words, and the answers get logged under `## Checkpoint quiz`.
- Code lives in the phase folder; when a gate passes, mark the table above and close the phase issue.
- Security lines in P6–P9 gates are pass criteria, not suggestions.
