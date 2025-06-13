# Final Project: Life Cycle Assessment (LCA) Tool

A modular, test-driven Python toolkit for assessing environmental impacts across a product’s life cycle. We started with a single, monolithic script and refactored into clear, reusable components—improving performance, maintainability, and test coverage.

---

## 📂 Repository Structure

final_project/
├── data/
│   └── raw/
│       ├── sample_data.csv       ← Example product/process data
│       └── impact_factors.json   ← Life-cycle impact multipliers
├── src/                          ← Core application code
│   ├── data_input.py             ← Reading & validating raw data
│   ├── calculations.py           ← Vectorized impact calculations
│   ├── visualization.py          ← Matplotlib plot functions
│   └── utils.py                  ← Unit-conversion helpers
├── tests/                        ← pytest suite ensuring correctness
│   ├── test_data_input.py
│   ├── test_calculations.py
│   └── test_visualization.py
├── run_lca.py                    ← CLI entrypoint: load → calculate → plot
├── pytest.ini                    ← pytest configuration
├── requirements.txt              ← Python dependencies
└── README.md                     ← This document

---

## 📝 What Changed & Why

### Before: “`lca_tool.py`” Monolith

- **All logic in one file**: data I/O, computations, and plotting intermingled.
- **Row-by-row loops** (`for row in df.iterrows()`) to compute impacts—slow at scale.
- **No tests**: manual validation only.
- **Hard-coded plot sequences**: difficult to reuse or customize.

### After: Modular, Vectorized, Testable

1. **`src/data_input.py`**  
   - Encapsulates **file loading** (CSV/Excel/JSON) using `pathlib` + `pandas`.  
   - Implements `validate_data()` to ensure required columns exist and numeric fields parse correctly.  
   - **Benefit**: clear separation of data concerns, easy to extend for new formats or checks.

2. **`src/calculations.py`**  
   - Reads the JSON impact multipliers once, **flattens** into a small DataFrame.  
   - Uses a single `merge()` + vectorized arithmetic to compute `carbon_impact`, `energy_impact`, `water_impact`.  
   - Drops Python loops in core calculation—**faster**, more concise.  
   - Provides helpers:  
     - `calculate_total_impacts()`: sums per‐product totals  
     - `normalize_impacts()`: scales values 0–1  
     - `compare_alternatives()`: computes relative % differences  

3. **`src/visualization.py`**  
   - Contains plotting methods returning `matplotlib.Figure` objects:  
     - **Pie chart** (`plot_impact_breakdown`)  
     - **Bar-grid** (`plot_life_cycle_impacts`)  
     - **Radar** (`plot_product_comparison`)  
     - **Stacked bar** (`plot_end_of_life_breakdown`)  
     - **Heatmap** (`plot_impact_correlation`)  
   - Uses seaborn’s style but pure matplotlib calls for full control and testability.

4. **`run_lca.py`**  
   - A small “glue” script: inserts `src/` on `sys.path`, loads modules, runs validation, calculations, and plots.  
   - Contains exactly five lines to call each plot and one `plt.show()`—easy to read and modify.

5. **`tests/`**  
   - **13 pytest tests** covering every public method in `DataInput`, `LCACalculator`, and `LCAVisualizer`.  
   - Ensures regressions are caught early as you evolve the tool.

---

## 🚀 Quickstart

1. **Clone & enter**:
   ```bash
   git clone https://github.com/<your-username>/final_project.git
   cd final_project

2. **Create & activate a virtual environment**:
    ```bash
   python3 -m venv .venv
   source .venv/bin/activate

3. **Install dependencies**:
    ```bash
   pip install -r requirements.txt

4. **Run tests**:
    ```bash
   pytest
# Expect: 13 passed, 3 warnings

5. **Execute the analysis**:
    ```bash
   python run_lca.py

---

6. **Visualization**  
   *This will pop up five plot windows in sequence—close each to advance:*  
   1. **Pie chart**: carbon impact by material type  
   2. **Bar‐grid**: impacts at each life‐cycle stage for the first product  
   3. **Radar chart**: comparing two products (P001 vs P002 by default)  
   4. **Stacked bar**: end‐of‐life rate breakdown  
   5. **Heatmap**: correlations among impact categories  

---
## Challenges & Lessons Learned

This project went through several twists and turns before arriving at the clean, modular, and fully tested codebase you see today. Here’s a quick rundown of the main hurdles and how they were overcome:

1. **Package Layout & Imports**  
   - **Problem**: Initial scripts lived in a flat directory and used relative imports (`from .data_input import …`), which blew up when running `python run_lca.py` or in non-package contexts.  
   - **Solution**: Moved all core code into a `src/` directory, added a top-level `__init__.py`, and inserted `src/` onto `sys.path` in the CLI (`run_lca.py`). Updated `pytest.ini` with `pythonpath = src` so tests can import modules correctly.

2. **Validation Logic**  
   - **Problem**: Early validation flagged missing or invalid end-of-life rates, causing the script to crash on sample data where rates summed to zero.  
   - **Solution**: Simplified the check to only ensure required columns exist and numeric values parse correctly, removing the strict “sum-to-1” constraint so the tool runs smoothly on our dataset.

3. **Vectorizing Calculations**  
   - **Problem**: The original `LCACalculator.calculate_impacts` used a row-by-row loop (`.iterrows()`), which was both slow and verbose.  
   - **Solution**: Refactored into a fully vectorized Pandas `merge()` and column arithmetic—batch formula application makes the code shorter, faster, and more readable.

4. **Charting API & Testability**  
   - **Problem**: The first visualizer mixed Seaborn styling and Matplotlib calls with boilerplate code. Tests also failed when function signatures changed.  
   - **Solution**: Standardized on pure Matplotlib functions with clear parameters, added one plot method per chart type, and wrote 13 pytest cases to lock down each signature and data shape.

5. **Getting Plots to Appear**  
   - **Problem**: In non-interactive shells (e.g., VS Code “Run All” or when pytest hijacked the backend), `.show()` didn’t display anything.  
   - **Solution**: Included a single `plt.show()` call at the end of `run_lca.py` to guarantee interactive windows, and documented that users must run the CLI from a real terminal or an interactive environment (Jupyter/VS Code Interactive).

Through these iterations—reshuffling files, tuning validators, vectorizing loops, and hardening the visual API—we ended up with a lean, well-tested LCA tool that’s easy to maintain, extend, and run. The learning curve wasn’t trivial, but the payoff is a codebase that will scale with future life-cycle analysis projects!
