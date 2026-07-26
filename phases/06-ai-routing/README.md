# Phase 6 — AI Routing

## What it is & why

Routing is the discipline of deciding *who answers each request*, and it comes in two distinct kinds. The first is **model routing**: for every query, pick the right LLM by cost and capability, sending easy lookups to a cheap model and hard reasoning to an expensive one. This is the token-economics lever you learned in Phase 5, but applied at the system level — instead of optimizing one agent's context, you optimize the unit economics of every request your product serves. The second kind is **task/agent routing**: for every request, pick the right agent or tool, so a "what's our Q2 margin?" question reaches your finance specialist and a "how many units of SKU-418?" question reaches inventory.

Both kinds answer the same question — "what does this request need?" — at different layers of the stack, and both matter for your ERP product. Routing is the gateway skill to multi-agent systems: the supervisor, handoff, and swarm patterns you'll use in later phases are all just routing decisions repeated over time. It's also where quality, latency, and SaaS unit economics meet, which makes this phase your highest-ROI topic on the roadmap. Budget 2–4 weeks including the build gate. Prerequisites are real: you need embeddings and retrieval (Phase 4), tool calling and structured output (Phases 2–3), and token-pricing intuition (Phase 5) before any of this sticks.

## Core concepts in learning order

Each concept below reuses the previous one's mental model while adding one new dimension: meaning → rules → learned judgment → economics → control transfer.

**1. Intent classification & semantic routing (embeddings).** Routing starts with "what does the user want?" The foundational technique: define one route per intent with 8–10 example utterances, embed them, and match incoming queries by cosine similarity against a score threshold. This is deterministic, runs in ~100ms, and costs almost nothing — versus seconds and dollars for an LLM call. Learn confidence thresholds and fallbacks: when no route matches, escalate to an LLM tiebreaker or a human. Aurelio AI's `semantic-router` library is the reference tool, with static vs. dynamic routes and threshold optimization.

**2. Rule-based / heuristic routing.** Keyword rules, regex, and request-feature heuristics (prompt length, presence of code, customer tier, SLA), plus config rules in LLM gateways. Rules beat learned routers when the logic is fixed and auditable — directly relevant to ERP permissions and tenant tiers ("enterprise tier always gets the strong model"). Their failure mode is nuance: a "simple"-looking question about quantum physics still needs a strong model, and a keyword rule can't see that.

**3. LLM-based routing.** Put a model on the request path as the classifier/dispatcher: structured-output intent classification, function-calling to select a tool or agent, or a routing node inside an agent framework that classifies input, directs it to specialists, then synthesizes results. This handles ambiguity embeddings and rules miss, but you must internalize the cost/latency trade-off of paying for an LLM call on every request.

**4. Cost/latency-aware model routing.** The RouteLLM idea: train a small router (matrix factorization, BERT, causal-LLM classifier, or similarity-weighted) on preference data to predict whether a strong model is actually needed, then calibrate a threshold to trade cost against quality. The reported headline: ~85% cost reduction on MT-Bench at 95% of GPT-4 quality. What matters in practice: calibrate the threshold against *your own* traffic, check quality per segment, keep router overhead under a ~50ms budget, and learn cascade patterns (cheap model first, escalate on low confidence). Survey the commercial/gateway layer too: RouteLLM, OpenRouter's auto-router, Martian, and Unify.

**5. Multi-agent handoffs & orchestration patterns.** The agent-level version of routing. The supervisor pattern uses a central coordinator that delegates via handoff tools; the swarm/handoff pattern lets agents transfer control to each other via tools like `transfer_to_sales`, tracking `active_agent` in shared state. Learn when to use router vs. supervisor vs. handoffs vs. subagents (LangChain's multi-agent docs include a good decision table). Master handoff payload design: explicit state schemas, token budgeting and context compression at handoff boundaries, schema validation, bounded retries and timeouts, and structured logging at every transition. Typical failure modes: misroutes, supervisor cascades, repeated handoffs to the same agent, context truncation.

## Study resources

### YouTube

| Resource | Why watch it |
|---|---|
| LangChain — "Understanding multi-agent handoffs" (https://www.youtube.com/watch?v=WTr6mHTw5cM) | The single best official video for the agent side of routing: how specialized agents pass control via LangGraph Swarm, with trace analysis of real handoffs. |
| LangChain — "Hierarchical multi-agent systems with LangGraph" (https://www.youtube.com/watch?v=B_0TNuYi56w) | Introduces the `langgraph-supervisor` library: supervisor pattern, information handoff, code implementation, multi-team hierarchies. Directly applicable to an ERP router-agent architecture. |
| James Briggs — "NEW AI Framework — Steerable Chatbots with Semantic Router" (https://www.youtube.com/watch?v=ro312jDqAh0) + free 6-part course playlist (https://www.youtube.com/playlist?list=PLIUOU7oqGTLhYDPiDKlALecva3jab531-) | From the creator of the `semantic-router` library: defining routes and guardrails, initializing a RouteLayer, using the router with LangChain agents; the playlist includes "Faster LLM Function Calling — Dynamic Routes." |
| Probably Private — "RouteLLM: Exploring how to reduce token spend via LLM Query Routing" (https://www.youtube.com/watch?v=-0C35d8ZtwA) | Bridges theory to cost-aware practice: why route prompts, testing models and bias, call-performance thresholds, eval data. |
| Srikanth Bhakthan — "Route LLM — Learning to Route LLMs with Preference Data" (https://www.youtube.com/watch?v=-XInK1s8QM4) | Paper walkthrough covering the four router types (similarity-weighted, matrix factorization, BERT, LLM classifier) and preference-data training. |
| MG — "Smart LLM Routing \| 85% Cheaper With RouteLLM" (https://www.youtube.com/watch?v=jc2RCG1Ys7g) | Short practitioner take on cutting spend up to 85% at ~95% GPT-4 performance; a quick motivational overview before the deeper material. |

### X (Twitter)

| Account / thread | Why follow |
|---|---|
| @OpenRouterAI (https://x.com/OpenRouterAI) | Model catalog updates, routing features (auto-router, provider routing, fallbacks), uptime notes — the front line of model-routing product thinking. |
| @jamescalam — James Briggs (https://x.com/jamescalam) | Creator of `semantic-router`; posts semantic routing, embeddings, and agent decision-layer content. |
| @simonw — Simon Willison (https://x.com/simonw; fully presented in Phase 5) | Practical LLM tooling experiments and honest build notes; frequently covers model selection, cost, and gateway tooling in practice. |
| @hwchase17 — Harrison Chase (https://x.com/hwchase17; on your list since Phase 1) | LangChain CEO; shares LangGraph multi-agent releases (supervisor, swarm, handoffs) and routing/orchestration design philosophy. |
| @shao__meng mixture-of-models thread (https://x.com/shao__meng/status/1811187309116895402) | The canonical Mixture-of-Models explainer — the architecture behind vLLM Semantic Router. (Note: verified via search citations rather than a direct page open.) |

### Docs & blogs

| Resource | What you get |
|---|---|
| RouteLLM repo — https://github.com/lm-sys/routellm | Framework for serving/evaluating LLM routers: drop-in OpenAI client replacement, pre-trained routers, threshold-calibration CLI. |
| RouteLLM paper — https://arxiv.org/abs/2406.18665 (HTML: https://arxiv.org/html/2406.18665v4) | "Learning to Route LLMs with Preference Data" — the research foundation for cost-aware routing. |
| Aurelio AI Semantic Router — https://github.com/aurelio-labs/semantic-router and https://docs.aurelio.ai/semantic-router/get-started/introduction | Superfast semantic decision layer: static/dynamic routes, local encoders, Pinecone/Qdrant persistence, threshold-optimization notebooks. |
| vLLM Semantic Router — https://github.com/vllm-project/semantic-router | Production-grade, Kubernetes-native Intelligent Mixture-of-Models router for heterogeneous LLM inference (`pip install vllm-sr`). |
| OpenRouter docs — https://openrouter.ai/blog/insights/model-routing/ , https://openrouter.ai/docs/api_reference/overview , https://openrouter.ai/docs/guides/routing/routers/auto-router | Two routing layers (model vs. provider), fallback arrays, `:nitro`/`:floor` variants, and the `cost_quality_tradeoff` dial. |
| LangChain multi-agent docs — https://docs.langchain.com/oss/python/langchain/multi-agent and https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs , plus langgraph-supervisor reference https://reference.langchain.com/python/langgraph-supervisor | Router vs. handoffs vs. subagents vs. skills decision table, with working `create_handoff_tool` / `Command(goto=...)` code. |
| Martian Model Router — https://docs.withmartian.com/ | Commercial router that estimates per-model performance by mapping queries into a unified vector space. |
| Unify — https://unify.ai/docs | Router console and concepts; note Unify has pivoted toward assistants, so treat it as concept reference. |
| Awesome-LLM-Routing — https://github.com/dstripelis/Awesome-LLM-Routing | Curated list of routing papers, companies, and repos for going deeper. |
| Truto — "How to Implement Semantic Routing for AI Agents to Select API Endpoints" (https://truto.one/blog/how-to-implement-semantic-routing-for-ai-agents-to-select-api-endpoints/) | **Very ERP-relevant**: a production stack sketch (embedding model, pgvector, semantic-router, MCP tool layer) for routing agent calls to the right API endpoints, plus shadow-mode rollout advice. |
| Burnwise — "LLM Model Routing: Cut Costs 85% with Smart Model Selection" (https://www.burnwise.io/blog/llm-model-routing-guide) | Concepts → RouteLLM implementation → thresholds → monitoring metrics → cost math. |
| peppereffect — "Agent Handoff Protocols" (https://peppereffect.com/blog/agent-handoff-protocols) | Explicit state schemas, token budgeting, validation at handoff boundaries, retry/timeout policy, transition logging. |
| TechnoLynx — "RouteLLM Explained" (https://www.technolynx.com/post/routellm-explained-how-model-routing-cuts-llm-inference-cost/) | Excellent FAQ on threshold calibration against your own traffic and per-segment quality. |
| gravity.fast — "AI Agent Handoff Patterns" (https://gravity.fast/blog/ai-agent-handoff-patterns/) | Decision rules for router vs. sequential vs. supervisor vs. swarm, plus each pattern's signature failure mode. |
| MarkTechPost — "Using RouteLLM to Optimize LLM Usage" (https://www.marktechpost.com/2025/08/10/using-routellm-to-optimize-llm-usage/) | Hands-on code walkthrough: install, config, calibrate threshold, test routing. |

## Hands-on build gate: the ERP Query Router

This build gate doubles as a prototype for your product, so give it real effort — 1–2 weekends. The goal: a routing layer for a multi-agent ERP assistant that (a) classifies intent semantically, (b) hands off to the right specialist agent, and (c) picks the cheapest capable model per request — both faces of routing in one project.

```
User query
  → [1] semantic-router (intent: finance | inventory | hr | sales | chitchat | out_of_scope)
       ├─ confidence < threshold → LLM tiebreaker (cheap model, structured output)
  → [2] LangGraph supervisor: handoff tool transfer_to_<dept>_agent
  → [3] Each specialist calls its tools (mock ERP APIs: get_invoice, check_stock, get_leave_balance)
  → [4] Model routing per agent: strong/weak pair (RouteLLM or OpenRouter `models` fallback + `openrouter/auto`)
        — simple lookups → weak model; multi-step reasoning ("why did margin drop in Q2?") → strong model
  → [5] Log every decision: query, intent, confidence, chosen agent, chosen model, tokens, cost, latency
```

**Build steps:**

1. **Semantic intent layer.** Define 6 routes × 8–10 utterances each with `semantic-router`, using a local FastEmbed/HuggingFace encoder to keep it free. Measure routing latency — target ~100ms.
2. **Graph skeleton.** Wrap the router in a LangGraph graph: START → intent router node → conditional edges to 4 specialist agent nodes, each with 2–3 mock tools returning fake ERP data (invoices, stock levels, employees, orders).
3. **Supervisor conversion.** Rebuild with `langgraph-supervisor`'s `create_supervisor` + `create_handoff_tool`, then compare against the swarm/handoff pattern (`active_agent` in state). Note which is easier to debug.
4. **Cost-aware model routing.** Run each specialist on OpenRouter with a `models` fallback array, then swap in RouteLLM (`router-mf-<threshold>`) between a strong and weak model. Calibrate the threshold on ~50 of your own test queries.
5. **Evaluation plan.** Build a 60-query test set with labeled intents and difficulty. Report: intent accuracy, misroute rate, cost/query vs. an all-strong-model baseline (expect 40–70% savings), and p95 latency. Log decisions to SQLite/JSONL and write a failure-mode analysis: which queries misroute, and why.

**Stretch goals:** shadow mode (the semantic router logs decisions while LLM routing still serves traffic; then compare); per-tenant routing rules (enterprise tier → strong model always, mirroring real SaaS pricing tiers); a fallback/human-escalation route for low-confidence queries.

## Common pitfalls

- **The router as a single point of failure.** Every request passes through your routing layer, so when it misclassifies, hangs, or goes down, every specialist agent is unreachable at once. Mitigate with rule-based fallbacks, bounded timeouts, and a default route to a generalist agent. Shadow mode (stretch goal above) exists precisely to de-risk this before the router owns production traffic.
- **Over-routing to expensive models.** A miscalibrated threshold quietly sends everything to the strong model, and your cost savings evaporate while the dashboard still claims routing is "working." Calibrate against your own traffic, re-check per-segment quality regularly, and watch the strong/weak split ratio as a first-class metric — not just total spend.
- **Unmeasurable routing quality without evals.** A router is a classifier; without a labeled test set you cannot say whether it's good. Teams routinely ship routing layers with zero misroute-rate measurement and discover problems only through user complaints. Build the 60-query eval set *before* tuning thresholds, log every routing decision, and write the failure-mode analysis — it's where the real learning is.

## Checkpoint: ready for Phase 7?

You're ready to move on when you can:

1. Explain the difference between model routing and task/agent routing, and name where each lives in your ERP architecture.
2. Implement a semantic router with defined routes, confidence thresholds, and an explicit fallback path — and state its latency and cost advantage over LLM-based classification.
3. Articulate when rule-based routing beats learned routing (auditable business logic, tenant tiers) and when it fails (nuance).
4. Calibrate a RouteLLM-style threshold on your own traffic and report cost/query vs. an all-strong baseline with per-segment quality checks.
5. Build a LangGraph supervisor with handoff tools, design clean handoff payloads (state schemas, token budgets, validation, bounded retries), and log every transition.
6. Measure routing quality with a labeled eval set — intent accuracy, misroute rate, p95 latency — and produce a failure-mode analysis.

If all six hold, you've internalized routing as both an architectural pattern and an economic lever. Phase 7 builds directly on this: your supervisor's mock specialists are about to get real jobs, real tools, and hard boundaries, and the handoff disciplines you practiced here — payload design, bounded retries, transition logging — are exactly what keeps a team of role-specialized agents from cascading into chaos.
