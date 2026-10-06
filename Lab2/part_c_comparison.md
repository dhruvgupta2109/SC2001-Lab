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
**1. Fixed |V| at 500, |E| increases**
| Density | \|E\| | Part (a) Time (seconds) | Part (b) Time (seconds) | Faster Implementation |
| :---: | :---: | :---: | :---: | :---: |
| **1%** | 1,247 | 0.01085 | 0.00247 | Part (b) (~4.4x faster) |
| **10%** | 12,475 | 0.01175 | 0.00619 | Part (b) (~1.9x faster) |
| **25%** | 31,187 | 0.01262 | 0.00894 | Part (b) (~1.4x faster) |
| **50%** | 62,375 | 0.01418 | 0.01795 | Part (a) (~1.3x faster) |
| **90%** | 112,275 | 0.01490 | 0.03126 | Part (a) (~2.1x faster) |

**2. Fixed density ~25%, |V| increases**
| \|V\| | \|E\| (density ~25%)| Part (a) Time (seconds) | Part (b) Time (seconds) |
| :---: | :---: | :---: | :---: |
| **100** | 1,237 | 0.000524 | 0.000736 |
| **200** | 4,975 | 0.001956 | 0.001721 |
| **400** | 19,950 | 0.008049 | 0.006990 |
| **600** | 44,925 | 0.018580 | 0.017903 |
| **800** | 79,900 | 0.032769 | 0.027746 |

### Memory usage
| \|V\|| Part (a): Matrix Space $\Theta(\|V\|^2)$ | Part (b): List Space $\Theta(\|V\| + \|E\|)$ (Sparse, $\|E\| = 5\|V\|$) | Feasibility |
| :---: | :---: | :---: | :---: |
| **500** | $500^2 = 250,000$ entries | $500 + 2(2,500) = 5,500$ stored items | Both run easily |
| **5,000** | $5,000^2 = 25,000,000$ entries | $5,000 + 2(25,000) = 55,000$ stored items | Both run |
| **50,000** | $50,000^2 = 2,500,000,000$ entries | $50,000 + 2(250,000) = 550,000$ stored items | **Matrix allocation fails**, List completes in 0.90s |

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
