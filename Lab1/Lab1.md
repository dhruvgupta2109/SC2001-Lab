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
