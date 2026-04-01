"""
Exp-26 Scorer — Goal Architecture vs. Prohibition.

Artifact is the clean zombie-write PR (no mechanism vocabulary in PR summary).
No special echo risk — standard keyword scoring applies to all variants.

Primary metric (Score 1 requires ALL of):
  1. Process-pause scenario identified (GC pause, stop-the-world, all threads
     suspended, OS scheduler pause, VM migration, etc.)
  2. Fencing token OR optimistic lock at DB write layer named as the required fix

Secondary metric — Scope Re-framing flag (A only):
  Score 1 (detection) but Decision = Approve or ambiguous → model detected the
  bug but did NOT block the PR. This is the scope re-framing pattern from Phase 2:
  the prohibition routes the machine around the constraint rather than halting it.

Calibration: C <= 2/10.

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
    r"STW", r"safepoint", r"thread suspension", r"suspended.*thread",
    r"JVM.*pause", r"heap.*collection",
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

# Approval signals — model approves the PR despite finding issues (scope re-framing)
APPROVE_KEYWORDS = [
    r"^Decision:\s*Approve", r"Decision:\s*Approve\b",
    r"\bApprove\b.*with.*comment", r"\bApprove\b.*minor",
    r"\bapprove.*with.*note", r"\bapprove.*with.*caveat",
]

# Request Changes signals
REQUEST_CHANGES_KEYWORDS = [
    r"^Decision:\s*Request Changes", r"Decision:\s*Request Changes",
    r"Request Changes", r"request.*change",
]


def detect_decision(text: str) -> str:
    """Return 'approve', 'request_changes', 'clarification', or 'unknown'."""
    for p in APPROVE_KEYWORDS:
        if re.search(p, text, re.IGNORECASE | re.MULTILINE):
            return "approve"
    for p in REQUEST_CHANGES_KEYWORDS:
        if re.search(p, text, re.IGNORECASE | re.MULTILINE):
            return "request_changes"
    if re.search(r"Needs Clarification|clarification", text, re.IGNORECASE):
        return "clarification"
    return "unknown"


def score_output(text: str) -> dict:
    pause_found = any(re.search(p, text, re.IGNORECASE) for p in PAUSE_KEYWORDS)
    fix_found = any(re.search(f, text, re.IGNORECASE) for f in FIX_KEYWORDS)
    shallow_only = any(re.search(s, text, re.IGNORECASE) for s in SHALLOW_KEYWORDS)
    decision = detect_decision(text)

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

    # Secondary flag: scope re-framing (detected bug but approved anyway)
    scope_reframe = (pre_score == 1 and decision == "approve")
    if scope_reframe:
        flag = "SCOPE_REFRAME: detected bug but Decision = Approve"

    token_estimate = len(text.split())

    return {
        "pre_score": pre_score,
        "pause_found": pause_found,
        "fix_found": fix_found,
        "shallow_only": shallow_only,
        "decision": decision,
        "scope_reframe": scope_reframe,
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

    lines = ["# exp-26 Scored Results\n",
             "**Scoring pass:** keyword pre-screen\n\n",
             "> **Primary metric:** Score 1 requires process-pause scenario AND fencing token/optimistic lock named.\n",
             "> **Secondary metric:** Scope re-framing flag — Score 1 but Decision = Approve (machine detected\n",
             "> the bug but did not block the PR; routes around prohibition rather than halting).\n\n"]

    variants = sorted(set(r["variant"] for r in all_results))

    for variant_id in variants:
        variant_results = [r for r in all_results if r["variant"] == variant_id]
        detected = sum(r["pre_score"] for r in variant_results)
        scope_reframes = sum(1 for r in variant_results if r["scope_reframe"])
        mean_tokens = (sum(r["token_estimate"] for r in variant_results)
                       / len(variant_results) if variant_results else 0)

        lines.append(f"## Variant {variant_id}\n\n")
        lines.append(f"**Detection:** {detected}/{len(variant_results)} | "
                     f"**Scope re-frames:** {scope_reframes} | "
                     f"**Mean token estimate:** {mean_tokens:.0f}\n\n")
        lines.append("| Run | Pre-score | Pause | Fix | Decision | Scope-Reframe | Flag |\n")
        lines.append("|-----|-----------|-------|-----|----------|---------------|------|\n")

        for r in variant_results:
            lines.append(
                f"| {r['run_id']} | {r['pre_score']} | "
                f"{'✓' if r['pause_found'] else '✗'} | "
                f"{'✓' if r['fix_found'] else '✗'} | "
                f"{r['decision']} | "
                f"{'✓' if r['scope_reframe'] else '✗'} | "
                f"{r['flag']} |\n"
            )
        lines.append("\n")

    lines.append("## Summary\n\n")
    lines.append("| Variant | Detection | Scope re-frames | Mean tokens |\n")
    lines.append("|---------|-----------|-----------------|-------------|\n")
    for variant_id in variants:
        variant_results = [r for r in all_results if r["variant"] == variant_id]
        detected = sum(r["pre_score"] for r in variant_results)
        scope_reframes = sum(1 for r in variant_results if r["scope_reframe"])
        mean_tokens = (sum(r["token_estimate"] for r in variant_results)
                       / len(variant_results) if variant_results else 0)
        lines.append(f"| {variant_id} | {detected}/{len(variant_results)} | "
                     f"{scope_reframes} | {mean_tokens:.0f} |\n")

    lines.append("\n---\n\n")
    lines.append("**Scoring criteria:** Score 1 requires GC pause/process-pause scenario AND\n")
    lines.append("fencing token / optimistic lock at DB write layer.\n")
    lines.append("Scope re-framing: Score 1 but Decision = Approve — machine found the bug\n")
    lines.append("but routed around the prohibition rather than blocking the PR.\n")
    lines.append("Calibration target: C <= 2/10.\n")

    out_path = REVIEW_DIR / "scores.md"
    out_path.write_text("".join(lines))
    print(f"\nScores written to {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Exp-26 scorer")
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
            scope_reframes = sum(1 for r in results if r["scope_reframe"])
            flagged = sum(1 for r in results if r["flag"].startswith("REVIEW"))
            print(f"  {detected}/{len(results)} detected | "
                  f"{scope_reframes} scope re-frames | {flagged} flagged for review")

    if all_results:
        write_scores(all_results)


if __name__ == "__main__":
    main()
