# Part (c): Comparison

## Results to compare

### Theoretical complexity comparison
| operation | part (a): adjacency matrix and array priority queue | part(b): adjacency list and min heap priority queue |
| :--- | :--- | :--- |
| **Initialisation** | O(\|V\|) | O(\|V\|) |
| **Extract-Min (per call)** | O(\|V\|) (scan all unvisited elemets) | O(log \|V\|) (sift-down binary heap) |
| **Extract-Min (total for all vertices)** | O(\|V\|^2) | O(\|V\| log \|V\|) |
| **Scan for neigbours** | O(\|V\|^2) (inspects all \|V\| cells per vertex) | O(\|E\|) (traverses active incident edges) |
| **Distance Update (per call)** | O(1) (assign array index directly) | O(log \|V\|) (sift-up using position tracking) |
| **Distance Update (worst-case total)** | O(\|E\|) | O(\|E\| log \|V\|) |
| **Total Worst-Case Time Complexity** | O(\|V\|^2) | O((\|V\| + \|E\|) log \|V\|) |
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
| \|V\|| Part (a): Matrix Space $\Theta(\|V\|^2)$ [no. of entries] | Part (b): List Space $\Theta(\|V\| + \|E\|)$ (Sparse, $\|E\| = 5\|V\|$) [no. of entries] | Feasibility |
| :---: | :---: | :---: | :---: |
| **500** | $500^2 = 250,000$ | $500 + 2(2,500) = 5,500$ | Both run easily |
| **5,000** | $5,000^2 = 25,000,000$ | $5,000 + 2(25,000) = 55,000$  | Both run |
| **50,000** | $50,000^2 = 2,500,000,000$ | $50,000 + 2(250,000) = 550,000$  | Matrix allocation fails but List completes in 0.90s |


**Circumstances in which part (a) implementation is better**
1. Dense graph ( \|E\| $\approx$ \|V\|^2, Density > 40%) : When nearly every vertex connects to every other vertex, Part (a) O(\|V\|^2) runtime beats Part (b)’s O(\|V\|^2 log \|V\|) by eliminating repeated O(log \|V\|) heap sifts.
2. Small Graphs (\|V\| $\le$ 100): For small problem sizes, the simplicity of contiguous 2D array lookups benefits from CPU cache locality, avoiding the overhead of maintaining binary tree structures and position lookup tables.
3. Implementation Simplicity: When rapid prototyping is required without external priority queue dependencies, Part (a) requires only standard arrays without needing custom heap index tracking.

**Circumstances in which part (b) implementation is better**
1. Sparse Graphs (\|E\| << \|V\|): When vertices have a limited degree (for eg. \|E\| $\approx$ O(\|V\|) ), Part (b) O(\|E\| log \|V\|) complexity completely outperforms the $\Theta(\|V\|^2)$ matrix scan.
2. Large-Scale Graphs (\|V\| 	$\ge$ 1000 up to \|V\| = 50,000 and beyond): As shown in memory usage chart, Part (b) scales linearly to \|V\| = 50,000 (0.90s), whereas Part (a) becomes impractical past \|V\| $\approx$ 1,000 due to quadratic memory growth $\Theta(\|V\|^2)$.
3. Real-World Networks: Nearly all real-world networks—including road navigation maps (e.g. google maps), telecommunications routing, and social networks—are naturally sparse action on millions of vertices. As a result, Part (b) represents the industry-standard choice for real-world software.

**How Code Simplicity and Constant Costs Affect Measured Results**
1. part a
  - Contiguous array: scanning a row in an adjacency matrix matrix[u][v] accesses contiguous blocks of memory in RAM. Modern CPU architectures prefetch adjacent memory lines into high-speed CPU caches (L1/L2/L3), making sequential iteration extremely fast.
  - Low constant factor: The inner loops in Part (a) consist of straightforward pointer arithmetic, simple boolean checks (if not visited[v]), and direct index writes, resulting in minimal CPU instruction overhead.
2. part b
  - List traversal: An adjacency list consists of dynamic lists or references stored across fragmented memory locations. Iterating through neighbors incurs cache misses (pointer chasing) compared to contiguous matrix scans.
  - Higher constant factor: In Part (b), maintaining the heap requires navigating tree structures, repeatedly tracking indices in a secondary position array, and swapping items during sift-up and sift-down operations. Each logical step requires multiple low-level instructions.

**Therefore**, Because Part (a) has a much smaller constant factor per operation than the heap-based logic of Part (b), Part (a) outperforms Part (b) as soon as edge density surpasses $\approx$ 35-40%.Even though Part (b)'s theoretical bound is  O((\|V\| + \|E\|) log \|V\|), the constant overhead of maintaining heap invariants and sifting up during decrease_key makes it noticeably slower than Part (a)'s lightweight O(1) direct array overwrites on dense graphs.
