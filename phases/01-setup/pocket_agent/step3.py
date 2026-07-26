import anthropic, re

client = anthropic.Anthropic()

def calculator(expression: str) -> str:
    if not re.fullmatch(r"[0-9+\-*/(). ]+", expression):
        return "Error: expression contains disallowed characters"
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"Error: {e}"

tools = [{
    "name": "calculator",
    "description": "Evaluate a basic arithmetic expression. Use this for any calculation instead of computing it yourself.",
    "input_schema": {
        "type": "object",
        "properties": {"expression": {"type": "string", "description": "e.g. '1847.5 * 12.3'"}},
        "required": ["expression"],
    },
}]

messages = [{"role": "user", "content": "What is 1847.5 * 12.3?"}]

r1 = client.messages.create(model="claude-opus-5", max_tokens=500, tools=tools, messages=messages)

tool_use = next(b for b in r1.content if b.type == "tool_use")
result = calculator(tool_use.input["expression"])
print(f"executed: {tool_use.input['expression']} -> {result}")

messages.append({"role": "assistant", "content": r1.content})
messages.append({"role": "user", "content": [
    {"type": "tool_result", "tool_use_id": tool_use.id, "content": result}
]})

r2 = client.messages.create(model="claude-opus-5", max_tokens=500, tools=tools, messages=messages)

print("stop_reason:", r2.stop_reason)
for block in r2.content:
    if block.type == "text":
        print("FINAL:", block.text)