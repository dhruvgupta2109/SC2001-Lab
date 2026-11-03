"""Part (5): Empirical Runtime Analysis for Unbounded Knapsack Problem.

Benchmarks Top-Down (Memoized) vs. Bottom-Up DP:
1. Varying Capacity C (fixed n)
2. Varying Number of Item Types n (fixed C)
Saves comparison plots as PNG files for slides.
"""

import sys
from pathlib import Path
import time
import matplotlib.pyplot as plt


try:
    from part_1_recursive import max_profit_recursive
    from part_3_bottom_up import build_dp_table
except ModuleNotFoundError:
    from Lab3.part_1_recursive import max_profit_recursive
    from Lab3.part_3_bottom_up import build_dp_table


def benchmark_varying_c():
    """Experiment 1: Fix n = 3, vary Capacity C to test linearity in C."""
    weights = [4, 5, 8]
    profits = [7, 6, 9]

    # Test capacities (stays within safe recursion depth)
    c_values = [200, 400, 800, 1200, 1600, 2000, 2400]

    times_bottom_up = []
    times_top_down = []
    trials = 10

    for c in c_values:
        # Measure Bottom-Up (Tabulation)
        start_bu = time.perf_counter()
        for _ in range(trials):
            build_dp_table(c, weights, profits)
        times_bottom_up.append((time.perf_counter() - start_bu) / trials)

        # Measure Top-Down (Memoized)
        start_td = time.perf_counter()
        for _ in range(trials):
            max_profit_recursive(c, weights, profits)
        times_top_down.append((time.perf_counter() - start_td) / trials)

    # Plot Experiment 1
    plt.figure(figsize=(7, 5))
    plt.plot(c_values, times_bottom_up, marker='o', label='Bottom-Up (Tabulation)', color='#1f77b4', linewidth=2)
    plt.plot(c_values, times_top_down, marker='s', label='Top-Down (Memoized)', color='#ff7f0e', linewidth=2)
    plt.title('Empirical Scaling: Runtime vs. Capacity $C$\n(Fixed $n = 3$)', fontsize=12, fontweight='bold')
    plt.xlabel('Capacity $C$', fontsize=11)
    plt.ylabel('Wall-Clock Time (seconds)', fontsize=11)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.savefig('empirical_varying_capacity.png', dpi=300)
    plt.close()
    print("Saved: empirical_varying_capacity.png")


def benchmark_varying_n():
    """Experiment 2: Fix C = 1500, vary Item Types n to test linearity in n."""
    fixed_c = 1500
    n_values = [5, 10, 15, 20, 30, 40, 50]

    times_bottom_up = []
    times_top_down = []
    trials = 10

    for n in n_values:
        # Generate deterministic weights and profits for consistency
        weights = [(i * 3) % 13 + 3 for i in range(n)]
        profits = [w + ((i * 5) % 7 + 1) for i, w in enumerate(weights)]

        # Measure Bottom-Up (Tabulation)
        start_bu = time.perf_counter()
        for _ in range(trials):
            build_dp_table(fixed_c, weights, profits)
        times_bottom_up.append((time.perf_counter() - start_bu) / trials)

        # Measure Top-Down (Memoized)
        start_td = time.perf_counter()
        for _ in range(trials):
            max_profit_recursive(fixed_c, weights, profits)
        times_top_down.append((time.perf_counter() - start_td) / trials)

    # Plot Experiment 2
    plt.figure(figsize=(7, 5))
    plt.plot(n_values, times_bottom_up, marker='o', label='Bottom-Up (Tabulation)', color='#1f77b4', linewidth=2)
    plt.plot(n_values, times_top_down, marker='s', label='Top-Down (Memoized)', color='#ff7f0e', linewidth=2)
    plt.title('Empirical Scaling: Runtime vs. Item Types $n$\n(Fixed $C = 1500$)', fontsize=12, fontweight='bold')
    plt.xlabel('Number of Item Types $n$', fontsize=11)
    plt.ylabel('Wall-Clock Time (seconds)', fontsize=11)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.savefig('empirical_varying_n.png', dpi=300)
    plt.close()
    print("Saved: empirical_varying_n.png")


if __name__ == "__main__":
    # Raise recursion depth to handle up to C = 2400 safely
    sys.setrecursionlimit(6000)

    print("Running Experiment 1: Varying Capacity C...")
    benchmark_varying_c()

    print("Running Experiment 2: Varying Number of Item Types n...")
    benchmark_varying_n()

    print("Benchmarking finished! Check your folder for the two PNG plots.")