# Reading the Margin — Maryland Census-Tract Child Poverty

A standalone, single-page explainer on how Maryland measures child poverty at the
census-tract level: **point estimates, margins of error, and year-over-year change**
for ACS 5-Year vintages **2022, 2023, 2024**.

Built as a plain-language response to a recurring question from local partners —
*"How can a tract's child poverty rate go from 43% to 10% in one year if it's 5-year
data?"* The answer is the margin of error, and the site makes it visible.

## What it does

- **Map** — every Maryland tract, toggleable by year (2022/2023/2024) and by measure
  (poverty rate · margin of error · year-over-year change).
- **Distributions** — per-year histograms of rates, margins of error, and changes,
  showing that the typical margin of error is nearly as large as the typical estimate.
- **Tract search** — look up any tract by number, GEOID, or place name; get the
  three-year estimate with its confidence range and a plain-language read of whether
  any change is statistically real.
- **Shareable URLs** — `?tract=GEOID` deep-links to a specific tract's breakdown.
- **Methodology** — how the ACS 5-year estimate is constructed and why ranges, not
  point estimates, are the honest unit of comparison.

## Build

```bash
uv run --with shapely python build.py
```

Reads `source_data/` (three ACS-year tract CSVs + tract names + tract geometry) and
emits `docs/data/{tracts,geometry,stats}.json`. The site (`docs/index.html`) is a
single static file — no build step for the frontend.

## Data

U.S. Census Bureau, American Community Survey 5-Year Estimates — child poverty
(related children under 18 below poverty) by census tract — as compiled by the
Maryland Department of Planning. Margins of error are the Bureau's published 90%
values. Tract names/descriptions are GOC-maintained. Public/aggregate data only;
no individual-level or PII data.

Deployed via GitHub Pages from `docs/`.
