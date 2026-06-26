# Maryland Census Tract Child Poverty Rate Overview

A single static page that maps every Maryland census tract's child poverty rate for the
last three ACS vintages — and, more to the point, shows the **margin of error** around
each number. The whole reason this exists: tract-level poverty figures are survey
*estimates*, the samples are small, and the margins are big. A tract can read 43% one year
and 10% the next without anything real changing. The page makes that legible instead of
alarming.

**Live:** https://maryland-governors-office-for-children.github.io/md-child-poverty-tracts/

## Artifacts & sources of truth

Two things are authoritative here. Everything else is derived from them.

- **The poverty numbers — source of truth is the Census Bureau.** Every estimate, margin
  of error, and child-population count comes from the **ACS 5-Year Estimates**, as
  compiled for Maryland by the **Department of Planning**. We don't calculate, adjust, or
  smooth anything — we publish the Bureau's number for every tract, consistently, statewide.
  That's the protocol, and it's what keeps the map defensible across all 1,463 tracts.
- **Eligibility — source of truth is the ENOUGH Eligibility Map.** This site is *not* the
  eligibility authority. It reports poverty and uncertainty; the 30% line is shown for
  context. If the question is "is this tract eligible," the
  [ENOUGH Eligibility Map](https://experience.arcgis.com/experience/74b0e6f0107d4e8fab2f192625d915f9/)
  is the answer.

Here's what's in the repo and how each piece operates:

| Artifact | What it is | Source of truth? |
|---|---|---|
| `source_data/acs_2022.csv` `_2023` `_2024` | Raw tract extracts — one per ACS vintage. Estimate, child population, and MoE per tract. | ⬅ from Census/MD Planning |
| `source_data/tract_meta.json` | GEOID → plain-English tract name + community description. | GOC-maintained |
| `source_data/tract_geometry.geojson` | Tract polygons. | from MD Planning |
| `build.py` | The only moving part. Joins the three years + names + geometry, computes the confidence ranges and year-over-year change, simplifies the geometry. | — (transform) |
| `docs/data/{tracts,geometry,stats}.json` | What `build.py` emits. **Generated — never hand-edit.** | — (derived) |
| `docs/index.html` | The entire site. One file: Leaflet map, Plotly distributions, tract search, methodology. No framework, no build step. | — (presentation) |

## How the number is made (the part people get wrong)

- **"5-year" means pooled, not current.** The 2024 estimate blends survey responses from
  2020–2024. Pooling five years is the only way to get a tract-level sample big enough to
  report at all — but it's a rolling average, not a snapshot of this year.
- **Small places, small samples.** Each year the window drops its oldest year and adds a
  new one, so *which* households land in the sample shifts — and the estimate shifts with
  it. That's the year-over-year "swing," and it's usually noise.
- **The margin of error is part of the measurement.** A rate of 43.2% with a ±24.4 margin
  means: we're 90% confident the true rate is somewhere between 19% and 68%. When two
  years' ranges overlap, the change between their point estimates **isn't statistically
  meaningful.** Compare ranges, not points — that's the whole job of the range bars on the
  page.

### Year mapping — the one gotcha

The source files are named by GOC fiscal year, not by ACS vintage. Don't trust the filename:

| File | ACS vintage | Shown on site as |
|---|---|---|
| `acs_2022.csv` | ACS 2018–2022 | **2022** |
| `acs_2023.csv` | ACS 2019–2023 | **2023** |
| `acs_2024.csv` | ACS 2020–2024 | **2024** |

(Verified: each file's `CHILD_POV_PCT` equals the next file's prior-year column.) In the
2022/2023 files the MoE lives in the `NOTES` column as `(+/-) X.X`; the 2024 file has a
clean MoE column. `(+/-) **` means suppressed — too few children to report — and is treated
as "no published estimate."

## Build

```bash
uv run --with shapely python build.py
```

Reads `source_data/`, writes `docs/data/*.json`. The frontend has no build step — open
`docs/index.html` or push and GitHub Pages serves it from `docs/`.

## A note on access

Public, aggregate Census data only — no PII, nothing youth-level. The repo is **public**
because GitHub Pages won't serve a private repo on the org's plan, and the data is safe to
have public regardless.
