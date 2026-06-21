# risbergetfinnskogen.no

Eleventy source for the rebuilt Risberget Finnskogen website. 

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

Commit and push changes and the GitHub Page will be updated in a few minutes.

## Content migration

- Shared site data is under `src/_data/`.
- Reusable templates are under `src/_includes/`.
- Migrated content pages are under `src/pages/`.
- Cleaned, renamed assets belong under `src/assets/`.
- Old-to-new URL decisions are recorded in `src/_data/redirects.json`.
