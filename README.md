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
|   ├── results.csv            # experiment results for part (c)
|   ├── results_partd.csv      # experiment results for part (d)
|   ├── plots/                 # generated comparison plots
|   └── Slides.pptx
└── README.md
```

Run order: `python exp.py` (writes `results.csv`) -> `python generate_plots.py` (writes `plots/*.png`) -> `python original_vs_hybrid.py` (writes `results_partd.csv`).
