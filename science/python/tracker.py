#!/usr/bin/env python3
"""
PARC cost and run tracker.

Reads data/runs/totals.json from every experiment and produces a cost
summary across the full research program.

Usage:
    python tracker.py                        # summary across all experiments
    python tracker.py --experiment exp-01    # single experiment detail
    python tracker.py --by-model             # aggregate by model
    python tracker.py --by-provider          # aggregate by provider
"""

import argparse
import json
import sys
from pathlib import Path

_here = Path(__file__).parent
sys.path.insert(0, str(_here))

from lib.config import find_models

EXPERIMENTS_DIR = _here.parent / "experiments"


def load_all_totals() -> list[dict]:
    records = []
    for totals_file in sorted(EXPERIMENTS_DIR.glob("*/data/runs/totals.json")):
        try:
            data = json.loads(totals_file.read_text())
            data["_experiment_dir"] = totals_file.parent.parent.parent.name
            records.append(data)
        except (json.JSONDecodeError, KeyError):
            pass
    return records


def fmt_cost(cost: float) -> str:
    return f"${cost:.4f}"


def fmt_tokens(n: int) -> str:
    if n >= 1_000_000:
        return f"{n/1_000_000:.2f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(n)


def print_summary(records: list[dict]) -> None:
    if not records:
        print("No experiment run data found.")
        return

    total_runs = sum(r.get("totalRuns", 0) for r in records)
    total_cost = sum(r.get("totalCostUSD", 0.0) for r in records)
    total_in = sum(r.get("totalInputTokens", 0) for r in records)
    total_out = sum(r.get("totalOutputTokens", 0) for r in records)

    print(f"\n{'─' * 64}")
    print(f"  PARC Research Tracker")
    print(f"{'─' * 64}")
    print(f"  Experiments with data:  {len(records)}")
    print(f"  Total runs:             {total_runs:,}")
    print(f"  Total input tokens:     {fmt_tokens(total_in)}")
    print(f"  Total output tokens:    {fmt_tokens(total_out)}")
    print(f"  Total cost:             {fmt_cost(total_cost)}")
    print(f"{'─' * 64}\n")

    print(f"  {'Experiment':<16} {'Runs':>6} {'Input':>8} {'Output':>8} {'Cost':>10}")
    print(f"  {'─'*16} {'─'*6} {'─'*8} {'─'*8} {'─'*10}")
    for r in records:
        exp = r.get("experiment") or r.get("_experiment_dir", "?")
        runs = r.get("totalRuns", 0)
        inp = fmt_tokens(r.get("totalInputTokens", 0))
        out = fmt_tokens(r.get("totalOutputTokens", 0))
        cost = fmt_cost(r.get("totalCostUSD", 0.0))
        print(f"  {exp:<16} {runs:>6} {inp:>8} {out:>8} {cost:>10}")

    print(f"\n  {'─'*16} {'─'*6} {'─'*8} {'─'*8} {'─'*10}")
    print(f"  {'TOTAL':<16} {total_runs:>6} {fmt_tokens(total_in):>8} "
          f"{fmt_tokens(total_out):>8} {fmt_cost(total_cost):>10}\n")


def print_experiment_detail(records: list[dict], experiment: str) -> None:
    match = [r for r in records
             if r.get("experiment") == experiment or r.get("_experiment_dir") == experiment]
    if not match:
        print(f"No run data found for '{experiment}'")
        return

    r = match[0]
    print(f"\n{'─' * 48}")
    print(f"  {r.get('experiment', experiment)}")
    print(f"{'─' * 48}")
    print(f"  Total runs:    {r.get('totalRuns', 0):,}")
    print(f"  Input tokens:  {fmt_tokens(r.get('totalInputTokens', 0))}")
    print(f"  Output tokens: {fmt_tokens(r.get('totalOutputTokens', 0))}")
    print(f"  Total cost:    {fmt_cost(r.get('totalCostUSD', 0.0))}")

    by_variant = r.get("byVariant", {})
    if by_variant:
        print(f"\n  {'Variant':<24} {'Runs':>5} {'Input':>8} {'Output':>8} {'Cost':>10}")
        print(f"  {'─'*24} {'─'*5} {'─'*8} {'─'*8} {'─'*10}")
        for vid, v in sorted(by_variant.items()):
            name = v.get("variantName", "")
            label = f"{vid} — {name}"[:24]
            print(f"  {label:<24} {v.get('runs',0):>5} "
                  f"{fmt_tokens(v.get('inputTokens',0)):>8} "
                  f"{fmt_tokens(v.get('outputTokens',0)):>8} "
                  f"{fmt_cost(v.get('costUSD',0.0)):>10}")
    print()


def print_by_model(records: list[dict]) -> None:
    by_model: dict[str, dict] = {}
    for r in records:
        for model, data in r.get("byModel", {}).items():
            if model not in by_model:
                by_model[model] = {"inputTokens": 0, "outputTokens": 0, "costUSD": 0.0, "experiments": 0}
            by_model[model]["inputTokens"] += data.get("inputTokens", 0)
            by_model[model]["outputTokens"] += data.get("outputTokens", 0)
            by_model[model]["costUSD"] += data.get("costUSD", 0.0)
            by_model[model]["experiments"] += 1

    print(f"\n{'─' * 72}")
    print(f"  Cost by Model")
    print(f"{'─' * 72}")
    print(f"  {'Model':<32} {'Exps':>5} {'Input':>8} {'Output':>8} {'Cost':>10}")
    print(f"  {'─'*32} {'─'*5} {'─'*8} {'─'*8} {'─'*10}")
    for model, data in sorted(by_model.items(), key=lambda x: -x[1]["costUSD"]):
        print(f"  {model:<32} {data['experiments']:>5} "
              f"{fmt_tokens(data['inputTokens']):>8} "
              f"{fmt_tokens(data['outputTokens']):>8} "
              f"{fmt_cost(data['costUSD']):>10}")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="PARC cost and run tracker")
    parser.add_argument("--experiment", metavar="ID",
                        help="Show detail for a single experiment")
    parser.add_argument("--by-model", action="store_true",
                        help="Aggregate costs by model")
    args = parser.parse_args()

    records = load_all_totals()

    if args.experiment:
        print_experiment_detail(records, args.experiment)
    elif args.by_model:
        print_by_model(records)
    else:
        print_summary(records)


if __name__ == "__main__":
    main()
