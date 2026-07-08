# Chapter Ranking Tables Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add sorted rating and price tables to the practical guide chapters so readers immediately see the best choices per category.

**Architecture:** Keep the chapter ranking data as structured editorial constants in `scripts/build_site.py`, then render it through one reusable table function for every language. Each table defaults to rating high-to-low and includes a lightweight client-side sort menu for rating, price and name.

**Tech Stack:** Python standard library static generator, inline HTML/CSS/JavaScript, `unittest`.

---

### Task 1: Add failing coverage

- [x] Extend `tests/test_build_site.py` with beach and restaurant fixture chapters.
- [x] Assert chapter pages include a ranking table, sort menu, stars, prices, guide review text and default top-down ordering.

### Task 2: Render reusable chapter ranking tables

- [x] Add multilingual labels for chapter ranking sections.
- [x] Add structured editorial ranking data for beaches, restaurants, wine, cycling, walking, villages/cities and hidden gems.
- [x] Render the ranking table above the chapter body whenever a chapter has ranking data.
- [x] Add table CSS and a small sorting script.

### Task 3: Verify and publish

- [x] Run focused and full tests plus validation/build scripts.
- [x] Inspect generated live-target HTML for all ranked chapters.
- [ ] Commit, push and verify GitHub Pages deploy.
