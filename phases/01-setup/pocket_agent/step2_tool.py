import anthropic, json

client = anthropic.Anthropic()

tools = [{
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

response = client.messages.create(
    model="claude-opus-5",
    max_tokens=500,
    tools=tools,
    messages=[{"role": "user", "content": "What is the capital of France?"}],
)

print("stop_reason:", response.stop_reason)
for block in response.content:
    if block.type == "text":
        print("TEXT:", block.text)
    elif block.type == "tool_use":
        print("TOOL CALL:", block.name, json.dumps(block.input), "id:", block.id)