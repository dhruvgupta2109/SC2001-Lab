import random
import sys
import time

from sorting_algo import generate_random_array, hybrid_sort, original_merge_sort

sys.setrecursionlimit(2000000)

RANDOM_SEED = 42
S_VALUE = 10
N_VALUE = 10000000


def is_sorted(arr):
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


def time_hybrid(data, S):
    arr = data.copy()
    counter = [0]
    start = time.process_time()
    hybrid_sort(arr, 0, len(arr) - 1, S, counter)
    elapsed = time.process_time() - start
    assert is_sorted(arr), f"Hybrid sort failed to sort n={len(data)}"
    return counter[0], elapsed


def time_original_merge(data):
    arr = data.copy()
    counter = [0]
    start = time.process_time()
    original_merge_sort(arr, 0, len(arr) - 1, counter)
    elapsed = time.process_time() - start
    assert is_sorted(arr), f"Original merge sort failed to sort n={len(data)}"
    return counter[0], elapsed


def main():
    random.seed(RANDOM_SEED)
    data = generate_random_array(N_VALUE)
    h_comps, h_time = time_hybrid(data, S_VALUE)
    print(f"Hybrid Sort:         comparisons = {h_comps:>14,} | time = {h_time:.4f}s")

    m_comps, m_time = time_original_merge(data)
    print(f"Original Merge Sort: comparisons = {m_comps:>14,} | time = {m_time:.4f}s")

    time_diff = m_time - h_time
    percentage_faster = (time_diff / m_time) * 100
    comp_diff = m_comps - h_comps

    print("\n" + "=" * 22 + " results " + "=" *22)
    print(f"Time Saved:        {time_diff:.4f}s ({percentage_faster:.2f}% faster)")
    print(f"Comparisons Saved: {comp_diff:,}")


if __name__ == "__main__":
    main()
