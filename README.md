# SC2001 Lab Projects
 
Code for our SC2001 (Algorithm Design and Analysis) lab projects.

## Team Members
- Gupta Dhruv (U2523576H)
- Gajulapalli Anish Reddy (U2523276F)
- Koh Jin En (U2521578F)


## Repo Structure

```
.
├── Lab1/
│   ├── plots/                         # generated experiment plots
│   │   ├── comparisons_vs_n.png       # comparisons as input size n increases
│   │   ├── comparisons_vs_S.png       # comparisons as threshold S changes
│   │   └── optimal_s_split.png        # CPU time used to select S across input sizes
│   ├── sorting_algo.py               # sorting algorithms, comparison counting and data generation
│   ├── test_sorting_algo.py          # correctness and edge-case tests
│   ├── exp.py                        # runs parts (c)(i)–(c)(iii) and writes results.csv
│   ├── generate_plots.py             # generates the plots above from results.csv
│   ├── original_vs_hybrid.py         # runs part (d) and writes results_partd.csv
│   ├── results.csv                   # measurements from parts (c)(i)–(c)(iii)
│   ├── results_partd.csv             # hybrid-versus-baseline measurements for part (d)
│   ├── sc2001_lab1_slides.pptx       # presentation deck
│   └── sc2001_project1_final.pptx    # final project presentation
├── Lab2/
│   ├── part_a_matrix_array.py        # matrix + array Dijkstra implementation
│   ├── part_a_experiment.py          # part (a) empirical analysis
│   ├── part_a_analysis.md            # part (a) written analysis
│   ├── test_part_a.py                # part (a) correctness tests
│   ├── part_b_list_heap.py           # adjacency list + min-heap Dijkstra implementation
│   ├── part_b_experiment.py          # part (b) empirical analysis
│   ├── part_b_analysis.md            # part (b) written analysis
│   ├── test_part_b.py                # part (b) correctness tests
│   └── part_c_comparison.md          # part (c) report scaffold
├── Lab3/
│   ├── part_1_recursive.py           # recursive definition of P(C), with a memo
│   ├── part_1_recursive_definition.md # part (1) definition and explanation
│   ├── test_part_1.py                # part (1) tests against brute force
│   ├── part_2_subproblem_graph.py    # builds and draws the subproblem graph for P(15)
│   ├── part_2_subproblem_graph.md    # part (2) graph and explanation
│   ├── test_part_2.py                # part (2) graph checks
│   ├── part_3_bottom_up.py           # bottom-up DP and packing reconstruction
│   ├── part_3_bottom_up_algorithm.md # part (3) pseudocode and explanation
│   ├── test_part_3.py                # bottom-up tests against brute force
│   ├── part_4_run_examples.py        # runs P(16) and P(12)
│   ├── part_4_results.md             # part (4) DP tables and optimal packings
│   └── results/                      # subproblem graph image and DP run log
├── .gitignore
├── requirements.txt                  # Python dependencies
└── README.md                         # project overview and usage instructions
```

## Setup and Run

From the repository root:

```bash
python3 -m pip install -r requirements.txt
python3 -m unittest discover -s Lab1 -p 'test_*.py'
python3 Lab1/exp.py
python3 Lab1/generate_plots.py
python3 Lab1/original_vs_hybrid.py
```

For Project 2 part (a):

```bash
python3 Lab2/part_a_matrix_array.py
python3 -m unittest discover -s Lab2 -p 'test_*.py'
python3 Lab2/part_a_experiment.py
```

For Project 2 part (b):

```bash
python3 Lab2/part_b_list_heap.py
python3 -m unittest discover -s Lab2 -p 'test_*.py'
python3 Lab2/part_b_experiment.py
```

For Project 3 parts (1) and (2):

```bash
python3 Lab3/part_1_recursive.py
python3 Lab3/part_2_subproblem_graph.py
python3 -m unittest discover -s Lab3 -p 'test_*.py'
```

For Project 3 parts (3) and (4), Dhruv's portion:

```bash
python3 Lab3/part_4_run_examples.py
python3 -m unittest discover -s Lab3 -p 'test_*.py' -v
```

The bottom-up algorithm gives `P(16) = 28` for weights `[4, 5, 8]` and
`P(12) = 16` for weights `[5, 6, 7]`, both with profits `[7, 6, 9]`.
See [the algorithm](Lab3/part_3_bottom_up_algorithm.md) and
[the worked results](Lab3/part_4_results.md).

The experiment scripts use random seed `42` and generate integers in the
inclusive range `[1, 1_000_000]`. The full experiment includes repeated sorts
of 10 million integers, so it requires substantial time and memory.
