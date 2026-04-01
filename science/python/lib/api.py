"""API call wrappers for Claude and Gemini with retry logic."""

import time
from dataclasses import dataclass

import anthropic


@dataclass
class APIResponse:
    """Normalized response from any provider."""
    text: str
    input_tokens: int
    output_tokens: int


def call_claude(model: str, temperature: float, max_tokens: int,
                prompt: str, system: str = "") -> APIResponse:
    client = anthropic.Anthropic()
    max_retries = 5
    last_exc: Exception = RuntimeError("unreachable")

    kwargs: dict = dict(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[{"role": "user", "content": prompt}],
    )
    if system:
        kwargs["system"] = system

    for attempt in range(max_retries):
        try:
            message = client.messages.create(**kwargs)
            text_blocks = [b for b in message.content if b.type == "text"]
            text = text_blocks[0].text if text_blocks else ""
            return APIResponse(text, message.usage.input_tokens, message.usage.output_tokens)
        except anthropic.APIStatusError as e:
            if e.status_code == 529 and attempt < max_retries - 1:
                wait = 30 * (2 ** attempt)
                print(f"\n  [overloaded] retrying in {wait}s...", end=" ", flush=True)
                time.sleep(wait)
                last_exc = e
            else:
                raise
    raise last_exc


def call_gemini(model: str, temperature: float, max_tokens: int,
                prompt: str, system: str = "") -> APIResponse:
    import os
    from google import genai
    from google.genai import types

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set")

    client = genai.Client(api_key=api_key)
    config = types.GenerateContentConfig(
        max_output_tokens=max_tokens,
        temperature=temperature,
    )
    if system:
        config.system_instruction = system

    response = client.models.generate_content(
        model=model,
        config=config,
        contents=prompt,
    )
    text = response.text or ""
    in_tok = response.usage_metadata.prompt_token_count or 0
    out_tok = response.usage_metadata.candidates_token_count or 0
    return APIResponse(text, in_tok, out_tok)


def call_api(provider: str, model: str, temperature: float, max_tokens: int,
             prompt: str, system: str = "") -> APIResponse:
    provider = provider.upper()
    if provider == "CLAUDE":
        return call_claude(model, temperature, max_tokens, prompt, system)
    elif provider in ("GEMINI", "GOOGLE"):
        return call_gemini(model, temperature, max_tokens, prompt, system)
    else:
        raise ValueError(f"Unknown provider: {provider}. Supported: CLAUDE, GEMINI")
