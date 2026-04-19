# token-chai

Token-efficient LLM prompting via Chinese compression.

Translates your prompt to Chinese before sending to the AI (Chinese uses fewer tokens than English), then translates the response back to your language, whic will save you money on API costs.

## Installation

```bash
pip install token-chai
```

## Supported Models

| Key | Provider | Default Model |
|---|---|---|
| `openai` | OpenAI | `gpt-4o` |
| `google-genai` | Google AI | `gemini-2.0-flash` |
| `claude` | Anthropic | `claude-sonnet-4-20250514` |

---

## Usage

There are two ways to use token-chai:

### Method 1: Configure once, use everywhere (recommended)

Set your options once with `chai.configure()` and never repeat them:

```python
import chai

chai.configure(
    ai_model="google-genai",
    api_key="your api key",
    model="gemini-2.0-flash",
    response_lang="en",
)

response = chai.get_response("Explain black holes in simple terms")
print(response)
```

You can still override any option per call:

```python
response = chai.get_response("What is recursion?", response_lang="hi")
```

---

### Method 2: Pass everything directly

```python
import chai

response = chai.get_response(
    prompt="Explain black holes in simple terms",
    ai_model="google-genai",
    api_key="your api key",
    model="gemini-2.0-flash",
    response_lang="en",
)
print(response)
```

---

## Examples

### Google Gemini

**Configure once:**
```python
import chai

chai.configure(
    ai_model="google-genai",
    api_key="your api key",
    model="gemini-2.0-flash",
    response_lang="en",
)

response = chai.get_response("What is the theory of relativity?")
print(response)
```

**Direct:**
```python
import chai

response = chai.get_response(
    prompt="What is the theory of relativity?",
    ai_model="google-genai",
    api_key="your api key.",
    model="gemini-2.0-flash",
    response_lang="en",
)
print(response)
```

---

### OpenAI ChatGPT

**Configure once:**
```python
import chai

chai.configure(
    ai_model="openai",
    api_key="your api key",
    model="gpt-4o",
    response_lang="en",
)

response = chai.get_response("Explain quantum computing simply")
print(response)
```

**Direct:**
```python
import chai

response = chai.get_response(
    prompt="Explain quantum computing simply",
    ai_model="openai",
    api_key="your api key",
    model="gpt-4o",
    response_lang="en",
)
print(response)
```

---

### Anthropic Claude

**Configure once:**
```python
import chai

chai.configure(
    ai_model="claude",
    api_key="your api key",
    model="claude-sonnet-4-20250514",
    response_lang="en",
)

response = chai.get_response("How does photosynthesis work?")
print(response)
```

**Direct:**
```python
import chai

response = chai.get_response(
    prompt="How does photosynthesis work?",
    ai_model="claude",
    api_key="your api key",
    model="claude-sonnet-4-20250514",
    response_lang="en",
)
print(response)
```

---

## Check Token Savings

Preview how much compression you get before sending:

```python
import chai

stats = chai.estimate_savings("Explain black holes in simple terms")
print(stats)
# {
#   'original_chars': 36,
#   'chinese_chars': 17,
#   'compression_ratio': 0.47,
#   'chinese_preview': '用简单的术语解释黑洞...'
# }
```

---

## Response Languages

Pass any BCP-47 language code to `response_lang`:

| Code | Language |
|---|---|
| `en` | English |
| `hi` | Hindi |
| `fr` | French |
| `de` | German |
| `ja` | Japanese |
| `es` | Spanish |
| `zh` | Chinese (skip back-translation) |

---

## Debug Mode

Skip translation entirely to test raw API responses:

```python
response = chai.get_response(
    prompt="Hello!",
    skip_translation=True,
)
print(response)
```

---

## Supported API Providers

For now, chai only supports models from OpenAI, Google and Anthropic with a valid API key.

---

## License

MIT
