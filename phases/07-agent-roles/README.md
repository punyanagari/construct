# Phase 7 — Agent Roles Assignment

## What it is & why

Agent roles assignment is the discipline of splitting one generalist agent into a *team of specialists* — a planner that decomposes, a researcher that gathers, a coder that builds, a reviewer that verifies, an orchestrator that routes — and defining who does what, with which tools, and who is allowed to judge whom. At team scale, specialization beats generalization for the same reason it does in human companies: a narrow job with a narrow toolset and a distinct output artifact is easier to prompt well, easier to test, and easier to fix when it breaks.

But the first skill in this phase is restraint, not design. A single well-engineered agent is cheaper, easier to debug, and easier to govern than any team — and the 2025–2026 industry consensus has shifted from "more agents" to "workflow first, agents when necessary." Multi-agent systems buy specialization, parallelism, and fault isolation at a real price: coordination overhead, token costs that commonly multiply 3–5x, and new failure modes (delegation loops, context sprawl) that don't exist in single-agent systems. The rule of thumb: start single-agent; add roles only when a generalist demonstrably fails on your actual workload, or when you need hard role/tool boundaries (e.g., your ERP's finance agent must never see HR tools). If you can't point to a trace where one agent provably failed, you're not ready to split. Budget 1–2 weeks for this phase, with the build gate at the end as the real test.

## Core concepts in learning order

**1. Single-agent vs. multi-agent tradeoffs.** Internalize the cost ledger before any framework: one agent keeps planning and execution in one context — cheap, traceable, governable — but degrades as tasks span multiple domains. Teams add specialization and parallelism but pay in tokens, latency, and coordination bugs. Learn the decision frameworks (Microsoft's Cloud Adoption Framework and Dataiku's enterprise checklist in the resources) so "should this be multi-agent?" becomes an evidence question, not a vibes question. Your ERP's Query Router from Phase 6 is already a proto-multi-agent system; this phase is where its specialists get real jobs.

**2. The canonical role vocabulary.** Five roles cover almost every system you'll see: **planner** (decomposes goals), **researcher** (gathers evidence), **coder/executor** (produces artifacts), **reviewer/critic/QA** (validates against criteria), **orchestrator/manager** (routes and aggregates). The mental model from the DeepLearning.AI crewAI course: think like a manager hiring a team. Before touching code, map a business process you know — say, generating an ERP monthly-close report — onto this vocabulary on paper.

**3. Role prompt design: role / goal / backstory.** CrewAI's signature architecture injects three fields into each agent's system prompt. Per the official "Crafting Effective Agents" guide: roles should be specific professional archetypes ("Senior UX Researcher specializing in interview analysis," not "Writer"); goals should be outcome-focused with success criteria; backstory carries context and constraints. Tasks then carry step-by-step instructions (`description`) and output contracts (`expected_output`). This is prompt engineering (Phase 2) applied at team scale — and YAML config files (`agents.yaml`, `tasks.yaml`) are how real projects keep role definitions separate from code.

**4. Task decomposition & avoiding role overlap.** Every sub-task must be independently verifiable; every agent gets a narrow job, a narrow toolset, and a distinct output artifact. Learn the overlap symptoms: agents re-doing each other's work, passing half-finished artifacts back and forth, or two agents with interchangeable backstories. This matters doubly because role descriptions double as routing metadata for managers and selectors — skill-based assignment only works if the descriptions are mutually exclusive.

**5. Flat / sequential teams.** The right default topology: CrewAI's `Process.sequential` runs tasks in a fixed chain with earlier outputs flowing into later tasks via `context=[...]`. It's deterministic, testable, and cheap — the multi-agent equivalent of the workflows you already trust. (AutoGen's equivalent is sequential/nested chats between `ConversableAgent`s — worth knowing conceptually, but note AutoGen is in maintenance mode, migrating to Microsoft Agent Framework, so don't build new production on it.)

**6. Delegation & handoffs.** CrewAI's `allow_delegation=True` lets an agent ask a peer for help; LangGraph and the OpenAI Agents SDK model handoffs as explicit `transfer_to_<agent>` primitives. The operational questions you must be able to answer: who may delegate, to whom, how loops are prevented (delegation is disabled by default for workers; cap iterations/depth), and what context travels with the handoff — the payload discipline you practiced in Phase 6.

**7. Supervisor / manager pattern (star topology).** One supervisor decomposes → delegates → reviews → aggregates; workers never talk to the user. CrewAI implements this as `Process.hierarchical` with a `manager_llm` or custom `manager_agent` that validates outcomes and re-assigns work; LangGraph does it with a supervisor node routing via handoffs. Learn the signature failure modes: delegation loops, manager-as-prompt-repeater, context sprawl, fuzzy evaluation, and the supervisor as single point of failure.

**8. Topology choice: hierarchical vs. flat vs. mesh.** Hierarchical = supervisor-of-supervisors (sub-teams with leads); flat = peers on a shared bus; mesh = full peer-to-peer. Hierarchies scale context management and contain blast radius, but add latency, cost, and information loss as results get summarized upward. The decision rule: adopt hierarchy only when runtime decomposition genuinely can't be predefined. For your ERP, a supervisor over finance/inventory/HR leads is the natural endgame — but you earn it last, not first.

**9. Reviewer loops & guardrails.** Verification as a first-class role is the mechanism that makes multi-agent systems *more reliable* than a single agent, not just more elaborate: reviewer agents with explicit acceptance criteria, CrewAI task guardrails (a validation function that can reject output and retry with feedback), termination conditions, and human-in-the-loop checkpoints (`human_input=True`). This role is the seed of the guardrails/evaluation work coming in later phases.

**10. Production realities.** Per-role model sizing connects directly back to Phases 5 and 6: put a strong reasoning model on the manager and reviewer, cheap/fast models on workers — role assignment is where routing economics and team design meet. Add cost/latency budgeting across the whole crew, observability/tracing across agent boundaries, and the eval question that closes the loop: *was delegation actually better than a single-agent baseline?* Keep landscape awareness too: AutoGen is in maintenance mode (migrating to Microsoft Agent Framework); CrewAI, LangGraph, and the OpenAI Agents SDK embody different role philosophies worth comparing.

## Study resources

### YouTube

| Resource | Why watch it |
|---|---|
| Krish Naik — "Agentic AI With Autogen Crash Course" (https://www.youtube.com/watch?v=yDpV_jgO93c) | 4-hour full course covering architecture, agents in depth, multi-agent teams, termination conditions, human-in-the-loop, tools, and a project on the modern AutoGen 0.4+ API. Caveat: AutoGen is in maintenance mode, migrating to Microsoft Agent Framework — watch for the team/termination concepts, not as a production bet. |
| Krish Naik — "crewAI Crash Course For Beginners" (https://www.youtube.com/watch?v=UV81LAb3x2g) | ~140K views, 32 min. Builds a researcher + writer crew from YouTube transcripts to blog posts; shows role/goal/backstory, tool assignment, and agent-to-agent delegation in practice. |
| CodingDeft — "Crew AI Tutorial \| Build Multi AI Agents" (https://www.youtube.com/watch?v=K2UAE1OlC8s) | Short (14 min) and current; covers project setup and, importantly, **YAML configuration of agents** — how real CrewAI projects separate role definitions from code. |
| Simplilearn — "CrewAI Tutorial For Beginners 2026" (https://www.youtube.com/watch?v=hbvm_q8xBTw) | 2026-dated beginner tutorial explaining the Crew vs. Flow distinction and building a multi-agent workflow end to end; a good second-pass video. |
| AIGrounded — "Build a Multi-Agent AI System with CrewAI + GPT-4o Mini" (https://www.youtube.com/watch?v=QfxwVgUew8c) | Full walkthrough of three specialized agents on a small/cheap model — the closest match to this phase's build gate and a live demo of per-role model sizing. |
| Simplified AI Course — "Building AI Agents with AutoGen" 9-part playlist (https://www.youtube.com/playlist?list=PLz6pthWWCdfSzzfwTa_E6Jt76Kq6aVNZQ) | Gentle on-ramp to conversable agents, user-proxy vs. assistant agents, LLM config, and initiating multi-agent chats. Same caveat: AutoGen is in maintenance mode — learn the conversation-driven role model, then apply it elsewhere. |

### X (Twitter)

| Account | Why follow |
|---|---|
| João Moura — @joaomdmoura (https://x.com/joaomdmoura) | Founder & CEO of CrewAI; posts releases, role/delegation design demos, and enterprise multi-agent case studies. The primary voice for this exact topic. (Verified via search citations; x.com blocks unauthenticated reads.) |
| CrewAI (official) — @crewAIInc (https://x.com/crewAIInc) | Release announcements, example crews, hierarchical-process features, community showcases. |
| AutoGen — @pyautogen (https://x.com/pyautogen) | GroupChat patterns and multi-agent conversation research — and, critically, migration news toward Microsoft Agent Framework, since AutoGen is in maintenance mode. |
| Harrison Chase — @hwchase17 (https://x.com/hwchase17) | LangChain/LangGraph founder; supervisor-pattern and handoff libraries, plus opinionated takes on when NOT to go multi-agent — a useful counterweight to framework marketing. |
| Elvis Saravia — @omarsar0 (https://x.com/omarsar0) | DAIR.AI founder running "AI Agents Weekly"; curates agent orchestration papers and commentary on agent-manager and multi-agent design trends. |

### Docs & blogs

| Resource | What you get |
|---|---|
| CrewAI — *Crafting Effective Agents* (https://docs.crewai.com/v1.15.2/en/guides/agents/crafting-effective-agents) | The official role/goal/backstory design guide — the reference for concept 3. |
| CrewAI — *Hierarchical Process* (https://docs.crewai.com/v1.15.2/en/learn/hierarchical-process) | Manager agents, task delegation, and result validation — the reference for concepts 7–8. |
| CrewAI examples — https://github.com/crewAIInc/crewAI-examples (plus quickstarts: https://github.com/crewAIInc/crewAI-quickstarts and main repo: https://github.com/crewAIInc/crewAI) | Researcher/writer/reviewer crew patterns and feature demos to crib structure from. |
| LangGraph multi-agent supervisor tutorial (https://langchain-ai.github.io/langgraph/tutorials/multi_agent/agent_supervisor) | The supervisor pattern as an explicit graph with handoffs — complements CrewAI's declarative approach. |
| DeepLearning.AI — *Multi AI Agent Systems with crewAI* (https://www.deeplearning.ai/courses/multi-ai-agent-systems-with-crewai) and *Practical Multi AI Agents and Advanced Use Cases with crewAI* (https://www.deeplearning.ai/short-courses/practical-multi-ai-agents-and-advanced-use-cases-with-crewai/) | The canonical courses, taught by João Moura himself: role-playing, focus, cooperation, guardrails; then parallel/sequential/hybrid crews and multiple LLMs per role. |
| ActiveWizards — *When Hierarchical AI Agents Are Worth the Complexity* (https://activewizards.com/blog/hierarchical-ai-agents-a-guide-to-crewai-delegation/) | The best tradeoff analysis found: `allow_delegation` operationally, delegation loops, and a decision framework for when hierarchy earns its keep. |
| Microsoft Cloud Adoption Framework — *Choosing Between a Single-Agent or Multi-Agent System* (https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/single-agent-multiple-agents) and Dataiku — *Single-agent vs. multi-agent systems* (https://www.dataiku.com/blog/single-agent-vs-multi-agent-systems) | Two decision-framework/checklist pieces for concept 1 — the "should you split at all?" judgment. |
| MDPI Future Internet (2026) — *LLM-Based Multi-Agent Orchestration: A Survey* (https://www.mdpi.com/1999-5903/18/6/326) | Centralized/decentralized/hierarchical taxonomy with framework mapping and token-cost comparison tables — the academic map of concept 8. |

## Hands-on build gate: planner → executor → reviewer with a rejection loop

Build a 3-agent CrewAI crew where the reviewer's job is to *catch a wrong output and send it back* — making the reviewer role tangible rather than decorative. Setup: `pip install crewai crewai-tools`, one LLM API key, a cheap model for workers and a stronger one for the reviewer (concept 10 in practice).

**Agents:**

1. **Planner** — role: "Technical Content Planner"; goal: decompose the user's topic into a 5-section outline with one verifiable fact requirement per section; `allow_delegation=False`.
2. **Executor (Writer)** — role: "Staff Technical Writer"; goal: draft the article strictly following the outline and fact requirements; `allow_delegation=False`.
3. **Reviewer** — role: "Ruthless Fact & Spec Editor"; goal: verify every section against the outline and fact requirements; output must be either `APPROVED` or `REJECTED: <numbered list of violations>`. Give the reviewer *no* writing tools — its only job is judgment.

**The build, in three passes:**

1. **Seed the trap.** Wire the tasks `Process.sequential`: planner → writer (`context=[task1]`) → reviewer (`context=[task1, task2]`). In the writer's task description, quietly require "exactly 5 sections with a cited statistic in each," then give it a topic where statistics are scarce. The writer will hallucinate or skip citations; watch the reviewer's trace reject the draft with numbered violations. Run the same prompt through a single-agent baseline and note what it ships silently.
2. **Close the loop.** Use CrewAI's task guardrail mechanism — a validation function returning `(success, data)` that retries with the reviewer's feedback appended — or pass the `REJECTED: ...` output back into the writer's task context until `APPROVED`. Cap at 2 retries to avoid loops.
3. **Hierarchical variant (stretch).** Convert to `Process.hierarchical` with a custom `manager_agent` so the manager routes rejections back itself, then compare cost, latency, and trace clarity against the sequential + guardrail version.

**Deliverables:** the crew code, two verbose traces (rejection visible, approval after rework), and a half-page note on what the reviewer caught that the single-agent run shipped silently. If you want an ERP-flavored variant, swap the content pipeline for a "monthly-close report" crew: planner outlines the report, executor drafts it from mock ERP APIs, reviewer verifies every figure against the mock data.

## Common pitfalls

- **Role overlap.** Two agents with interchangeable backstories re-do each other's work and pass half-finished artifacts back and forth — and any manager routing on role descriptions starts mis-assigning. The fix is concept 4 discipline: mutually exclusive descriptions, narrow toolsets, distinct output artifacts, independently verifiable tasks.
- **Agents arguing in circles.** Delegation enabled everywhere plus no termination conditions equals writer → reviewer → writer loops that burn tokens until the iteration cap fires. Keep `allow_delegation=False` on workers, cap retries/depth explicitly, and make the reviewer's output contract binary (`APPROVED` / `REJECTED:`) so loops have an exit.
- **Cost blowup.** Token usage in role-based systems commonly multiplies 3–5x over a single agent — every delegation, review, and retry is another full context. This is Phase 5's token economics returning with interest: apply per-role model sizing (cheap workers, strong manager/reviewer), budget cost per crew run, and always compare against the single-agent baseline. A team that isn't measurably better than one good agent is just an expensive one.

## Checkpoint: ready for Phase 8?

You're ready to move on when you can:

1. State the single-vs-multi-agent tradeoff as a cost/benefit ledger, and show a trace where one well-engineered agent provably failed before you split the work.
2. Map any business process onto the planner / researcher / executor / reviewer / orchestrator vocabulary — on paper, before any framework.
3. Write role/goal/backstory definitions (in YAML) that are specific, outcome-focused, and mutually exclusive, with task descriptions and output contracts to match.
4. Build a sequential crew with `context=[...]` chaining, and explain exactly who may delegate to whom, with what loop prevention and what handoff payload.
5. Implement a reviewer with a binary acceptance contract and a guardrail retry loop — and produce traces showing a seeded error caught and reworked.
6. Compare sequential vs. hierarchical runs on cost, latency, and trace clarity, and justify per-role model sizing in dollar terms.
7. Answer, with evidence: "was delegation actually better than the single-agent baseline?"

If all seven hold, you can decompose problems into non-overlapping, verifiable roles — the design skill every later phase presupposes. Phase 8 (new in roadmap v2) instruments exactly this crew: you'll build the eval harness, judge calibration, and tracing on it before anything multiplies. Then Phase 9 moves up one level: the roles you've assigned become actors inside a full organization, and the reviewer you built here evolves into org-wide guardrails and evaluation.
