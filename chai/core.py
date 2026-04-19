import importlib
from .translators import to_chinese, from_chinese
from .exceptions import UnsupportedModelError, ProviderError

# --- Default models per provider ---
PROVIDER_DEFAULTS = {
    "openai":       ("chai.providers.openai",    "gpt-4o"),
    "google-genai": ("chai.providers.google",    "gemini-2.5-flash"),
    "claude":       ("chai.providers.anthropic", "claude-sonnet-4-20250514"),
}

# --- chai_opts: set once, reuse everywhere ---
# Works just like ydl_opts — configure once, don't repeat every call
chai_opts = {
    "ai_model":         None,   # e.g. "openai"
    "api_key":          None,   # your API key
    "model":            None,   # specific model string, or None to use provider default
    "response_lang":    "en",   # default response language
    "skip_translation": False,  # debug mode — skips Chinese compression
}


def configure(**kwargs):
    """
    Set global defaults so you don't repeat them every call.

    Usage:
        chai.configure(
            ai_model="openai",
            api_key="sk-...",
            model="gpt-4-turbo",   # optional, uses provider default if omitted
            response_lang="en",
        )
    """
    for key in kwargs:
        if key not in chai_opts:
            raise ValueError(f"Unknown option '{key}'. Valid options: {list(chai_opts.keys())}")
    chai_opts.update(kwargs)


def get_response(
    prompt: str,
    ai_model: str | None = None,
    api_key: str | None = None,
    response_lang: str | None = None,
    model: str | None = None,
    skip_translation: bool | None = None,
) -> str:
    """
    Translates prompt to Chinese, sends to AI, translates response back.

    Args:
        prompt:           Your prompt in any language.
        ai_model:         One of: 'openai', 'google-genai', 'claude'
                          Falls back to chai_opts if not provided.
        api_key:          API key for the chosen provider.
                          Falls back to chai_opts if not provided.
        response_lang:    Language code for the response (e.g. 'en', 'hi', 'fr').
                          Falls back to chai_opts if not provided.
        model:            Specific model string e.g. 'gpt-4-turbo', 'gemini-1.5-pro'.
                          Falls back to chai_opts, then provider default if not provided.
        skip_translation: If True, skips translation entirely (debug mode).

    Returns:
        The AI's response in the requested language.
    """
    # Merge per-call args with chai_opts (call args take priority)
    resolved_model      = ai_model         or chai_opts["ai_model"]
    resolved_key        = api_key          or chai_opts["api_key"]
    resolved_lang       = response_lang    or chai_opts["response_lang"]
    resolved_specific   = model            or chai_opts["model"]
    resolved_skip       = skip_translation if skip_translation is not None else chai_opts["skip_translation"]

    if not resolved_model:
        raise UnsupportedModelError("No ai_model provided. Pass it directly or use chai.configure().")
    if not resolved_key:
        raise ProviderError("No api_key provided. Pass it directly or use chai.configure().")
    assert isinstance(resolved_model, str) 
    assert isinstance(resolved_key, str) 
    if resolved_model not in PROVIDER_DEFAULTS:
        raise UnsupportedModelError(
            f"'{resolved_model}' is not supported. Choose from: {list(PROVIDER_DEFAULTS.keys())}"
        )

    module_path, default_model = PROVIDER_DEFAULTS[resolved_model]
    final_model = resolved_specific or default_model

    # Step 1: Translate prompt to Chinese
    compressed_prompt = prompt if resolved_skip else to_chinese(prompt)

    # Step 2: Call the provider
    provider = importlib.import_module(module_path)
    raw_response = provider.get_response(compressed_prompt, resolved_key, model=final_model)

    # Step 3: Translate response to target language
    if resolved_skip or resolved_lang in ("zh", "zh-CN", "zh-TW"):
        return raw_response

    return from_chinese(raw_response, resolved_lang)


def estimate_savings(prompt: str) -> dict:
    """Preview token compression stats before sending."""
    chinese = to_chinese(prompt)
    return {
        "original_chars":    len(prompt),
        "chinese_chars":     len(chinese),
        "compression_ratio": round(len(chinese) / len(prompt), 2),
        "chinese_preview":   chinese[:100] + "..." if len(chinese) > 100 else chinese,
    }