
---

## 🧩 Task 1 — Git & Environment Setup
**Objective:** Prepare a clean and reproducible working environment.  

**Steps:**
1. Created repository `solar-challenge-week0` on GitHub.  
2. Cloned locally and set up a Python virtual environment (`.venv`).  
3. Created `.gitignore`, `requirements.txt`, and `README.md`.  
4. Configured **GitHub Actions** to verify environment setup.  
5. Used proper Git branching (`setup-task`) and meaningful commits.

**Key Files:**
- `.gitignore` — ignored CSVs, virtual environments, and checkpoints.  
- `.github/workflows/ci.yml` — verifies installation of dependencies.  
- `requirements.txt` — includes pandas, matplotlib, seaborn, numpy, scipy.

**Result:**  
Successfully merged setup branch into `main` via pull request.

---

## 🔍 Task 2 — Data Profiling, Cleaning & EDA

**Objective:** Clean and analyze solar datasets for Benin, Sierra Leone, and Togo.  

**Key Steps:**
1. Created branch `eda-<country>` for each dataset.  
2. Loaded raw data and checked for missing values using:
   ```python
   df.describe(), df.isna().sum()
3. Identified and handled outliers using Z-scores.

4. Cleaned data by imputing or dropping invalid records.

5. Exported cleaned datasets as data/<country>_clean.csv (ignored by Git).

6. Conducted time-series and correlation analysis using plots:

   . GHI, DNI, DHI trends

   . Temperature vs humidity

   . Wind speed and direction patterns

🌍 Task 3 — Cross-Country Comparison

Objective: Compare solar potential across Benin, Togo, and Sierra Leone.

Steps:

1. Created branch compare-countries and notebook compare_countries.ipynb.

2. Combined all cleaned datasets into one DataFrame.

3. Created comparison plots:

  . Boxplots of GHI, DNI, DHI by country.

  . Bar chart ranking countries by average GHI.

4. Computed summary statistics (mean, median, std).

5. Applied Kruskal–Wallis test (non-parametric ANOVA) → p ≈ 0.000 → significant differences exist.


🖥️ Task 4 — Interactive Dashboard (Streamlit)

Objective: Build and deploy a Streamlit dashboard to visualize insights interactively.

Branch: dashboard-dev

Main Files:
   app/main.py — Streamlit app script.


   Technologies Used

     . Python (pandas, numpy, scipy, seaborn, matplotlib, plotly)

     . Streamlit (for dashboard UI)

     . Git & GitHub (version control and collaboration)

     . GitHub Actions (for CI checks)


     👩‍💻 Author: Bethelihem weldgebrial