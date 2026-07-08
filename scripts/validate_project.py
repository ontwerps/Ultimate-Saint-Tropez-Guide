#!/usr/bin/env python3
import csv
import sys
from pathlib import Path


REQUIRED_DIRECTORIES = [
    "chapters",
    "database",
    "assets",
    "templates",
    "scripts",
    "output",
    "translations",
]

EXPECTED_CSV_HEADERS = {
    "places.csv": [
        "id",
        "name",
        "category",
        "municipality",
        "latitude",
        "longitude",
        "summary",
        "parking_notes",
        "best_time",
        "source",
        "status",
    ],
    "beaches.csv": [
        "id",
        "name",
        "municipality",
        "latitude",
        "longitude",
        "summary",
        "parking",
        "water_quality",
        "snorkeling",
        "facilities",
        "best_time",
        "costs",
        "source",
        "status",
    ],
    "restaurants.csv": [
        "id",
        "name",
        "municipality",
        "latitude",
        "longitude",
        "category",
        "price_level",
        "recommended_dishes",
        "wine_notes",
        "parking",
        "cycling_access",
        "reservation_notes",
        "source",
        "status",
    ],
    "bike_routes.csv": [
        "id",
        "name",
        "type",
        "distance_km",
        "elevation_m",
        "surface",
        "start",
        "finish",
        "gpx_file",
        "coffee_stops",
        "water_points",
        "traffic_notes",
        "source",
        "status",
    ],
    "hikes.csv": [
        "id",
        "name",
        "distance_km",
        "elevation_m",
        "difficulty",
        "best_season",
        "start",
        "finish",
        "parking",
        "water",
        "gpx_file",
        "source",
        "status",
    ],
    "sources.csv": [
        "id",
        "title",
        "publisher",
        "url",
        "accessed_at",
        "notes",
    ],
}

VALID_BIKE_TYPES = {"Trekking", "Race", "Gravel", "E-bike"}
VALID_RESEARCH_STATUSES = {
    "seed_needs_official_verification",
    "official_partial_verification",
    "verified",
    "draft",
    "concept",
}
REQUIRED_FRONT_MATTER_FIELDS = ["title", "chapter", "status"]
TRANSLATION_LANGUAGES = ["en", "fr"]


def validate_project(root):
    root = Path(root)
    errors = []
    errors.extend(validate_directories(root))
    errors.extend(validate_csv_files(root))
    errors.extend(validate_chapters(root))
    errors.extend(validate_translations(root))
    return errors


def validate_directories(root):
    errors = []
    for directory in REQUIRED_DIRECTORIES:
        if not (root / directory).is_dir():
            errors.append(f"Missing required directory: {directory}")
    return errors


def validate_csv_files(root):
    errors = []
    database_dir = root / "database"
    source_ids = load_source_ids(database_dir / "sources.csv")
    for filename, expected_headers in EXPECTED_CSV_HEADERS.items():
        path = database_dir / filename
        relative_path = path.relative_to(root)
        if not path.is_file():
            errors.append(f"Missing required CSV file: {relative_path}")
            continue

        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            actual_headers = reader.fieldnames or []
            if actual_headers != expected_headers:
                joined_headers = ",".join(actual_headers)
                errors.append(f"{relative_path} has unexpected headers: {joined_headers}")
                continue

            rows = list(reader)
            errors.extend(validate_unique_ids(relative_path, rows))
            errors.extend(validate_statuses(relative_path, rows))
            errors.extend(validate_source_references(relative_path, rows, source_ids))

            if filename == "bike_routes.csv":
                errors.extend(validate_bike_route_types(relative_path, rows))
                errors.extend(validate_bike_route_gpx_files(root, relative_path, rows))
    return errors


def load_source_ids(path):
    if not path.is_file():
        return set()

    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return {row["id"] for row in reader if row.get("id")}


def validate_unique_ids(relative_path, rows):
    errors = []
    seen = {}
    for row_number, row in enumerate(rows, start=2):
        row_id = row.get("id", "")
        if not row_id:
            continue
        if row_id in seen:
            errors.append(f"{relative_path} row {row_number} duplicates id from row {seen[row_id]}: {row_id}")
        else:
            seen[row_id] = row_number
    return errors


def validate_statuses(relative_path, rows):
    errors = []
    for row_number, row in enumerate(rows, start=2):
        status = row.get("status", "")
        if status and status not in VALID_RESEARCH_STATUSES:
            errors.append(f"{relative_path} row {row_number} has invalid status: {status}")
    return errors


def validate_source_references(relative_path, rows, source_ids):
    errors = []
    for row_number, row in enumerate(rows, start=2):
        source_value = row.get("source", "")
        if not source_value:
            continue
        for source_id in source_value.split(";"):
            source_id = source_id.strip()
            if source_id and source_id not in source_ids:
                errors.append(f"{relative_path} row {row_number} references unknown source: {source_id}")
    return errors


def validate_bike_route_types(relative_path, rows):
    errors = []
    for row_number, row in enumerate(rows, start=2):
        route_type = row.get("type", "")
        if route_type and route_type not in VALID_BIKE_TYPES:
            errors.append(f"{relative_path} row {row_number} has invalid type: {route_type}")
    return errors


def validate_bike_route_gpx_files(root, relative_path, rows):
    errors = []
    for row_number, row in enumerate(rows, start=2):
        gpx_file = row.get("gpx_file", "").strip()
        if not gpx_file or "://" in gpx_file:
            continue
        asset_path = Path("assets") / "gpx" / gpx_file
        if not (root / asset_path).is_file():
            errors.append(f"{relative_path} row {row_number} references missing GPX file: {asset_path}")
    return errors


def validate_chapters(root):
    errors = []
    chapters_dir = root / "chapters"
    if not chapters_dir.is_dir():
        return errors

    for path in sorted(chapters_dir.glob("*.md")):
        if path.name == "README.md":
            continue
        errors.extend(validate_chapter(root, path))
    return errors


def validate_translations(root):
    errors = []
    chapters_dir = root / "chapters"
    if not chapters_dir.is_dir():
        return errors

    canonical_chapters = sorted(path.name for path in chapters_dir.glob("*.md") if path.name != "README.md")
    for lang in TRANSLATION_LANGUAGES:
        translation_dir = root / "translations" / lang / "chapters"
        relative_dir = Path("translations") / lang / "chapters"
        if not translation_dir.is_dir():
            errors.append(f"Missing translation directory: {relative_dir}")
            continue

        translated_chapters = sorted(path.name for path in translation_dir.glob("*.md"))
        for chapter_name in canonical_chapters:
            if chapter_name not in translated_chapters:
                errors.append(f"{relative_dir} missing translated chapter: {chapter_name}")
        for chapter_name in translated_chapters:
            if chapter_name not in canonical_chapters:
                errors.append(f"{relative_dir} has extra translated chapter: {chapter_name}")

        for path in sorted(translation_dir.glob("*.md")):
            errors.extend(validate_chapter(root, path))
    return errors


def validate_chapter(root, path):
    errors = []
    relative_path = path.relative_to(root)
    text = path.read_text(encoding="utf-8")
    front_matter = parse_front_matter(text)
    if front_matter is None:
        return [f"{relative_path} missing YAML front matter"]

    for field in REQUIRED_FRONT_MATTER_FIELDS:
        if field not in front_matter or not front_matter[field]:
            errors.append(f"{relative_path} missing front matter field: {field}")

    title = front_matter.get("title")
    if title and f"# {title}" not in text:
        errors.append(f"{relative_path} missing matching H1 for title: {title}")
    return errors


def parse_front_matter(text):
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return None

    front_matter = {}
    for line in lines[1:]:
        if line == "---":
            return front_matter
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        front_matter[key.strip()] = value.strip()
    return None


def main(argv=None):
    argv = argv or sys.argv[1:]
    root = Path(argv[0]) if argv else Path.cwd()
    errors = validate_project(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Project validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
