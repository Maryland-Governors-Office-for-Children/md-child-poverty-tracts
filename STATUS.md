# Reading the Margin — Status & Open Steps

_Last reviewed: 2026-11-10._ Living index of what's done, open, and needs a decision.
See `CLAUDE.md` for context and `README.md` for build/run steps.

## Done

- Scaffolded standalone repo `~/projects/md-child-poverty-tracts/`, copied only the
  select inputs needed (3 ACS-year tract CSVs, tract names, tract geometry).
- `build.py` → `docs/data/{tracts,geometry,stats}.json` (1,463 tracts; geometry
  simplified to ~945 KB).
- `docs/index.html` single-page site: year+metric map, per-year distributions, tract
  search, shareable `?tract=GEOID` URLs.
- Playwright-tested: 1,463 map polygons, toggles, search, deep-link, no console errors.
- **Generalized** title → "Maryland Census Tract Child Poverty Rate Overview"; removed the
  request-specific framing.
- **Case-study section removed**; the map leads as a general resource (commit `fbb2b91`).
- **Methodology section (04) removed** from the site (commit `d1b61cd`).
- **County dropdown** snap-zooms the map to a county (flyToBounds) and dims out-of-county
  tracts; syncs when a tract is searched.
- **LLM-council visual pass** applied:
  - inline range-bar key (dot = estimate, hatched band = margin of error, green = 30% line);
  - the 30% threshold explained inline;
  - "%" and better contrast on dark labels;
  - above-30% band shading and a legend threshold marker;
  - mobile stacking.
- **README rewritten** to lead with artifacts and sources of truth (commit `3e5c465`).
- **Replied to the original requester** with a deep link to the site (2026-06-26).
- **Census memo review — closed out 2026-11-10.** Used this repo's tract data to review and
  redraft internal GOC memos on federal Census changes (Sept 29 – Oct 7), then handed off.
  - The memo work is now owned by its GOC authors; this repo has no further action on it.
  - **Working files** are in `memo-review/`, which is **gitignored and local only**: drafts,
    fact-check files, council transcripts, and the step log (`memo-review/STEPS.md`, which
    records the hand-off).
  - **Tooling.** Reusable scripts for building and checking Google Docs tabs are in
    `memo-review/_tools/` (`docbuild.py`, `docverify.py`, `stylev3.py`, `export.py`).
  - **Analysis.** Margins of error by ACS vintage (`memo-review/analysis.md`), and ACS sample
    size by state, county, and tract from the Census API (`memo-review/acs_sampling.md`).
    The latter now documents how the per-tract "about 40 households with children, roughly
    9 a year" figure is derived (B00002 × B11005).

## Live
- **Site:** https://maryland-governors-office-for-children.github.io/md-child-poverty-tracts/
- **Repo:** `Maryland-Governors-Office-for-Children/md-child-poverty-tracts`. It is
  **public**, because Pages is not available for private repos on this org's plan. The data
  is public, aggregate ACS with no PII, so public is safe. Pages serves `/docs` from `main`.

## Open (needs Nick / external)
- [ ] Optional: confirm the displayed year labels (2022/2023/2024) are how leadership wants
  the ACS vintages named publicly.
- [ ] Optional: add the per-vintage margin-of-error table (FY2024–FY2026) to the site. The
  analysis is in `memo-review/analysis.md`.

## Notes
- Public/aggregate data only in tracked files — safe to push. No PII.
- **Never commit `memo-review/`.** It holds internal, pre-decisional drafts. Before any
  push, check with `git add -A --dry-run`.
- **This repo is public, so keep tracked files generic.** No colleague names, internal doc
  or draft IDs, or memo content in `STATUS.md`. Those go in `memo-review/STEPS.md`.
- Parent project: `~/projects/enough-eligibility-analysis` (source of the data).
