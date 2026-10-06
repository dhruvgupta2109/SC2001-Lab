# Part (c): Comparison

## Results to compare

### Theoretical complexity comparison
| operation | part (a): adjacency matrix and array priority queue | part(b): adjacency list and min heap priority queue |
| :--- | :--- | :--- |
| **Initialisation** | O(\|V\|) | O(\|V\|) |
| **Extract-Min (per call)** | O(\|V\|) (scan all unvisited elemets) | O(log \|V\|) (sift-down binary heap) |
| **Extract-Min (total for all vertices)** | O(\|V\|^2) | O(\|V\| log \|V\|) |
| **Scan for neigbours** | O(\|V\|^2) (inspects all \|V\| cells per vertex) | O(\|E\|) (traverses active incident edges) |
| **Distance Update (per call)** | O(1) (direct array index assignment) | O(log \|V\|) (sift-up using position tracking) |
| **Distance Update (worst-case total)** | O(\|E\|) | O(\|E\| log \|V\|) |
| **Total Worst-Case Time Complexity** | **O(\|V\|^2)** | **O((\|V\| + \|E\|) log \|V\|)** |
| **Typical / Empirical Time Complexity** | ~ O(\|V\|^2) (independent of \|E\|) | ~ O(\|E\| + \|V\| log \|V\|) (only few edges sift up) |
| **Space Complexity** | O(\|V\|^2) | O(\|V\| + \|E\|) |

### Empirical complexity comparison
Fixed |V| at 500, |E| increases
| Density | \|E\| | Part (a) Time (in s) | Part (b) Time (in s) | Faster Implementation |
| :---: | :---: | :---: | :---: | :---: |
| **1%** | 1,247 | 0.01085 | 0.00247 | Part (b) (~4.4x faster) |
| **10%** | 12,475 | 0.01175 | 0.00619 | Part (b) (~1.9x faster) |
| **25%** | 31,187 | 0.01262 | 0.00894 | Part (b) (~1.4x faster) |
| **50%** | 62,375 | 0.01418 | 0.01795 | Part (a) (~1.3x faster) |
| **90%** | 112,275 | 0.01490 | 0.03126 | Part (a) (~2.1x faster) |


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
