#!/usr/bin/env python3

"""Check generated HTML for broken local links and basic document structure."""

from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = PROJECT_ROOT / "docs"
PATH_PREFIX = "/risbergetfinnskogen"


class DocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.references: list[tuple[str, str]] = []
        self.h1_count = 0
        self.title_depth = 0
        self.title_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "h1":
            self.h1_count += 1
        if tag == "title":
            self.title_depth += 1
        for attribute in ("href", "src"):
            value = attributes.get(attribute)
            if value:
                self.references.append((attribute, value))

    def handle_endtag(self, tag: str) -> None:
        if tag == "title" and self.title_depth:
            self.title_depth -= 1

    def handle_data(self, value: str) -> None:
        if self.title_depth:
            self.title_text.append(value)


def target_path(source: Path, reference: str) -> Path | None:
    parsed = urlparse(reference)
    if parsed.scheme or parsed.netloc or reference.startswith(("#", "mailto:", "tel:", "data:")):
        return None

    path = unquote(parsed.path)
    if not path:
        return None
    if path.startswith("/"):
        if path == PATH_PREFIX:
            path = "/"
        elif path.startswith(f"{PATH_PREFIX}/"):
            path = path.removeprefix(PATH_PREFIX)
        target = SITE_ROOT / path.removeprefix("/")
    else:
        target = source.parent / path
    if path.endswith("/"):
        target /= "index.html"
    return target


def main() -> int:
    if not SITE_ROOT.exists():
        print("Missing docs. Run npm run build first.", file=sys.stderr)
        return 1

    errors: list[str] = []
    html_files = sorted(SITE_ROOT.rglob("*.html"))
    for source in html_files:
        parser = DocumentParser()
        parser.feed(source.read_text(encoding="utf-8"))
        relative_source = source.relative_to(SITE_ROOT)

        if parser.h1_count != 1:
            errors.append(f"{relative_source}: expected one h1, found {parser.h1_count}")
        if not " ".join(parser.title_text).strip():
            errors.append(f"{relative_source}: missing document title")

        for attribute, reference in parser.references:
            target = target_path(source, reference)
            if target is not None and not target.exists():
                errors.append(
                    f"{relative_source}: broken {attribute}={reference!r} "
                    f"(expected {target.relative_to(SITE_ROOT)})"
                )

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print(f"Checked {len(html_files)} HTML files; no broken local links or heading errors.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
