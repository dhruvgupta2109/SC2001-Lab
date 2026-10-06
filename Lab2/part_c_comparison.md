# Part (c): Comparison

## Results to compare

### Theoretical complexity comparison
| operation | part (a): adjacency matrix and array priority queue | part(b): adjacency list and min heap priority queue |
|---:|---:|---:|
| extract_min | o(|V|) per call --> O(|V|^2) total | O(log |V|) per call --> O(|V| log |V|) total|
| 200 | 4,975 | 0.001956 |
| 400 | 19,950 | 0.008049 |
| 600 | 44,925 | 0.018580 |
| 800 | 79,900 | 0.032769 |

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
