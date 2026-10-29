# Part (4): Implementation and Required Runs

**Owner: Dhruv.** The bottom-up implementation is in
[part_3_bottom_up.py](part_3_bottom_up.py), with its algorithm and correctness
explanation in [part (3)](part_3_bottom_up_algorithm.md).
[part_4_run_examples.py](part_4_run_examples.py) runs both required datasets
and saves the full output to
[results/part_4_run_log.txt](results/part_4_run_log.txt).

## Run from the repository root

```bash
python3 Lab3/part_4_run_examples.py
python3 -m unittest discover -s Lab3 -p "test_*.py" -v
```

The example script uses only Python's standard library and the part (3)
implementation. The full Lab 3 test suite also imports part (2), which uses
the repository's existing `matplotlib` dependency.

Types are numbered `0`, `1`, `2`, matching parts (1) and (2).

## Run 1: P(16)

Capacity `C = 16`:

| Type | Weight | Profit |
|---:|---:|---:|
| 0 | 4 | 7 |
| 1 | 5 | 6 |
| 2 | 8 | 9 |

The completed bottom-up table is:

| Capacity c | dp[c] = P(c) |
|---:|---:|
| 0 | 0 |
| 1 | 0 |
| 2 | 0 |
| 3 | 0 |
| 4 | 7 |
| 5 | 7 |
| 6 | 7 |
| 7 | 7 |
| 8 | 14 |
| 9 | 14 |
| 10 | 14 |
| 11 | 14 |
| 12 | 21 |
| 13 | 21 |
| 14 | 21 |
| 15 | 21 |
| 16 | **28** |

The last entry compares:

```text
dp[16] = max(7 + dp[12], 6 + dp[11], 9 + dp[8])
       = max(7 + 21,     6 + 14,     9 + 14)
       = max(28, 20, 23)
       = 28
```

Reconstruction follows `P(16) -> P(12) -> P(8) -> P(4) -> P(0)`, choosing
type `0` four times.

- Object counts: `[4, 0, 0]`.
- Total weight: `4 x 4 = 16`.
- Total profit: `4 x 7 = 28`.
- Unused capacity: `0`.

**Result: P(16) = 28.**

## Run 2: P(12)

This is a new instance with **different weights**. Rebuild the table using
`w = [5, 6, 7]` and `p = [7, 6, 9]`, with capacity `C = 12`.

| Type | Weight | Profit |
|---:|---:|---:|
| 0 | 5 | 7 |
| 1 | 6 | 6 |
| 2 | 7 | 9 |

The completed table is:

| Capacity c | dp[c] = P(c) |
|---:|---:|
| 0 | 0 |
| 1 | 0 |
| 2 | 0 |
| 3 | 0 |
| 4 | 0 |
| 5 | 7 |
| 6 | 7 |
| 7 | 9 |
| 8 | 9 |
| 9 | 9 |
| 10 | 14 |
| 11 | 14 |
| 12 | **16** |

The last entry compares:

```text
dp[12] = max(7 + dp[7], 6 + dp[6], 9 + dp[5])
       = max(7 + 9,     6 + 7,     9 + 7)
       = max(16, 13, 16)
       = 16
```

Types `0` and `2` tie at this step. The implementation keeps type `0`
because it is encountered first. Reconstruction follows
`P(12) -> P(7) -> P(0)`, choosing type `0` and then type `2`.

- Object counts: `[1, 0, 1]`.
- Total weight: `5 + 7 = 12`.
- Total profit: `7 + 9 = 16`.
- Unused capacity: `0`.

**Result: P(12) = 16.** The entry `P(12) = 21` in run 1 belongs to the
first dataset; its weights are different.

## Validation

The full Lab 3 suite passes **19 tests**. The eight new tests in
[test_part_3.py](test_part_3.py) cover:

- Both required answers and their reconstructed object counts.
- Zero capacity, no fitting objects, and no available object types.
- Unlimited copies, unused capacity, tied choices, and a case where choosing
  the best profit-to-weight ratio greedily fails.
- A capacity of `5000`, computed without recursive calls.
- Invalid capacities, mismatched arrays, and invalid weights or profits.
- Every table entry on 100 random small inputs, compared with independent
  enumeration of all feasible object counts and the existing recursive
  implementation. Every reconstructed packing is also checked for its
  capacity and profit.

## Results for the team handoff

| Instance | Weights | Profits | Maximum profit | Object counts |
|---|---|---|---:|---|
| P(16) | [4, 5, 8] | [7, 6, 9] | 28 | [4, 0, 0] |
| P(12) | [5, 6, 7] | [7, 6, 9] | 16 | [1, 0, 1] |
