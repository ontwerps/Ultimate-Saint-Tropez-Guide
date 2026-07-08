# Editorial Rankings and Images Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add first-view winner guidance, Top 10 recommendations, editorial ratings, price bands, review-style notes and chapter hero images to the multilingual guide.

**Architecture:** Keep ratings and rankings in `scripts/build_site.py` as structured editorial constants for this pass, because the static builder already owns multilingual rendering. Store local chapter hero image assets under `assets/images/chapters/` and copy them into `_site/assets/images/chapters/` during builds. Render the winner and Top 10 on each language index, and render a hero image at the top of every chapter.

**Tech Stack:** Python standard library static generator, Markdown chapters, SVG image assets, `unittest`.

---

### Task 1: Add failing builder tests

- [x] Extend `tests/test_build_site.py` to assert the index includes a first-view winner, Top 10, star rating, price band and review text.
- [x] Assert chapter pages include an image tag and copied chapter asset.

### Task 2: Add local chapter images

- [x] Create `assets/images/chapters/*.svg` for all 13 chapters.
- [x] Use lightweight scenic illustrations with accessible alt text provided by the builder.

### Task 3: Render rankings and images

- [x] Add editorial recommendation data to `scripts/build_site.py`.
- [x] Render first-view winner and Top 10 cards on language indexes.
- [x] Render chapter hero images and copy assets to `_site/`.
- [x] Keep labels multilingual.

### Task 4: Document, verify, deploy

- [x] Update changelog.
- [x] Run all tests and build scripts.
- [x] Commit, push and verify GitHub Pages.
