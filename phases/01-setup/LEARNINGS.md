# Phase 1 — LEARNINGS

> Lesson log for Phase 1, per protocol v3 (hybrid tutor mode): Claude teaches with explanations and step-by-step actions/decisions; the owner types, runs, decides at decision points, and answers the checkpoint quiz. Lessons are appended below as they are taught.

## TL;DR (≤10 bullets)

- A **workflow** is an LLM inside control flow *you* wrote; an **agent** is an LLM writing its own control flow in a loop. Most "agent" ideas are workflows wearing a costume — the taxonomy exists to stop you overbuilding.
- The whole trick is ~15 lines: messages in → model returns text or a tool call → execute → append result → repeat until the model stops or a guard fires. Everything else any framework sells you is scaffolding around this.
- You are not prompt-engineering the model as much as you are **prompt-engineering your tools**: names, descriptions, and parameter schemas drive tool choice; the tool's code is invisible to the model.
- The message history *is* the agent's state. When it misbehaves, you debug by reading the transcript, not by stepping through code.
- A loop without a max-iterations cap is not an agent, it's an open tab on your credit card.
- Print every tool call from day one. Untraced agents don't fail loudly — they fail expensively.
- The five workflow patterns (chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer) are the vocabulary for everything through Phase 9. Learn the names now; build them in P2+.
- Golden rule, memorize verbatim: **a well-prompted single call beats a workflow, a workflow beats an agent, one agent with good tools usually beats a crew.**
- For the ERP: the query-routing layer is a *workflow* (routing pattern); the specialists behind it are *agents*. Being able to say why is a pass criterion.

## Lessons (as taught)

- **L1 (2026-07-26)** — Workflow vs agent; the anatomy of the raw loop; environment setup and the first controlled API call. Owner gotchas hit and understood: cmd-vs-PowerShell env-var syntax, `.\` command precedence, venv activation = PATH manipulation. Token cost math done on real output (out-tokens cost 5× in-tokens; stateless API → history resend → quadratic growth preview).
- **L2 (2026-07-26)** — Tool calling: declare (name/description/schema) → model *requests* via `tool_use` block → nothing executes until owner's code acts. Observed live: `stop_reason` as the branch condition, nondeterministic content lists (text block present in one run, absent in the next), per-call `toolu_` ids. Contrast run: geography question → `end_turn`, no tool call — tool choice is authored in the description's English. Warm-up quiz passed: LOA extraction = LLM fills the slot, code decides (workflow).
- **L3 (2026-07-26)** — The return leg: echo full assistant `content`, send `tool_result` tagged with the id in a *user* message, same tools list, model phrases a number it never computed. Security thread opened: model output is untrusted input (allowlist-guarded eval); errors returned as observations, never raised.
- **L4 (2026-07-27)** — The loop: step 3 with two assumptions removed. `for` with MAX_ITERATIONS as structure, `stop_reason` exit at top, dispatch dict, all tool results in one user message (API rule). Multi-step ERP-flavored task (revised order value → GST on it) to witness result-feeds-next-decision. Owner runs it; gate assignment (system prompt + web_search + notes tools, owner-written) is next.

## Decisions (who chose what, why)

- **DP1 — Phase 1 model: `claude-opus-5`** *(owner, 2026-07-26)*. Claude recommended `claude-opus-4-8` from a stale June model catalog; the owner surfaced the Jul 24, 2026 Opus 5 release. Verified against live docs: $5/$25 per MTok (identical to 4.8), 1M context, 128K max output, adaptive thinking, same clean API surface — strictly better at equal price. Meta-lesson: model catalogs go stale in weeks; verify against live docs (or the Models API) before deciding, and don't let your tutor's cache outrank a primary source.

## Gate design decisions (D1–D6)

**D1 — No framework in Phase 1, at all.**
*Decision:* the gate is ~100 lines of raw Python; LangGraph and MCP wait for Phase 3.
*Why:* frameworks abstract the message history, and the message history is where every production bug will be debugged. The rebuild in P3 only teaches you something if there's a raw version to compare against.
*Falsified if:* after P3 you find the raw build taught you nothing the LangGraph rebuild didn't — i.e., you never once reasoned about state at the message level while debugging the graph version.

**D2 — Exactly three tools: `web_search`, `read_notes`/`write_notes`, `calculator`.**
*Decision:* one external-API tool, one file-I/O pair, one pure function — no more.
*Why:* three tools is the minimum that forces real tool *choice* (the model must pick, not just fire the only gun on the wall), while covering the three tool species you'll meet forever after: network calls that fail, side effects that persist, and deterministic helpers. More tools at this stage adds selection noise, not learning.
*Falsified if:* the model never confuses or misuses tools during your runs — then the selection-pressure argument was theater and two tools would have done.

**D3 — Max 10 iterations, hard stop, no exceptions.**
*Decision:* the loop terminates at 10 turns even mid-task.
*Why:* the first guard you ever add should be the one that bounds cost, and it should be low enough that you actually hit it during development and feel what "the agent didn't finish" looks like. Recovery strategies (best-answer-so-far, reflection) are P2 material.
*Falsified if:* 10 proves so high you never hit it on the gate task — or so low the task can't complete even on clean runs. Either way, log the number of iterations your successful runs actually used.

**D4 — Print every tool call to stdout; no tracing library.**
*Decision:* observability in P1 is `print(tool_name, args)` and nothing fancier.
*Why:* the habit matters more than the tooling. LangSmith arrives in P3; if you can't read a plain-text trace, a dashboard won't save you.
*Falsified if:* you find a bug during the gate that stdout tracing couldn't localize but structured tracing would have — write down what was missing.

**D5 — Notes live in a markdown file, not in the conversation.**
*Decision:* findings are persisted via `write_notes` to a local file the agent must explicitly read back.
*Why:* it plants the P4 seed early — context is not storage. The model deciding *what deserves to be written down* is a miniature of every memory architecture you'll build later.
*Falsified if:* the agent completes the task equally well with notes disabled — then the file was ceremony, and the task needs to be harder before the pattern earns its place.

**D6 — The gate task is research + synthesis ("SLMs for on-device agents"), not a coding task.**
*Decision:* the task exercises search → read → decide → persist, ending in a 5-bullet cited summary.
*Why:* research tasks force multi-step tool use with judgment between steps and produce an artifact whose quality you can check (are the sources real? cited? current?). A coding task would tempt you into evaluating the code instead of the loop.
*Falsified if:* the agent one-shots it in ≤2 tool calls — then the task is too shallow to exercise the loop and should be swapped for a comparative question.

## Gotchas

- Model tier: a cheap model is fine for the loop mechanics but will hallucinate citations in the summary. If your bullets cite sources the search never returned, that's the model, not your loop — check the transcript before "fixing" code.
- `web_search` without a result cap will flood the context with 10× more tokens than the model needs. Truncate results *in the tool*, not in the prompt — a preview of P5.
- If the model replies with prose *about* calling a tool instead of an actual tool call, your schema descriptions are vague or your system prompt buries the instruction. Fix the tool description first.
- Windows note: keep the notes file path relative and open with `encoding="utf-8"` — the default codepage will bite you on the first em-dash the model writes.
- Return tool errors to the model as observations ("search failed: timeout") instead of raising. You'll formalize this in P2, but you'll want it the first time the search API hiccups.

## Break log (owner)

*(Run the gate, then break it once on purpose — kill the network mid-run, feed it a poisoned search result, drop the iteration cap to 3 — and record here what happened and what you learned.)*

## Checkpoint quiz (owner's answers)

*(At phase end, Claude asks the P1 pass-criteria questions — rewrite the loop from memory, explain workflow-vs-agent, name an ERP task that stays a workflow. The owner's answers, in their own words, get recorded here.)*
