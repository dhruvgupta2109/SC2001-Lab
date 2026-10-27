# Project 3: Dynamic Programming (Unbounded Knapsack)

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

## Run parts (1) and (2)

From the repository root, run:

```bash
python3 Lab3/part_1_recursive.py
python3 Lab3/part_2_subproblem_graph.py
python3 -m unittest discover -s Lab3 -p "test_*.py"
```

## Results so far

- With `w = [4, 5, 8]` and `p = [7, 6, 9]`, `P(15) = 21`.
- The subproblem graph for `P(15)` has 10 vertices and 15 edges.
- For checking part (4), the recursive function gives `P(16) = 28` with the
  same data, and `P(12) = 16` with `w = [5, 6, 7]` and `p = [7, 6, 9]`.
