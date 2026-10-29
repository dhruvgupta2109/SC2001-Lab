# Project 3: Dynamic Programming (Unbounded Knapsack)

## Work split

- Anish: parts (1) and (2), the recursive definition and subproblem graph.
- Dhruv: parts (3) and (4), the bottom-up DP algorithm and required runs.
- Jin En: time/space complexity analysis and slides.

## Files

- `part_1_recursive.py`: the recursive definition of `P(C)`, written as a
  recursive function with a memo.
- `part_1_recursive_definition.md`: the definition, why it is correct, and a
  worked example.
- `test_part_1.py`: checks the recursive function against a brute-force search.
- `part_2_subproblem_graph.py`: builds and draws the subproblem graph for
  `P(15)`.
- `part_2_subproblem_graph.md`: the graph's vertices and edges, and what the
  graph shows.
- `test_part_2.py`: checks the vertices and edges of the graph.
- `results/part_2_subproblem_graph_P15.png`: the drawn subproblem graph.
- `part_3_bottom_up.py`: bottom-up DP implementation and packing reconstruction.
- `part_3_bottom_up_algorithm.md`: part (3) algorithm, pseudocode, and correctness
  explanation.
- `test_part_3.py`: checks the bottom-up table and recovered packings against
  brute force and the recursive implementation.
- `part_4_run_examples.py`: runs both datasets required by part (4).
- `part_4_results.md`: full DP tables, calculations, and optimal packings for
  `P(16)` and `P(12)`.
- `results/part_4_run_log.txt`: saved output from the two required runs.

## Run parts (1) and (2)

From the repository root, run:

```bash
python3 Lab3/part_1_recursive.py
python3 Lab3/part_2_subproblem_graph.py
python3 -m unittest discover -s Lab3 -p "test_*.py"
```

## Run Dhruv's parts (3) and (4)

From the repository root:

```bash
python3 Lab3/part_4_run_examples.py
python3 -m unittest discover -s Lab3 -p "test_*.py" -v
```

The runner prints both complete DP tables and an optimal packing for each,
then saves its output to `results/part_4_run_log.txt`. No new dependencies
are needed. Start with [the algorithm](part_3_bottom_up_algorithm.md) and
[the worked results](part_4_results.md) for the complete write-up.

## Verified results

- With `w = [4, 5, 8]` and `p = [7, 6, 9]`, `P(15) = 21`.
- The subproblem graph for `P(15)` has 10 vertices and 15 edges.
- Bottom-up DP gives `P(16) = 28` with the same data, using four objects of
  weight `4` and profit `7`.
- For `w = [5, 6, 7]` and `p = [7, 6, 9]`, bottom-up DP gives `P(12) = 16`,
  using one weight-`5` object and one weight-`7` object.
- All 19 Lab 3 tests pass, including the eight bottom-up correctness tests.
