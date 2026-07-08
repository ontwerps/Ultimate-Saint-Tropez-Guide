# Architecture

Repository Layout

- chapters/
- database/
- assets/
- templates/
- scripts/
- output/

Markdown is the canonical content format.
Structured data belongs in CSV/SQLite.

## Current Data Flow

1. Write narrative content in `chapters/`.
2. Store reusable facts in `database/`.
3. Use `templates/` for repeated entry types.
4. Add media and route files to `assets/`.
5. Generate future PDF, EPUB, website and mobile outputs into `output/`.
