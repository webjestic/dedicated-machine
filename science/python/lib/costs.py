"""Model pricing lookup and cost calculation."""

import json
from pathlib import Path


def load_model_pricing(models_path: Path, provider: str, model_id: str) -> dict:
    """Return the full model entry from models.json, including max_tokens ceiling."""
    with open(models_path) as f:
        models = json.load(f)
    provider_models = models.get(provider.upper(), {}).get("models", [])
    for m in provider_models:
        if m["model"] == model_id:
            return m
    available = [m["model"] for m in provider_models]
    raise ValueError(
        f"Model '{model_id}' not found under provider '{provider}' in {models_path}.\n"
        f"Available: {available}"
    )


def calculate_cost(pricing: dict, input_tokens: int, output_tokens: int) -> float:
    return round(
        (input_tokens * pricing["incfactor"]) + (output_tokens * pricing["outfactor"]),
        6,
    )
