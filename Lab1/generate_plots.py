import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("results.csv")

# ---- (c)(i): comparisons vs n, S fixed ----
c1 = df[df["part"] == "c1"].sort_values("n")
S_fixed = c1["S"].iloc[0]

fig, ax = plt.subplots(figsize=(7, 5))
ax.plot(c1["n"], c1["comparisons"], marker="o", color="#1E2761", label="Empirical (hybrid)")

# Theoretical curve: comparisons ~= n*log2(n/S) + n*S/4, scaled to match first point
n_vals = c1["n"].values
theory = n_vals * np.log2(n_vals / S_fixed) + n_vals * S_fixed / 4
scale = c1["comparisons"].iloc[0] / theory[0]
ax.plot(n_vals, theory * scale, linestyle="--", color="#3D5AFE", label="Theoretical shape (scaled)")

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("Input size n")
ax.set_ylabel("Key comparisons")
ax.set_title(f"(c)(i) Comparisons vs. n  (S = {S_fixed} fixed)")
ax.legend()
ax.grid(True, which="both", alpha=0.3)
fig.tight_layout()
fig.savefig("plots/comparisons_vs_n.png", dpi=150)
print("Saved plots/comparisons_vs_n.png")

# ---- (c)(ii): comparisons vs S, n fixed ----
c2 = df[df["part"] == "c2"].sort_values("S")
n_fixed = c2["n"].iloc[0]

fig, ax = plt.subplots(figsize=(7, 5))
ax.plot(c2["S"], c2["comparisons"], marker="o", color="#1E2761", label="Empirical (hybrid)")

S_vals = c2["S"].values
theory2 = n_fixed * np.log2(n_fixed / S_vals) + n_fixed * S_vals / 4
scale2 = c2["comparisons"].iloc[0] / theory2[0]
ax.plot(S_vals, theory2 * scale2, linestyle="--", color="#3D5AFE", label="Theoretical shape (scaled)")

ax.set_xlabel("Threshold S")
ax.set_ylabel("Key comparisons")
ax.set_title(f"(c)(ii) Comparisons vs. S  (n = {n_fixed:,} fixed)")
ax.legend()
ax.grid(True, alpha=0.3)


#----------(c)(iii): time vs s, n as line------
c3 = df[df["part"] == "c3"].copy()
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 5))

#subgraph 1
small_sizes = [10000, 50000, 100000, 500000, 1000000]
for n_val in small_sizes:
    subset = c3[c3["n"] == n_val].sort_values("S")
    if not subset.empty:
        ax1.plot(subset["S"], subset["time_seconds"], marker="o", label=f"n = {n_val:,}")

ax1.set_xlabel("Threshold S")
ax1.set_ylabel("CPU Time (seconds)")
ax1.set_title("Sizes n = 10k to 1M")
ax1.legend()
ax1.grid(True, alpha=0.3)

#subgraph 2: n = 5 mil
subset_5m = c3[c3["n"] == 5000000].sort_values("S")
if not subset_5m.empty:
    ax2.plot(subset_5m["S"], subset_5m["time_seconds"], marker="o", color="#8c564b", label="n = 5M")
ax2.set_xlabel("Threshold S")
ax2.set_ylabel("CPU Time (seconds)")
ax2.set_title("Size n = 5,000,000")
ax2.legend()
ax2.grid(True, alpha=0.3)

#subgraph 2: n = 10 mil
subset_10m = c3[c3["n"] == 10_000_000].sort_values("S")
if not subset_10m.empty:
    ax3.plot(subset_10m["S"], subset_10m["time_seconds"], marker="o", color="#e377c2", label="n = 10M")
ax3.set_xlabel("Threshold S")
ax3.set_ylabel("CPU Time (seconds)")
ax3.set_title("Size n = 10,000,000")
ax3.legend()
ax3.grid(True, alpha=0.3)

fig.suptitle("Part (c)(iii): Optimal S Across Different Scale Regimes", fontsize=14, fontweight="bold")
fig.tight_layout()
fig.savefig("plots/optimal_s_split.png", dpi=150)
print("Saved plots/optimal_s_split.png")
plt.show()
fig.tight_layout()
fig.savefig("plots/comparisons_vs_S.png", dpi=150)
print("Saved plots/comparisons_vs_S.png")
