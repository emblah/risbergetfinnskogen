#!/usr/bin/env python3

"""Build the migration inventory from the archived One.com HTML."""

from __future__ import annotations

import html
import json
import posixpath
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_ROOT = PROJECT_ROOT.parent / "risbergetvaalerfinnskog.com"
DOCS_ROOT = PROJECT_ROOT / "docs"
REDIRECTS_FILE = PROJECT_ROOT / "src" / "_data" / "redirects.json"


MIGRATION = {
    "index.html": ("/", "Forside", "standard page"),
    "rringdatering.html": ("/historie/arringdatering/", "Historie og kultur", "standard page"),
    "dendrokronologi.html": ("/historie/dendrokronologi/", "Historie og kultur", "standard page"),
    "118111329.html": ("/risberget/rundt/", "Om Risberget", "standard page"),
    "118111365.html": ("/risberget/skiloyper/", "Om Risberget", "standard page"),
    "118111340.html": ("/historie/350-arsjubileum/del-1/", "Historie og kultur", "event"),
    "118111353.html": ("/historie/350-arsjubileum/del-2/", "Historie og kultur", "event"),
    "118111341/index.html": ("/historie/finnebosetning/", "Historie og kultur", "standard page"),
    "118111341/118111349.html": ("/historie/skogfinner/", "Historie og kultur", "standard page"),
    "451549850.html": ("/historie/svedjefinnene/", "Historie og kultur", "standard page"),
    "118111330/index.html": ("/risberget/finnskogen/", "Om Risberget", "standard page"),
    "118111330/118111331.html": ("/risberget/risbergsmarka/", "Om Risberget", "standard page"),
    "118111355.html": ("/historie/minnepark/", "Historie og kultur", "standard page"),
    "118111348.html": ("/historie/arbeidern/", "Historie og kultur", "standard page"),
    "118111326.html": ("/arrangementer/kulturdag-2020/", "Arrangementer", "event"),
    "450359384.html": ("/arrangementer/kulturdag-2021/", "Arrangementer", "event"),
    "453232083.html": ("/arrangementer/kulturdag-2022/", "Arrangementer", "event"),
    "118111364.html": ("/arrangementer/kulturdag-2019/", "Arrangementer", "event"),
    "118111342/index.html": ("/bilder/", "Bilder", "gallery index"),
    "118111342/118111343.html": ("/bilder/vinter/", "Bilder", "gallery"),
    "118111342/118111345.html": ("/bilder/var/", "Bilder", "gallery"),
    "118111342/118111346.html": ("/bilder/sommer/", "Bilder", "gallery"),
    "118111342/118111347.html": ("/bilder/host/", "Bilder", "gallery"),
    "118111333/index.html": ("/kirken/", "Risberget kirke", "standard page"),
    "118111333/118111334.html": ("/kirken/kirkesal/", "Risberget kirke", "standard page"),
    "118111333/118111335.html": ("/kirken/gravferd/", "Risberget kirke", "standard page"),
    "118111336.html": ("/kirken/gravlund/", "Risberget kirke", "standard page"),
    "118111356/index.html": ("/foreningen/arsmoteprotokoller/", "Foreningen", "annual report index"),
    "118111356/r-2025.html": ("/foreningen/arsmoteprotokoller/2025/", "Foreningen", "annual report"),
    "118111356/r-2024.html": ("/foreningen/arsmoteprotokoller/2024/", "Foreningen", "annual report"),
    "118111356/r..2023-1.html": ("/foreningen/arsmoteprotokoller/2023/", "Foreningen", "annual report"),
    "118111356/r..2022.html": ("/foreningen/arsmoteprotokoller/2022/", "Foreningen", "annual report"),
    "118111356/452443065.html": ("/foreningen/arsmoteprotokoller/2021/", "Foreningen", "annual report"),
    "118111356/118111327.html": ("/foreningen/arsmoteprotokoller/2020/", "Foreningen", "annual report"),
    "118111356/118111363.html": ("/foreningen/arsmoteprotokoller/2019/", "Foreningen", "annual report"),
    "118111356/118111357.html": ("/foreningen/arsmoteprotokoller/2018/", "Foreningen", "annual report"),
    "118111332.html": ("/lenker/", "Foreningen", "link index"),
    "118111337.html": ("/foreningen/styret/", "Foreningen", "standard page"),
    "118111338.html": ("/kontakt/", "Kontakt", "standard page"),
    "118111339.html": ("/foreningen/medlemskap/", "Foreningen", "standard page"),
}


ISSUES = {
    "118111336.html": ["Legacy layout visibly squeezes one image."],
    "118111338.html": ["Obsolete One.com contact form must not be migrated."],
    "118111342/index.html": ["Gallery introduction was previously reported missing."],
    "118111341/index.html": [
        "Archived comments allege factual errors and the article lacks a clear author."
    ],
    "451549850.html": [
        "The expanded article/PDF was hosted through Facebook and is absent from the local archive."
    ],
    "118111356/r-2024.html": [
        "The page embeds scan.pdf from the old domain; the original scrape omitted it."
    ],
    "118111356/r-2025.html": [
        "The legacy page heading says 2024, while the scanned primary document is dated 2025."
    ],
}


@dataclass
class PageData:
    title_parts: list[str] = field(default_factory=list)
    heading_parts: list[str] = field(default_factory=list)
    links: list[str] = field(default_factory=list)
    images: list[str] = field(default_factory=list)
    _in_title: bool = False
    _heading_depth: int = 0
    _found_heading: bool = False
    _skip_depth: int = 0


class ArchiveParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.data = PageData()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag in {"script", "style"}:
            self.data._skip_depth += 1
            return
        if self.data._skip_depth:
            return
        if tag == "title":
            self.data._in_title = True
        if tag == "h1" and not self.data._found_heading:
            self.data._heading_depth = 1
            self.data._found_heading = True
        elif self.data._heading_depth:
            self.data._heading_depth += 1
        if tag == "a" and attributes.get("href"):
            self.data.links.append(attributes["href"])
        if tag == "img" and attributes.get("src"):
            self.data.images.append(attributes["src"])
        if attributes.get("data-background"):
            self.data.images.append(attributes["data-background"])

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"} and self.data._skip_depth:
            self.data._skip_depth -= 1
            return
        if self.data._skip_depth:
            return
        if tag == "title":
            self.data._in_title = False
        if self.data._heading_depth:
            self.data._heading_depth -= 1

    def handle_data(self, value: str) -> None:
        if self.data._skip_depth:
            return
        if self.data._in_title:
            self.data.title_parts.append(value)
        if self.data._heading_depth:
            self.data.heading_parts.append(value)


def clean_text(parts: list[str]) -> str:
    return " ".join(html.unescape("".join(parts)).replace("\xa0", " ").split())


def normalized_archive_link(source: str, href: str) -> str | None:
    parsed = urlparse(href)
    if parsed.scheme or parsed.netloc or href.startswith(("#", "mailto:", "tel:", "javascript:")):
        return None
    path = unquote(parsed.path)
    if not path:
        return None
    resolved = posixpath.normpath(posixpath.join(posixpath.dirname(source), path))
    if resolved == ".":
        resolved = "index.html"
    if resolved.endswith("/"):
        resolved += "index.html"
    return resolved


def collect_page(source_path: Path) -> dict:
    source = source_path.relative_to(ARCHIVE_ROOT).as_posix()
    parser = ArchiveParser()
    parser.feed(source_path.read_text(encoding="utf-8", errors="replace"))

    title = clean_text(parser.data.title_parts).removesuffix(" | risbergetvaalerfinnskog.com")
    heading = clean_text(parser.data.heading_parts)
    internal_links = sorted(
        {
            link
            for href in parser.data.links
            if (link := normalized_archive_link(source, href)) in MIGRATION
        }
    )
    external_links = sorted(
        {
            href
            for href in parser.data.links
            if urlparse(href).scheme in {"http", "https"}
        }
    )
    image_paths = sorted(
        {
            unquote(urlparse(src).path).rsplit("/", 1)[-1]
            for src in parser.data.images
            if "topwide_bg.png" not in src and "comments_default_divider.png" not in src
        }
    )
    proposed_url, parent, content_type = MIGRATION[source]

    page_issues = list(ISSUES.get(source, []))
    if "comment" in source_path.read_text(encoding="utf-8", errors="replace").lower():
        page_issues.append("Legacy comment markup detected; exclude it from migrated content.")

    return {
        "source": source,
        "old_url": f"/{source}",
        "title": title,
        "heading": heading,
        "proposed_url": proposed_url,
        "parent_section": parent,
        "content_type": content_type,
        "migration_status": "migrated" if proposed_url in {
            "/",
            "/risberget/rundt/",
            "/risberget/skiloyper/",
            "/risberget/finnskogen/",
            "/risberget/risbergsmarka/",
            "/historie/arringdatering/",
            "/historie/dendrokronologi/",
            "/historie/skogfinner/",
            "/historie/finnebosetning/",
            "/historie/svedjefinnene/",
            "/historie/minnepark/",
            "/historie/arbeidern/",
            "/historie/350-arsjubileum/del-1/",
            "/historie/350-arsjubileum/del-2/",
            "/arrangementer/kulturdag-2019/",
            "/arrangementer/kulturdag-2020/",
            "/arrangementer/kulturdag-2021/",
            "/arrangementer/kulturdag-2022/",
            "/bilder/",
            "/bilder/vinter/",
            "/bilder/var/",
            "/bilder/sommer/",
            "/bilder/host/",
            "/kirken/",
            "/kirken/kirkesal/",
            "/kirken/gravferd/",
            "/kirken/gravlund/",
            "/lenker/",
            "/foreningen/styret/",
            "/kontakt/",
            "/foreningen/medlemskap/",
            "/foreningen/arsmoteprotokoller/",
            "/foreningen/arsmoteprotokoller/2018/",
            "/foreningen/arsmoteprotokoller/2019/",
            "/foreningen/arsmoteprotokoller/2020/",
            "/foreningen/arsmoteprotokoller/2021/",
            "/foreningen/arsmoteprotokoller/2022/",
            "/foreningen/arsmoteprotokoller/2023/",
            "/foreningen/arsmoteprotokoller/2024/",
            "/foreningen/arsmoteprotokoller/2025/",
        } else "pending",
        "images": image_paths,
        "internal_links": internal_links,
        "external_links": external_links,
        "issues": sorted(set(page_issues)),
    }


def write_markdown(pages: list[dict]) -> None:
    lines = [
        "# Archived page inventory",
        "",
        "Generated by `npm run inventory`. Detailed link and image lists are in",
        "`page-inventory.json`.",
        "",
        f"Total archived HTML pages: **{len(pages)}**.",
        "",
        "| Source | Title / heading | Type | Parent | Proposed URL | Status | Images | Issues |",
        "| --- | --- | --- | --- | --- | --- | ---: | ---: |",
    ]
    for page in pages:
        label = page["heading"] or page["title"]
        lines.append(
            f"| `{page['source']}` | {label.replace('|', '\\|')} | "
            f"{page['content_type']} | {page['parent_section']} | "
            f"`{page['proposed_url']}` | {page['migration_status']} | "
            f"{len(page['images'])} | {len(page['issues'])} |"
        )
    lines.extend(
        [
            "",
            "## Information architecture",
            "",
            "- Forside",
            "- Om Risberget",
            "- Historie og kultur",
            "- Risberget kirke",
            "- Arrangementer",
            "- Bilder",
            "- Foreningen",
            "- Kontakt",
            "",
            "## Migration totals",
            "",
            f"- Migrated in the current Eleventy source: {sum(p['migration_status'] == 'migrated' for p in pages)}",
            f"- Pending migration: {sum(p['migration_status'] == 'pending' for p in pages)}",
            f"- Pages with recorded editorial or legacy-markup issues: {sum(bool(p['issues']) for p in pages)}",
            "",
        ]
    )
    (DOCS_ROOT / "page-inventory.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    archive_files = sorted(ARCHIVE_ROOT.rglob("*.html"))
    archive_sources = {path.relative_to(ARCHIVE_ROOT).as_posix() for path in archive_files}
    if archive_sources != set(MIGRATION):
        missing = sorted(archive_sources - set(MIGRATION))
        stale = sorted(set(MIGRATION) - archive_sources)
        raise SystemExit(f"Migration map mismatch. Missing: {missing}; stale: {stale}")

    pages = [collect_page(path) for path in archive_files]
    DOCS_ROOT.mkdir(exist_ok=True)
    (DOCS_ROOT / "page-inventory.json").write_text(
        json.dumps(pages, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_markdown(pages)

    redirects = [
        {"from": page["old_url"], "to": page["proposed_url"], "status": 301}
        for page in pages
    ]
    REDIRECTS_FILE.write_text(
        json.dumps(redirects, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Inventoried {len(pages)} pages and wrote {len(redirects)} redirects.")


if __name__ == "__main__":
    main()
