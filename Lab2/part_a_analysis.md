# Part (a): Adjacency Matrix and Array Priority Queue

## Representation

The graph is stored in a `V` by `V` adjacency matrix. The value at row `u`
and column `v` is the weight of the edge from `u` to `v`. A value of `None`
means that the edge does not exist.

The priority queue is represented by two arrays:

- `distances[v]` stores the best distance currently known for vertex `v`.
- `visited[v]` records whether vertex `v` has been removed from the queue.

To remove the vertex with minimum distance, the algorithm scans the whole
`distances` array and chooses the nearest unvisited vertex.

## Theoretical time complexity

Let `V = |V|` be the number of vertices and `E = |E|` be the number of edges.

Initialising the three arrays takes `O(V)` time. The main loop runs at most `V`
times. On each iteration:

1. Finding the unvisited vertex with the smallest distance scans `V` entries,
   so it takes `O(V)` time.
2. Finding its neighbours scans one complete row of the adjacency matrix, so
   it also takes `O(V)` time.

The total running time is therefore:

`O(V) + V * (O(V) + O(V)) = O(V^2)`.

It can also be written as `O(V^2 + E)`, because at most `E` successful edge
relaxations occur. Since `E <= V^2`, this simplifies to `O(V^2)`. The matrix
forces the algorithm to inspect `V^2` possible edges even when the actual graph
has very few edges.

The adjacency matrix uses `O(V^2)` space. The `distances`, `previous`, and
`visited` arrays use another `O(V)` space. Total space usage is `O(V^2)`.

## Empirical method

The experiment uses connected, undirected graphs with random integer weights
from 1 to 100. Graph generation is performed before timing begins. Each timed
measurement runs Dijkstra's algorithm five times on the same graph and records
the average using `time.perf_counter()`.

Two experiments are included:

1. Increase `V` from 100 to 800 while keeping graph density near 25%. If the
   theoretical analysis is correct, the time should grow approximately with
   `V^2`.
2. Keep `V = 500` and increase graph density from 1% to 90%. The running time
   should change much less because the algorithm scans the same 500 by 500
   matrix regardless of how many entries contain edges.

Run `python3 Lab2/part_a_experiment.py` from the repository root. The program
writes the exact measurements and two plots to `Lab2/results/`.

## Empirical results

The following measurements were produced on 4 October 2026. Times will differ
between computers, so the growth pattern is more useful than the exact values.

| V | E (about 25% density) | Average time (seconds) | Time / V^2 |
|---:|---:|---:|---:|
| 100 | 1,237 | 0.000524 | 5.24 x 10^-8 |
| 200 | 4,975 | 0.001956 | 4.89 x 10^-8 |
| 400 | 19,950 | 0.008049 | 5.03 x 10^-8 |
| 600 | 44,925 | 0.018580 | 5.16 x 10^-8 |
| 800 | 79,900 | 0.032769 | 5.12 x 10^-8 |

`Time / V^2` stays close to `5 x 10^-8`. Also, increasing `V` from 100 to
800 multiplies `V^2` by 64, while the measured time is multiplied by about
62.5. This supports the theoretical `O(V^2)` result.

With `V` fixed at 500, the results were:

| V | E | Density | Average time (seconds) |
|---:|---:|---:|---:|
| 500 | 1,247 | 1% | 0.010849 |
| 500 | 12,475 | 10% | 0.011748 |
| 500 | 31,187 | 25% | 0.012619 |
| 500 | 62,375 | 50% | 0.014179 |
| 500 | 112,275 | 90% | 0.014898 |

The number of edges increased by about 90 times, but the measured time only
increased by about 1.37 times. Denser matrices do a little more work inside the
edge checks, but every run still scans all `500^2` matrix positions. The
experiments therefore agree with the conclusion that `V`, rather than `E`,
dominates this implementation's running time.
