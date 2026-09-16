import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

LAB_DIR = Path(__file__).resolve().parent
PLOTS_DIR = LAB_DIR / "plots"
PLOTS_DIR.mkdir(exist_ok=True)

df = pd.read_csv(LAB_DIR / "results.csv")

# ---- (c)(i): comparisons vs n, S fixed ----
c1 = df[df["part"] == "c1"].sort_values("n")
S_fixed = c1["S"].iloc[0]

fig1, ax1 = plt.subplots(figsize=(7, 5))
ax1.plot(c1["n"], c1["comparisons"], marker="o", color="#1E2761", label="Empirical (hybrid)")

# Theoretical curve: comparisons ~= n*log2(n/S) + n*S/4, scaled to match first point
n_vals = c1["n"].values
theory = n_vals * np.log2(n_vals / S_fixed) + n_vals * S_fixed / 4
scale = c1["comparisons"].iloc[0] / theory[0]
ax1.plot(n_vals, theory * scale, linestyle="--", color="#3D5AFE", label="Theoretical shape (scaled)")

ax1.set_xscale("log")
ax1.set_yscale("log")
ax1.set_xlabel("Input size n")
ax1.set_ylabel("Key comparisons")
ax1.set_title(f"(c)(i) Comparisons vs. n  (S = {S_fixed} fixed)")
ax1.legend()
ax1.grid(True, which="both", alpha=0.3)
fig1.tight_layout()
fig1.savefig(PLOTS_DIR / "comparisons_vs_n.png", dpi=150)
print(f"Saved {PLOTS_DIR / 'comparisons_vs_n.png'}")

# ---- (c)(ii): comparisons vs S, n fixed ----
c2 = df[df["part"] == "c2"].sort_values("S")
n_fixed = c2["n"].iloc[0]

fig2, ax2 = plt.subplots(figsize=(7, 5))
ax2.plot(c2["S"], c2["comparisons"], marker="o", color="#1E2761", label="Empirical (hybrid)")

S_vals = c2["S"].values
theory2 = n_fixed * np.log2(n_fixed / S_vals) + n_fixed * S_vals / 4
scale2 = c2["comparisons"].iloc[0] / theory2[0]
ax2.plot(S_vals, theory2 * scale2, linestyle="--", color="#3D5AFE", label="Theoretical shape (scaled)")

ax2.set_xlabel("Threshold S")
ax2.set_ylabel("Key comparisons")
ax2.set_title(f"(c)(ii) Comparisons vs. S  (n = {n_fixed:,} fixed)")
ax2.legend()
ax2.grid(True, alpha=0.3)
fig2.tight_layout()
fig2.savefig(PLOTS_DIR / "comparisons_vs_S.png", dpi=150)
print(f"Saved {PLOTS_DIR / 'comparisons_vs_S.png'}")

# ---- (c)(iii): CPU time vs S, one line per size ----
# Plot the best observed time consistently with the metric used to choose S
# for the Part (d) comparison. The mean remains available in results.csv.
c3 = df[df["part"] == "c3"].copy()
fig3, (ax3a, ax3b, ax3c) = plt.subplots(1, 3, figsize=(16, 5))

# subgraph 1: small-to-mid sizes together
small_sizes = [10000, 50000, 100000, 500000, 1000000]
for n_val in small_sizes:
    subset = c3[c3["n"] == n_val].sort_values("S")
    if not subset.empty:
        ax3a.plot(subset["S"], subset["time_seconds_min"], marker="o", label=f"n = {n_val:,}")

ax3a.set_xlabel("Threshold S")
ax3a.set_ylabel("CPU Time (seconds, best of repeats)")
ax3a.set_title("Sizes n = 10k to 1M")
ax3a.legend()
ax3a.grid(True, alpha=0.3)

# subgraph 2: n = 5M
subset_5m = c3[c3["n"] == 5000000].sort_values("S")
if not subset_5m.empty:
    ax3b.plot(subset_5m["S"], subset_5m["time_seconds_min"], marker="o", color="#8c564b", label="n = 5M")
ax3b.set_xlabel("Threshold S")
ax3b.set_ylabel("CPU Time (seconds, best of repeats)")
ax3b.set_title("Size n = 5,000,000")
ax3b.legend()
ax3b.grid(True, alpha=0.3)

# subgraph 3: n = 10M
subset_10m = c3[c3["n"] == 10_000_000].sort_values("S")
if not subset_10m.empty:
    ax3c.plot(subset_10m["S"], subset_10m["time_seconds_min"], marker="o", color="#e377c2", label="n = 10M")
ax3c.set_xlabel("Threshold S")
ax3c.set_ylabel("CPU Time (seconds, best of repeats)")
ax3c.set_title("Size n = 10,000,000")
ax3c.legend()
ax3c.grid(True, alpha=0.3)

fig3.suptitle("Part (c)(iii): Optimal S Across Different Scale Regimes", fontsize=14, fontweight="bold")
fig3.tight_layout()
fig3.savefig(PLOTS_DIR / "optimal_s_split.png", dpi=150)
print(f"Saved {PLOTS_DIR / 'optimal_s_split.png'}")
