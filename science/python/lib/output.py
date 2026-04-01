"""Output recording and totals management."""

import json
from datetime import datetime, timezone
from pathlib import Path

from .api import APIResponse


def save_raw_output(raw_dir: Path, variant_id: str, run_num: int, content: str) -> Path:
    raw_dir.mkdir(parents=True, exist_ok=True)
    path = raw_dir / f"{variant_id}-{run_num:02d}.md"
    path.write_text(content)
    return path


def build_run_record(config: dict, variant_id: str, variant_name: str,
                     run_num: int, response: APIResponse,
                     cost: float, output_file: Path, exp_dir: Path) -> dict:
    return {
        "runId": f"{variant_id}-{run_num:02d}",
        "experiment": config["experiment"],
        "variant": variant_id,
        "variantName": variant_name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "provider": config["provider"],
        "model": config["model"],
        "temperature": config["temperature"],
        "inputTokens": response.input_tokens,
        "outputTokens": response.output_tokens,
        "totalTokens": response.input_tokens + response.output_tokens,
        "costUSD": cost,
        "outputFile": str(output_file.relative_to(exp_dir)),
    }


def save_run_record(runs_dir: Path, record: dict) -> None:
    runs_dir.mkdir(parents=True, exist_ok=True)
    path = runs_dir / f"{record['runId']}.json"
    path.write_text(json.dumps(record, indent=2))


def load_totals(runs_dir: Path) -> dict:
    defaults: dict = {
        "experiment": "",
        "totalRuns": 0,
        "totalInputTokens": 0,
        "totalOutputTokens": 0,
        "totalTokens": 0,
        "totalCostUSD": 0.0,
        "byVariant": {},
        "byModel": {},
        "runs": [],
    }
    totals_file = runs_dir / "totals.json"
    if totals_file.exists():
        defaults.update(json.loads(totals_file.read_text()))
    return defaults


def update_totals(totals: dict, record: dict) -> dict:
    totals["experiment"] = record["experiment"]
    totals["totalRuns"] += 1
    totals["totalInputTokens"] += record["inputTokens"]
    totals["totalOutputTokens"] += record["outputTokens"]
    totals["totalTokens"] += record["totalTokens"]
    totals["totalCostUSD"] = round(totals["totalCostUSD"] + record["costUSD"], 6)

    v = record["variant"]
    if v not in totals["byVariant"]:
        totals["byVariant"][v] = {
            "variantName": record["variantName"],
            "runs": 0,
            "inputTokens": 0,
            "outputTokens": 0,
            "costUSD": 0.0,
        }
    bv = totals["byVariant"][v]
    bv["runs"] += 1
    bv["inputTokens"] += record["inputTokens"]
    bv["outputTokens"] += record["outputTokens"]
    bv["costUSD"] = round(bv["costUSD"] + record["costUSD"], 6)

    m = record["model"]
    if m not in totals["byModel"]:
        totals["byModel"][m] = {"inputTokens": 0, "outputTokens": 0, "costUSD": 0.0}
    bm = totals["byModel"][m]
    bm["inputTokens"] += record["inputTokens"]
    bm["outputTokens"] += record["outputTokens"]
    bm["costUSD"] = round(bm["costUSD"] + record["costUSD"], 6)

    totals["runs"].append({
        "runId": record["runId"],
        "variant": record["variant"],
        "timestamp": record["timestamp"],
        "inputTokens": record["inputTokens"],
        "outputTokens": record["outputTokens"],
        "totalTokens": record["totalTokens"],
        "costUSD": record["costUSD"],
    })

    return totals


def save_totals(runs_dir: Path, totals: dict) -> None:
    runs_dir.mkdir(parents=True, exist_ok=True)
    (runs_dir / "totals.json").write_text(json.dumps(totals, indent=2))
