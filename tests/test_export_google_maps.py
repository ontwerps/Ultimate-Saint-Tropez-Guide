import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "export_google_maps.py"


def load_exporter():
    spec = importlib.util.spec_from_file_location("export_google_maps", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ExportGoogleMapsTests(unittest.TestCase):
    def setUp(self):
        self.exporter = load_exporter()

    def make_project(self):
        temp_dir = tempfile.TemporaryDirectory()
        root = Path(temp_dir.name)
        (root / "database").mkdir()
        (root / "output").mkdir()
        return temp_dir, root

    def write_csv(self, path, headers, rows):
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)

    def test_build_atlas_rows_includes_only_geocoded_records(self):
        temp_dir, root = self.make_project()
        self.addCleanup(temp_dir.cleanup)
        self.write_csv(
            root / "database" / "places.csv",
            ["id", "name", "category", "municipality", "latitude", "longitude", "summary", "parking_notes", "best_time", "source", "status"],
            [
                {
                    "id": "viewpoint",
                    "name": "Viewpoint",
                    "category": "viewpoint",
                    "municipality": "Ramatuelle",
                    "latitude": "43.2",
                    "longitude": "6.6",
                    "summary": "A mapped place.",
                    "source": "src-test",
                    "status": "official_partial_verification",
                },
                {"id": "missing", "name": "Missing Coords", "category": "viewpoint", "municipality": "Ramatuelle", "summary": "Skip me."},
            ],
        )
        self.write_csv(
            root / "database" / "beaches.csv",
            ["id", "name", "municipality", "latitude", "longitude", "summary", "parking", "water_quality", "snorkeling", "facilities", "best_time", "costs", "source", "status"],
            [
                {
                    "id": "beach",
                    "name": "Beach",
                    "municipality": "Saint-Tropez",
                    "latitude": "43.3",
                    "longitude": "6.7",
                    "summary": "A mapped beach.",
                    "source": "src-beach",
                    "status": "seed_needs_official_verification",
                }
            ],
        )
        self.write_csv(
            root / "database" / "restaurants.csv",
            ["id", "name", "municipality", "latitude", "longitude", "category", "price_level", "recommended_dishes", "wine_notes", "parking", "cycling_access", "reservation_notes", "source", "status"],
            [],
        )

        rows = self.exporter.build_atlas_rows(root)

        self.assertEqual(["beaches:beach", "places:viewpoint"], [row["atlas_id"] for row in rows])
        self.assertEqual("Beaches", rows[0]["layer"])
        self.assertEqual("A mapped beach.", rows[0]["description"])

    def test_export_atlas_writes_google_maps_csv(self):
        temp_dir, root = self.make_project()
        self.addCleanup(temp_dir.cleanup)
        self.write_csv(
            root / "database" / "places.csv",
            ["id", "name", "category", "municipality", "latitude", "longitude", "summary", "parking_notes", "best_time", "source", "status"],
            [
                {
                    "id": "place",
                    "name": "Place",
                    "category": "quiet_walk",
                    "municipality": "Saint-Tropez",
                    "latitude": "43.1",
                    "longitude": "6.5",
                    "summary": "Mapped place.",
                    "source": "src-place",
                    "status": "official_partial_verification",
                }
            ],
        )
        self.write_csv(
            root / "database" / "beaches.csv",
            ["id", "name", "municipality", "latitude", "longitude", "summary", "parking", "water_quality", "snorkeling", "facilities", "best_time", "costs", "source", "status"],
            [],
        )
        self.write_csv(
            root / "database" / "restaurants.csv",
            ["id", "name", "municipality", "latitude", "longitude", "category", "price_level", "recommended_dishes", "wine_notes", "parking", "cycling_access", "reservation_notes", "source", "status"],
            [],
        )

        output_path = self.exporter.export_atlas(root)

        with output_path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(root / "output" / "google_maps_atlas.csv", output_path)
        self.assertEqual(["Layer", "Name", "Latitude", "Longitude", "Description", "Category", "Municipality", "Source", "Status", "Atlas ID"], list(rows[0].keys()))
        self.assertEqual("Places", rows[0]["Layer"])
        self.assertEqual("Place", rows[0]["Name"])


if __name__ == "__main__":
    unittest.main()
