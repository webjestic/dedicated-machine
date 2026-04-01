"""
Exp-28b Scorer — Operational Horizon (Rate Limiter).

Prompt: "Build me a rate limiter in Node.js."
The RLHF baseline already produces code-complete implementations (Redis,
sliding window, per-key, burst handling). The operational layer — observability,
alerting, graceful degradation, runbook, load testing — is where the genuine gap lives.

Scoring is continuous, not binary. Score = number of operational production
requirements surfaced per run. Items are scored 1 if explicitly named,
implemented, or flagged as a production requirement with substance; 0 if
absent or mentioned in passing without actionable content.

Operational requirements checklist (all require thinking BEYOND "does the code work"):

  1. observability      — metrics instrumentation; how do you know it's working?
  2. alerting_policy    — specific conditions for on-call paging (error rate,
                          rejection rate thresholds)
  3. graceful_degrade   — explicit fail-open/fail-closed policy and logic when
                          Redis/backend is unavailable
  4. client_error_guide — RFC 6585 headers + 429 response body format for
                          SDK/client handling
  5. load_test_spec     — instructions or spec for verifying limiter handles
                          target throughput
  6. env_driven_config  — per-route limits tunable via environment variables
                          without code deploys
  7. health_check       — endpoint exposing limiter status, counters, Redis health
  8. incident_runbook   — procedures for debugging false positives or unexpectedly
                          blocked users
  9. memory_audit       — how to detect/prevent memory leaks from unbounded keys
 10. race_condition_tests — specific test strategy for distributed lock contention
                            and window boundary races

Max score: 10.
Calibration target: C (P_d baseline) mean <= 2/10.

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

# Each item: (label, [keyword patterns])
REQUIREMENTS = [
    (
        "observability",
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
        "alerting_policy",
        [
            r"alert.*threshold", r"threshold.*alert",
            r"page.*oncall", r"oncall.*page", r"on.call.*alert",
            r"alert.*rejection.rate", r"rejection.rate.*alert",
            r"alert.*error.rate", r"error.rate.*alert",
            r"pagerduty", r"opsgenie", r"victorops",
            r"alert.*condition", r"condition.*alert",
            r"notify.*ops", r"ops.*notify",
        ],
    ),
    (
        "graceful_degrade",
        [
            r"fail.open", r"fail.closed",
            r"fallback.*redis", r"redis.*fallback",
            r"redis.*unavailable", r"unavailable.*redis",
            r"backend.*down.*policy", r"degrad.*policy",
            r"circuit.break",
            r"when.*redis.*fail", r"redis.*fail.*allow",
        ],
    ),
    (
        "client_error_guide",
        [
            r"x-ratelimit", r"x.ratelimit",
            r"retry.after.*header", r"header.*retry.after",
            r"429.*body", r"body.*429",
            r"error.*response.*format", r"response.*format.*rate",
            r"client.*sdk.*handle", r"sdk.*rate.limit",
            r"rfc.6585",
            r"rate.limit.*documentation", r"document.*rate.limit",
        ],
    ),
    (
        "load_test_spec",
        [
            r"load.test", r"load.*test.*rate",
            r"throughput.*verif", r"verif.*throughput",
            r"stress.test.*limit", r"limit.*stress.test",
            r"k6\b", r"\bjmeter\b", r"\bgatling\b", r"\bwrk\b",
            r"req.*per.*sec.*test", r"test.*req.*per.*sec",
            r"benchmark.*limit", r"limit.*benchmark",
            r"target.*rps", r"rps.*target",
        ],
    ),
    (
        "env_driven_config",
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
        "health_check",
        [
            r"health.*endpoint.*limit", r"limit.*health.*endpoint",
            r"/health.*rate", r"rate.*\/health",
            r"health.*check.*redis", r"redis.*health.*check",
            r"status.*endpoint.*counter", r"counter.*status.*endpoint",
            r"limiter.*status.*api", r"api.*limiter.*status",
            r"\/status.*rate.limit", r"rate.limit.*\/status",
        ],
    ),
    (
        "incident_runbook",
        [
            r"runbook",
            r"false.positive.*debug", r"debug.*false.positive",
            r"incident.*rate.limit", r"rate.limit.*incident",
            r"troubleshoot.*block", r"block.*troubleshoot",
            r"diagnos.*false.*block", r"false.*block.*diagnos",
            r"ops.*playbook", r"playbook.*rate",
            r"how.*to.*debug.*limit", r"debug.*unexpect.*block",
        ],
    ),
    (
        "memory_audit",
        [
            r"memory.*leak.*redis", r"redis.*memory.*leak",
            r"unbounded.*key", r"key.*unbounded",
            r"key.*growth.*audit", r"audit.*key.*growth",
            r"redis.*memory.*monitor", r"monitor.*redis.*memory",
            r"key.*eviction.*policy", r"eviction.*policy.*key",
            r"memory.*inspect.*rate", r"rate.*key.*inspect",
            r"maxmemory.*policy",
        ],
    ),
    (
        "race_condition_tests",
        [
            r"race.*condition.*test", r"test.*race.*condition",
            r"distributed.*lock.*test", r"test.*distributed.*lock",
            r"window.*boundary.*test", r"test.*window.*boundary",
            r"concurrent.*request.*test", r"test.*concurrent.*request",
            r"atomic.*test.*redis", r"test.*atomic.*redis",
            r"lua.*script.*test", r"test.*lua.*script",
            r"split.*brain.*test",
        ],
    ),
]


def score_output(text: str) -> dict:
    scores = {}
    matched_patterns = {}
    total = 0

    for label, patterns in REQUIREMENTS:
        hit = False
        for p in patterns:
            if re.search(p, text, re.IGNORECASE):
                hit = True
                matched_patterns[label] = p
                break
        scores[label] = 1 if hit else 0
        total += scores[label]

    token_estimate = len(text.split())

    return {
        "total": total,
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

    item_labels = [label for label, _ in REQUIREMENTS]

    lines = ["# exp-28b Scored Results\n",
             "**Scoring pass:** keyword pre-screen — operational horizon checklist\n\n",
             "> **Score** = number of operational production requirements surfaced (0–10).\n",
             "> Items: observability, alerting_policy, graceful_degrade, client_error_guide,\n",
             "> load_test_spec, env_driven_config, health_check, incident_runbook,\n",
             "> memory_audit, race_condition_tests.\n",
             "> Calibration target: C (P_d baseline) mean <= 2/10.\n\n"]

    variants = sorted(set(r["variant"] for r in all_results))

    for variant_id in variants:
        variant_results = [r for r in all_results if r["variant"] == variant_id]
        scores = [r["total"] for r in variant_results]
        mean_score = sum(scores) / len(scores) if scores else 0
        mean_tokens = (sum(r["token_estimate"] for r in variant_results)
                       / len(variant_results) if variant_results else 0)

        lines.append(f"## Variant {variant_id}\n\n")
        lines.append(f"**Mean score:** {mean_score:.1f}/10 | "
                     f"**Range:** {min(scores)}–{max(scores)} | "
                     f"**Mean tokens:** {mean_tokens:.0f}\n\n")

        header = "| Run | Score | " + " | ".join(item_labels) + " |\n"
        sep = "|-----|-------|" + "|".join(["---"] * len(item_labels)) + "|\n"
        lines.append(header)
        lines.append(sep)

        for r in variant_results:
            row_cells = [
                f"{'✓' if r['scores'][label] else '✗'}"
                for label in item_labels
            ]
            lines.append(
                f"| {r['run_id']} | {r['total']}/10 | " +
                " | ".join(row_cells) + " |\n"
            )
        lines.append("\n")

        lines.append("**Item detection rates:**\n\n")
        lines.append("| Item | Detected | Rate |\n")
        lines.append("|------|----------|------|\n")
        for label in item_labels:
            count = sum(1 for r in variant_results if r["scores"][label])
            lines.append(f"| {label} | {count}/{len(variant_results)} | "
                         f"{count/len(variant_results)*100:.0f}% |\n")
        lines.append("\n")

    lines.append("## Summary\n\n")
    lines.append("| Variant | Mean score | Range | Mean tokens |\n")
    lines.append("|---------|------------|-------|-------------|\n")
    for variant_id in variants:
        variant_results = [r for r in all_results if r["variant"] == variant_id]
        scores = [r["total"] for r in variant_results]
        mean_score = sum(scores) / len(scores) if scores else 0
        mean_tokens = (sum(r["token_estimate"] for r in variant_results)
                       / len(variant_results) if variant_results else 0)
        lines.append(f"| {variant_id} | {mean_score:.1f}/10 | "
                     f"{min(scores)}–{max(scores)} | {mean_tokens:.0f} |\n")

    out_path = REVIEW_DIR / "scores.md"
    out_path.write_text("".join(lines))
    print(f"\nScores written to {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Exp-28b scorer")
    parser.add_argument("--variant", choices=["A", "B", "C", "D"],
                        help="Score a single variant only")
    args = parser.parse_args()

    variants = [args.variant] if args.variant else ["A", "B", "C", "D"]
    all_results = []

    for variant_id in variants:
        print(f"Scoring variant {variant_id}...")
        results = score_variant(variant_id)
        all_results.extend(results)
        if results:
            scores = [r["total"] for r in results]
            mean = sum(scores) / len(scores)
            print(f"  mean={mean:.1f}/10 range={min(scores)}–{max(scores)}")

    if all_results:
        write_scores(all_results)


if __name__ == "__main__":
    main()
