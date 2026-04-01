"""Config loading and path discovery for PARC experiment runner."""

import json
import os
from pathlib import Path


def load_env(start: Path) -> None:
    """Walk up directory tree looking for .env and load it."""
    current = start.resolve()
    for _ in range(10):
        candidate = current / ".env"
        if candidate.exists():
            with open(candidate) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, _, val = line.partition("=")
                        os.environ.setdefault(key.strip(), val.strip())
            return
        parent = current.parent
        if parent == current:
            break
        current = parent


def find_models(start: Path) -> Path:
    """Walk up from start looking for api/models.json."""
    current = start.resolve()
    for _ in range(10):
        candidate = current / "api" / "models.json"
        if candidate.exists():
            return candidate
        parent = current.parent
        if parent == current:
            break
        current = parent
    raise FileNotFoundError(f"Could not find api/models.json from {start}")


def load_config(exp_dir: Path) -> dict:
    """Load and validate config.json from experiment directory."""
    config_file = exp_dir / "config.json"
    if not config_file.exists():
        raise FileNotFoundError(f"No config.json in {exp_dir}")
    with open(config_file) as f:
        config = json.load(f)

    required = {"experiment", "provider", "model", "temperature", "max_tokens",
                "runs_per_variant", "variants"}
    missing = required - config.keys()
    if missing:
        raise ValueError(f"config.json missing required keys: {missing}")

    return config
