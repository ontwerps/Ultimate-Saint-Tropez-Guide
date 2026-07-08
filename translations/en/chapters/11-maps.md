---
title: Maps
chapter: 12
status: draft
---

# Maps

## Summary

This chapter defines map layers for the guide: villages, beaches, restaurants, hiking routes, cycling routes, parking, viewpoints and practical stops.

## Google Maps Atlas

Generate the first atlas with:

```bash
python3 scripts/export_google_maps.py
```

The export writes `output/google_maps_atlas.csv`. Generated output stays out of Git; source data remains in `database/*.csv`.

## Current Rules

- Places, beaches and restaurants with latitude and longitude are exported as points.
- Records without coordinates are skipped until they are reliably geocoded.
- GPX routes remain separate files under `assets/gpx/`.
- Each atlas row keeps source reference, research status, category, municipality and stable Atlas ID.

## Next Improvements

Add more coordinates, choose colours and icons per layer, test Google My Maps import and mobile readability, and decide later whether GPX routes become KML or GeoJSON.

## Guide Use

The map is currently an orientation atlas. Use coordinates as a reliable start for import, but treat GPX routes as navigable only after official or local geometry checks.

## Final Map Layers

Places should show villages, viewpoints, heritage and wineries. Beaches should be grouped by comfort, nature, Saint-Tropez combination, shuttle access and unsupervised status. Restaurants should show moment and budget, not just category. Hiking and cycling routes should remain separate until geometry is reliable.

## Mobile Use

The mobile map should answer three questions quickly: what is near my base, what fits this time of day, and which places require booking, parking or safety checks?
