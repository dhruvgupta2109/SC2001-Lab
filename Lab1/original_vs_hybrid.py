import random
import sys
import gc
import time
import csv

from sorting_algo import generate_random_array, hybrid_sort, original_merge_sort

sys.setrecursionlimit(2000000)

RANDOM_SEED = 42
S_VALUE = 10
N_VALUE = 10000000
REPEATS = 3
OUTPUT_CSV = "results_partd.csv"


def is_sorted(arr):
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


def time_hybrid_once(data, S):
    arr = data.copy()
    counter = [0]
    gc.disable()
    start = time.process_time()
    hybrid_sort(arr, 0, len(arr) - 1, S, counter)
    elapsed = time.process_time() - start
    gc.enable()
    assert is_sorted(arr), f"Hybrid sort failed to sort n={len(data)}"
    return counter[0], elapsed


def time_original_merge_once(data):
    arr = data.copy()
    counter = [0]
    gc.disable()
    start = time.process_time()
    original_merge_sort(arr, 0, len(arr) - 1, counter)
    elapsed = time.process_time() - start
    gc.enable()
    assert is_sorted(arr), f"Original merge sort failed to sort n={len(data)}"
    return counter[0], elapsed


def repeated(run_once, *args, repeats):
    """Comparisons are deterministic; time is taken as the min across repeats
    (system noise can only slow a run down, never speed it up)."""
    times = []
    comparisons = None
    for _ in range(repeats):
        comparisons, t = run_once(*args)
        times.append(t)
    return comparisons, min(times)


def main():
    random.seed(RANDOM_SEED)
    data = generate_random_array(N_VALUE)

    h_comps, h_time = repeated(time_hybrid_once, data, S_VALUE, repeats=REPEATS)
    print(f"Hybrid Sort (S={S_VALUE}):  comparisons = {h_comps:>14,} | time (min of {REPEATS}) = {h_time:.4f}s")

    m_comps, m_time = repeated(time_original_merge_once, data, repeats=REPEATS)
    print(f"Original Merge Sort:  comparisons = {m_comps:>14,} | time (min of {REPEATS}) = {m_time:.4f}s")

    time_diff = m_time - h_time
    percentage_faster = (time_diff / m_time) * 100
    comp_diff = m_comps - h_comps

    print("\n" + "=" * 22 + " results " + "=" * 22)
    print(f"Time Saved:        {time_diff:.4f}s ({percentage_faster:.2f}% faster)")
    print(f"Comparisons Saved: {comp_diff:,}")

    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["algorithm", "n", "S", "comparisons", "time_seconds", "repeats"])
        writer.writeheader()
        writer.writerow({"algorithm": "Hybrid Sort", "n": N_VALUE, "S": S_VALUE,
                          "comparisons": h_comps, "time_seconds": round(h_time, 4), "repeats": REPEATS})
        writer.writerow({"algorithm": "Original Merge Sort", "n": N_VALUE, "S": "",
                          "comparisons": m_comps, "time_seconds": round(m_time, 4), "repeats": REPEATS})

    print(f"\nSaved results to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
