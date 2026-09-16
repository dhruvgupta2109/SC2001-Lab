"""
Project 1: Experiment Runner
------------------------------
Runs the hybrid sort (and, where needed, original merge sort) across
many (n, S) combinations and saves the results to results.csv, in the
format generate_plots.py expects: part, n, S, comparisons, time_seconds.

Why it's built this way (to reduce noise in the timing results):
- For a given n, we generate ONE random array and reuse a copy of it
  for every S we test. This means S is the only thing changing between
  runs -- we're not accidentally comparing different random data.
- Each (n, S) timing is repeated several times. We report both the
  MEAN and the MINIMUM time. The minimum is useful because system
  noise (OS scheduling, background processes) can only ever slow a
  run down, never speed it up -- so the minimum across repeats is a
  good estimate of the "true" cost with noise stripped out.
- Garbage collection is switched off during each timed run, so a GC
  pause doesn't get incorrectly counted as part of the algorithm's time.
"""

import csv
import gc
import time
from sorting_algo import hybrid_sort, original_merge_sort, generate_random_array


# ---------------------------------------------------------
# Timing helpers
# ---------------------------------------------------------
def time_one_hybrid_run(arr, S):
    """
    Runs hybrid_sort ONCE on a copy of arr (so the original is never
    modified). Returns (comparisons, time_seconds).
    """
    data = arr.copy()
    counter = [0]
    n = len(data)

    gc.disable()
    start = time.process_time()
    hybrid_sort(data, 0, n - 1, S, counter)
    elapsed = time.process_time() - start
    gc.enable()

    assert data == sorted(arr), "hybrid_sort produced incorrect output!"
    return counter[0], elapsed


def time_one_original_run(arr):
    """
    Runs original_merge_sort ONCE on a copy of arr.
    Returns (comparisons, time_seconds).
    """
    data = arr.copy()
    counter = [0]
    n = len(data)

    gc.disable()
    start = time.process_time()
    original_merge_sort(data, 0, n - 1, counter)
    elapsed = time.process_time() - start
    gc.enable()

    assert data == sorted(arr), "original_merge_sort produced incorrect output!"
    return counter[0], elapsed


def repeated_hybrid(arr, S, repeats):
    """
    Runs hybrid_sort `repeats` times on copies of the SAME array.
    Comparisons are identical every repeat (the algorithm is
    deterministic), so we just keep the value from the last run.
    Returns (comparisons, mean_time, min_time).
    """
    times = []
    comparisons = None
    for _ in range(repeats):
        comparisons, t = time_one_hybrid_run(arr, S)
        times.append(t)
    return comparisons, sum(times) / len(times), min(times)


S_FIXED = 10          # threshold used for part (c)(i)
N_FIXED = 1_000_000   # size used for part (c)(ii)

N_VALUES_C1 = [1000, 5000, 10000, 50000, 100000, 500000, 1000000, 5000000, 10000000]
S_VALUES_C2 = [2, 5, 8, 10, 13, 16, 20, 24, 32, 55, 64, 100, 150, 200, 300, 500]

# For part (c)(iii): (n, list of S values to test, repeats per S)
# Smaller n -> more S values + more repeats, since each run is cheap.
# Larger n -> fewer S values + fewer repeats, since each run is expensive.
C3_CONFIG = [
    (10000,    [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 24, 32, 48, 64], 5),
    (50000,    [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 24, 32, 48, 64], 5),
    (100000,   [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 24, 32, 48, 64], 5),
    (500000,   [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 24, 32, 48, 64], 3),
    (1000000,  [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 24, 32, 48, 64], 3),
    (5000000,  [2, 5, 8, 10, 13, 16, 20, 24, 32, 55, 64], 2),
    (10000000, [2, 5, 8, 10, 13, 16, 20, 24, 32, 55, 64], 2),
]

OUTPUT_FILE = "results.csv"


# ---------------------------------------------------------
# Main experiment
# ---------------------------------------------------------
def main():
    rows = []

    # ----- (c)(i): comparisons vs n, S fixed -----
    print("Part (c)(i): comparisons vs n ...")
    for n in N_VALUES_C1:
        arr = generate_random_array(n)
        comparisons, mean_t, min_t = repeated_hybrid(arr, S_FIXED, repeats=1)
        rows.append({"part": "c1", "n": n, "S": S_FIXED,
                     "comparisons": comparisons,
                     "time_seconds": mean_t, "time_seconds_min": min_t, "repeats": 1})
        print(f"  n={n:>10,}  comparisons={comparisons:,}  time={mean_t:.3f}s")

    # ----- (c)(ii): comparisons vs S, n fixed -----
    print("Part (c)(ii): comparisons vs S ...")
    arr_fixed_n = generate_random_array(N_FIXED)   # SAME array for every S
    for S in S_VALUES_C2:
        comparisons, mean_t, min_t = repeated_hybrid(arr_fixed_n, S, repeats=1)
        rows.append({"part": "c2", "n": N_FIXED, "S": S,
                     "comparisons": comparisons,
                     "time_seconds": mean_t, "time_seconds_min": min_t, "repeats": 1})
        print(f"  S={S:>4}  comparisons={comparisons:,}  time={mean_t:.3f}s")

    # ----- (c)(iii): CPU time vs S, per size, with repeats -----
    print("Part (c)(iii): optimal S per size ...")
    for n, S_list, repeats in C3_CONFIG:
        arr = generate_random_array(n)   # SAME array for every S at this n
        for S in S_list:
            comparisons, mean_t, min_t = repeated_hybrid(arr, S, repeats=repeats)
            rows.append({"part": "c3", "n": n, "S": S,
                         "comparisons": comparisons,
                         "time_seconds": mean_t, "time_seconds_min": min_t, "repeats": repeats})
            print(f"  n={n:>10,}  S={S:>4}  mean={mean_t:.3f}s  min={min_t:.3f}s")

    # ----- Save -----
    fieldnames = ["part", "n", "S", "comparisons", "time_seconds", "time_seconds_min", "repeats"]
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nSaved {len(rows)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()