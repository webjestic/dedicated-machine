"""
Exp-27 Scorer — Horizon Blindness / Gap Detection.

Prompt: "Build me a blockchain implementation in Node.js."
Underspecified. No mention of mempool, ECDSA signing, difficulty adjustment,
P2P networking, persistence, or API layer.

Scoring is continuous, not binary. Score = number of unsolicited production
requirements surfaced per run. Items are scored 1 if explicitly named or
implemented; 0 if absent or only mentioned in a checklist without substance.

Production requirements checklist (the prompt did NOT ask for these):

  Layer 1 — Integration (ties the four components together):
    1. mempool / transaction pool  — pending transactions before mining
    2. ECDSA / secp256k1 signing   — cryptographic wallet signing
    3. difficulty adjustment        — dynamic mining difficulty
    4. coinbase / mining reward     — block reward transaction

  Layer 2 — System completeness:
    5. P2P networking / peer discovery — nodes communicate, chain syncs
    6. persistence / storage           — chain survives process restart
    7. REST/RPC API                    — external interface for submissions

  Layer 3 — Correctness guards:
    8. double-spend prevention          — balance check before mempool add
    9. Merkle root / transaction hash   — block header integrity
   10. chain sync / fork resolution     — longest chain rule on conflict

Max score: 10.
Calibration target: A (P_d baseline) ≤ 3/10.

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
        "mempool",
        [
            r"\bmempool\b", r"transaction.pool", r"pending.transact",
            r"unconfirmed.transact", r"transact.*queue", r"pool.*transact",
        ],
    ),
    (
        "ecdsa_signing",
        [
            r"\becdsa\b", r"secp256k1", r"elliptic.curve", r"key.pair",
            r"private.key.*sign", r"sign.*private.key",
            r"cryptographic.*sign", r"digital.*sign",
            r"require\(.*elliptic", r"require\(.*crypto.*\)",
        ],
    ),
    (
        "difficulty_adjustment",
        [
            r"difficulty.adjust", r"adjust.*difficulty",
            r"target.*difficulty", r"difficulty.*target",
            r"every.*\d+.*block.*difficulty", r"retarget",
            r"block.time.*adjust", r"mining.difficulty.*change",
        ],
    ),
    (
        "coinbase_reward",
        [
            r"\bcoinbase\b", r"mining.reward", r"block.reward",
            r"miner.reward", r"reward.*transact", r"transact.*reward",
        ],
    ),
    (
        "p2p_networking",
        [
            r"\bp2p\b", r"peer.to.peer", r"peer.*discover",
            r"websocket.*peer", r"peer.*websocket",
            r"broadcast.*block", r"block.*broadcast",
            r"node.*network", r"network.*node.*connect",
            r"chain.*sync", r"sync.*chain",
        ],
    ),
    (
        "persistence",
        [
            r"\bleveldb\b", r"\bsqlite\b", r"\brocksdb\b",
            r"persist.*chain", r"chain.*persist",
            r"fs\.write", r"writeFile.*chain", r"save.*chain",
            r"storage.*chain", r"chain.*storage", r"disk.*chain",
            r"surviv.*restart", r"restart.*surviv",
        ],
    ),
    (
        "api_layer",
        [
            r"express.*route", r"REST.*api", r"api.*endpoint",
            r"/api/transact", r"/api/block", r"/api/mine",
            r"app\.post.*transact", r"app\.get.*block",
            r"http.*server.*chain", r"rpc.*endpoint",
        ],
    ),
    (
        "double_spend",
        [
            r"double.spend", r"balance.*check", r"check.*balance",
            r"sufficient.*fund", r"fund.*sufficient",
            r"utxo", r"unspent.*output",
            r"validate.*balance", r"balance.*validat",
        ],
    ),
    (
        "merkle_root",
        [
            r"\bmerkle\b", r"merkle.root", r"merkle.tree",
            r"transaction.*hash.*block", r"block.*header.*hash.*transact",
        ],
    ),
    (
        "chain_sync_fork",
        [
            r"longest.chain", r"chain.*conflict", r"fork.*resolut",
            r"consensus.*rule", r"chain.*replac",
            r"replace.*chain.*longer", r"longer.*chain.*replac",
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

    lines = ["# exp-27 Scored Results\n",
             "**Scoring pass:** keyword pre-screen — continuous metric\n\n",
             "> **Score** = number of unsolicited production requirements surfaced (0–10).\n",
             "> Items: mempool, ecdsa_signing, difficulty_adjustment, coinbase_reward,\n",
             "> p2p_networking, persistence, api_layer, double_spend, merkle_root,\n",
             "> chain_sync_fork.\n",
             "> Calibration target: A (P_d baseline) mean ≤ 3/10.\n\n"]

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

        # Per-item detection rate
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
    parser = argparse.ArgumentParser(description="Exp-27 scorer")
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
            mean = sum(scores) / len(scores)
            print(f"  mean={mean:.1f}/10 range={min(scores)}–{max(scores)}")

    if all_results:
        write_scores(all_results)


if __name__ == "__main__":
    main()
