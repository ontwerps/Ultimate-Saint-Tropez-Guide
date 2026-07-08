import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "build_site.py"


def load_builder():
    spec = importlib.util.spec_from_file_location("build_site", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class BuildSiteTests(unittest.TestCase):
    def setUp(self):
        self.builder = load_builder()

    def make_project(self):
        temp_dir = tempfile.TemporaryDirectory()
        root = Path(temp_dir.name)
        (root / "chapters").mkdir()
        (root / "database").mkdir()
        (root / "Docs").mkdir()
        return temp_dir, root

    def write_chapter(self, path, title, chapter, body):
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
                    body,
                ]
            ),
            encoding="utf-8",
        )

    def test_collect_chapters_reads_front_matter_and_body(self):
        temp_dir, root = self.make_project()
        self.addCleanup(temp_dir.cleanup)
        self.write_chapter(root / "chapters" / "00-start.md", "Start", 1, "Welkom.")
        (root / "chapters" / "README.md").write_text("# Chapters\n", encoding="utf-8")

        chapters = self.builder.collect_chapters(root)

        self.assertEqual(1, len(chapters))
        self.assertEqual("Start", chapters[0]["title"])
        self.assertEqual("00-start.html", chapters[0]["output_name"])
        self.assertIn("Welkom.", chapters[0]["body"])
        self.assertNotIn("---", chapters[0]["body"])

    def test_build_site_writes_index_chapters_and_nojekyll(self):
        temp_dir, root = self.make_project()
        self.addCleanup(temp_dir.cleanup)
        self.write_chapter(root / "chapters" / "00-start.md", "Start", 1, "Welkom.")
        self.write_chapter(root / "chapters" / "01-next.md", "Next", 2, "- A\n- B")
        (root / "Docs" / "FINAL_CHECK.md").write_text("# Final Check\n\nReady notes.", encoding="utf-8")

        output_dir = self.builder.build_site(root)

        self.assertEqual(root / "_site", output_dir)
        self.assertTrue((output_dir / ".nojekyll").is_file())
        self.assertIn("Ultimate Saint-Tropez Guide", (output_dir / "index.html").read_text(encoding="utf-8"))
        self.assertIn('href="chapters/00-start.html"', (output_dir / "index.html").read_text(encoding="utf-8"))
        chapter_html = (output_dir / "chapters" / "01-next.html").read_text(encoding="utf-8")
        self.assertIn("<li>A</li>", chapter_html)
        self.assertIn('href="../index.html"', chapter_html)


if __name__ == "__main__":
    unittest.main()
