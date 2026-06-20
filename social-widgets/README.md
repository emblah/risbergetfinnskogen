# Social Widgets Archive

This folder contains social sharing widget code and social metadata removed from `risbergetvaalerfinnskog.com/`.

Archived items:

- Removed `data-kind="SHAREBUTTONS"` HTML blocks are in `snippets/`.
- Removed `og:*` and `twitter:*` metadata is in `meta/`.
- The local share-widget script is in `onewebstatic/2f4cfda0cb.js`.
- `manifest.json` records the original source files.

To restore the archived widgets, metadata, and asset, run:

```bash
cd social-widgets
./restore-social-widgets.py
```
