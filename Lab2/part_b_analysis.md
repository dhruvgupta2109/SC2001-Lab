# Part (b): Array of Adjacency Lists and Minimizing Heap

## Representation

The graph is stored as an array of adjacency lists. `adjacency_list[u]` is a
Python list of `(v, weight)` pairs, one pair for each edge `u -> v`. Only edges
that really exist are stored, so an undirected graph with `E` edges stores
`2E` pairs in total.

The priority queue is a binary minimizing heap written from scratch in
`MinHeap` (see `part_b_list_heap.py`). It uses three arrays:

- `vertices[i]` is the vertex stored at heap position `i`.
- `keys[i]` is that vertex's current distance, which is the heap key.
- `position[v]` is where vertex `v` currently sits in the heap, or `-1` if it
  has already been removed.

The `position` array is what makes `decrease_key` efficient. Without it, the
heap would have to be searched (`O(V)`) to find a vertex before lowering its
key.

| Heap operation | What it does | Cost |
|---|---|---|
| `insert` | Append, then sift up | `O(log V)` |
| `extract_min` | Swap root with last item, remove it, sift down | `O(log V)` |
| `decrease_key` | Find vertex with `position`, lower key, sift up | `O(log V)` |
| `contains` | Check `position[v] != -1` | `O(1)` |

## Algorithm

1. Set every distance to infinity, except `distances[source] = 0`.
2. Insert every vertex into the heap, keyed by its distance.
3. While the heap is not empty, `extract_min` gives the closest vertex `u`. Its
   distance is now final.
4. For each `(v, w)` in `adjacency_list[u]`, if `v` is still in the heap and
   `distances[u] + w < distances[v]`, update `distances[v]` and call
   `decrease_key(v)`.
5. If `extract_min` returns a vertex with distance infinity, all remaining
   vertices are unreachable, so the loop stops early.

## Theoretical time complexity

Let `V = |V|` and `E = |E|`.

1. **Initialisation.** Creating `distances` and `previous` takes `O(V)`.
   Inserting `V` vertices into the heap takes `O(V log V)` in general. In this
   implementation the source has key `0` and every other key is infinity, so
   no insert needs to sift up, and building the heap actually takes `O(V)`.
2. **Extracting vertices.** Each vertex is removed from the heap once, so there
   are at most `V` calls to `extract_min`, each `O(log V)`. Total:
   `O(V log V)`.
3. **Scanning edges.** A vertex's adjacency list is scanned once, when that
   vertex is extracted. Over the whole run, the total length of all lists
   scanned is `E` for a directed graph or `2E` for an undirected graph. Each
   check is `O(1)`, so scanning takes `O(E)`.
4. **Relaxing edges.** In the worst case every edge check improves a distance
   and calls `decrease_key`, giving at most `E` calls of `O(log V)` each:
   `O(E log V)`.

Adding these together:

`O(V) + O(V log V) + O(E) + O(E log V) = O((V + E) log V)`.

If the graph is connected, `E >= V - 1`, so this is often written as
`O(E log V)`.

**Sparse graphs** (`E` is about `V`): the running time is `O(V log V)`, much
better than the `O(V^2)` of part (a).

**Dense graphs** (`E` is about `V^2`): the running time becomes
`O(V^2 log V)`, which is worse than part (a) by a factor of `log V`. This
happens because each of the `V^2` edges may trigger a `decrease_key` costing
`O(log V)`, while the array in part (a) can update a distance in `O(1)`.

**Space.** The adjacency lists use `O(V + E)` space, and the heap,
`distances`, `previous` and `position` arrays use `O(V)`. Total space is
`O(V + E)`, compared to `O(V^2)` for the adjacency matrix in part (a).

### Why the worst case is not usually reached

The `O(E log V)` term assumes every edge causes a `decrease_key`. In practice
only edges that find a *shorter* path do. On random graphs, most edges reach
a neighbour that already has a good distance, so most edge checks are just a
cheap `O(1)` comparison. The experiment below counts `decrease_key` calls to
show this. So on typical graphs the measured time behaves more like
`O(E + V log V)`. This does not change the worst-case bound. Some graphs do
trigger a `decrease_key` on almost every edge, and for those the
`O((V + E) log V)` bound still applies.

## Empirical method

`part_b_experiment.py` uses the same settings as part (a) so the two parts
can be compared directly:

- Random seed `42`, connected undirected graphs, integer weights from 1 to 100.
- Graph generation (and conversion to adjacency lists) happens before timing.
- Each graph is run once as an untimed warm-up, then timed 5 times with
  `time.perf_counter()`, and the average is recorded.
- After timing, Dijkstra's algorithm is run once more with a `CountingMinHeap`
  that counts `extract_min` calls, `decrease_key` calls and heap swaps. This
  run is not timed.

Experiments 1 and 2 call part (a)'s graph generator with the same seed and
settings, then convert each matrix to adjacency lists. Both parts are
therefore measured on **identical graphs**.

1. **Vary V**: `V` from 100 to 800 with density about 25%.
2. **Vary E**: `V = 500`, density from 1% to 90%.
3. **Large sparse graphs**: `V` from 1,000 to 50,000 with `E = 5V`. These are
   generated directly as adjacency lists. A matrix for `V = 50,000` would need
   2.5 billion entries, so part (a) cannot run these graphs at all.

Run `python3 Lab2/part_b_experiment.py` from the repository root. The program
writes `results/part_b_results.csv` and three plots. Each plot shows the
measured times and a `c (V + E) log V` curve scaled to match the largest point,
so you can compare the shapes.

## Empirical results

These measurements were produced on 6 October 2026, on a different machine from
part (a). Times will differ between computers, so look at how times grow
rather than the exact values. For the part (c) comparison, rerun both
experiments on the same machine.

In the tables, `(V+E) log V` is the theoretical quantity. "Time / work" is
time divided by `(V + E) log2 V`, in units of `10^-8` seconds.

### Experiment 1: increasing V (density about 25%)

| V | E | Time (s) | Time / work | `decrease_key` calls | `decrease_key` / 2E |
|---:|---:|---:|---:|---:|---:|
| 100 | 1,237 | 0.000736 | 8.29 | 272 | 11.0% |
| 200 | 4,975 | 0.001721 | 4.35 | 701 | 7.0% |
| 400 | 19,950 | 0.006990 | 3.97 | 1,542 | 3.9% |
| 600 | 44,925 | 0.017903 | 4.26 | 2,399 | 2.7% |
| 800 | 79,900 | 0.027746 | 3.57 | 3,440 | 2.2% |

From `V = 100` to `V = 800`, `(V + E) log V` grows about 88 times, while the
measured time grows about 38 times. Time grows more slowly than the worst-case
bound because the number of `decrease_key` calls grows only about 13 times.
Most edge checks are cheap `O(1)` comparisons and do not touch the heap.

### Experiment 2: increasing E (V = 500)

| Density | E | Time (s) | Time / work | `decrease_key` calls | `decrease_key` / 2E |
|---:|---:|---:|---:|---:|---:|
| 1% | 1,247 | 0.002473 | 15.79 | 697 | 27.9% |
| 10% | 12,475 | 0.006190 | 5.32 | 1,620 | 6.5% |
| 25% | 31,187 | 0.008941 | 3.15 | 1,979 | 3.2% |
| 50% | 62,375 | 0.017950 | 3.18 | 2,157 | 1.7% |
| 90% | 112,275 | 0.031260 | 3.09 | 2,268 | 1.0% |

This is the main difference from part (a). In part (a), increasing `E` about
90 times only increased the time about 1.4 times, because the matrix is always
fully scanned. Here, the time grows about 13 times, and the plot
`part_b_time_vs_edges.png` is almost a straight line in `E`. This happens
because the adjacency lists get longer as `E` grows, so there are more edges
to scan. `decrease_key` calls only grow from 697 to 2,268 (about 3.3 times),
so the extra time comes mostly from the `O(E)` edge scanning, not from heap
work.

### Experiment 3: large sparse graphs (E = 5V)

| V | E | Time (s) | Time / work | `decrease_key` calls | Heap swaps |
|---:|---:|---:|---:|---:|---:|
| 1,000 | 5,000 | 0.007833 | 13.10 | 1,928 | 10,730 |
| 2,000 | 10,000 | 0.018248 | 13.87 | 3,919 | 23,294 |
| 5,000 | 25,000 | 0.061352 | 16.64 | 9,706 | 65,397 |
| 10,000 | 50,000 | 0.121142 | 15.19 | 19,588 | 140,012 |
| 20,000 | 100,000 | 0.310503 | 18.11 | 39,148 | 299,968 |
| 50,000 | 250,000 | 0.901396 | 19.25 | 97,728 | 817,729 |

When `E/V` is fixed, the theory predicts time grows like `V log V`. The heap
operations match this closely. The number of heap swaps divided by `V log2 V`
stays between 1.05 and 1.08 for every row, and about 19.5% of edge checks
cause a `decrease_key` at every size. From `V = 1,000` to `V = 50,000`,
`(V + E) log V` grows about 78 times, and the heap swaps grow about 76 times.

The measured time grows a little faster, about 115 times. The operation counts
follow the theory, so the extra time comes from the hardware rather than the
algorithm. With 50,000 vertices, the heap and adjacency lists no longer fit in
the CPU cache. Python objects are spread through memory, so each access is
slower on large graphs. Even so, the algorithm finishes a 50,000-vertex graph
in under a second. Part (a) would need a 50,000 by 50,000 matrix, which is far
too large to store.

## Summary

- Theory: `O((V + E) log V)` time and `O(V + E)` space.
- Experiments 1 and 3 show that the number of heap operations grows the way
  the theory predicts.
- Experiment 2 shows that, unlike part (a), the running time depends strongly
  on `E`.
- On random graphs, only a small fraction of edges cause a `decrease_key`
  (1% to 28% here). Real running times are therefore well below the worst-case
  `E log V` term, and behave more like `O(E + V log V)`.
