# Migration Plan: risbergetfinnskogen.no

## Objective

Rebuild the archived One.com website as a modern, lightweight static website using Eleventy.

The new source code will live under:

```text
risbergetfinnskogen.no/
```

The existing scraped website under `risbergetvaalerfinnskog.com/` will remain unchanged and serve as the migration source and visual/content reference.

## Current Progress

Last updated: 21 June 2026.

- Eleventy project scaffold, shared layouts, navigation, CSS, metadata,
  sitemap, robots file, and 404 page are implemented.
- All 40 archived pages have inventory records and old-to-new URL mappings.
- All 40 archived pages are migrated.
- The two 350-year anniversary pages and Culture Day pages for 2019–2022
  are migrated with 103 local event images.
- Seasonal galleries, church pages, annual reports, association pages, and
  Risberget/Finnskogen background pages are migrated.
- Gallery and content images currently link directly to larger local images
  and work without JavaScript.
- The generated site currently contains 45 HTML files.
- The automated build and local link/heading checks pass.
- Editorial uncertainties and withheld contact/payment details are recorded
  in `risbergetfinnskogen.no/docs/editorial-issues.md`.

Detailed status is generated in:

- `risbergetfinnskogen.no/docs/page-inventory.md`
- `risbergetfinnskogen.no/docs/page-inventory.json`
- `risbergetfinnskogen.no/src/_data/redirects.json`

## Technical Direction

- Eleventy (11ty) as the static-site generator.
- Nunjucks for layouts, includes, macros, and page templates.
- Markdown where pages are primarily prose.
- JSON or JavaScript data files for navigation and repeated structured content.
- Native CSS using custom properties, Grid, and Flexbox.
- Small amounts of vanilla JavaScript for progressive enhancement only.
- Static HTML output that works without JavaScript.
- No React, client-side router, Tailwind, component framework, or runtime server.
- Add dependencies only when they solve a demonstrated requirement.

The website will be a multi-page static site rather than a true SPA. Normal links and pre-generated HTML provide better resilience, accessibility, search indexing, and maintenance for this content-heavy site.

## Proposed Project Structure

```text
risbergetfinnskogen.no/
├── src/
│   ├── _data/
│   │   ├── navigation.json
│   │   ├── redirects.json
│   │   └── site.json
│   ├── _includes/
│   │   ├── components/
│   │   │   ├── breadcrumbs.njk
│   │   │   ├── footer.njk
│   │   │   ├── gallery.njk
│   │   │   ├── header.njk
│   │   │   └── navigation.njk
│   │   └── layouts/
│   │       ├── base.njk
│   │       ├── gallery.njk
│   │       └── page.njk
│   ├── assets/
│   │   ├── css/
│   │   │   └── site.css
│   │   ├── fonts/
│   │   ├── images/
│   │   └── js/
│   │       └── site.js
│   ├── pages/
│   ├── 404.njk
│   └── index.njk
├── public/
├── scripts/
├── eleventy.config.js
├── package.json
└── README.md
```

The exact content hierarchy may change after the page inventory is complete.

## Phase 1: Inventory and Content Model — Complete

1. Create an inventory of all 40 archived HTML pages.
2. Record for each page:
   - Existing file and URL.
   - Page title and heading.
   - Proposed new URL.
   - Parent section.
   - Content type: standard page, gallery, event, annual report, or index.
   - Images and downloadable files used.
   - Internal and external links.
   - Missing, duplicated, or visibly broken content.
3. Define the new top-level information architecture.
4. Identify repeated content that belongs in data files or shared components.
5. Create a permanent old-to-new URL mapping before moving content.

Likely top-level sections:

- Forside
- Om Risberget
- Historie og kultur
- Risberget kirke
- Arrangementer
- Bilder
- Foreningen
- Kontakt

Deliverables:

- Complete page inventory.
- Approved navigation hierarchy.
- Old-to-new URL map.
- List of content problems requiring editorial decisions.

## Phase 2: Scaffold the Eleventy Project — Complete

1. Create `risbergetfinnskogen.no/` if not already existing.
2. Add a minimal `package.json` with Eleventy as the only initial dependency.
3. Configure:
   - `src/` as the input directory.
   - `_site/` as the generated output directory.
   - Passthrough copying for static assets.
   - Nunjucks and Markdown templates.
   - Clean output before production builds.
4. Add development and production scripts:

```json
{
  "scripts": {
    "dev": "eleventy --serve",
    "build": "eleventy"
  }
}
```

5. Add a project README with setup, development, build, and deployment instructions.
6. Ensure generated files and dependencies are ignored by Git.

Deliverables:

- A working local Eleventy development server.
- A reproducible static production build.
- A minimal dependency tree.

## Phase 3: Build the Shared Design System — Mostly Complete

1. Establish design tokens for:
   - Colors.
   - Typography.
   - Spacing.
   - Content widths.
   - Borders, shadows, and focus states.
2. Build the base page layout with shared metadata, header, navigation, main content, and footer.
3. Build reusable components for:
   - Responsive navigation.
   - Breadcrumbs.
   - Page introductions.
   - Image figures and captions.
   - Responsive galleries.
   - Clickable gallery images that open a larger version.
   - Link lists and cards.
   - Notices and event information.
4. Implement responsive behavior for phone, tablet, and desktop widths.
5. Use a local system-font stack initially. Add a self-hosted font only if it materially improves the final design.
6. Keep all primary navigation and content functional without JavaScript.

Deliverables:

- Approved homepage and standard-page templates.
- Reusable components for all known content types.
- A responsive CSS foundation without a CSS framework.

Remaining:

- Complete visual testing at phone, tablet, and desktop widths.
- Complete manual keyboard and screen-reader testing of the lightbox.

## Phase 4: Prepare Images and Static Assets — In Progress

1. Treat the archived images as source material rather than copying the current malformed directory structure into the new site.
2. Match images to their pages and determine whether multiple files represent:
   - The same original image.
   - Cropped variants.
   - Resized variants.
   - Genuine duplicates.
3. Rename retained images using stable, descriptive filenames.
4. Organize images by subject or content section.
5. Preserve original-resolution files where available.
6. Generate appropriately sized display variants when beneficial.
7. Add dimensions, useful alternative text, captions, and lazy loading.
8. Link gallery thumbnails to a larger local image so opening an image still
   works without JavaScript.
9. Progressively enhance image links with an accessible lightbox or dialog:
   - Keyboard operable.
   - Closeable with Escape and a visible close button.
   - Focus remains managed correctly while open and returns to the triggering image.
   - Previous and next controls are available where useful.
   - Image captions and alternative text remain available.
   - Browser back navigation and direct image links are not broken.
10. Remove One.com scripts, styles, widgets, tracking code, and theme assets from the new project.
11. Verify that the two known missing theme images are not required by the new design.

Possible future dependency:

- `@11ty/eleventy-img`, added only if automated image resizing and modern output formats justify the additional build complexity.

Deliverables:

- Clean, understandable image library.
- No image references to One.com infrastructure.
- No unnecessary legacy builder assets.

Current status:

- Images for all 40 migrated source pages are local and use clean paths.
- Known malformed legacy image dimensions have been corrected.
- Larger local images can be opened through normal links.

Remaining:

- Review whether responsive variants justify adding `@11ty/eleventy-img`.
- Audit alternative text and captions across the complete image library.

## Phase 5: Migrate Content — Complete

Migrate content section by section rather than performing a blind HTML conversion.

For each page:

1. Extract the meaningful text, headings, images, captions, and links.
2. Remove One.com layout markup, inline styles, generated classes, and scripts.
3. Correct heading order and basic document structure.
4. Assign the appropriate shared layout.
5. Add front matter including:
   - Title.
   - Description.
   - Permalink.
   - Navigation metadata.
   - Optional last-updated date.
6. Replace repeated markup with components or structured data.
7. Verify Norwegian characters and punctuation.
8. Compare the migrated page with the archived source.
9. Flag uncertain wording or missing material instead of silently inventing content.

Suggested migration order:

1. Homepage and primary navigation pages.
2. Contact, membership, board, and association information.
3. Risberget and Finnskogen background pages.
4. Church, cemetery, and memorial pages.
5. Cultural event and anniversary pages.
6. Historical and research pages.
7. Annual meeting records.
8. Seasonal and subject galleries.

Known archived-content issues to resolve during migration:

- The misplaced comment sections on some pages should not be migrated.
- Restore or rewrite the missing gallery introduction on the gallery index.
- Correct the squeezed image from `118111336.html`.
- Do not restore the obsolete One.com contact form.
- Publish a new `@risbergetfinnskogen.no` email link only after the mailbox is
  created and tested.

Deliverables:

- All 40 source pages either migrated, intentionally consolidated, or documented as intentionally excluded.
- No copied One.com page-builder markup in the new templates.

Completed event migration:

1. Migrated the two pages covering the 350-year anniversary.
2. Migrated Culture Day pages for 2019, 2020, 2021, and 2022.
3. Cleaned, renamed, described, and linked 103 associated event images.
4. Updated the arrangement and history indexes.
5. Marked all six pages as migrated and regenerated the inventory.

## Phase 6: URLs, Redirects, and Metadata — Mostly Complete

1. Use readable Norwegian URLs, for example:

```text
/risberget/
/historie/skogfinner/
/kirken/gravlund/
/arrangementer/kulturdag-2022/
/foreningen/arsmoteprotokoller/2025/
/bilder/vinter/
```

2. Avoid changing approved URLs after launch.
3. Preserve every old URL through one of:
   - Host-level permanent redirects.
   - Static compatibility pages with canonical links and redirects.
4. Add per-page:
   - Unique title.
   - Meta description.
   - Canonical URL.
   - Open Graph metadata.
5. Generate `sitemap.xml` and `robots.txt`.
6. Add a useful static 404 page.
7. Decide whether the old `.com` domain will redirect to the matching new `.no` URLs or remain as an archive.

Deliverables:

- Tested redirect map.
- No known broken internal links.
- Search-engine-ready metadata and sitemap.

Current status:

- All 40 old URLs have proposed permanent redirect targets.
- Canonical URLs, titles, descriptions, Open Graph metadata, sitemap,
  robots file, and 404 page are generated.
- Internal links and local assets pass the current automated check.

Remaining:

- Implement redirects in the selected hosting platform.
- Review titles and descriptions after all event pages are migrated.
- Decide whether the old `.com` domain redirects to the new site or remains
  available as an archive.

## Phase 7: Accessibility, Performance, and Quality Checks — In Progress

Accessibility checks:

- Correct document language.
- Logical heading hierarchy.
- Keyboard-operable navigation.
- Keyboard-operable image enlargement with visible controls and managed focus.
- Visible focus styles.
- Sufficient color contrast.
- Descriptive link text.
- Meaningful image alternative text.
- Decorative images hidden from assistive technology.
- Respect for reduced-motion preferences.

Performance checks:

- No unnecessary client-side framework or JavaScript.
- Responsive image dimensions and formats.
- Gallery thumbnails open a larger local image without requiring JavaScript.
- No render-blocking third-party assets.
- Self-host required assets.
- Minimize cumulative layout shift.

Content and technical checks:

- Validate generated HTML.
- Check all internal links and local assets.
- Check external links and label obsolete ones.
- Check all 40 migration decisions against the inventory.

Deliverables:

- Documented quality-check results.
- No critical accessibility, link, or layout defects.

Current status:

- Automated build, internal-link, local-asset, title, and single-`h1` checks
  pass.
- Primary navigation works without JavaScript.
- Image enlargement works as normal links without JavaScript.
- Gallery links are progressively enhanced with a native dialog lightbox,
  visible controls, Escape handling, arrow-key navigation, and focus return.

Remaining:

- Complete manual keyboard and screen-reader testing of the lightbox.
- Run HTML validation and accessibility audits.
- Test navigation and image enlargement using only a keyboard.
- Test representative pages with a screen reader.
- Check color contrast and reduced-motion behavior.
- Audit all external links.
- Review performance, image sizes, and cumulative layout shift.
- Test layouts at representative phone, tablet, and desktop widths.
- Compare all 40 migration decisions with the final generated site.

## Definition of Done

The migration is complete when:

- The new site is generated entirely from `risbergetfinnskogen.no/`.
- A clean install and build succeeds using documented commands.
- Shared layouts eliminate repeated site-wide markup.
- Every archived page has a recorded migration decision.
- All retained content and images are local to the new project.
- The new site contains no One.com runtime dependency.
- Internal links and assets pass automated checks.
- Old public URLs have an intentional redirect or archive strategy.
- The site is responsive, keyboard accessible, and usable without JavaScript.

## First Implementation Milestone — Complete

Build a vertical slice containing:

1. Eleventy configuration.
2. Base layout, navigation, footer, and core CSS.
3. The homepage.
4. One text-heavy history page.
5. One image-gallery page.
6. One annual-report index and detail page.

This milestone will validate the content model, layouts, image handling, and URL conventions before migrating the remaining pages.

## Remaining Implementation Sequence

1. Complete metadata, external-link, accessibility, responsive-layout, and
   performance reviews.
2. Confirm or replace the archived association mailbox, board details,
   membership fee, and payment instructions after launch ownership is settled.
3. Configure and test the 40 permanent redirects on the chosen host.
4. Document deployment and perform a clean `npm ci` production build.
5. Perform final launch checks and decide the old `.com` domain strategy.
