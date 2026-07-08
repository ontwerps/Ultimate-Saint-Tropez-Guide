# Repository Structure Design

## Goal

Create the first usable structure for the Ultimate Gulf of Saint-Tropez Guide so content can be written in Markdown, facts can be tracked in structured data, and future outputs can be generated from one source of truth.

## Scope

This first release creates the repository skeleton, starter chapter files, operational templates, CSV data headers, and internal documentation updates. It does not perform external destination research or publish factual recommendations that have not been verified.

## Architecture

Markdown chapters live in `chapters/`. Structured facts live in `database/` as CSV files. Reusable entry formats live in `templates/`. Media and route files live in `assets/`. Export automation will live in `scripts/`, and generated files will live in `output/`.

## Content Rules

All chapter text is written in professional Dutch. Facts and personal recommendations are separated. Starter content uses concept sections and research notes where details still need verification.

## Verification

The first verification pass checks that the expected directories and Markdown/CSV files exist and that all Markdown files are discoverable.

