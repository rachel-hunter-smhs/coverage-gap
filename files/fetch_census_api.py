"""
fetch_census_api.py

Pulls state-level uninsured rate data from the Census Bureau's
SAHIE (Small Area Health Insurance Estimates) API and writes
clean/state_uninsured_rates.csv.

Endpoint: api.census.gov/data/timeseries/healthins/sahie
Docs:     https://www.census.gov/data/developers/data-sets/Health-Insurance-Statistics.html

SETUP
-----
1. Get a free API key (instant):
   https://api.census.gov/data/key_signup.html

2. Set it as an environment variable:
   export CENSUS_API_KEY="your_key_here"

3. Run:
   python3 fetch_census_api.py            # defaults to latest year (2023)
   python3 fetch_census_api.py --year 2019  # or any year back to 2006
"""

import argparse
import csv
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API_BASE  = "https://api.census.gov/data/timeseries/healthins/sahie"
LATEST    = 2023   # most recent SAHIE year as of 2026

# Variables we want:
#   NAME       — state name
#   PCTUI_PT   — percent uninsured, estimate
#   PCTUI_MOE  — margin of error on that estimate
#   NUI_PT     — number uninsured, estimate
#   STABREV    — 2-letter state abbreviation
#
# Filters (keep these narrow so the response stays small):
#   AGECAT=0   — under 65 (the standard scope for uninsured analysis)
#   IPRCAT=0   — all incomes
#   SEXCAT=0   — both sexes
#   RACECAT=0  — all races
VARIABLES = "NAME,STABREV,PCTUI_PT,PCTUI_MOE,NUI_PT"


def build_url(year: int, api_key: str) -> str:
    params = {
        "get":     VARIABLES,
        "for":     "state:*",
        "time":    str(year),
        "AGECAT":  "0",
        "IPRCAT":  "0",
        "SEXCAT":  "0",
        "RACECAT": "0",
    }
    if api_key:
        params["key"] = api_key
    return f"{API_BASE}?{urllib.parse.urlencode(params)}"


def fetch(year: int, api_key: str):
    url = build_url(year, api_key)
    safe_url = url.replace(api_key, "***") if api_key else url
    print(f"Fetching: {safe_url}\n")

    req = urllib.request.Request(url, headers={"User-Agent": "coverage-gap-project/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code} error:\n{body}", file=sys.stderr)
        if e.code == 400 and not api_key:
            print("\nTip: get a free key at https://api.census.gov/data/key_signup.html"
                  "\nthen: export CENSUS_API_KEY='your_key_here'", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Network error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Fetch state uninsured rates from SAHIE API")
    parser.add_argument("--year",    type=int, default=LATEST,
                        help=f"SAHIE year, 2006–{LATEST} (default: {LATEST})")
    parser.add_argument("--api-key", default=os.environ.get("CENSUS_API_KEY", ""),
                        help="Census API key (or set CENSUS_API_KEY env var)")
    parser.add_argument("--out",     default="clean/state_uninsured_rates.csv",
                        help="Output CSV path")
    args = parser.parse_args()

    if not args.api_key:
        print("No API key found.\n"
              "Get a free one at: https://api.census.gov/data/key_signup.html\n"
              "Then: export CENSUS_API_KEY='your_key_here'", file=sys.stderr)
        sys.exit(1)

    raw = fetch(args.year, args.api_key)
    header, *rows = raw

    name_i  = header.index("NAME")
    abbr_i  = header.index("STABREV")
    pct_i   = header.index("PCTUI_PT")
    moe_i   = header.index("PCTUI_MOE")
    nui_i   = header.index("NUI_PT")

    states = []
    for row in rows:
        try:
            states.append({
                "state":            row[name_i],
                "abbreviation":     row[abbr_i],
                "pct_uninsured":    float(row[pct_i]),
                "pct_uninsured_moe": float(row[moe_i]),
                "num_uninsured":    int(row[nui_i]),
                "sahie_year":       args.year,
            })
        except (TypeError, ValueError):
            continue

    states.sort(key=lambda r: r["pct_uninsured"], reverse=True)

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=states[0].keys())
        writer.writeheader()
        writer.writerows(states)

    print(f"Wrote {len(states)} states → {args.out}\n")

    col_w = max(len(s["state"]) for s in states)
    print(f"  {'STATE':<{col_w}}  {'UNINSURED %':>11}  {'MOE':>6}  {'# UNINSURED':>12}")
    print(f"  {'-'*(col_w+35)}")
    for s in states[:5]:
        print(f"  {s['state']:<{col_w}}  {s['pct_uninsured']:>10.1f}%"
              f"  ±{s['pct_uninsured_moe']:<4.1f}  {s['num_uninsured']:>12,}")
    print(f"  {'...':}")
    for s in states[-5:]:
        print(f"  {s['state']:<{col_w}}  {s['pct_uninsured']:>10.1f}%"
              f"  ±{s['pct_uninsured_moe']:<4.1f}  {s['num_uninsured']:>12,}")

    avg = sum(s["pct_uninsured"] for s in states) / len(states)
    print(f"\n  Avg across {len(states)} states: {avg:.1f}%  ·  SAHIE {args.year}  ·  ages under 65, all incomes")


if __name__ == "__main__":
    main()
