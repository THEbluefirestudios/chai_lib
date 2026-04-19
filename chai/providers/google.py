def get_response(prompt: str, api_key: str, model: str) -> str:
    from google import genai
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model,
        contents=prompt
    )
    return response.text or ""