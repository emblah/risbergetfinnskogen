# risbergetfinnskogen.no

Eleventy source for the rebuilt Risberget website. The archived One.com site in
the repository root remains the migration source and must not be edited as part
of this project.

## Requirements

- Node.js 20 or newer
- npm

## Development

```sh
npm install
npm start
```

Eleventy serves the site at `http://localhost:8080/`.

## Production build

```sh
npm run build
```

The generated static site is written to `docs/` with the
`/risbergetfinnskogen/` path prefix required by GitHub Pages.

The /docs directory is hosted on GitHub Pages.

## Content migration

- Shared site data is under `src/_data/`.
- Reusable templates are under `src/_includes/`.
- Migrated content pages are under `src/pages/`.
- Cleaned, renamed assets belong under `src/assets/`.
- Old-to-new URL decisions are recorded in `src/_data/redirects.json`.
- Unresolved source-content problems are recorded in
  `docs/editorial-issues.md`.
