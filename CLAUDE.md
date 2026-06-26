# CLAUDE.md — Reading the Margin (MD Census-Tract Child Poverty)

## What This Project Is

A standalone GitHub Pages explainer on how Maryland measures **census-tract child
poverty** — estimates, margins of error, and year-over-year change for ACS 5-Year
vintages 2022, 2023, 2024. Created as a public-facing response to the "Census Track
Data" email thread with Kimberly Eisenreich (Howard County LCB), who flagged that
Wilde Lake tract 6054.03 read ~43% then ~10% in consecutive years and asked how
5-year data could swing that much. The answer — sampling noise within a large margin
of error — is the spine of the whole site.

Deliberately scoped narrower than the parent `enough-eligibility-analysis` project:
**only** poverty estimate / MOE / YoY change. No eligibility logic, no schools, no
grantees.

## Repo Structure

```
source_data/      Select inputs copied from enough-eligibility-analysis:
                    acs_2022.csv  (= tracts_2024.csv, ACS 2018-2022)
                    acs_2023.csv  (= tracts_2025.csv, ACS 2019-2023)
                    acs_2024.csv  (= tracts_2026.csv, ACS 2020-2024)
                    tract_meta.json       (GEOID -> name/description/grantee)
                    tract_geometry.geojson
build.py          Combines years -> docs/data/{tracts,geometry,stats}.json
docs/             GitHub Pages site
  index.html      The entire single-page app (Leaflet + Plotly, no framework)
  data/*.json     Generated
```

## Key Facts / Gotchas

- **Year mapping:** the GOC source files are named by fiscal year. `tracts_2024.csv`
  is the ACS **2022** 5-year estimate, `_2025` = **2023**, `_2026` = **2024**.
  Verified: file N's `CHILD_POV_PCT` == file N+1's `F2023_...` column.
- **MOE source:** in the 2022/2023 files the margin of error lives in the `NOTES`
  column as `(+/-) X.X`; the 2024 file has a clean
  `F2024_Child_Poverty_Rate_Margin_Of_Error` column. `(+/-) **` = suppressed
  (tiny/zero child population) → treated as no published estimate.
- **Headline finding:** median tract MOE (~9.7) ≈ median tract estimate (~7) — tract
  estimates are inherently imprecise. This is the statewide version of the Wilde Lake
  point.
- **Confidence-interval overlap** drives the "is this change real?" interpretation in
  the breakdown card.

## Build

```bash
uv run --with shapely python build.py
```

## Status

Built 2026-06-26. Site complete and tested (Playwright: map 1,463 polygons, toggles,
search, deep-link share URLs, no console errors). Pending: GitHub repo + Pages deploy.
