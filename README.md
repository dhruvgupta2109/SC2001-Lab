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

The experiment scripts use random seed `42` and generate integers in the
inclusive range `[1, 1_000_000]`. The full experiment includes repeated sorts
of 10 million integers, so it requires substantial time and memory.
