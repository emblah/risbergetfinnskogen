# Developer guide

This site is built with [Eleventy](https://www.11ty.dev/) from files in `src/`.
Use this guide when adding or changing content.

## Local development

Requirements:

- Node.js 20 or newer
- npm

Install dependencies and start the development server:

```sh
npm install
npm start
```

The local site is available at `http://localhost:8080/`.

Before committing, run:

```sh
npm run build
```

This writes the production site to `docs/` and runs `scripts/check-site.py`.
The check fails on broken local links, missing document titles, or pages that do
not contain exactly one `<h1>`.

Do not edit files in `docs/` directly. They are generated from `src/`.

## Repository structure

- `src/pages/`: normal content pages
- `src/_includes/layouts/`: page layouts
- `src/_includes/components/`: shared Nunjucks components
- `src/_data/`: data available to every template
- `src/assets/images/`: site images, grouped by subject
- `src/assets/documents/`: downloadable documents
- `src/assets/css/site.css`: site styles
- `src/assets/js/site.js`: navigation and gallery lightbox behavior
- `src/_data/navigation.json`: sidebar navigation
- `src/_data/redirects.json`: legacy URL mappings
- `src/_data/eventGalleries.js`: image definitions for event galleries

## Choosing Markdown or Nunjucks

Use a `.md` file for primarily written content. Markdown is easier to review and
should be the default for articles and simple pages.

Use a `.njk` file when the page needs substantial HTML structure, such as card
grids, document images, or a gallery whose data is declared in front matter.

Nunjucks is enabled inside both `.md` and `.njk` files. Small amounts of HTML
may also be embedded directly in Markdown when Markdown alone is insufficient.

## Front matter

Every content page starts with YAML front matter:

```yaml
---
layout: layouts/page.njk
title: Page title
description: A concise description used in metadata.
introduction: Optional introductory text shown below the heading.
permalink: /section/page/
breadcrumbs:
  - label: Section
    url: /section/
  - label: Page title
---
```

Conventions:

- Use `layouts/page.njk` for standard pages.
- Use `layouts/gallery.njk` for standalone image galleries.
- Use `layouts/event.njk` for archived events with an optional event gallery.
- Give normal page permalinks a leading and trailing slash.
- Write public text in Norwegian Bokmål unless the source material requires
  otherwise.
- Keep `title` short and unique.
- Write `description` as a plain-text summary suitable for search results.
- Do not add an `<h1>` in the page body; layouts render it from `title`.
- Breadcrumbs start below the home page because the component adds `Forside`
  automatically.
- The final breadcrumb normally has no `url`, so it represents the current page.

## Markdown pages

A standard Markdown page looks like this:

```md
---
layout: layouts/page.njk
title: Eksempelside
description: Kort beskrivelse av eksempelsiden.
introduction: En valgfri innledning.
permalink: /historie/eksempelside/
breadcrumbs:
  - label: Historie og kultur
    url: /historie/
  - label: Eksempelside
---
Brødtekst skrives som vanlig Markdown.

## Mellomtittel

Bruk [beskrivende lenketekst](/historie/) for interne lenker.
```

Use semantic headings in order: the layout supplies `<h1>`, so page content
normally begins with `##`. Avoid using headings only for visual styling.

Root-relative internal URLs such as `/historie/` and `/assets/images/...` are
the project convention. Eleventy's HTML base plugin adds the GitHub Pages path
prefix during production builds.

## Nunjucks pages

Nunjucks output uses `{{ ... }}` and control flow uses `{% ... %}`:

```njk
{% if introduction %}
  <p>{{ introduction }}</p>
{% endif %}

{% for item in items %}
  <a href="{{ item.url }}">{{ item.label }}</a>
{% endfor %}
```

Shared components belong in `src/_includes/components/`; layouts belong in
`src/_includes/layouts/`. Reference either relative to the includes directory:

```njk
{% include "components/header.njk" %}
```

Eleventy supplies rendered page content through `content`. Layouts must use
`{{ content | safe }}` when intentionally inserting that generated HTML.
Do not apply `safe` to untrusted or user-provided content.

Prefer semantic HTML and existing CSS classes. Check `src/assets/css/site.css`
before adding new markup or styles.

## Images

Store images under the closest subject directory in `src/assets/images/`.
Use lowercase, descriptive filenames with hyphens. Gallery and event files use
zero-padded sequence numbers, for example `var-01.jpg`.

Every `<img>` must include:

- A useful Norwegian `alt` description, or `alt=""` only for a genuinely
  decorative image
- The image's intrinsic `width` and `height`
- `loading="lazy"` for images that are not expected to be the first prominent
  image on the page

Do not put credits or extra context in `alt`; use a visible caption instead.
Linking an image with `data-lightbox` activates the shared lightbox behavior.

## Standalone galleries

Standalone galleries keep their image data in the page front matter:

```yaml
---
layout: layouts/gallery.njk
title: Eksempelgalleri
description: Bilder fra et eksempelgalleri i Risberget.
introduction: Valgfri introduksjon til galleriet.
permalink: /bilder/eksempel/
breadcrumbs:
  - label: Bilder
    url: /bilder/
  - label: Eksempelgalleri
images:
  - src: /assets/images/galleries/example/example-01.jpg
    alt: Konkret beskrivelse av motivet.
    width: 1280
    height: 960
    caption: Valgfri synlig bildetekst.
  - src: /assets/images/galleries/example/example-02.jpg
    large: /assets/images/galleries/example/example-02-large.jpg
    alt: Beskrivelse av det andre motivet.
    width: 640
    height: 480
---
```

`large` is optional. When present, the thumbnail uses `src` and the lightbox
opens `large`; otherwise both use `src`.

When adding a gallery:

1. Put its images in a dedicated directory under
   `src/assets/images/galleries/`.
2. Add the gallery page under `src/pages/`.
3. Add a card or link from its section index.
4. Add it to `src/_data/navigation.json` only if it belongs in the sidebar.

## Events

Event pages use Markdown for event text and reference a gallery key:

```md
---
layout: layouts/event.njk
title: Kulturdagen 2026
description: Program og bilder fra Kulturdagen 2026 i Risberget.
introduction: Kort introduksjon til arrangementet.
permalink: /arrangementer/kulturdag-2026/
eventGallery: kulturdag2026
breadcrumbs:
  - label: Arrangementer
    url: /arrangementer/
  - label: Kulturdagen 2026
---
Tekst om arrangementet.
```

Event images are stored in:

```text
src/assets/images/events/kulturdag-2026/
```

Define the key used by `eventGallery` in `src/_data/eventGalleries.js`. The
existing `numberedImages()` helper is preferred when files follow a numbered
pattern:

```js
kulturdag2026: numberedImages({
  folder: "kulturdag-2026",
  prefix: "kulturdag-2026",
  count: 12,
  label: "Kulturdagen 2026 i Risberget",
  dimensions: size(1280, 960),
  firstAlt: "Konkret beskrivelse av motivet i det første bildet.",
}),
```

Use a custom `dimensions(number)` function when image sizes vary. Use
`altByNumber` for images that need a more specific description and
`firstCaption` for a visible caption on the first image.

An event page may omit `eventGallery` when it has no images. When adding an
event, also update:

- `src/pages/arrangementer/index.njk`
- `src/_data/navigation.json`, if the event should appear in the sidebar
- `src/_data/redirects.json`, if an old public URL must continue to work

Historical events outside `/arrangementer/` may still use the event layout, as
the 350-year anniversary page does.

## Navigation and links

Navigation is maintained manually in `src/_data/navigation.json`. Adding a page
does not add it to the sidebar automatically. Preserve the existing object
shape:

```json
{
  "label": "Visible label",
  "url": "/section/page/"
}
```

Top-level entries may contain a `children` array. Keep navigation ordering
intentional and consistent with section index pages.

Use root-relative URLs for internal pages and assets. Use descriptive link text;
avoid labels such as “click here”. After renaming or moving a published page,
record the old-to-new mapping in `src/_data/redirects.json`.

## Documents

Store downloadable files in `src/assets/documents/`. Link to the file with a
root-relative URL and include the file type in visible text when useful:

```md
[Årsmøteprotokoll 2026 (PDF)](/assets/documents/arsmoteprotokoll-2026.pdf)
```

If a document is presented as page images, follow the existing
`arsmoteprotokoller` pages and use the `document-image` class.

## Completion checklist

- Content is under `src/`, not `docs/`.
- Front matter has the correct layout, title, description, permalink, and
  breadcrumbs.
- The page body does not add a second `<h1>`.
- Internal links and asset URLs are root-relative.
- Images have accurate dimensions and useful alternative text.
- Section index pages, navigation, and redirects are updated where applicable.
- `npm run build` completes successfully.
- The changed page is checked in the local development server at desktop and
  narrow viewport widths.
