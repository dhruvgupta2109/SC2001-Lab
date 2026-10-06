# Part (c): Comparison

## Results to compare

### Theoretical complexity comparison
| operation | part (a): adjacency matrix and array priority queue | part(b): adjacency list and min heap priority queue |
| **Initialisation** | $O(V)$ | $O(V)$ |
| **Extract-Min (per call)** | $O(V)$ (linear scan over unvisited elements) | $O(\log V)$ (sift-down in binary heap) |
| **Extract-Min (total for $V$ calls)** | $O(V^2)$ | $O(V \log V)$ |
| **Neighbor Scanning (total across run)** | $O(V^2)$ (inspects all $V$ cells per vertex) | $O(E)$ (traverses active incident edges) |
| **Decrease-Key / Distance Update (per call)** | $O(1)$ (direct array index assignment) | $O(\log V)$ (sift-up using position tracking) |
| **Decrease-Key / Distance Update (worst-case total)** | $O(E)$ | $O(E \log V)$ |
| **Total Worst-Case Time Complexity** | **$O(V^2)$** | **$O((V + E) \log V)$** |
| **Typical / Empirical Time Complexity** | $\approx O(V^2)$ (independent of $E$) | $\approx O(E + V \log V)$ (only few edges sift up) |
| **Space Complexity** | $O(V^2)$ | $O(V + E)$ |

- Theoretical running time of both implementations
- Experimental time as `V` increases
- Experimental time as `E` increases
- Memory used by an adjacency matrix and adjacency lists

## Questions to answer

1. Which implementation is better for a sparse graph, where `E` is much
   smaller than `V^2`?
2. Which implementation is better for a dense graph, where `E` is close to
   `V^2`?
3. How do the simpler code and constant costs affect the measured results?
