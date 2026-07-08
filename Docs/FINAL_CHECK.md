# Final Check

This document separates completed desk-research work from publication work that still needs current official confirmation, local inspection or editorial judgement.

## Run Before Every Commit

```bash
python3 -m unittest discover tests
python3 scripts/validate_project.py
python3 scripts/export_google_maps.py
python3 scripts/audit_readiness.py
python3 scripts/build_site.py
```

## Current Readiness Snapshot

Latest generated audit:

- Total structured records: 58
- Mapped records with latitude/longitude: 5
- `official_partial_verification`: 38
- `seed_needs_official_verification`: 20
- `verified`: 0

The project is structurally complete for the first baseline. It is not publication-final until records graduate from seed/partial status to `verified`.

The generated GitHub Pages preview is suitable for reviewing the book structure and draft text in Dutch, English and French. It must carry the readiness caveat until publication verification is complete.

## Publication Verification

- [ ] Confirm official route geometry for all cycling GPX records.
- [ ] Confirm hiking route geometry, closures, erosion risk, water points and safety notes.
- [ ] Confirm beach water quality from official bathing-water data close to publication.
- [ ] Confirm beach parking tariffs, lifeguard dates, toilets, showers and dog rules for the target season.
- [ ] Confirm restaurant opening hours, menus, prices, reservation rules and closures.
- [ ] Confirm wine tasting hours, pricing, reservation rules and vendanges restrictions.
- [ ] Confirm village and Port Grimaud parking rules, market/event timing and access restrictions.
- [ ] Add more latitude/longitude fields for atlas coverage.
- [ ] Convert verified GPX route layers to a Google Maps-compatible route format if needed.
- [ ] Add local/personal scoring only after a real visit or trusted local review.

## Status Rules

- `seed_needs_official_verification`: research lead only; do not publish as a recommendation.
- `official_partial_verification`: factual base exists; missing details must be checked before publication.
- `verified`: current source and practical details have been checked and the record is safe to use.

## Final Editorial Gate

Before exporting a publishable PDF, website or mobile version:

- No record used in a recommendation may remain `seed_needs_official_verification`.
- Every recommended route must have usable geometry or a clear non-navigation caveat.
- Every recommendation must separate facts from personal judgement.
- Every date-sensitive claim must have an access date and a target season.
- English and French translations must match the Dutch chapter set.
- Generated outputs must come from source files, not manual edits in `output/`.
