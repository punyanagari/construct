import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env

response = client.messages.create(
    model="claude-opus-5",     # or your Step-2 choice
    max_tokens=500,
    system="You are terse. Answer in one sentence.",
    messages=[{"role": "user", "content": "What is a system prompt for?"}],
)

for block in response.content:
    if block.type == "text":
        print(block.text)
print(f"\nin: {response.usage.input_tokens} tokens, out: {response.usage.output_tokens} tokens")