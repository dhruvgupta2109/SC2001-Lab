# Part (1): Recursive Definition of P(C)

## The problem

There are `n` types of objects. An object of type `i` has weight `w_i` and
profit `p_i`, where every `w_i` and `p_i` is a positive integer. There is an
unlimited supply of each type. `P(C)` is the largest total profit of any set
of objects whose total weight is at most `C`.

## Definition

```
P(C) = 0                                              if w_i > C for every i

P(C) = max { p_i + P(C - w_i) : 0 <= i <= n-1, w_i <= C }   otherwise
```

The two cases can also be written as one line:

```
P(C) = max( {0} ∪ { p_i + P(C - w_i) : w_i <= C } )
```

## Why the definition is correct

**Base case.** If every object is heavier than `C`, nothing can be packed, so
the best profit is `0`. This includes `P(0) = 0`, because every weight is
positive.

**Recursive case.** Take any optimal packing for capacity `C` that contains at
least one object, and suppose one of its objects has type `i`. If we remove
that object, the rest of the packing has total weight at most `C - w_i`.

The rest must be an optimal packing for capacity `C - w_i`. If a more
profitable packing for `C - w_i` existed, we could add the type `i` object back
to it and get a packing for `C` with more profit than the optimal one. That is
impossible. So the optimal profit for `C` is `p_i + P(C - w_i)`.

We do not know in advance which type `i` the optimal packing contains, so we
try every type that fits and keep the largest result. This property, where an
optimal solution is built from optimal solutions to smaller problems, is
called **optimal substructure**.

When at least one object fits, it is always better to pack something, because
every profit is positive. That is why the recursive case does not need a
separate "pack nothing" option.

## Why P has only one parameter

In the 0/1 knapsack problem, each object can be used at most once, so a
subproblem must also record which objects are still available. That needs
two parameters, such as `P(i, C)`.

Here the supply of every type is unlimited. After packing an object of type
`i`, all `n` types are still available. The only thing that changes is the
remaining capacity, so `P(C)` is enough.

## Example

Using the data from part (2), with `w = [4, 5, 8]` and `p = [7, 6, 9]`:

| C | Calculation | P(C) |
|---:|---|---:|
| 0, 1, 2, 3 | no object fits | 0 |
| 5 | max(7 + P(1), 6 + P(0)) = max(7, 6) | 7 |
| 6 | max(7 + P(2), 6 + P(1)) = max(7, 6) | 7 |
| 7 | max(7 + P(3), 6 + P(2)) = max(7, 6) | 7 |
| 10 | max(7 + P(6), 6 + P(5), 9 + P(2)) = max(14, 13, 9) | 14 |
| 11 | max(7 + P(7), 6 + P(6), 9 + P(3)) = max(14, 13, 9) | 14 |
| 15 | max(7 + P(11), 6 + P(10), 9 + P(7)) = max(21, 20, 16) | 21 |

So `P(15) = 21`. One optimal packing is three objects of type 0
(weight `3 x 4 = 12`, profit `3 x 7 = 21`).

## Code

`part_1_recursive.py` implements the definition directly as a recursive
function. It stores each answer in a dictionary (a memo) so that each `P(c)`
is computed only once.

Without the memo, the recursion for `P(15)` makes 20 calls, but there are only
10 different subproblems. For example, `P(7)` is reached from both `P(15)` and
`P(11)`. The repeated work grows quickly for larger capacities. This is why
part (3) uses dynamic programming, which solves each subproblem once.

`test_part_1.py` checks the function against a brute-force search that tries
every possible combination of objects on 200 random small inputs.

Run from the repository root:

```bash
python3 Lab3/part_1_recursive.py
python3 -m unittest discover -s Lab3 -p "test_*.py"
```
