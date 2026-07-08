import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "audit_readiness.py"


def load_auditor():
    spec = importlib.util.spec_from_file_location("audit_readiness", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AuditReadinessTests(unittest.TestCase):
    def setUp(self):
        self.auditor = load_auditor()

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

    def test_build_audit_counts_statuses_and_mapped_rows(self):
        temp_dir, root = self.make_project()
        self.addCleanup(temp_dir.cleanup)
        self.write_csv(
            root / "database" / "places.csv",
            ["id", "name", "category", "municipality", "latitude", "longitude", "summary", "parking_notes", "best_time", "source", "status"],
            [
                {"id": "verified-place", "name": "Verified", "latitude": "43.1", "longitude": "6.1", "status": "verified"},
                {"id": "seed-place", "name": "Seed", "status": "seed_needs_official_verification"},
            ],
        )
        self.write_csv(
            root / "database" / "beaches.csv",
            ["id", "name", "municipality", "latitude", "longitude", "summary", "parking", "water_quality", "snorkeling", "facilities", "best_time", "costs", "source", "status"],
            [{"id": "partial-beach", "name": "Partial", "status": "official_partial_verification"}],
        )

        audit = self.auditor.build_audit(root)

        self.assertEqual(3, audit["total_records"])
        self.assertEqual(1, audit["status_counts"]["verified"])
        self.assertEqual(1, audit["status_counts"]["official_partial_verification"])
        self.assertEqual(1, audit["status_counts"]["seed_needs_official_verification"])
        self.assertEqual(1, audit["mapped_records"])

    def test_export_audit_writes_markdown_report(self):
        temp_dir, root = self.make_project()
        self.addCleanup(temp_dir.cleanup)
        self.write_csv(
            root / "database" / "restaurants.csv",
            ["id", "name", "municipality", "latitude", "longitude", "category", "price_level", "recommended_dishes", "wine_notes", "parking", "cycling_access", "reservation_notes", "source", "status"],
            [{"id": "restaurant", "name": "Restaurant", "status": "official_partial_verification"}],
        )

        output_path = self.auditor.export_audit(root)

        report = output_path.read_text(encoding="utf-8")
        self.assertEqual(root / "output" / "readiness_audit.md", output_path)
        self.assertIn("# Readiness Audit", report)
        self.assertIn("| restaurants.csv | 1 |", report)
        self.assertIn("official_partial_verification", report)


if __name__ == "__main__":
    unittest.main()
