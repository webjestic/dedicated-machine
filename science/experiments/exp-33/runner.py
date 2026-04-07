#!/usr/bin/env python3
"""
exp-33 pipeline runner — zombie-write two-agent pipeline on claude-sonnet-4-6.

Replicates exp-29 (n=1, Opus) at n=10 on Sonnet to isolate pipeline architecture
effect from model capability effect.

Each run:
  1. Agent 1 (Layer 1): correctness review — zombie-layer1-review.md + artifact
  2. Agent 2 (Layer 2): production readiness — zombie-layer2-review.md + artifact + L1 handoff

Usage:
    python runner.py [--start-run N] [--dry-run]
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

_here = Path(__file__).parent
_lib = _here.parent.parent / "python"
sys.path.insert(0, str(_lib))

from lib.api import call_api
from lib.costs import load_model_pricing, calculate_cost
from lib.config import load_env, find_models

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

EXPERIMENT = "exp-33"
MODEL = "claude-sonnet-4-6"
PROVIDER = "CLAUDE"
TEMPERATURE = 0.5
MAX_TOKENS_L1 = 3000
MAX_TOKENS_L2 = 4000
N_RUNS = 10

LAYER1_PROMPT = _here.parent.parent.parent / "examples" / "zombie-layer1-review.md"
LAYER2_PROMPT = _here.parent.parent.parent / "examples" / "zombie-layer2-review.md"
ARTIFACT_PATH = _here.parent / "exp-09" / "ARTIFACT.md"

RAW_DIR = _here / "data" / "raw"
RUNS_DIR = _here / "data" / "runs"


# ---------------------------------------------------------------------------
# Handoff extraction
# ---------------------------------------------------------------------------

def extract_handoff_summary(agent1_output: str) -> str:
    """Extract the handoff summary section from Agent 1's output."""
    # Try bold markdown heading: **Handoff summary...**
    match = re.search(
        r'\*\*[Hh]andoff summary[^:*]*:\*\*\s*(.*?)(?=\n\n\*\*|\Z)',
        agent1_output, re.DOTALL
    )
    if match:
        return match.group(1).strip()

    # Try plain heading: "Handoff summary for ...: "
    match = re.search(
        r'[Hh]andoff summary[^\n]*:\s*\n(.*?)(?=\n\n[A-Z*\[]|\Z)',
        agent1_output, re.DOTALL
    )
    if match:
        return match.group(1).strip()

    # Fallback: last two paragraphs
    paragraphs = [p.strip() for p in agent1_output.split('\n\n') if p.strip()]
    return '\n\n'.join(paragraphs[-2:]) if len(paragraphs) >= 2 else agent1_output[-600:]


# ---------------------------------------------------------------------------
# Output recording
# ---------------------------------------------------------------------------

def save_run_record(run_num: int, l1_resp, l2_resp, l1_cost, l2_cost,
                    l1_file: Path, l2_file: Path, handoff: str) -> dict:
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    record = {
        "runId": f"run-{run_num:02d}",
        "experiment": EXPERIMENT,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model": MODEL,
        "temperature": TEMPERATURE,
        "layer1": {
            "inputTokens": l1_resp.input_tokens,
            "outputTokens": l1_resp.output_tokens,
            "costUSD": l1_cost,
            "outputFile": str(l1_file.relative_to(_here)),
        },
        "layer2": {
            "inputTokens": l2_resp.input_tokens,
            "outputTokens": l2_resp.output_tokens,
            "costUSD": l2_cost,
            "outputFile": str(l2_file.relative_to(_here)),
        },
        "handoffExtracted": handoff[:300] + "..." if len(handoff) > 300 else handoff,
        "totalInputTokens": l1_resp.input_tokens + l2_resp.input_tokens,
        "totalOutputTokens": l1_resp.output_tokens + l2_resp.output_tokens,
        "totalCostUSD": round(l1_cost + l2_cost, 6),
    }
    (RUNS_DIR / f"run-{run_num:02d}.json").write_text(json.dumps(record, indent=2))
    return record


def load_totals() -> dict:
    defaults: dict = {
        "experiment": EXPERIMENT,
        "totalRuns": 0,
        "totalInputTokens": 0,
        "totalOutputTokens": 0,
        "totalCostUSD": 0.0,
        "runs": [],
    }
    path = RUNS_DIR / "totals.json"
    if path.exists():
        defaults.update(json.loads(path.read_text()))
    return defaults


def update_and_save_totals(totals: dict, record: dict) -> dict:
    totals["experiment"] = EXPERIMENT
    totals["totalRuns"] += 1
    totals["totalInputTokens"] += record["totalInputTokens"]
    totals["totalOutputTokens"] += record["totalOutputTokens"]
    totals["totalCostUSD"] = round(totals["totalCostUSD"] + record["totalCostUSD"], 6)
    totals["runs"].append({
        "runId": record["runId"],
        "timestamp": record["timestamp"],
        "l1CostUSD": record["layer1"]["costUSD"],
        "l2CostUSD": record["layer2"]["costUSD"],
        "totalCostUSD": record["totalCostUSD"],
    })
    (RUNS_DIR / "totals.json").write_text(json.dumps(totals, indent=2))
    return totals


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="exp-33 pipeline runner")
    parser.add_argument("--start-run", type=int, default=1, metavar="N",
                        help="Resume from run N (default: 1)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print config without making API calls")
    args = parser.parse_args()

    load_env(_here)

    models_path = find_models(_lib)
    pricing = load_model_pricing(models_path, PROVIDER, MODEL)

    if args.dry_run:
        print(f"\n=== DRY RUN: {EXPERIMENT} ===")
        print(f"  Model:          {MODEL}")
        print(f"  Temperature:    {TEMPERATURE}")
        print(f"  Runs:           {N_RUNS}")
        print(f"  L1 max_tokens:  {MAX_TOKENS_L1}")
        print(f"  L2 max_tokens:  {MAX_TOKENS_L2}")
        print(f"  Layer 1 prompt: {LAYER1_PROMPT.name} ({'found' if LAYER1_PROMPT.exists() else 'MISSING'})")
        print(f"  Layer 2 prompt: {LAYER2_PROMPT.name} ({'found' if LAYER2_PROMPT.exists() else 'MISSING'})")
        print(f"  Artifact:       {ARTIFACT_PATH.name} ({'found' if ARTIFACT_PATH.exists() else 'MISSING'})")
        print(f"  Pricing:        {pricing.get('inprice', 'n/a')} in / {pricing.get('outprice', 'n/a')} out")
        # Rough cost estimate: ~4K input tokens per call, ~2K output, 2 calls per run
        est_per_run = (
            calculate_cost(pricing, 4000, 2000) +  # L1
            calculate_cost(pricing, 5500, 3000)    # L2 (larger input with L1 handoff)
        )
        print(f"  Est. cost/run:  ${est_per_run:.4f}")
        print(f"  Est. total:     ${est_per_run * N_RUNS:.4f}")
        print()
        return

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    layer1_template = LAYER1_PROMPT.read_text()
    layer2_template = LAYER2_PROMPT.read_text()
    artifact = ARTIFACT_PATH.read_text()

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    RUNS_DIR.mkdir(parents=True, exist_ok=True)

    totals = load_totals()

    print(f"\n=== {EXPERIMENT} — zombie-write pipeline on {MODEL} ===")
    print(f"  Runs {args.start_run}–{N_RUNS}\n")

    for run_num in range(args.start_run, N_RUNS + 1):
        print(f"Run {run_num:02d}:")

        # Agent 1 — Layer 1 correctness review
        l1_prompt = layer1_template.replace("{{CODE}}", artifact)
        print(f"  L1...", end=" ", flush=True)
        l1_resp = call_api(PROVIDER, MODEL, TEMPERATURE, MAX_TOKENS_L1, l1_prompt)
        l1_cost = calculate_cost(pricing, l1_resp.input_tokens, l1_resp.output_tokens)
        l1_file = RAW_DIR / f"L1-{run_num:02d}.md"
        l1_file.write_text(l1_resp.text)
        print(f"in={l1_resp.input_tokens} out={l1_resp.output_tokens} ${l1_cost:.4f}")

        # Extract handoff summary from Agent 1 output
        handoff = extract_handoff_summary(l1_resp.text)

        # Agent 2 — Layer 2 production readiness review
        l2_prompt = (layer2_template
                     .replace("{{CODE}}", artifact)
                     .replace("{{LAYER_1_SUMMARY}}", handoff))
        print(f"  L2...", end=" ", flush=True)
        l2_resp = call_api(PROVIDER, MODEL, TEMPERATURE, MAX_TOKENS_L2, l2_prompt)
        l2_cost = calculate_cost(pricing, l2_resp.input_tokens, l2_resp.output_tokens)
        l2_file = RAW_DIR / f"L2-{run_num:02d}.md"
        l2_file.write_text(l2_resp.text)
        print(f"in={l2_resp.input_tokens} out={l2_resp.output_tokens} ${l2_cost:.4f}")

        record = save_run_record(run_num, l1_resp, l2_resp, l1_cost, l2_cost,
                                 l1_file, l2_file, handoff)
        totals = update_and_save_totals(totals, record)
        print(f"  run {run_num:02d} total: ${record['totalCostUSD']:.4f}\n")

    print(f"=== Done ===")
    print(f"  Runs: {totals['totalRuns']}  Cost: ${totals['totalCostUSD']:.4f}")
    print(f"  Raw:  {RAW_DIR}")
    print(f"  Data: {RUNS_DIR}")


if __name__ == "__main__":
    main()
