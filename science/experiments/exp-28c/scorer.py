"""
Exp-28c Scorer — SRE Bridge (Rate Limiter Production Readiness Review).

Same 10-item operational checklist as exp-28b, with Tier 1 / Tier 2
split tracked separately. The SRE Bridge hypothesis lives in the Tier 2
column — items that reached 0% across all 40 exp-28b runs.

Tier 1 — engineering-adjacent (accessible to engineering P_p + gap-detection):
  observability, graceful_degrade, client_error_guide, env_driven_config,
  memory_audit

Tier 2 — SRE Wall (0% in all exp-28b variants):
  alerting_policy, load_test_spec, health_check, incident_runbook,
  race_condition_tests

Calibration target: C (P_d baseline) mean <= 2/10 total, <= 1/10 Tier 2.

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

# (label, tier, [patterns])
REQUIREMENTS = [
    (
        "observability", 1,
        [
            r"prometheu", r"\bstatsd\b", r"\bdatadog\b", r"\bnewrelic\b",
            r"metric.*instrument", r"instrument.*metric",
            r"metric.*rate.limit", r"rate.limit.*metric",
            r"gauge.*limit", r"counter.*reject",
            r"track.*rejection", r"rejection.*track",
            r"monitor.*limiter", r"limiter.*monitor",
            r"telemetry.*rate", r"rate.*telemetry",
        ],
    ),
    (
        "alerting_policy", 2,
        [
            r"alert.*threshold", r"threshold.*alert",
            r"page.*oncall", r"oncall.*page", r"on.call.*alert",
            r"alert.*rejection.rate", r"rejection.rate.*alert",
            r"alert.*error.rate", r"error.rate.*alert",
            r"pagerduty", r"opsgenie", r"victorops",
            r"alert.*condition", r"condition.*alert",
            r"notify.*ops", r"ops.*notify",
            r"fire.*alert.*rate", r"rate.*limit.*alert",
        ],
    ),
    (
        "graceful_degrade", 1,
        [
            r"fail.open", r"fail.closed",
            r"fallback.*redis", r"redis.*fallback",
            r"redis.*unavailable", r"unavailable.*redis",
            r"backend.*down.*policy", r"degrad.*policy",
            r"circuit.break",
            r"when.*redis.*fail", r"redis.*fail.*allow",
            r"redis.*down", r"down.*redis.*allow",
        ],
    ),
    (
        "client_error_guide", 1,
        [
            r"x-ratelimit", r"x.ratelimit",
            r"retry.after.*header", r"header.*retry.after",
            r"429.*body.*format", r"body.*format.*429",
            r"error.*response.*format", r"response.*format.*rate",
            r"client.*sdk.*handle", r"sdk.*rate.limit",
            r"rfc.6585",
            r"rate.limit.*documentation", r"document.*rate.limit",
            r"retry.after.*standard", r"standard.*retry",
        ],
    ),
    (
        "load_test_spec", 2,
        [
            r"load.test", r"load.*test.*rate",
            r"throughput.*verif", r"verif.*throughput",
            r"stress.test.*limit", r"limit.*stress.test",
            r"k6\b", r"\bjmeter\b", r"\bgatling\b", r"\bwrk\b",
            r"req.*per.*sec.*test", r"test.*req.*per.*sec",
            r"benchmark.*limit", r"limit.*benchmark",
            r"target.*rps", r"rps.*target",
            r"performance.*test.*rate", r"rate.*performance.*test",
        ],
    ),
    (
        "env_driven_config", 1,
        [
            r"env.*per.route", r"per.route.*env",
            r"environment.*limit.*config", r"config.*limit.*env",
            r"RATE_LIMIT.*env", r"env.*RATE_LIMIT",
            r"process\.env.*limit", r"limit.*process\.env",
            r"config.*without.*deploy", r"without.*deploy.*config",
            r"env.*tunabl", r"tunabl.*env",
            r"env.*per.endpoint", r"per.endpoint.*env",
        ],
    ),
    (
        "health_check", 2,
        [
            r"health.*endpoint.*limit", r"limit.*health.*endpoint",
            r"/health.*rate", r"rate.*\/health",
            r"health.*check.*redis", r"redis.*health.*check",
            r"status.*endpoint.*limiter", r"limiter.*status.*endpoint",
            r"liveness.*probe", r"readiness.*probe",
            r"health.*api.*rate", r"rate.*limiter.*health",
            r"\/metrics.*endpoint", r"metrics.*endpoint.*rate",
        ],
    ),
    (
        "incident_runbook", 2,
        [
            r"runbook",
            r"false.positive.*debug", r"debug.*false.positive",
            r"incident.*rate.limit", r"rate.limit.*incident",
            r"troubleshoot.*block", r"block.*troubleshoot",
            r"diagnos.*false.*block", r"false.*block.*diagnos",
            r"ops.*playbook", r"playbook.*rate",
            r"how.*to.*debug.*limit", r"debug.*unexpect.*block",
            r"on.call.*procedure", r"procedure.*on.call",
        ],
    ),
    (
        "memory_audit", 1,
        [
            r"memory.*leak.*redis", r"redis.*memory.*leak",
            r"unbounded.*key", r"key.*unbounded",
            r"key.*growth.*audit", r"audit.*key.*growth",
            r"redis.*memory.*monitor", r"monitor.*redis.*memory",
            r"key.*eviction.*policy", r"eviction.*policy.*key",
            r"memory.*inspect.*rate", r"rate.*key.*inspect",
            r"maxmemory.*policy",
            r"key.*accumulate", r"accumulate.*key",
        ],
    ),
    (
        "race_condition_tests", 2,
        [
            r"race.*condition.*test", r"test.*race.*condition",
            r"distributed.*lock.*test", r"test.*distributed.*lock",
            r"window.*boundary.*test", r"test.*window.*boundary",
            r"concurrent.*request.*test", r"test.*concurrent.*request",
            r"atomic.*test.*redis", r"test.*atomic.*redis",
            r"lua.*script.*test", r"test.*lua.*script",
            r"split.*brain.*test",
            r"concurren.*race.*test", r"test.*concurren.*race",
        ],
    ),
]

TIER1_LABELS = {label for label, tier, _ in REQUIREMENTS if tier == 1}
TIER2_LABELS = {label for label, tier, _ in REQUIREMENTS if tier == 2}


def score_output(text: str) -> dict:
    scores = {}
    matched_patterns = {}
    total = 0
    tier1_total = 0
    tier2_total = 0

    for label, tier, patterns in REQUIREMENTS:
        hit = False
        for p in patterns:
            if re.search(p, text, re.IGNORECASE):
                hit = True
                matched_patterns[label] = p
                break
        scores[label] = 1 if hit else 0
        total += scores[label]
        if tier == 1:
            tier1_total += scores[label]
        else:
            tier2_total += scores[label]

    token_estimate = len(text.split())

    return {
        "total": total,
        "tier1": tier1_total,
        "tier2": tier2_total,
        "scores": scores,
        "matched_patterns": matched_patterns,
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

    item_labels = [label for label, _, _ in REQUIREMENTS]
    tier1_labels = [label for label, tier, _ in REQUIREMENTS if tier == 1]
    tier2_labels = [label for label, tier, _ in REQUIREMENTS if tier == 2]

    lines = ["# exp-28c Scored Results\n",
             "**Scoring pass:** keyword pre-screen — operational horizon checklist\n\n",
             "> **Score** = operational production requirements identified in review (0–10).\n",
             "> **Tier 1** (engineering-adjacent): observability, graceful_degrade,\n",
             ">   client_error_guide, env_driven_config, memory_audit.\n",
             "> **Tier 2** (SRE Wall): alerting_policy, load_test_spec, health_check,\n",
             ">   incident_runbook, race_condition_tests.\n",
             "> Calibration target: C mean <= 2/10 total, <= 1/10 Tier 2.\n\n"]

    variants = sorted(set(r["variant"] for r in all_results))

    for variant_id in variants:
        variant_results = [r for r in all_results if r["variant"] == variant_id]
        scores = [r["total"] for r in variant_results]
        t1_scores = [r["tier1"] for r in variant_results]
        t2_scores = [r["tier2"] for r in variant_results]
        mean_score = sum(scores) / len(scores) if scores else 0
        mean_t1 = sum(t1_scores) / len(t1_scores) if t1_scores else 0
        mean_t2 = sum(t2_scores) / len(t2_scores) if t2_scores else 0
        mean_tokens = (sum(r["token_estimate"] for r in variant_results)
                       / len(variant_results) if variant_results else 0)

        lines.append(f"## Variant {variant_id}\n\n")
        lines.append(
            f"**Total:** {mean_score:.1f}/10 | "
            f"**Tier 1:** {mean_t1:.1f}/5 | "
            f"**Tier 2:** {mean_t2:.1f}/5 | "
            f"**Range:** {min(scores)}–{max(scores)} | "
            f"**Mean tokens:** {mean_tokens:.0f}\n\n"
        )

        header = "| Run | Total | T1 | T2 | " + " | ".join(item_labels) + " |\n"
        sep = "|-----|-------|----|----|" + "|".join(["---"] * len(item_labels)) + "|\n"
        lines.append(header)
        lines.append(sep)

        for r in variant_results:
            row_cells = [
                f"{'✓' if r['scores'][label] else '✗'}"
                for label in item_labels
            ]
            lines.append(
                f"| {r['run_id']} | {r['total']}/10 | {r['tier1']}/5 | {r['tier2']}/5 | " +
                " | ".join(row_cells) + " |\n"
            )
        lines.append("\n")

        # Tier 1 detection rates
        lines.append("**Tier 1 detection rates:**\n\n")
        lines.append("| Item | Detected | Rate |\n")
        lines.append("|------|----------|------|\n")
        for label in tier1_labels:
            count = sum(1 for r in variant_results if r["scores"][label])
            lines.append(f"| {label} | {count}/{len(variant_results)} | "
                         f"{count/len(variant_results)*100:.0f}% |\n")
        lines.append("\n")

        # Tier 2 detection rates
        lines.append("**Tier 2 detection rates:**\n\n")
        lines.append("| Item | Detected | Rate |\n")
        lines.append("|------|----------|------|\n")
        for label in tier2_labels:
            count = sum(1 for r in variant_results if r["scores"][label])
            lines.append(f"| {label} | {count}/{len(variant_results)} | "
                         f"{count/len(variant_results)*100:.0f}% |\n")
        lines.append("\n")

    # Summary table
    lines.append("## Summary\n\n")
    lines.append("| Variant | Total | Tier 1 | Tier 2 | Range |\n")
    lines.append("|---------|-------|--------|--------|-------|\n")
    for variant_id in variants:
        variant_results = [r for r in all_results if r["variant"] == variant_id]
        scores = [r["total"] for r in variant_results]
        t1 = [r["tier1"] for r in variant_results]
        t2 = [r["tier2"] for r in variant_results]
        lines.append(
            f"| {variant_id} | {sum(scores)/len(scores):.1f}/10 | "
            f"{sum(t1)/len(t1):.1f}/5 | "
            f"{sum(t2)/len(t2):.1f}/5 | "
            f"{min(scores)}–{max(scores)} |\n"
        )

    out_path = REVIEW_DIR / "scores.md"
    out_path.write_text("".join(lines))
    print(f"\nScores written to {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Exp-28c scorer")
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
            scores = [r["total"] for r in results]
            t2 = [r["tier2"] for r in results]
            mean = sum(scores) / len(scores)
            mean_t2 = sum(t2) / len(t2)
            print(f"  total={mean:.1f}/10  tier2={mean_t2:.1f}/5  range={min(scores)}–{max(scores)}")

    if all_results:
        write_scores(all_results)


if __name__ == "__main__":
    main()
