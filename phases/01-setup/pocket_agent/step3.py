import anthropic, re

client = anthropic.Anthropic()

def calculator(expression: str) -> str:
    if not re.fullmatch(r"[0-9+\-*/(). ]+", expression):
        return "Error: expression contains disallowed characters"
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"Error: {e}"

TOOLS = [{
    "name": "calculator",
    "description": "Evaluate a basic arithmetic expression. Use this for any calculation instead of computing it yourself.",
    "input_schema": {
        "type": "object",
        "properties": {
            "expression": {"type": "string", "description": "e.g. '1847.5 * 12.3'"}
        },
        "required": ["expression"],
    },
}]

TOOL_FUNCTIONS = {"calculator": lambda inp: calculator(inp["expression"])}

MAX_ITERATIONS = 10

def run_agent(question: str) -> None:
    messages = [{"role": "user", "content": question}]

    for iteration in range(1, MAX_ITERATIONS + 1):
        response = client.messages.create(
            model="claude-opus-5", max_tokens=1000, tools=TOOLS, messages=messages,
        )

        if response.stop_reason != "tool_use":          # done — exit the loop
            for block in response.content:
                if block.type == "text":
                    print(f"\nANSWER: {block.text}")
            return

        messages.append({"role": "assistant", "content": response.content})

        tool_results = []
        for block in response.content:                   # may be SEVERAL tool calls
            if block.type == "tool_use":
                result = TOOL_FUNCTIONS[block.name](block.input)
                print(f"[{iteration}] {block.name}({block.input}) -> {result}")
                tool_results.append({"type": "tool_result",
                                     "tool_use_id": block.id, "content": result})

        messages.append({"role": "user", "content": tool_results})  # ALL results, ONE message

    print("\nStopped: hit MAX_ITERATIONS without a final answer.")

run_agent("A work order has 37 items at 1847.50 each. 3 items were cancelled. "
          "What is the revised order value, and what is 18% GST on that revised value?")