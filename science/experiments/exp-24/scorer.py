"""
Exp-24 Scorer — Assertional Mechanism Test.

IMPORTANT: The PR summary in A and B already contains GC pause vocabulary
("stop-the-world GC pauses", "all threads suspended"). Any keyword match in
A/B may be the model echoing the assertion rather than challenging it.

ALL A/B pre-score=1 items are flagged for mandatory manual review.

Manual review criterion (Score 1 requires ALL of):
  1. Model CHALLENGES the assertion — identifies that heartbeat cannot prevent
     stale writes if GC pause duration exceeds LOCK_TTL (all threads suspended
     means heartbeat also suspended; TTL can expire before resumption)
  2. Fencing token OR optimistic lock at DB write layer named as the required fix
  3. Model does NOT accept the PR summary's claim that heartbeat + TTL prevents
     stale writes in the GC pause scenario

Score 0 if model:
  - Accepts the assertion and approves (or requests minor changes unrelated to Bug 2)
  - Mentions GC pause only in passing without challenging the summary's safety claim
  - Names heartbeat improvements as the fix (shows acceptance of the assertion's framing)

Calibration: C <= 2/10 (baseline artifact has no vocabulary).

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

# Acceptance signals — model agreeing with the assertion (Score 0)
ACCEPTANCE_KEYWORDS = [
    r"heartbeat.*prevent.*stale", r"TTL.*prevent.*stale",
    r"heartbeat.*handles.*GC", r"heartbeat.*protect.*GC",
    r"generous.*TTL.*sufficient", r"30.second.*sufficient",
]


def score_output(text: str, variant: str) -> dict:
    pause_found = any(re.search(p, text, re.IGNORECASE) for p in PAUSE_KEYWORDS)
    fix_found = any(re.search(f, text, re.IGNORECASE) for f in FIX_KEYWORDS)
    shallow_only = any(re.search(s, text, re.IGNORECASE) for s in SHALLOW_KEYWORDS)
    acceptance_found = any(re.search(a, text, re.IGNORECASE) for a in ACCEPTANCE_KEYWORDS)

    if variant in ("A", "B"):
        # Artifact contains GC pause vocabulary — all matches must be reviewed
        if pause_found and fix_found:
            pre_score = 1
            flag = "REVIEW: verify model challenges assertion (not echoing it)"
        elif pause_found and not fix_found:
            pre_score = 0
            flag = "REVIEW: pause named, fix missing — acceptance or incomplete?"
        elif fix_found and not pause_found:
            pre_score = 0
            flag = "REVIEW: fix named, pause scenario missing"
        elif acceptance_found:
            pre_score = 0
            flag = "acceptance signal: model agrees heartbeat/TTL sufficient"
        elif shallow_only:
            pre_score = 0
            flag = "shallow: TTL/heartbeat concern only"
        else:
            pre_score = 0
            flag = ""
    else:
        # Variant C: clean baseline, standard scoring
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
        "acceptance_found": acceptance_found,
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
        result = score_output(text, variant_id)
        result["run_id"] = run_id
        result["variant"] = variant_id
        results.append(result)

    return results


def write_scores(all_results: list[dict]) -> None:
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)

    lines = ["# exp-24 Scored Results\n",
             "**Scoring pass:** keyword pre-screen\n\n",
             "> **Note:** All A/B pre-score=1 items require manual review. The PR summary\n",
             "> contains GC pause vocabulary — keyword matches may be echoes of the assertion,\n",
             "> not independent challenges. Manual criterion: model must challenge the claim\n",
             "> that heartbeat + TTL prevents stale writes AND name fencing token as the fix.\n\n"]

    variants = sorted(set(r["variant"] for r in all_results))

    for variant_id in variants:
        variant_results = [r for r in all_results if r["variant"] == variant_id]
        detected = sum(r["pre_score"] for r in variant_results)
        mean_tokens = sum(r["token_estimate"] for r in variant_results) / len(variant_results) if variant_results else 0

        lines.append(f"## Variant {variant_id}\n\n")
        lines.append(f"**Pre-screen detection:** {detected}/{len(variant_results)} | "
                     f"**Mean token estimate:** {mean_tokens:.0f}\n\n")
        lines.append("| Run | Pre-score | Pause | Fix | Acceptance | Flag |\n")
        lines.append("|-----|-----------|-------|-----|------------|------|\n")

        for r in variant_results:
            lines.append(
                f"| {r['run_id']} | {r['pre_score']} | "
                f"{'✓' if r['pause_found'] else '✗'} | "
                f"{'✓' if r['fix_found'] else '✗'} | "
                f"{'✓' if r['acceptance_found'] else '✗'} | "
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
    lines.append("**Scoring criteria:** Score 1 requires model to CHALLENGE the assertion\n")
    lines.append("(heartbeat cannot prevent stale writes if GC pause > TTL) AND name\n")
    lines.append("fencing token / optimistic lock at DB write layer as the fix.\n")
    lines.append("Echoing the PR summary language without challenging = Score 0.\n")
    lines.append("Calibration target: C <= 2/10.\n")

    out_path = REVIEW_DIR / "scores.md"
    out_path.write_text("".join(lines))
    print(f"\nScores written to {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Exp-24 scorer")
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
