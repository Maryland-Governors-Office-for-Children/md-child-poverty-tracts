# Reading the Margin — Status & Open Steps

_Last reviewed: 2026-06-26._ Living index of what's done, open, and needs a decision.
See `CLAUDE.md` for context and `README.md` for build/run steps.

## Done
- Scaffolded standalone repo `~/projects/md-child-poverty-tracts/`, copied only the
  select inputs needed (3 ACS-year tract CSVs, tract names, tract geometry).
- `build.py` → `docs/data/{tracts,geometry,stats}.json` (1,463 tracts; geometry
  simplified to ~945 KB).
- `docs/index.html` single-page site: case-study (Wilde Lake), year+metric map,
  per-year distributions, tract search, shareable `?tract=GEOID` URLs, methodology
  narrative answering the Eisenreich thread.
- Playwright-tested: 1,463 map polygons, toggles, search, deep-link, no console errors.

## Live
- **Site:** https://maryland-governors-office-for-children.github.io/md-child-poverty-tracts/
- Repo `Maryland-Governors-Office-for-Children/md-child-poverty-tracts` — **public**
  (Pages is not available for private repos on this org's plan; data is public/aggregate
  ACS with no PII, so public is safe). Pages serves `/docs` from `main`.

## Open (needs Nick / external)
- [ ] Decide whether to **reply to Kim** with the live link (the site is
  written to be that reply), and whether to loop in Christina/Ojeda.
- [ ] Optional: confirm the displayed year labels (2022/2023/2024) are how leadership
  wants the ACS vintages named publicly.

## Notes
- Public/aggregate data only — safe to push. No PII.
- Parent project: `~/projects/enough-eligibility-analysis` (source of the data).
