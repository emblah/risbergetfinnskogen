# Website Takeover TODO

## Current State

- Scraped site lives in `risbergetvaalerfinnskog.com/`.
- Site is static HTML from One.com Website Builder.
- Found `40` HTML files.
- All `40` HTML files are reachable from `index.html`.
- No broken internal HTML links were found.
- Local builder assets are in `risbergetvaalerfinnskog.com/onewebstatic/`.
- `onewebstatic/` contains `53` files: CSS, JS, PNG, SVG, and WOFF2 assets.

## Completed

- Analyzed local HTML, CSS, JS, and static asset references.
- Confirmed the current minimal local site should keep all HTML files and `onewebstatic/`.
- Added `download-unique-images.sh` to extract and download unique `impro.usercontent.one` image URLs.
- Downloaded images into `risbergetvaalerfinnskog.com/downloaded-images/`.
- Verified downloaded images against the HTML references.
- Recovered missing local asset `onewebstatic/11712492fd.png`.
- Rewrote downloaded `https://impro.usercontent.one/...` image references in HTML to local files under `downloaded-images/`.
- Moved social sharing widgets, social metadata, and the local share-widget script into `social-widgets/` with a restore helper.

## Image Download Results

- Expected unique image paths from HTML: `187`.
- Downloaded unique image paths: `185`.
- Extra downloaded image paths: `0`.
- Missing image paths: `2`.

The two missing upstream images return HTTP `404` and could not be downloaded:

- `comments_default_divider.png`
- `topwide_bg.png`

These appear to be small website-builder/theme background assets, not primary content photos.

## Known Issues

- The HTML still references external `https://impro.usercontent.one/...` URLs only for the two missing 404 builder images.
- Normal content links may still point to external services, but active social sharing widgets and social metadata have been archived in `social-widgets/`.

## Next Steps

1. Decide whether to keep or remove other external embeds/content links.
2. Add placeholders or remove references for the two missing builder images.
3. Test the site locally with a static server.
4. Create a clean deploy folder containing only needed HTML, `onewebstatic/`, downloaded images, and any required support files.

## Useful Commands

Download unique images again:

```bash
./download-unique-images.sh
```

Run a simple local static server:

```bash
cd risbergetvaalerfinnskog.com
python3 -m http.server 8000
```

Then open:

```text
http://localhost:8000/
```
