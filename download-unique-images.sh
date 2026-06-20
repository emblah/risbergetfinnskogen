#!/usr/bin/env bash
set -euo pipefail

site_dir="${1:-risbergetvaalerfinnskog.com}"
output_dir="${2:-$site_dir/downloaded-images}"

if ! command -v wget >/dev/null 2>&1; then
  printf 'Error: wget is required. Install it first, then rerun this script.\n' >&2
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  printf 'Error: python3 is required.\n' >&2
  exit 1
fi

if [ ! -d "$site_dir" ]; then
  printf 'Error: site directory not found: %s\n' "$site_dir" >&2
  exit 1
fi

mkdir -p "$output_dir"

url_file="$(mktemp)"
trap 'rm -f "$url_file"' EXIT

python3 - "$site_dir" > "$url_file" <<'PY'
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
import html
import re
import sys

site_dir = Path(sys.argv[1])
urls_by_base = {}

for path in site_dir.rglob("*.html"):
    text = html.unescape(path.read_text(errors="ignore"))

    for match in re.finditer(r"https://impro\.usercontent\.one/[^\"'\s<>]+", text):
        url = match.group(0).rstrip(",)")
        parts = urlsplit(url)
        base = urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))

        if base not in urls_by_base:
            urls_by_base[base] = url

for base in sorted(urls_by_base):
    print(urls_by_base[base])
PY

count="$(wc -l < "$url_file" | tr -d ' ')"
printf 'Found %s unique image URLs. Downloading to %s\n' "$count" "$output_dir"

if [ "$count" = "0" ]; then
  exit 0
fi

wget \
  --input-file="$url_file" \
  --directory-prefix="$output_dir" \
  --force-directories \
  --no-host-directories \
  --no-clobber \
  --tries=3 \
  --timeout=30 \
  --wait=0.1

printf 'Download complete.\n'
