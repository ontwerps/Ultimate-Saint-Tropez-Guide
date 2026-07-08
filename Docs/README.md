# Ultimate Gulf of Saint-Tropez Guide

This repository contains the source for a premium travel handbook covering the Gulf of Saint-Tropez.

## Goals

- Single source of truth
- Markdown-first
- PDF, EPUB and Website generation
- Annual updates
- AI-assisted authoring

## Repository Structure

- `chapters/`: canonical handbook chapters.
- `database/`: structured CSV data for places, beaches, restaurants, routes, hikes and sources.
- `templates/`: reusable operational content templates.
- `assets/`: images, maps, GPX files and other media.
- `scripts/`: future generation and validation automation.
- `output/`: generated exports.

## Validation

Run this before committing content changes:

```bash
python3 scripts/validate_project.py
```

The validator checks required folders, CSV headers, duplicate CSV IDs, unknown source references, allowed research statuses, cycling route categories, local bike-route GPX file references and chapter front matter.

See PROJECT.md first.
