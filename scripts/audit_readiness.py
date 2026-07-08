#!/usr/bin/env python3
import csv
import sys
from collections import Counter
from pathlib import Path


DATA_FILES = [
    "places.csv",
    "beaches.csv",
    "restaurants.csv",
    "bike_routes.csv",
    "hikes.csv",
]

STATUS_ORDER = [
    "verified",
    "official_partial_verification",
    "seed_needs_official_verification",
    "draft",
    "concept",
]


def build_audit(root):
    root = Path(root)
    database_dir = root / "database"
    by_file = {}
    status_counts = Counter()
    mapped_records = 0
    total_records = 0

    for filename in DATA_FILES:
        path = database_dir / filename
        rows = read_rows(path)
        file_status_counts = Counter(row.get("status", "") or "missing_status" for row in rows)
        by_file[filename] = {
            "total": len(rows),
            "status_counts": file_status_counts,
            "mapped": count_mapped_rows(rows),
        }
        total_records += len(rows)
        status_counts.update(file_status_counts)
        mapped_records += by_file[filename]["mapped"]

    return {
        "total_records": total_records,
        "status_counts": status_counts,
        "mapped_records": mapped_records,
        "by_file": by_file,
    }


def read_rows(path):
    if not path.is_file():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def count_mapped_rows(rows):
    return sum(1 for row in rows if row.get("latitude", "").strip() and row.get("longitude", "").strip())


def export_audit(root):
    root = Path(root)
    audit = build_audit(root)
    output_path = root / "output" / "readiness_audit.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_audit(audit), encoding="utf-8")
    return output_path


def render_audit(audit):
    lines = [
        "# Readiness Audit",
        "",
        "Generated from source CSV data. This report is reproducible and is not committed when written to `output/`.",
        "",
        "## Summary",
        "",
        f"- Total structured records: {audit['total_records']}",
        f"- Mapped records with latitude/longitude: {audit['mapped_records']}",
        "",
        "## Status Counts",
        "",
        "| Status | Records |",
        "| --- | ---: |",
    ]

    for status in ordered_statuses(audit["status_counts"]):
        lines.append(f"| {status} | {audit['status_counts'][status]} |")

    lines.extend(
        [
            "",
            "## Files",
            "",
            "| File | Records | Mapped | Verified | Partial | Seed |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )

    for filename in DATA_FILES:
        file_audit = audit["by_file"][filename]
        counts = file_audit["status_counts"]
        lines.append(
            "| {filename} | {total} | {mapped} | {verified} | {partial} | {seed} |".format(
                filename=filename,
                total=file_audit["total"],
                mapped=file_audit["mapped"],
                verified=counts["verified"],
                partial=counts["official_partial_verification"],
                seed=counts["seed_needs_official_verification"],
            )
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `verified`: ready to use as a factual record, subject to normal date-sensitive rechecks before publication.",
            "- `official_partial_verification`: supported by at least one official or primary source but still missing publication details.",
            "- `seed_needs_official_verification`: useful research lead, not a final recommendation.",
            "",
        ]
    )
    return "\n".join(lines)


def ordered_statuses(status_counts):
    known = [status for status in STATUS_ORDER if status_counts[status]]
    unknown = sorted(status for status in status_counts if status not in STATUS_ORDER)
    return known + unknown


def main(argv=None):
    argv = argv or sys.argv[1:]
    root = Path(argv[0]) if argv else Path.cwd()
    output_path = export_audit(root)
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
