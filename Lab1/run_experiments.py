"""
Writes results.csv with columns: part, n, S, comparisons, time_seconds

Run with:
    python3 run_experiments.py
"""

import csv
import random
import sys
import time

from sorting_algo import hybrid_sort, generate_random_array

RANDOM_SEED = 42
OUTPUT_CSV = "results.csv"

# (c)(i): fixed S, sweep n across the full assignment range
FIXED_S_FOR_C1 = 10
SIZES_FOR_C1 = [1000, 5000, 10000, 50000, 100000, 500000, 1000000,
                5000000, 10000000]

# (c)(ii): fixed n, sweep S
FIXED_N_FOR_C2 = 1000000
S_VALUES_FOR_C2 = [2, 5, 10, 20, 50, 75, 100, 150, 200, 300, 500]


def time_hybrid(data, S):
    arr = data.copy()
    counter = [0]
    start = time.process_time()
    hybrid_sort(arr, 0, len(arr) - 1, S, counter)
    elapsed = time.process_time() - start
    assert arr == sorted(data), f"Hybrid sort incorrect for n={len(data)}, S={S}"
    return counter[0], elapsed


def run_c1(writer):
    print(f"\n[c1] Fixed S = {FIXED_S_FOR_C1}, varying n over {SIZES_FOR_C1}")
    for n in SIZES_FOR_C1:
        data = generate_random_array(n)
        comps, elapsed = time_hybrid(data, FIXED_S_FOR_C1)
        print(f"  n={n:>10,}  comparisons={comps:,}  time={elapsed:.4f}s")
        writer.writerow({"part": "c1", "n": n, "S": FIXED_S_FOR_C1,
                          "comparisons": comps, "time_seconds": elapsed})


def run_c2(writer):
    print(f"\n[c2] Fixed n = {FIXED_N_FOR_C2:,}, varying S over {S_VALUES_FOR_C2}")
    data = generate_random_array(FIXED_N_FOR_C2)
    for S in S_VALUES_FOR_C2:
        comps, elapsed = time_hybrid(data, S)
        print(f"  S={S:>5}  comparisons={comps:,}  time={elapsed:.4f}s")
        writer.writerow({"part": "c2", "n": FIXED_N_FOR_C2, "S": S,
                          "comparisons": comps, "time_seconds": elapsed})

def run_c3(writer):
    print(f"\n[c3] finding optimal S across varying n and S:")
    for n in N_VALUES_FOR_C3:
        print(f"\nTesting array size n = {n:,}")
        data = generate_random_array(n)

        for S in S_VALUES_FOR_C3:
            comps, elapsed = time_hybrid(data, S)
            print(f"  S={S:>3}  comparisons={comps:>12,}  time={elapsed:.4f}s")
            writer.writerow({"part" : "c3", "n" : n, "S": S, "comparisons": comps, "time_seconds": elapsed})


def main():
    random.seed(RANDOM_SEED)
    sys.setrecursionlimit(10000)

    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["part", "n", "S", "comparisons", "time_seconds"])
        writer.writeheader()
        run_c1(writer)
        run_c2(writer)
        run_c3(writer) 

    print(f"\nDone. Results written to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
