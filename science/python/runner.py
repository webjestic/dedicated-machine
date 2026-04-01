#!/usr/bin/env python3
"""
PARC experiment runner.

Runs any PARC experiment that follows the standard structure:

    experiment-dir/
      config.json          required — model, variants, run count
      variants/            required — A-name.md, B-name.md, ...
      ARTIFACT.md          optional — injected as {{ARTIFACT}} in variant files
      data/
        runs/              written — per-run JSON records + totals.json
        raw/               written — raw model output per run

Usage:
    python runner.py <experiment-dir>
    python runner.py <experiment-dir> --variant A
    python runner.py <experiment-dir> --variant B --start-run 5
    python runner.py <experiment-dir> --dry-run

config.json format:
    {
      "experiment":       "exp-01",
      "description":      "human-readable label",
      "provider":         "CLAUDE" | "GEMINI",
      "model":            "claude-sonnet-4-6",
      "temperature":      0.5,
      "max_tokens":       2500,
      "runs_per_variant": 10,
      "variants":         ["A", "B", "C"],
      "artifact":         "ARTIFACT.md"   // optional
    }

Custom experiments can import from lib/ directly for non-standard prompt
construction while still using the shared API, cost, and output utilities.
"""

import argparse
import os
import sys
from pathlib import Path

_here = Path(__file__).parent
sys.path.insert(0, str(_here))

from lib.config import load_config, load_env, find_models
from lib.api import call_api
from lib.costs import load_model_pricing, calculate_cost
from lib.output import (
    save_raw_output, build_run_record, save_run_record,
    load_totals, update_totals, save_totals,
)


# ---------------------------------------------------------------------------
# Variant loading
# ---------------------------------------------------------------------------

def load_variant(variants_dir: Path, variant_id: str, artifact: str = "") -> str:
    matches = list(variants_dir.glob(f"{variant_id}-*.md"))
    if not matches:
        raise FileNotFoundError(f"No variant file for '{variant_id}' in {variants_dir}")
    text = matches[0].read_text()
    if artifact:
        text = text.replace("{{ARTIFACT}}", artifact)
    return text


def get_variant_name(variants_dir: Path, variant_id: str) -> str:
    matches = list(variants_dir.glob(f"{variant_id}-*.md"))
    if not matches:
        return variant_id
    return matches[0].stem[len(variant_id) + 1:]


# ---------------------------------------------------------------------------
# Dry run
# ---------------------------------------------------------------------------

def dry_run(exp_dir: Path, config: dict, pricing: dict) -> None:
    variants = config["variants"]
    n = config["runs_per_variant"]
    print(f"\n=== DRY RUN: {config['experiment']} ===")
    if config.get("description"):
        print(f"  {config['description']}")
    print(f"  Provider:    {config['provider']}")
    print(f"  Model:       {config['model']}")
    print(f"  Temperature: {config['temperature']}")
    print(f"  Max tokens:  {config['max_tokens']}")
    print(f"  Variants:    {variants}")
    print(f"  Runs each:   {n}  (total: {len(variants) * n})")
    print(f"  Pricing:")
    print(f"    Input:     {pricing.get('inprice', 'n/a')}")
    print(f"    Output:    {pricing.get('outprice', 'n/a')}")
    if config.get("artifact"):
        artifact_path = exp_dir / config["artifact"]
        status = "found" if artifact_path.exists() else "MISSING"
        print(f"  Artifact:    {config['artifact']} ({status})")
    print(f"  Output:")
    print(f"    Runs:      {exp_dir / 'data' / 'runs'}")
    print(f"    Raw:       {exp_dir / 'data' / 'raw'}")
    print()


# ---------------------------------------------------------------------------
# Experiment execution
# ---------------------------------------------------------------------------

def run_experiment(exp_dir: Path, config: dict, pricing: dict,
                   variants_to_run: list[str], start_run: int = 1) -> None:
    variants_dir = exp_dir / "variants"
    runs_dir = exp_dir / "data" / "runs"
    raw_dir = exp_dir / "data" / "raw"

    artifact = ""
    if config.get("artifact"):
        artifact_path = exp_dir / config["artifact"]
        if artifact_path.exists():
            artifact = artifact_path.read_text()
        else:
            print(f"Warning: artifact '{config['artifact']}' not found in {exp_dir}",
                  file=sys.stderr)

    totals = load_totals(runs_dir)

    for variant_id in variants_to_run:
        prompt = load_variant(variants_dir, variant_id, artifact)
        variant_name = get_variant_name(variants_dir, variant_id)

        run_start = start_run if variant_id == variants_to_run[0] else 1
        n = config["runs_per_variant"]
        print(f"\n[{variant_id}] {variant_name} — runs {run_start}–{n}")

        for run_num in range(run_start, n + 1):
            print(f"  run {run_num:02d}...", end=" ", flush=True)

            response = call_api(
                config["provider"],
                config["model"],
                config["temperature"],
                config["max_tokens"],
                prompt,
            )

            cost = calculate_cost(pricing, response.input_tokens, response.output_tokens)
            output_file = save_raw_output(raw_dir, variant_id, run_num, response.text)
            record = build_run_record(config, variant_id, variant_name, run_num,
                                      response, cost, output_file, exp_dir)
            save_run_record(runs_dir, record)
            totals = update_totals(totals, record)
            save_totals(runs_dir, totals)

            print(f"in={response.input_tokens} out={response.output_tokens} ${cost:.4f}")

    print(f"\n=== Done ===")
    print(f"  Runs:  {totals['totalRuns']}  Cost: ${totals['totalCostUSD']:.4f}")
    print(f"  Data:  {runs_dir}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="PARC experiment runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "experiment",
        metavar="EXPERIMENT_DIR",
        help="Path to experiment directory containing config.json",
    )
    parser.add_argument(
        "--variant",
        metavar="ID",
        help="Run a single variant only (e.g. A, B, C)",
    )
    parser.add_argument(
        "--start-run",
        type=int,
        default=1,
        metavar="N",
        help="Resume from run N for the first variant (default: 1)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print config and pricing without making API calls",
    )
    args = parser.parse_args()

    exp_dir = Path(args.experiment).resolve()
    if not exp_dir.is_dir():
        print(f"Error: not a directory: {exp_dir}", file=sys.stderr)
        sys.exit(1)

    load_env(exp_dir)
    config = load_config(exp_dir)
    models_path = find_models(_here)
    pricing = load_model_pricing(models_path, config["provider"], config["model"])

    valid_variants = config["variants"]
    if args.variant:
        if args.variant not in valid_variants:
            print(f"Error: variant '{args.variant}' not in {valid_variants}", file=sys.stderr)
            sys.exit(1)
        variants_to_run = [args.variant]
    else:
        variants_to_run = valid_variants

    # Validate max_tokens against model ceiling
    model_ceiling = pricing.get("max_tokens")
    if model_ceiling and config["max_tokens"] > model_ceiling:
        print(
            f"Error: max_tokens {config['max_tokens']} exceeds model ceiling "
            f"{model_ceiling} for {config['model']}",
            file=sys.stderr,
        )
        sys.exit(1)

    if args.dry_run:
        dry_run(exp_dir, config, pricing)
        return

    provider = config["provider"].upper()
    if provider == "CLAUDE" and not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY not set", file=sys.stderr)
        sys.exit(1)
    if provider in ("GEMINI", "GOOGLE") and not os.environ.get("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    run_experiment(exp_dir, config, pricing, variants_to_run, args.start_run)


if __name__ == "__main__":
    main()
