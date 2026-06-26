#!/usr/bin/env python3
"""Build the child-poverty tract dataset + simplified geometry for the site.

Inputs (source_data/):
  acs_2022.csv, acs_2023.csv  -- MD Planning tract extracts; estimate in
                                 CHILD_POV_PCT, margin of error in NOTES "(+/-) X.X"
  acs_2024.csv                -- adds clean MOE / upper-bound columns
  tract_meta.json             -- GEOID -> {name, description, grantee_name}
  tract_geometry.geojson      -- tract polygons (props incl. county_name)

ACS 5-year vintage mapping (the source files are named by GOC fiscal year):
  acs_2022.csv = ACS 2018-2022   -> displayed as "2022"
  acs_2023.csv = ACS 2019-2023   -> displayed as "2023"
  acs_2024.csv = ACS 2020-2024   -> displayed as "2024"

Outputs (docs/data/):
  tracts.json       -- per-tract: name, description, county, child pop, and for
                       each year {est, moe, lo, hi}, plus YoY change fields
  geometry.json     -- {GEOID: [[lng,lat],...] rings} simplified, low precision
"""
import csv
import json
import re
from pathlib import Path

from shapely.geometry import shape, mapping

SRC = Path("source_data")
OUT = Path("docs/data")
OUT.mkdir(parents=True, exist_ok=True)

YEARS = ["2022", "2023", "2024"]
FILES = {"2022": "acs_2022.csv", "2023": "acs_2023.csv", "2024": "acs_2024.csv"}

MOE_RE = re.compile(r"\(\+/-\)\s*([\d.]+)")


def fnum(s):
    s = (s or "").strip()
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def parse_year(path):
    """Return {geoid: {est, moe, child_pop}} for one ACS year file."""
    rows = {}
    for r in csv.DictReader(open(SRC / path)):
        geoid = r["GEOID20"].strip()
        est = fnum(r.get("CHILD_POV_PCT"))
        # MOE: clean column when present (2024 file), else parse NOTES "(+/-) X.X"
        moe = fnum(r.get("F2024_Child_Poverty_Rate_Margin_Of_Error"))
        if moe is None:
            m = MOE_RE.search(r.get("NOTES", "") or "")
            moe = float(m.group(1)) if m else None
        rows[geoid] = {
            "est": est,
            "moe": moe,
            "child_pop": int(fnum(r.get("CHILD_POPULATION_TOTAL")) or 0),
        }
    return rows


def main():
    meta = json.load(open(SRC / "tract_meta.json"))
    year_data = {y: parse_year(FILES[y]) for y in YEARS}

    # county per geoid from geometry props
    geo = json.load(open(SRC / "tract_geometry.geojson"))
    county = {}
    for f in geo["features"]:
        p = f["properties"]
        county[p["GEOID20"]] = p.get("county_name", "")

    geoids = sorted(set().union(*[set(d) for d in year_data.values()]))

    tracts = {}
    for g in geoids:
        m = meta.get(g, {})
        rec = {
            "geoid": g,
            "name": m.get("name", f"Census Tract {g}"),
            "desc": m.get("description", ""),
            "county": county.get(g, ""),
            "years": {},
        }
        for y in YEARS:
            d = year_data[y].get(g, {})
            est, moe = d.get("est"), d.get("moe")
            yr = {"est": est, "moe": moe, "pop": d.get("child_pop", 0)}
            if est is not None and moe is not None:
                yr["lo"] = round(max(0.0, est - moe), 1)
                yr["hi"] = round(est + moe, 1)
            rec["years"][y] = yr
        # year-over-year change in point estimate
        chg = {}
        for a, b in [("2022", "2023"), ("2023", "2024")]:
            ea = rec["years"][a]["est"]
            eb = rec["years"][b]["est"]
            chg[f"{a}_{b}"] = round(eb - ea, 1) if (ea is not None and eb is not None) else None
        rec["change"] = chg
        tracts[g] = rec

    json.dump(tracts, open(OUT / "tracts.json", "w"), separators=(",", ":"))

    # ---- geometry: simplify + round, keep only rings ----
    geom = {}
    for f in geo["features"]:
        g = f["properties"]["GEOID20"]
        try:
            shp = shape(f["geometry"]).simplify(0.0008, preserve_topology=True)
        except Exception:
            shp = shape(f["geometry"])
        mp = mapping(shp)
        coords = mp["coordinates"]

        def rnd(seq):
            out = []
            for ring in seq:
                out.append([[round(x, 4), round(y, 4)] for x, y in ring])
            return out

        if mp["type"] == "Polygon":
            geom[g] = {"t": "P", "c": rnd(coords)}
        else:  # MultiPolygon
            geom[g] = {"t": "M", "c": [rnd(poly) for poly in coords]}
    json.dump(geom, open(OUT / "geometry.json", "w"), separators=(",", ":"))

    # ---- summary stats per year for the distribution charts / headline ----
    stats = {}
    for y in YEARS:
        ests = [r["years"][y]["est"] for r in tracts.values() if r["years"][y]["est"] is not None]
        moes = [r["years"][y]["moe"] for r in tracts.values() if r["years"][y]["moe"] is not None]
        stats[y] = {
            "n": len(ests),
            "median_est": round(sorted(ests)[len(ests) // 2], 1),
            "median_moe": round(sorted(moes)[len(moes) // 2], 1),
            "over30": sum(1 for e in ests if e > 30),
        }
    json.dump(stats, open(OUT / "stats.json", "w"), separators=(",", ":"))

    sz = lambda p: f"{(OUT / p).stat().st_size/1024:.0f} KB"
    print(f"tracts.json   {len(tracts)} tracts  {sz('tracts.json')}")
    print(f"geometry.json {len(geom)} shapes  {sz('geometry.json')}")
    print(f"stats.json    {sz('stats.json')}")
    print("stats:", json.dumps(stats))


if __name__ == "__main__":
    main()
