import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_project.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_project", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ValidateProjectTests(unittest.TestCase):
    def setUp(self):
        self.validator = load_validator()

    def make_project(self):
        temp_dir = tempfile.TemporaryDirectory()
        root = Path(temp_dir.name)
        for directory in ["chapters", "database", "assets", "templates", "scripts", "output"]:
            (root / directory).mkdir()
            (root / directory / "README.md").write_text(f"# {directory}\n", encoding="utf-8")

        self.write_chapter(root / "chapters" / "00-preparation.md", "Voorbereiding", 1)
        self.write_chapter(root / "chapters" / "01-prairies-de-la-mer.md", "Prairies de la Mer", 2)

        for name, headers in self.validator.EXPECTED_CSV_HEADERS.items():
            self.write_csv(root / "database" / name, headers)

        return temp_dir, root

    def write_chapter(self, path, title, chapter):
        path.write_text(
            "\n".join(
                [
                    "---",
                    f"title: {title}",
                    f"chapter: {chapter}",
                    "status: concept",
                    "---",
                    "",
                    f"# {title}",
                    "",
                    "## Samenvatting",
                    "",
                ]
            ),
            encoding="utf-8",
        )

    def write_csv(self, path, headers, rows=None):
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=headers)
            writer.writeheader()
            for row in rows or []:
                writer.writerow(row)

    def test_valid_project_has_no_errors(self):
        temp_dir, root = self.make_project()
        self.addCleanup(temp_dir.cleanup)

        errors = self.validator.validate_project(root)

        self.assertEqual([], errors)

    def test_missing_required_directory_is_reported(self):
        temp_dir, root = self.make_project()
        self.addCleanup(temp_dir.cleanup)
        (root / "assets" / "README.md").unlink()
        (root / "assets").rmdir()

        errors = self.validator.validate_project(root)

        self.assertIn("Missing required directory: assets", errors)

    def test_csv_header_mismatch_is_reported(self):
        temp_dir, root = self.make_project()
        self.addCleanup(temp_dir.cleanup)
        self.write_csv(root / "database" / "restaurants.csv", ["id", "name"])

        errors = self.validator.validate_project(root)

        self.assertIn("database/restaurants.csv has unexpected headers: id,name", errors)

    def test_invalid_bike_route_type_is_reported(self):
        temp_dir, root = self.make_project()
        self.addCleanup(temp_dir.cleanup)
        headers = self.validator.EXPECTED_CSV_HEADERS["bike_routes.csv"]
        row = {header: "" for header in headers}
        row.update({"id": "route-1", "name": "Test Route", "type": "Mountain"})
        self.write_csv(root / "database" / "bike_routes.csv", headers, [row])

        errors = self.validator.validate_project(root)

        self.assertIn("database/bike_routes.csv row 2 has invalid type: Mountain", errors)

    def test_chapter_without_front_matter_status_is_reported(self):
        temp_dir, root = self.make_project()
        self.addCleanup(temp_dir.cleanup)
        (root / "chapters" / "00-preparation.md").write_text(
            "---\ntitle: Voorbereiding\nchapter: 1\n---\n\n# Voorbereiding\n",
            encoding="utf-8",
        )

        errors = self.validator.validate_project(root)

        self.assertIn("chapters/00-preparation.md missing front matter field: status", errors)


if __name__ == "__main__":
    unittest.main()

