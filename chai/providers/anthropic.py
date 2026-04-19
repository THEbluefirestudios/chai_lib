def get_response(prompt: str, api_key: str, model: str) -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    block = message.content[0]
    assert isinstance(block, anthropic.types.TextBlock)
    return block.text