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
|   ├── sorting_algo.py        # insertion sort, original merge sort, hybrid sort, data generator
|   ├── exp.py                 # runs experiments for (c)(i), (c)(ii), (c)(iii) -> results.csv
|   ├── original_vs_hybrid.py  # part (d): hybrid vs. original merge sort on n = 10,000,000 -> results_partd.csv
|   ├── generate_plots.py      # reads results.csv, produces plots/*.png
|   ├── test_sorting_algo.py   # correctness and edge-case tests
|   ├── results.csv            # experiment results for part (c)
|   ├── results_partd.csv      # experiment results for part (d)
|   ├── plots/                 # generated comparison plots
|   └── Slides.pptx
├── requirements.txt
└── README.md
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

The experiment scripts use random seed `42` and generate integers in the
inclusive range `[1, 1_000_000]`. The full experiment includes repeated sorts
of 10 million integers, so it requires substantial time and memory.
