"""
Exp-21b Scorer — Zombie-Write Binary Detection (Vocabulary-Only Slot-Swap).

Same detection criteria as exp-19. Same artifact.
Key difference: exp-21b variants have vocabulary orientation, not explicit procedure.
Expected: A may detect less reliably than exp-19 (no explicit procedure guide).

Detection requires ALL of:
  1. Process-pause scenario named (GC pause, VM migration, OS scheduler, all threads frozen)
  2. Fencing token OR optimistic lock at DB write level named as the fix

Usage:
    python scorer.py              # score all outputs in output/
    python scorer.py --variant A  # score a single variant
"""

import argparse
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "output"
REVIEW_DIR = SCRIPT_DIR / "review"

# Keywords indicating process-pause scenario (finding)
PAUSE_KEYWORDS = [
    r"GC pause", r"garbage.collect", r"stop.the.world", r"stop the world",
    r"VM migration", r"OS scheduler", r"process pause", r"all threads",
    r"simultaneously paused", r"simultaneously frozen", r"paused simultaneously",
    r"STW", r"safepoint",
]

# Keywords indicating fix found
FIX_KEYWORDS = [
    r"fencing token", r"optimistic lock", r"optimistic concurren",
    r"compare.and.swap", r"compare and swap", r"CAS ",
    r"WHERE.*stock\s*=", r"WHERE.*version\s*=", r"WHERE.*current",
    r"version column", r"row version", r"version number",
    r"conditional update", r"atomic update.*condition",
    r"UPDATE.*WHERE.*=.*stock", r"UPDATE.*WHERE.*=.*quantity",
]

# Red herring — heartbeat/TTL concern without process-pause understanding
SHALLOW_KEYWORDS = [
    r"TTL.*short", r"TTL.*too short", r"increase.*TTL", r"extend.*TTL",
    r"heartbeat.*insufficient", r"heartbeat.*not enough",
    r"lock.*expire", r"lock.*expir",
]


def score_output(text: str) -> dict:
    pause_found = any(re.search(p, text, re.IGNORECASE) for p in PAUSE_KEYWORDS)
    fix_found = any(re.search(f, text, re.IGNORECASE) for f in FIX_KEYWORDS)
    shallow_only = any(re.search(s, text, re.IGNORECASE) for s in SHALLOW_KEYWORDS)

    if pause_found and fix_found:
        pre_score = 1
        flag = ""
    elif pause_found and not fix_found:
        pre_score = 0
        flag = "REVIEW: pause named, fix missing"
    elif fix_found and not pause_found:
        pre_score = 0
        flag = "REVIEW: fix named, pause scenario missing"
    elif shallow_only:
        pre_score = 0
        flag = "shallow: TTL/heartbeat concern only"
    else:
        pre_score = 0
        flag = ""

    token_estimate = len(text.split())

    return {
        "pre_score": pre_score,
        "pause_found": pause_found,
        "fix_found": fix_found,
        "shallow_only": shallow_only,
        "flag": flag,
        "token_estimate": token_estimate,
    }


def score_variant(variant_id: str) -> list[dict]:
    results = []
    files = sorted(OUTPUT_DIR.glob(f"{variant_id}-*.md"))

    if not files:
        print(f"  No output files found for variant {variant_id}")
        return results

    for f in files:
        run_id = f.stem
        text = f.read_text()
        result = score_output(text)
        result["run_id"] = run_id
        result["variant"] = variant_id
        results.append(result)

    return results


def write_scores(all_results: list[dict]) -> None:
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)

    lines = ["# exp-21b Scored Results\n",
             "**Scoring pass:** keyword pre-screen — review flagged items manually\n\n"]

    variants = sorted(set(r["variant"] for r in all_results))

    for variant_id in variants:
        variant_results = [r for r in all_results if r["variant"] == variant_id]
        detected = sum(r["pre_score"] for r in variant_results)
        mean_tokens = sum(r["token_estimate"] for r in variant_results) / len(variant_results) if variant_results else 0

        lines.append(f"## Variant {variant_id}\n\n")
        lines.append(f"**Pre-screen detection:** {detected}/{len(variant_results)} | "
                     f"**Mean token estimate:** {mean_tokens:.0f}\n\n")
        lines.append("| Run | Pre-score | Pause | Fix | Flag |\n")
        lines.append("|-----|-----------|-------|-----|------|\n")

        for r in variant_results:
            lines.append(
                f"| {r['run_id']} | {r['pre_score']} | "
                f"{'✓' if r['pause_found'] else '✗'} | "
                f"{'✓' if r['fix_found'] else '✗'} | "
                f"{r['flag']} |\n"
            )
        lines.append("\n")

    lines.append("## Summary\n\n")
    lines.append("| Variant | Pre-screen detected | Mean tokens (est) |\n")
    lines.append("|---------|--------------------|---------------|\n")
    for variant_id in variants:
        variant_results = [r for r in all_results if r["variant"] == variant_id]
        detected = sum(r["pre_score"] for r in variant_results)
        mean_tokens = sum(r["token_estimate"] for r in variant_results) / len(variant_results) if variant_results else 0
        lines.append(f"| {variant_id} | {detected}/{len(variant_results)} | {mean_tokens:.0f} |\n")

    lines.append("\n---\n\n")
    lines.append("**Note:** Pre-screen scores require manual verification for REVIEW-flagged items.\n")
    lines.append("Keyword match without process-pause context = 0 per SCORING.md.\n")
    lines.append("Exp-21b calibration target: A >= 5/10 (vocabulary-only, lower than exp-19), C <= 2/10.\n")

    out_path = REVIEW_DIR / "scores.md"
    out_path.write_text("".join(lines))
    print(f"\nScores written to {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Exp-21b scorer")
    parser.add_argument("--variant", choices=["A", "B", "C"],
                        help="Score a single variant only")
    args = parser.parse_args()

    variants = [args.variant] if args.variant else ["A", "B", "C"]
    all_results = []

    for variant_id in variants:
        print(f"Scoring variant {variant_id}...")
        results = score_variant(variant_id)
        all_results.extend(results)
        if results:
            detected = sum(r["pre_score"] for r in results)
            flagged = sum(1 for r in results if r["flag"].startswith("REVIEW"))
            print(f"  {detected}/{len(results)} detected | {flagged} flagged for review")

    if all_results:
        write_scores(all_results)


if __name__ == "__main__":
    main()
