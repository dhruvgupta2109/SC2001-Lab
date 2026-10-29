"""Part (4): run the bottom-up algorithm for P(16) and P(12)."""

from pathlib import Path

from part_3_bottom_up import build_dp_table, reconstruct_counts


RESULTS_DIR = Path(__file__).resolve().parent / "results"
EXAMPLES = [
    (16, [4, 5, 8], [7, 6, 9]),
    (12, [5, 6, 7], [7, 6, 9]),
]


def format_example(capacity, weights, profits):
    """Show the full table and an optimal packing for one required example."""
    dp, choice = build_dp_table(capacity, weights, profits)
    counts = reconstruct_counts(capacity, weights, choice)
    total_weight = sum(counts[i] * weights[i] for i in range(len(weights)))
    total_profit = sum(counts[i] * profits[i] for i in range(len(profits)))

    lines = [
        "Capacity: " + str(capacity),
        "Weights: " + str(weights),
        "Profits: " + str(profits),
        "",
        " c | P(c) | chosen type",
        "---+------+------------",
    ]

    for c in range(capacity + 1):
        chosen_type = "-" if choice[c] is None else str(choice[c])
        lines.append(f"{c:2d} | {dp[c]:4d} | {chosen_type}")

    # Following choice[c] moves from c to c - weights[choice[c]].
    path = ["P(" + str(capacity) + ")"]
    remaining = capacity
    while choice[remaining] is not None:
        remaining -= weights[choice[remaining]]
        path.append("P(" + str(remaining) + ")")

    lines.extend([
        "",
        "Answer: P(" + str(capacity) + ") = " + str(dp[capacity]),
        "Object counts (types 0, 1, 2): " + str(counts),
        "Total weight: " + str(total_weight),
        "Unused capacity: " + str(capacity - total_weight),
        "Total profit: " + str(total_profit),
        "Reconstruction: " + " -> ".join(path),
    ])

    return "\n".join(lines)


def main():
    sections = [
        "Part (4): bottom-up DP results",
        "Object types are numbered 0, 1, 2. Supply is unlimited.",
    ]
    for capacity, weights, profits in EXAMPLES:
        sections.append(format_example(capacity, weights, profits))

    report = "\n\n".join(sections) + "\n"
    RESULTS_DIR.mkdir(exist_ok=True)
    output_path = RESULTS_DIR / "part_4_run_log.txt"
    output_path.write_text(report, encoding="utf-8")

    print(report, end="")
    print("\nSaved", output_path)


if __name__ == "__main__":
    main()
