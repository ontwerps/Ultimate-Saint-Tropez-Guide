# Repository Structure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first usable repository structure for the Ultimate Gulf of Saint-Tropez Guide.

**Architecture:** Use Markdown for canonical chapter content, CSV for structured factual data, templates for repeated entry formats, and dedicated folders for assets, scripts, and generated output. Keep factual claims conservative until source research is performed.

**Tech Stack:** Markdown, CSV, shell-based file verification.

---

### Task 1: Create Project Skeleton

**Files:**
- Create: `chapters/README.md`
- Create: `database/README.md`
- Create: `assets/README.md`
- Create: `templates/README.md`
- Create: `scripts/README.md`
- Create: `output/README.md`

- [x] **Step 1: Create the top-level content directories**

Run: `mkdir -p chapters database assets templates scripts output`

Expected: command exits with status 0.

- [x] **Step 2: Add README files that define each directory's role**

Each README explains what belongs in the directory and how it supports the Markdown-first handbook.

### Task 2: Add Starter Chapters

**Files:**
- Create: `chapters/00-preparation.md`
- Create: `chapters/01-prairies-de-la-mer.md`
- Create: `chapters/02-port-grimaud.md`
- Create: `chapters/03-saint-tropez.md`
- Create: `chapters/04-villages.md`
- Create: `chapters/05-beaches.md`
- Create: `chapters/06-hiking.md`
- Create: `chapters/07-cycling.md`
- Create: `chapters/08-restaurants.md`
- Create: `chapters/09-wine.md`
- Create: `chapters/10-hidden-gems.md`
- Create: `chapters/11-maps.md`
- Create: `chapters/12-concierge.md`

- [x] **Step 1: Create one Markdown file per major chapter**

Expected: each chapter has YAML front matter, a Dutch title, `status: concept`, and sections that separate factual research from personal recommendations.

### Task 3: Add Structured Data Scaffolds

**Files:**
- Create: `database/places.csv`
- Create: `database/beaches.csv`
- Create: `database/restaurants.csv`
- Create: `database/bike_routes.csv`
- Create: `database/hikes.csv`
- Create: `database/sources.csv`

- [x] **Step 1: Add CSV files with stable headers**

Expected: each CSV file has a header row and no invented destination data.

### Task 4: Add Operational Templates

**Files:**
- Create: `templates/location.md`
- Create: `templates/restaurant.md`
- Create: `templates/beach.md`
- Create: `templates/hike.md`
- Create: `templates/bike-route.md`

- [x] **Step 1: Add Dutch Markdown templates**

Expected: templates match the project content guide and include route categories for cycling.

### Task 5: Verify Structure

**Files:**
- Inspect all created files.

- [x] **Step 1: List Markdown files**

Run: `rg --files -g '*.md' -g '*.MD'`

Expected: command lists project docs, chapter files, templates, and internal plan/spec files.

- [x] **Step 2: List CSV files**

Run: `rg --files -g '*.csv'`

Expected: command lists the six database CSV files.

### Task 6: Initialize Version Control

**Files:**
- Create: `.gitignore`
- Initialize: `.git/`

- [x] **Step 1: Initialize Git**

Run: `git init`

Expected: repository is initialized in the project directory.

- [x] **Step 2: Rename the default branch**

Run: `git branch -m main`

Expected: `git branch --show-current` prints `main`.

- [x] **Step 3: Ignore local and generated files**

Expected: `.DS_Store` and generated exports under `output/` are ignored, while `output/README.md` remains tracked.
