# Project 2: Dijkstra's Algorithm

## Files

- `part_a_matrix_array.py`: completed beginner-friendly implementation for
  part (a), using an adjacency matrix and an array priority queue.
- `part_a_experiment.py`: completed empirical experiments for part (a).
- `part_a_analysis.md`: completed theoretical analysis and experiment method.
- `test_part_a.py`: correctness tests for part (a).
- `part_b_list_heap.py`: initial scaffold for the part (b) implementation.
- `part_b_experiment.py`: initial scaffold for the part (b) experiments.
- `part_c_comparison.md`: initial report structure for part (c).
- `results/`: generated CSV measurements and plots.

## Run part (a)

From the repository root, run:

```bash
python3 Lab2/part_a_matrix_array.py
python3 -m unittest discover -s Lab2 -p "test_*.py"
python3 Lab2/part_a_experiment.py
```

`None` represents a missing edge in the matrix. This means that a weight of
zero remains a valid edge weight. Dijkstra's algorithm requires every edge
weight to be non-negative.
