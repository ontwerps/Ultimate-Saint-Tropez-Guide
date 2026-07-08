#!/usr/bin/env python3
"""Build a lightweight static HTML version of the guide."""

from __future__ import annotations

import html
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT_TITLE = "Ultimate Saint-Tropez Guide"


def parse_front_matter(text):
    if not text.startswith("---\n"):
        return {}, text

    end_marker = "\n---\n"
    end = text.find(end_marker, 4)
    if end == -1:
        return {}, text

    front_matter = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        front_matter[key.strip()] = value.strip().strip('"')

    body = text[end + len(end_marker) :]
    return front_matter, body.lstrip()


def collect_chapters(root=ROOT):
    chapters = []
    for path in sorted((Path(root) / "chapters").glob("*.md")):
        if not re.match(r"^\d{2}-", path.name):
            continue
        metadata, body = parse_front_matter(path.read_text(encoding="utf-8"))
        title = metadata.get("title") or path.stem.replace("-", " ").title()
        try:
            chapter_number = int(metadata.get("chapter", len(chapters) + 1))
        except ValueError:
            chapter_number = len(chapters) + 1

        chapters.append(
            {
                "path": path,
                "title": title,
                "chapter": chapter_number,
                "status": metadata.get("status", "concept"),
                "body": body,
                "output_name": f"{path.stem}.html",
            }
        )

    return sorted(chapters, key=lambda item: (item["chapter"], item["path"].name))


def inline_markdown(text):
    escaped = html.escape(text, quote=False)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', escaped)
    return escaped


def render_markdown(markdown):
    blocks = []
    paragraph = []
    list_items = []
    code_lines = []
    in_code = False

    def flush_paragraph():
        if paragraph:
            blocks.append(f"<p>{inline_markdown(' '.join(paragraph))}</p>")
            paragraph.clear()

    def flush_list():
        if list_items:
            items = "\n".join(f"<li>{inline_markdown(item)}</li>" for item in list_items)
            blocks.append(f"<ul>\n{items}\n</ul>")
            list_items.clear()

    def flush_code():
        if code_lines:
            code = html.escape("\n".join(code_lines))
            blocks.append(f"<pre><code>{code}</code></pre>")
            code_lines.clear()

    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()

        if line.startswith("```"):
            if in_code:
                flush_code()
                in_code = False
            else:
                flush_paragraph()
                flush_list()
                in_code = True
            continue

        if in_code:
            code_lines.append(raw_line)
            continue

        if not line:
            flush_paragraph()
            flush_list()
            continue

        heading_match = re.match(r"^(#{1,4})\s+(.+)$", line)
        if heading_match:
            flush_paragraph()
            flush_list()
            level = len(heading_match.group(1))
            text = inline_markdown(heading_match.group(2))
            blocks.append(f"<h{level}>{text}</h{level}>")
            continue

        if line.startswith("- "):
            flush_paragraph()
            list_items.append(line[2:].strip())
            continue

        paragraph.append(line)

    flush_paragraph()
    flush_list()
    if in_code:
        flush_code()

    return "\n".join(blocks)


def page_shell(title, body, depth=0):
    prefix = "../" * depth
    return f"""<!doctype html>
<html lang="nl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} | {PROJECT_TITLE}</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #172026;
      --muted: #5f6b74;
      --line: #d9e0e5;
      --paper: #fbfaf7;
      --accent: #0f766e;
      --band: #eef5f3;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--paper);
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.65;
    }}
    header {{
      border-bottom: 1px solid var(--line);
      background: #ffffff;
    }}
    .bar, main, footer {{
      width: min(1120px, calc(100vw - 32px));
      margin: 0 auto;
    }}
    .bar {{
      min-height: 64px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
    }}
    .brand {{
      color: var(--ink);
      font-weight: 700;
      text-decoration: none;
    }}
    nav a {{
      color: var(--accent);
      font-weight: 600;
      text-decoration: none;
    }}
    main {{
      padding: 40px 0 56px;
    }}
    .hero {{
      padding: 30px 0 24px;
      border-bottom: 1px solid var(--line);
    }}
    .note {{
      background: var(--band);
      border-left: 4px solid var(--accent);
      margin: 24px 0;
      padding: 14px 16px;
    }}
    h1, h2, h3, h4 {{
      line-height: 1.2;
      margin: 1.7em 0 0.5em;
    }}
    h1 {{
      font-size: clamp(2rem, 5vw, 4rem);
      margin-top: 0;
    }}
    h2 {{ font-size: 1.6rem; }}
    h3 {{ font-size: 1.25rem; }}
    p, li {{
      max-width: 760px;
      font-size: 1rem;
    }}
    a {{ color: var(--accent); }}
    .chapter-list {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
      gap: 12px;
      list-style: none;
      padding: 0;
      margin: 24px 0 0;
    }}
    .chapter-list li {{
      max-width: none;
      border-top: 1px solid var(--line);
      padding: 14px 0;
    }}
    .chapter-list a {{
      display: block;
      font-weight: 700;
      text-decoration: none;
    }}
    .status {{
      color: var(--muted);
      display: block;
      font-size: 0.9rem;
      margin-top: 4px;
    }}
    pre {{
      overflow: auto;
      padding: 16px;
      background: #111820;
      color: #f7fafc;
    }}
    footer {{
      border-top: 1px solid var(--line);
      color: var(--muted);
      padding: 24px 0 40px;
    }}
  </style>
</head>
<body>
  <header>
    <div class="bar">
      <a class="brand" href="{prefix}index.html">{PROJECT_TITLE}</a>
      <nav><a href="{prefix}index.html">Inhoud</a></nav>
    </div>
  </header>
  <main>
{body}
  </main>
  <footer>Generated from the repository source files.</footer>
</body>
</html>
"""


def render_index(chapters, final_check_text):
    final_check_html = render_markdown(final_check_text)
    chapter_items = "\n".join(
        (
            f'<li><a href="chapters/{html.escape(chapter["output_name"])}">'
            f'{html.escape(chapter["title"])}</a>'
            f'<span class="status">Chapter {chapter["chapter"]} - {html.escape(chapter["status"])}</span></li>'
        )
        for chapter in chapters
    )
    body = f"""    <section class="hero">
      <h1>{PROJECT_TITLE}</h1>
      <p>A Markdown-first travel handbook for the Gulf of Saint-Tropez, generated directly from the repository.</p>
    </section>
    <section class="note">
      <strong>Readiness note:</strong> this preview is structurally ready, but recommendations still need current official and local verification before publication.
    </section>
    <section>
      <h2>Chapters</h2>
      <ul class="chapter-list">
{chapter_items}
      </ul>
    </section>
    <section>
      <h2>Final Check</h2>
{final_check_html}
    </section>"""
    return page_shell(PROJECT_TITLE, body)


def render_chapter(chapter):
    chapter_html = render_markdown(chapter["body"])
    body = f"""    <p><a href="../index.html">Back to contents</a></p>
    <article>
      <p class="status">Chapter {chapter["chapter"]} - {html.escape(chapter["status"])}</p>
{chapter_html}
    </article>"""
    return page_shell(chapter["title"], body, depth=1)


def build_site(root=ROOT):
    root = Path(root)
    output_dir = root / "_site"
    if output_dir.exists():
        shutil.rmtree(output_dir)
    (output_dir / "chapters").mkdir(parents=True)
    (output_dir / ".nojekyll").write_text("", encoding="utf-8")

    chapters = collect_chapters(root)
    final_check_path = root / "Docs" / "FINAL_CHECK.md"
    final_check_text = final_check_path.read_text(encoding="utf-8") if final_check_path.exists() else ""

    (output_dir / "index.html").write_text(render_index(chapters, final_check_text), encoding="utf-8")
    for chapter in chapters:
        target = output_dir / "chapters" / chapter["output_name"]
        target.write_text(render_chapter(chapter), encoding="utf-8")

    return output_dir


def main():
    output_dir = build_site(ROOT)
    print(f"Built {output_dir}")


if __name__ == "__main__":
    main()
