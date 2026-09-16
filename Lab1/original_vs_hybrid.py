import random
import gc
import time
import csv
from pathlib import Path

from sorting_algo import generate_random_array, hybrid_sort, original_merge_sort

RANDOM_SEED = 42
N_VALUE = 10000000
REPEATS = 3
LAB_DIR = Path(__file__).resolve().parent
RESULTS_CSV = LAB_DIR / "results.csv"        # part (c) results, read to find optimal S
OUTPUT_CSV = LAB_DIR / "results_partd.csv"


def determine_optimal_S(csv_path=RESULTS_CSV, n_target=N_VALUE, metric="time_seconds_min"):
    """
    Reads the (c)(iii) grid-search rows from results.csv and returns the S
    value that minimized `metric` (best observed CPU time by default) at n_target.
    Falls back to the closest tested n if n_target itself wasn't tested,
    and raises a clear error if there's no c3 data at all.
    """
    rows = []
    with open(csv_path, newline="") as f:
        for row in csv.DictReader(f):
            if row["part"] == "c3":
                rows.append(row)

    if not rows:
        raise RuntimeError(
            f"No part-c3 rows found in {csv_path}. Run exp.py first so "
            "there's data to pick an optimal S from."
        )

    available_ns = sorted({int(r["n"]) for r in rows}, key=lambda n: abs(n - n_target))
    chosen_n = available_ns[0]
    if chosen_n != n_target:
        print(f"[optimal S] n={n_target:,} wasn't in the c3 sweep; "
              f"using closest tested size n={chosen_n:,} instead.")

    candidates = [r for r in rows if int(r["n"]) == chosen_n]
    best_row = min(candidates, key=lambda r: float(r[metric]))
    best_S = int(best_row["S"])

    print(f"[optimal S] at n={chosen_n:,}, S={best_S} minimizes {metric} "
          f"({float(best_row[metric]):.4f}s)")
    return best_S


def is_sorted(arr):
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


def time_hybrid_once(data, S):
    arr = data.copy()
    counter = [0]
    gc_was_enabled = gc.isenabled()
    if gc_was_enabled:
        gc.disable()
    try:
        start = time.process_time()
        hybrid_sort(arr, 0, len(arr) - 1, S, counter)
        elapsed = time.process_time() - start
    finally:
        if gc_was_enabled:
            gc.enable()
    assert is_sorted(arr), f"Hybrid sort failed to sort n={len(data)}"
    return counter[0], elapsed


def time_original_merge_once(data):
    arr = data.copy()
    counter = [0]
    gc_was_enabled = gc.isenabled()
    if gc_was_enabled:
        gc.disable()
    try:
        start = time.process_time()
        original_merge_sort(arr, 0, len(arr) - 1, counter)
        elapsed = time.process_time() - start
    finally:
        if gc_was_enabled:
            gc.enable()
    assert is_sorted(arr), f"Original merge sort failed to sort n={len(data)}"
    return counter[0], elapsed


def repeated(run_once, *args, repeats):
    """Return deterministic comparisons and the best observed CPU time."""
    times = []
    comparisons = None
    for _ in range(repeats):
        comparisons, t = run_once(*args)
        times.append(t)
    return comparisons, min(times)


def main():
    random.seed(RANDOM_SEED)

    S_VALUE = determine_optimal_S()  # was hardcoded to 10, now derived from results.csv

    data = generate_random_array(N_VALUE)

    h_comps, h_time = repeated(time_hybrid_once, data, S_VALUE, repeats=REPEATS)
    print(f"Hybrid Sort (S={S_VALUE}):  comparisons = {h_comps:>14,} | time (min of {REPEATS}) = {h_time:.4f}s")

    m_comps, m_time = repeated(time_original_merge_once, data, repeats=REPEATS)
    print(f"Original Merge Sort:  comparisons = {m_comps:>14,} | time (min of {REPEATS}) = {m_time:.4f}s")

    time_diff = m_time - h_time
    percentage_faster = (time_diff / m_time) * 100
    comp_diff = h_comps - m_comps
    comp_percentage = (comp_diff / m_comps) * 100

    print("\n" + "=" * 22 + " results " + "=" * 22)
    if time_diff >= 0:
        print(f"Hybrid time saved: {time_diff:.4f}s ({percentage_faster:.2f}% faster)")
    else:
        print(f"Hybrid extra time: {-time_diff:.4f}s ({-percentage_faster:.2f}% slower)")

    if comp_diff >= 0:
        print(f"Hybrid comparisons: {comp_diff:,} more ({comp_percentage:.2f}% more)")
    else:
        print(f"Hybrid comparisons: {-comp_diff:,} fewer ({-comp_percentage:.2f}% fewer)")

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
