#!/usr/bin/env python3
import csv
import sys
from pathlib import Path


OUTPUT_HEADERS = [
    "Layer",
    "Name",
    "Latitude",
    "Longitude",
    "Description",
    "Category",
    "Municipality",
    "Source",
    "Status",
    "Atlas ID",
]

DATASETS = [
    {
        "filename": "beaches.csv",
        "layer": "Beaches",
        "category_field": None,
        "description_field": "summary",
    },
    {
        "filename": "places.csv",
        "layer": "Places",
        "category_field": "category",
        "description_field": "summary",
    },
    {
        "filename": "restaurants.csv",
        "layer": "Restaurants",
        "category_field": "category",
        "description_field": "recommended_dishes",
    },
]


def build_atlas_rows(root):
    root = Path(root)
    rows = []
    for dataset in DATASETS:
        path = root / "database" / dataset["filename"]
        if not path.is_file():
            continue
        rows.extend(build_dataset_rows(path, dataset))
    return sorted(rows, key=lambda row: (row["layer"], row["name"]))


def build_dataset_rows(path, dataset):
    rows = []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for source_row in reader:
            latitude = source_row.get("latitude", "").strip()
            longitude = source_row.get("longitude", "").strip()
            if not latitude or not longitude:
                continue
            rows.append(
                {
                    "layer": dataset["layer"],
                    "atlas_id": f"{dataset['layer'].lower()}:{source_row.get('id', '').strip()}",
                    "name": source_row.get("name", "").strip(),
                    "category": read_category(source_row, dataset),
                    "municipality": source_row.get("municipality", "").strip(),
                    "latitude": latitude,
                    "longitude": longitude,
                    "description": source_row.get(dataset["description_field"], "").strip(),
                    "source": source_row.get("source", "").strip(),
                    "status": source_row.get("status", "").strip(),
                }
            )
    return rows


def read_category(source_row, dataset):
    category_field = dataset["category_field"]
    if category_field:
        return source_row.get(category_field, "").strip()
    return dataset["layer"].lower()


def export_atlas(root):
    root = Path(root)
    output_path = root / "output" / "google_maps_atlas.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = build_atlas_rows(root)

    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_HEADERS)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "Layer": row["layer"],
                    "Name": row["name"],
                    "Latitude": row["latitude"],
                    "Longitude": row["longitude"],
                    "Description": row["description"],
                    "Category": row["category"],
                    "Municipality": row["municipality"],
                    "Source": row["source"],
                    "Status": row["status"],
                    "Atlas ID": row["atlas_id"],
                }
            )
    return output_path


def main(argv=None):
    argv = argv or sys.argv[1:]
    root = Path(argv[0]) if argv else Path.cwd()
    output_path = export_atlas(root)
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
