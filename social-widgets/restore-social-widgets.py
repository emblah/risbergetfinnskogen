#!/usr/bin/env python3
from pathlib import Path
import json
import shutil
import re

archive = Path(__file__).resolve().parent
root = archive.parent
site = root / 'risbergetvaalerfinnskog.com'
manifest = json.loads((archive / 'manifest.json').read_text(encoding='utf-8'))

for asset in manifest.get('moved_assets', []):
    src = root / asset['to']
    dst = root / asset['from']
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.exists() and not dst.exists():
        shutil.copy2(src, dst)

for entry in manifest.get('removed_social_meta', []):
    html = site / entry['file']
    meta = archive / entry['meta']
    if not html.exists() or not meta.exists():
        continue
    text = html.read_text(encoding='utf-8')
    meta_text = meta.read_text(encoding='utf-8')
    prefix_match = re.search(r'<!-- html-prefix: (.*?) -->', meta_text)
    if prefix_match and 'prefix="og: http://ogp.me/ns#"' not in text:
        text = text.replace('<html', '<html' + prefix_match.group(1), 1)
    tags = '\n'.join(line for line in meta_text.splitlines() if line.startswith('<meta '))
    if tags and tags not in text:
        marker = '<link rel="canonical"'
        if marker in text:
            text = text.replace(marker, tags + marker, 1)
        else:
            text = text.replace('<style>', tags + '<style>', 1)
    html.write_text(text, encoding='utf-8')

for entry in manifest.get('removed_html_widgets', []):
    html = site / entry['file']
    if not html.exists():
        continue
    text = html.read_text(encoding='utf-8')
    if 'data-kind="SHAREBUTTONS"' in text:
        continue
    insert = ''.join((archive / snippet).read_text(encoding='utf-8').rstrip('\n') for snippet in entry['snippets'])
    marker = '<div style="clear:both"></div></div></div></div></div></div><div class="Preview_float__1PmYU float"'
    if marker in text:
        text = text.replace(marker, insert + marker, 1)
    else:
        text = text.replace('</body>', insert + '</body>', 1)
    html.write_text(text, encoding='utf-8')
