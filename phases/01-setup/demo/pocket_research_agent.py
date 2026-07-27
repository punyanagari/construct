# =============================================================================
# Pocket Research Agent — Phase 1 demo artifact (protocol v4)
# Written by Claude, to be READ, not reproduced.
#
# This is the complete Phase 1 gate: the raw agent loop from L4 plus a system
# prompt and three tools. ~120 lines, no framework. Everything LangGraph will
# do for us in Phase 3 is scaffolding around what's in this file.
#
# Run it (from phases/01-setup/pocket_agent with the venv active):
#   pip install ddgs
#   python ..\demo\pocket_research_agent.py
# =============================================================================

import anthropic, re
from ddgs import DDGS

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment

MODEL = "claude-opus-5"         # DP1: owner's choice, logged in LEARNINGS.md
MAX_ITERATIONS = 10             # D3: the first guard an agent ever needs
NOTES_FILE = "notes.md"

# -----------------------------------------------------------------------------
# The system prompt: the agent's standing rules. Note what it does NOT contain:
# no steps, no "first search, then...". The model plans; the prompt constrains.
# The citation rule and the save-before-finishing rule are the two behaviors
# the gate criteria check for — behavior is authored HERE, in English.
# -----------------------------------------------------------------------------
SYSTEM = (
    "You are a research assistant. Research questions using your tools. "
    "Every factual claim in your findings must cite a source URL that appeared "
    "in your search results — never invent or embellish a URL. "
    "Before giving your final answer, save your findings to notes using "
    "write_notes. Keep findings concise: bullets, not essays."
)

# -----------------------------------------------------------------------------
# Tool implementations. Three rules carried over from L3, visible throughout:
#   1. Model input is UNTRUSTED (calculator validates before eval).
#   2. Errors return as strings — observations the model can react to — never
#      raised exceptions, which would kill the loop.
#   3. Outputs are truncated (search snippets) because every character here
#      is re-sent on EVERY later iteration (the stateless-API token math).
# -----------------------------------------------------------------------------

def web_search(query: str) -> str:
    try:
        results = DDGS().text(query, max_results=5)
    except Exception as e:
        return f"Error: search failed ({e})"
    if not results:
        return "No results found."
    formatted = []
    for r in results:
        snippet = (r.get("body") or "")[:300]              # truncate: token hygiene
        formatted.append(f"{r.get('title')}\n{r.get('href')}\n{snippet}")
    return "\n\n".join(formatted)

def read_notes() -> str:
    try:
        with open(NOTES_FILE, encoding="utf-8") as f:      # utf-8: the Windows gotcha
            return f.read()
    except FileNotFoundError:
        return "(no notes yet)"                            # error as observation

def write_notes(content: str) -> str:
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Saved {len(content)} characters."             # the model needs proof

def calculator(expression: str) -> str:
    if not re.fullmatch(r"[0-9+\-*/(). ]+", expression):   # allowlist: untrusted input
        return "Error: expression contains disallowed characters"
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"Error: {e}"

# -----------------------------------------------------------------------------
# Tool declarations: what the model actually sees. The descriptions say WHEN
# to use each tool, not just what it does — descriptions are prompts.
# -----------------------------------------------------------------------------
TOOLS = [
    {
        "name": "web_search",
        "description": "Search the web. Use this whenever the answer depends on "
                       "facts you are not certain of, especially anything recent.",
        "input_schema": {"type": "object",
                         "properties": {"query": {"type": "string"}},
                         "required": ["query"]},
    },
    {
        "name": "read_notes",
        "description": "Read the current contents of your notes file.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "write_notes",
        "description": "Overwrite your notes file. Use this to save findings "
                       "before finishing.",
        "input_schema": {"type": "object",
                         "properties": {"content": {"type": "string"}},
                         "required": ["content"]},
    },
    {
        "name": "calculator",
        "description": "Evaluate a basic arithmetic expression. Use this for any "
                       "calculation instead of computing it yourself.",
        "input_schema": {"type": "object",
                         "properties": {"expression": {"type": "string"}},
                         "required": ["expression"]},
    },
]

TOOL_FUNCTIONS = {
    "web_search":  lambda inp: web_search(inp["query"]),
    "read_notes":  lambda inp: read_notes(),
    "write_notes": lambda inp: write_notes(inp["content"]),
    "calculator":  lambda inp: calculator(inp["expression"]),
}

# -----------------------------------------------------------------------------
# The loop — identical in shape to the owner's L4 build. Five moves:
# send → check stop_reason → echo content → execute & collect → append results.
# -----------------------------------------------------------------------------
def run_agent(question: str) -> None:
    messages = [{"role": "user", "content": question}]

    for iteration in range(1, MAX_ITERATIONS + 1):
        # max_tokens=16000: on a thinking model, reasoning and answer spend from
        # the SAME budget. 2000 was the demo's first real bug — the final answer's
        # thinking consumed it all, and the run "finished" with no answer and no
        # notes. Diagnosed by the owner from the trace, 2026-07-27.
        response = client.messages.create(
            model=MODEL, max_tokens=16000, system=SYSTEM,
            tools=TOOLS, messages=messages,
        )

        if response.stop_reason != "tool_use":              # done — exit
            if response.stop_reason == "max_tokens":
                # "didn't ask for a tool" is NOT the same as "succeeded":
                print("\nWARNING: cut off by max_tokens — answer is incomplete.")
            for block in response.content:
                if block.type == "text":
                    print(f"\nANSWER:\n{block.text}")
            print(f"\n(stop_reason={response.stop_reason}; "
                  f"{iteration - 1} tool iterations; "
                  f"final call used {response.usage.input_tokens} input tokens)")
            return

        messages.append({"role": "assistant", "content": response.content})

        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                result = TOOL_FUNCTIONS[block.name](block.input)
                print(f"[{iteration}] {block.name}({block.input}) "
                      f"-> {result[:120]}{'...' if len(result) > 120 else ''}")
                tool_results.append({"type": "tool_result",
                                     "tool_use_id": block.id, "content": result})

        messages.append({"role": "user", "content": tool_results})

    print("\nStopped: hit MAX_ITERATIONS without a final answer.")

if __name__ == "__main__":
    run_agent(
        "Research the current state of small language models for on-device "
        "agents and save a 5-bullet summary with sources to notes."
    )
