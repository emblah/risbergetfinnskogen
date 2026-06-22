#!/usr/bin/env node

/**
 * Check generated HTML for broken local links and basic document structure.
 */

import fs from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";

import { parse } from "parse5";

function usage() {
  return [
    "Usage: node scripts/check-site.js --site-root <directory> --path-prefix <prefix>",
    "",
    "Options:",
    "  --site-root     Generated site directory, relative to the working directory",
    "  --path-prefix   URL path prefix used by the generated site; use / for none",
  ].join("\n");
}

function readOptions() {
  let values;
  try {
    ({ values } = parseArgs({
      options: {
        "site-root": { type: "string" },
        "path-prefix": { type: "string" },
        help: { type: "boolean", short: "h" },
      },
      strict: true,
    }));
  } catch (error) {
    throw new Error(`${error.message}\n\n${usage()}`);
  }

  if (values.help) {
    console.log(usage());
    return null;
  }
  if (!values["site-root"] || values["path-prefix"] === undefined) {
    throw new Error(`Both --site-root and --path-prefix are required.\n\n${usage()}`);
  }

  const pathPrefix =
    values["path-prefix"] === "/"
      ? ""
      : `/${values["path-prefix"].replace(/^\/+|\/+$/g, "")}`;

  return {
    siteRoot: path.resolve(values["site-root"]),
    pathPrefix,
  };
}

function findHtmlFiles(directory) {
  const files = [];

  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const entryPath = path.join(directory, entry.name);
    if (entry.isDirectory()) {
      files.push(...findHtmlFiles(entryPath));
    } else if (entry.isFile() && entry.name.endsWith(".html")) {
      files.push(entryPath);
    }
  }

  return files.sort();
}

function inspectDocument(html) {
  const references = [];
  const titleText = [];
  let h1Count = 0;

  function visit(node, insideTitle = false) {
    const collectingTitle = insideTitle || node.tagName === "title";

    if (node.tagName === "h1") {
      h1Count += 1;
    }

    for (const attribute of node.attrs ?? []) {
      if ((attribute.name === "href" || attribute.name === "src") && attribute.value) {
        references.push([attribute.name, attribute.value]);
      }
    }

    if (collectingTitle && node.nodeName === "#text") {
      titleText.push(node.value);
    }

    for (const child of node.childNodes ?? []) {
      visit(child, collectingTitle);
    }
  }

  visit(parse(html));
  return { h1Count, references, title: titleText.join(" ").trim() };
}

function targetPath(source, reference, siteRoot, pathPrefix) {
  if (
    reference.startsWith("#") ||
    reference.startsWith("//") ||
    /^[a-z][a-z\d+.-]*:/i.test(reference)
  ) {
    return null;
  }

  const encodedPath = reference.split(/[?#]/, 1)[0];
  if (!encodedPath) {
    return null;
  }

  let referencePath;
  try {
    referencePath = decodeURIComponent(encodedPath);
  } catch {
    referencePath = encodedPath;
  }

  let target;
  if (referencePath.startsWith("/")) {
    if (pathPrefix && referencePath === pathPrefix) {
      referencePath = "/";
    } else if (pathPrefix && referencePath.startsWith(`${pathPrefix}/`)) {
      referencePath = referencePath.slice(pathPrefix.length);
    }
    target = path.join(siteRoot, referencePath.replace(/^\/+/, ""));
  } else {
    target = path.join(path.dirname(source), referencePath);
  }

  if (referencePath.endsWith("/")) {
    target = path.join(target, "index.html");
  }
  return target;
}

function quote(value) {
  return `'${value.replaceAll("\\", "\\\\").replaceAll("'", "\\'")}'`;
}

function main() {
  let options;
  try {
    options = readOptions();
  } catch (error) {
    console.error(error.message);
    return 1;
  }
  if (options === null) {
    return 0;
  }

  const { pathPrefix, siteRoot } = options;
  if (!fs.existsSync(siteRoot)) {
    console.error(`Missing site root: ${siteRoot}`);
    return 1;
  }

  const errors = [];
  const htmlFiles = findHtmlFiles(siteRoot);

  for (const source of htmlFiles) {
    const document = inspectDocument(fs.readFileSync(source, "utf8"));
    const relativeSource = path.relative(siteRoot, source);

    if (document.h1Count !== 1) {
      errors.push(`${relativeSource}: expected one h1, found ${document.h1Count}`);
    }
    if (!document.title) {
      errors.push(`${relativeSource}: missing document title`);
    }

    for (const [attribute, reference] of document.references) {
      const target = targetPath(source, reference, siteRoot, pathPrefix);
      if (target !== null && !fs.existsSync(target)) {
        errors.push(
          `${relativeSource}: broken ${attribute}=${quote(reference)} ` +
            `(expected ${path.relative(siteRoot, target)})`,
        );
      }
    }
  }

  if (errors.length > 0) {
    console.error(errors.join("\n"));
    return 1;
  }

  console.log(
    `Checked ${htmlFiles.length} HTML files; no broken local links or heading errors.`,
  );
  return 0;
}

process.exitCode = main();
