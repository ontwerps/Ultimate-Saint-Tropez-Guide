# Scripts

Automation scripts will live here once generation starts.

## Available Scripts

- `validate_project.py`: validates required folders, CSV headers, duplicate CSV IDs, source references, research statuses, cycling route categories, local bike-route GPX file references, chapter front matter and translation parity.
- `export_google_maps.py`: generates `output/google_maps_atlas.csv` from geocoded places, beaches and restaurants.
- `audit_readiness.py`: generates `output/readiness_audit.md` with status counts, mapped-record counts and per-file readiness totals.
- `build_site.py`: generates `_site/`, a static GitHub Pages-ready HTML preview with Dutch at the root, English under `/en/` and French under `/fr/`.

## Likely Future Scripts

- Generate PDF and EPUB outputs.
- Build map data from CSV and GPX sources.
