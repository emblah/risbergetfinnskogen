# Repository Guidelines

## Project Structure & Module Organization

This repository contains an Eleventy 3 static site. Author source files under
`src/`; treat `docs/` as generated GitHub Pages output and never edit it
directly. Development builds output to `_site`.

- `src/pages/`: Markdown and Nunjucks content pages
- `src/_includes/`: shared layouts and components
- `src/_data/`: site, navigation, redirect, and gallery data
- `src/assets/`: CSS, JavaScript, images, and downloadable documents
- `scripts/check-site.py`: generated-site validation
- `eleventy.config.js`: Eleventy input, output, and passthrough configuration

Use Markdown for text-heavy pages and Nunjucks when substantial HTML or
templating is required.

## Build, Test, and Development Commands

- `npm install`: install the pinned development dependencies. Node.js 20 or
  newer is required.
- `npm start`: run Eleventy’s development server at `http://localhost:8080/`. Outputs files to `_site`.
- `npm run build`: generate the production site in `docs/` with the GitHub
  Pages path prefix, then run validation.
- `npm run check`: validate the existing `docs/` output without rebuilding it.

Always run `npm run build` before submitting a change.
