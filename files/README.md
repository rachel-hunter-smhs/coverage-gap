# The Coverage Gap — U.S. Health Insurance Access, 2024

A small data pipeline + interactive dashboard built around U.S. Census Bureau
American Community Survey (ACS) data on health insurance coverage.

**Live dashboard:** `https://<your-username>.github.io/coverage-gap/` (after you
enable Pages — see below)

## What's here

| File | What it does |
|---|---|
| `index.html` | The dashboard. Self-contained, no build step — also served by GitHub Pages. |
| `dashboard.html` | Identical copy of `index.html`, kept for local dev clarity. |
| `build_dataset.py` | Structures hand-compiled 2024 figures (sourced from KFF's published analysis of ACS data) into 8 clean CSVs. No API key needed — runs anywhere. |
| `fetch_census_api.py` | Pulls **live** state-by-state uninsured rates directly from the Census Bureau's own API (table S2701). Needs a free API key and normal internet access. |
| `source_notes.md` | Every figure used in the dashboard, with exact source citations. |
| `clean/*.csv` | Output of `build_dataset.py` — tidy, analysis-ready tables. |

## Why this dataset

I co-founded a nonprofit focused on insurance access advocacy, so this isn't an
arbitrary pick — it's the kind of question I actually work on: who falls through
the cracks of the U.S. health coverage system, and why.

The headline finding: for the first time since 2019, the uninsured rate rose in
2024 (9.5% → 9.8%, 26.7 million people under 65), driven mainly by Medicaid
"unwinding" after pandemic-era continuous enrollment ended. The gaps are sharply
unequal — uninsured rates are 3-4x higher for low-income families, young adults,
and several racial/ethnic groups than for the population overall.

## Two ways the data gets built

**1. From published figures (`build_dataset.py`)** — no setup required.
Compiles statistics manually sourced from KFF's June 2026 analysis of ACS data
into clean CSVs. This is what powers the dashboard's national/demographic
breakdowns.

**2. From the Census API directly (`fetch_census_api.py`)** — for state-level
detail. Queries `api.census.gov` for table S2701 ("Selected Characteristics of
Health Insurance Coverage") and pulls live per-state uninsured rates with
margins of error.

```bash
# one-time: get a free key at https://api.census.gov/data/key_signup.html
export CENSUS_API_KEY="your_key_here"
python3 fetch_census_api.py            # defaults to 2024 ACS 1-year estimates
python3 fetch_census_api.py --year 2023  # or any other available year
```

This writes `clean/state_uninsured_rates.csv` with one row per state: name,
population, percent uninsured, and margin of error.

## Running locally

```bash
git clone https://github.com/<your-username>/coverage-gap.git
cd coverage-gap
python3 build_dataset.py        # regenerate clean/*.csv from source figures
open index.html                 # or just double-click it
```

## Putting this on GitHub Pages

```bash
git init
git add .
git commit -m "Initial commit: coverage gap dashboard"
git branch -M main
git remote add origin https://github.com/<your-username>/coverage-gap.git
git push -u origin main
```

Then on GitHub: **Settings -> Pages -> Source: Deploy from a branch -> Branch:
main, folder: / (root) -> Save.**

GitHub will publish the site at `https://<your-username>.github.io/coverage-gap/`
within a minute or two -- that's the link to use anywhere a "link to something
you've built" is requested.

## Source

KFF, *"Key Facts about the Uninsured Population,"* Jennifer Tolbert, Sammy
Cervantes, Clea Bell, and Anthony Damico. Published June 16, 2026.
https://www.kff.org/uninsured/key-facts-about-the-uninsured-population/

Underlying data: U.S. Census Bureau, American Community Survey (ACS), 2023-2024
1-year estimates, table S2701.
