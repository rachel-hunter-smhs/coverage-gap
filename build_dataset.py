"""
build_dataset.py

Cleans and structures 2024 U.S. uninsured-population data (sourced from KFF's
analysis of Census ACS data) into tidy CSVs for downstream analysis/dashboarding.

Source: KFF, "Key Facts about the Uninsured Population" (June 16, 2026)
https://www.kff.org/uninsured/key-facts-about-the-uninsured-population/
Underlying data: U.S. Census Bureau, American Community Survey (ACS), 2023-2024

Output:
  clean/age_breakdown.csv
  clean/income_breakdown.csv
  clean/race_breakdown.csv
  clean/work_status_breakdown.csv
  clean/reasons_uninsured.csv
  clean/access_to_care.csv
  clean/financial_impact.csv
  clean/national_summary.csv
"""

import csv
import os

OUT_DIR = "clean"
os.makedirs(OUT_DIR, exist_ok=True)


def write_csv(filename, header, rows):
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
    print(f"wrote {path} ({len(rows)} rows)")


# --- National summary -------------------------------------------------
national_summary = [
    ("total_uninsured_millions_2024", 26.7),
    ("total_uninsured_millions_2023", 25.3),
    ("uninsured_rate_2024", 9.8),
    ("uninsured_rate_2023", 9.5),
    ("uninsured_rate_2019", 10.9),
    ("yoy_change_pct_points", round(9.8 - 9.5, 1)),
]
write_csv(
    "national_summary.csv",
    ["metric", "value"],
    national_summary,
)

# --- By age -------------------------------------------------------------
age_rows = [
    ("Children (0-18)", 5.9),
    ("Young adults (19-25)", 14.5),
    ("Adults (26-34)", 14.1),
    ("Adults (55-64)", 7.4),
    ("All adults (19-64)", 11.3),
]
write_csv("age_breakdown.csv", ["group", "uninsured_rate_pct"], age_rows)

# --- By income ------------------------------------------------------------
income_rows = [
    ("<100% FPL (in poverty)", 16.5),
    ("100-199% FPL", 16.5),
    ("200-399% FPL", 11.5),
    ("400%+ FPL", 4.5),
]
write_csv("income_breakdown.csv", ["income_band", "uninsured_rate_pct"], income_rows)

# --- By race/ethnicity -----------------------------------------------------
race_rows = [
    ("American Indian / Alaska Native", 18.9),
    ("Hispanic", 18.4),
    ("Native Hawaiian / Pacific Islander", 12.3),
    ("Black", 10.1),
    ("White", 6.8),
    ("Asian", 5.7),
]
write_csv("race_breakdown.csv", ["group", "uninsured_rate_pct"], race_rows)

# --- By family work status --------------------------------------------------
work_rows = [
    ("No workers in family", 14.1),
    ("Part-time worker(s) only", 13.6),
    ("One full-time worker", 10.1),
    ("Multiple full-time workers", 8.9),
]
write_csv("work_status_breakdown.csv", ["work_status", "uninsured_rate_pct"], work_rows)

# --- Reasons for being uninsured ---------------------------------------------
reasons_rows = [
    ("Coverage not affordable", 61.7),
    ("Not eligible for coverage", 28.9),
    ("Did not need/want coverage", 28.0),
    ("Difficulty signing up", 21.0),
]
write_csv("reasons_uninsured.csv", ["reason", "share_pct"], reasons_rows)

# --- Access to care gap --------------------------------------------------
access_rows = [
    ("Did not see a doctor in past 12 months", "Uninsured", 46.2),
    ("Did not see a doctor in past 12 months", "Private coverage", 14.7),
    ("Did not see a doctor in past 12 months", "Public coverage", 12.8),
    ("Delayed/skipped care due to cost", "Uninsured", 38.6),
    ("Delayed/skipped care due to cost", "Private coverage", 17.0),
    ("Delayed/skipped care due to cost", "Public coverage", 18.8),
]
write_csv("access_to_care.csv", ["measure", "coverage_status", "share_pct"], access_rows)

# --- Financial impact --------------------------------------------------------
financial_rows = [
    ("Say affording health care is difficult", "Uninsured", 82),
    ("Say affording health care is difficult", "Insured", 42),
    ("Had problems paying for health care", "Uninsured", 59),
    ("Had problems paying for health care", "Insured", 30),
    ("Have medical debt (strict definition)", "Uninsured", 34),
    ("Have medical debt (strict definition)", "Insured", 26),
    ("Have health care debt (broad definition)", "Uninsured", 62),
    ("Have health care debt (broad definition)", "Insured", 44),
]
write_csv(
    "financial_impact.csv",
    ["measure", "coverage_status", "share_pct"],
    financial_rows,
)

print("\nDone. All tables written to ./clean/")
