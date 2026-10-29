# Part (3): Bottom-Up Dynamic Programming Algorithm

**Owner: Dhruv.** Implementation: [part_3_bottom_up.py](part_3_bottom_up.py).
The required runs are in [part (4)](part_4_results.md).

## What the table stores

For each capacity `c`, store the maximum profit achievable with total weight
**at most** `c` in `dp[c]`. The answer is `dp[C]`.

Part (1) gives the rule used to fill each entry:

```text
dp[c] = max({0} union {profits[i] + dp[c - weights[i]] : weights[i] <= c})
```

The `0` represents packing nothing. Set `dp[0] = 0`, and leave any entry at
`0` if no object fits. A packing does not have to fill the capacity exactly.

## Order of computation

Fill capacities in increasing order: `0, 1, 2, ..., C`.

Every weight is positive, so `c - weights[i] < c`. Therefore, every smaller
answer needed to compute `dp[c]` has already been calculated. This is the
bottom-up order suggested by the subproblem graph in part (2).

For each capacity, try every object type that fits. Adding one object of
type `i` gives profit `profits[i]`, plus the best profit for the remaining
capacity, `dp[c - weights[i]]`. Keep the largest candidate.

All types are considered again at each capacity. The smaller packing can
already contain objects of type `i`, so this allows unlimited copies.

## Pseudocode

Inputs: non-negative integer capacity `C`, and arrays `w` and `p` of length
`n`, containing positive integer weights and profits. Object types are
numbered `0` to `n - 1`.

```text
BOTTOM_UP_KNAPSACK(C, w, p):
    n = length(w)
    dp[0 ... C] = 0
    choice[0 ... C] = NONE

    for c = 1 to C:
        for i = 0 to n - 1:
            if w[i] <= c:
                candidate = p[i] + dp[c - w[i]]
                if candidate > dp[c]:
                    dp[c] = candidate
                    choice[c] = i

    return dp, choice

Answer: dp[C]
```

`choice[c]` records one object type used to obtain `dp[c]`. It is optional
if only the maximum profit is needed, but lets part (4) show an actual
optimal packing. Using `>` keeps the first type encountered when profits tie.

## Recovering a packing

Start with remaining capacity `C` and zero objects of each type. While
`choice[remaining]` is not `NONE`:

1. Read `i = choice[remaining]`.
2. Add one object of type `i` to the packing.
3. Set `remaining = remaining - w[i]`.

Stop when no object fits. Any remaining capacity is unused. Each step
reduces the remaining capacity, so reconstruction terminates.

## Why the algorithm is correct

**Base case.** At capacity `0`, no positive-weight object fits, so
`dp[0] = 0 = P(0)`.

**Inductive step.** Suppose every entry for capacity less than `c` is
correct. For any type `i` that fits, `dp[c - w[i]]` is the optimal profit
for the remaining capacity by this assumption. Adding a type `i` object
therefore gives a feasible packing with profit `p[i] + dp[c - w[i]]`.

Every non-empty optimal packing contains some type `i`. Removing one such
object leaves a packing for `c - w[i]`, so the algorithm considers a
candidate at least as profitable as that optimal packing. Since every
candidate is feasible, taking their maximum gives exactly `P(c)`. If no
object fits, the entry stays `0`, which is also correct.

Thus every table entry is correct, including the final answer `dp[C]`.

## Python interface

```python
from part_3_bottom_up import (
    build_dp_table,
    max_profit_bottom_up,
    reconstruct_counts,
)

weights = [4, 5, 8]
profits = [7, 6, 9]

answer = max_profit_bottom_up(16, weights, profits)  # 28
dp, choice = build_dp_table(16, weights, profits)
counts = reconstruct_counts(16, weights, choice)    # [4, 0, 0]
```

The imports above work from the `Lab3` directory. From the repository root,
use `from Lab3.part_3_bottom_up import ...` for these functions, or run the
example script directly:

```bash
python3 Lab3/part_4_run_examples.py
python3 -m unittest discover -s Lab3 -p "test_*.py"
```
