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
        (root / "translations" / "en" / "chapters").mkdir(parents=True)
        (root / "translations" / "fr" / "chapters").mkdir(parents=True)
        return temp_dir, root

    def write_chapter(self, path, title, chapter, body, status="concept"):
        path.write_text(
            "\n".join(
                [
                    "---",
                    f"title: {title}",
                    f"chapter: {chapter}",
                    f"status: {status}",
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
        self.write_chapter(root / "chapters" / "00-start.md", "Start", 1, "Welkom.", status="draft")
        self.write_chapter(root / "chapters" / "01-next.md", "Next", 2, "- A\n- B", status="draft")
        self.write_chapter(root / "translations" / "en" / "chapters" / "00-start.md", "Start", 1, "Welcome.", status="draft")
        self.write_chapter(root / "translations" / "fr" / "chapters" / "00-start.md", "Départ", 1, "Bienvenue.", status="draft")
        (root / "Docs" / "FINAL_CHECK.md").write_text("# Final Check\n\nReady notes.", encoding="utf-8")

        output_dir = self.builder.build_site(root)

        self.assertEqual(root / "_site", output_dir)
        self.assertTrue((output_dir / ".nojekyll").is_file())
        self.assertIn("Ultimate Saint-Tropez Guide", (output_dir / "index.html").read_text(encoding="utf-8"))
        self.assertIn('href="en/index.html"', (output_dir / "index.html").read_text(encoding="utf-8"))
        self.assertIn('href="fr/index.html"', (output_dir / "index.html").read_text(encoding="utf-8"))
        self.assertIn('href="chapters/00-start.html"', (output_dir / "index.html").read_text(encoding="utf-8"))
        self.assertIn("preview", (output_dir / "index.html").read_text(encoding="utf-8"))
        self.assertNotIn(" - draft", (output_dir / "index.html").read_text(encoding="utf-8"))
        chapter_html = (output_dir / "chapters" / "01-next.html").read_text(encoding="utf-8")
        self.assertIn("<li>A</li>", chapter_html)
        self.assertIn('href="../index.html"', chapter_html)
        english_index = (output_dir / "en" / "index.html").read_text(encoding="utf-8")
        french_chapter = (output_dir / "fr" / "chapters" / "00-start.html").read_text(encoding="utf-8")
        self.assertIn("Welcome.", (output_dir / "en" / "chapters" / "00-start.html").read_text(encoding="utf-8"))
        self.assertIn('lang="en"', english_index)
        self.assertIn('href="../index.html"', english_index)
        self.assertIn("Bienvenue.", french_chapter)
        self.assertIn('href="../../chapters/00-start.html"', french_chapter)


if __name__ == "__main__":
    unittest.main()
