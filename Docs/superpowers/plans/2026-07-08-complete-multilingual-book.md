# Complete Multilingual Book Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Finish the visible draft gaps in the guide and publish Dutch, English and French versions on GitHub Pages, with Dutch as the default.

**Architecture:** Dutch source chapters remain canonical in `chapters/`. English and French translated chapter sources live under `translations/<lang>/chapters/`. `scripts/build_site.py` builds three static sites into `_site/`, with Dutch at the root and translated versions under `_site/en/` and `_site/fr/`.

**Tech Stack:** Python standard library static generator, Markdown source files, `unittest`, GitHub Pages workflow already in `.github/workflows/pages.yml`.

---

### Task 1: Finish Dutch Chapter Copy

**Files:**
- Modify: `chapters/*.md`

- [ ] Replace visible drafting placeholders such as "Nog te controleren", "Nog niet beoordeeld" and "Te koppelen" with reader-facing guidance.
- [ ] Keep unresolved facts as explicit verification notes rather than final claims.
- [ ] Keep factual statements grounded in existing chapter/database source status.

### Task 2: Add Translated Chapter Sources

**Files:**
- Create: `translations/en/chapters/*.md`
- Create: `translations/fr/chapters/*.md`
- Create: `translations/README.md`

- [ ] Translate all chapter titles and body copy into English and French.
- [ ] Preserve front matter fields `title`, `chapter` and `status`.
- [ ] Preserve verification caveats and source-status language in each language.

### Task 3: Upgrade Static Site Builder

**Files:**
- Modify: `scripts/build_site.py`
- Modify: `tests/test_build_site.py`

- [ ] Write tests proving the builder emits Dutch root pages plus `/en/` and `/fr/` pages.
- [ ] Add language configuration, language-aware paths and a language switcher.
- [ ] Render index/chapter navigation correctly for root and subdirectory languages.

### Task 4: Document and Verify

**Files:**
- Modify: `Docs/README.md`
- Modify: `Docs/FINAL_CHECK.md`
- Modify: `Docs/CHANGELOG.md`
- Modify: `scripts/README.md`

- [ ] Document multilingual output.
- [ ] Run `python3 -m unittest discover tests`.
- [ ] Run `python3 scripts/validate_project.py`.
- [ ] Run `python3 scripts/export_google_maps.py`.
- [ ] Run `python3 scripts/audit_readiness.py`.
- [ ] Run `python3 scripts/build_site.py`.
- [ ] Commit, push and trigger the Pages workflow.
