#!/usr/bin/env node
/**
 * Reference audit for public/assets.
 *
 * - Fails on referenced assets that do not exist (always).
 * - Reports unreferenced files; --strict also fails on them.
 *
 * References are collected conservatively from source, data, scripts, and
 * docs so a build-time-only path is not mistaken for an orphan.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const publicDir = path.join(root, 'public');
const assetsDir = path.join(publicDir, 'assets');
const strict = process.argv.includes('--strict');
const asJson = process.argv.includes('--json');

const REFERENCE_ROOTS = [
  'src',
  'functions',
  'scripts',
  'content',
  'public',
  'README.md',
  'README.zh.md',
  'README.fr.md',
  'QA.md',
  'DEPLOY.md',
  'astro.config.mjs',
];
const TEXT_EXT = new Set([
  '.astro', '.css', '.html', '.js', '.json', '.jsx', '.md', '.mjs', '.ts',
  '.tsx', '.txt', '.xml', '.yaml', '.yml',
]);
const SKIP_DIRS = new Set(['node_modules', 'dist', '.astro', '.git', 'assets']);

function walk(dir, out = []) {
  if (!fs.existsSync(dir)) return out;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name === '.DS_Store') continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (SKIP_DIRS.has(entry.name)) continue;
      walk(full, out);
    } else if (entry.isFile()) {
      out.push(full);
    }
  }
  return out;
}

const assetFiles = walk(assetsDir);
const assetSet = new Set(assetFiles.map((file) => `/${path.relative(publicDir, file).split(path.sep).join('/')}`));

const referenceFiles = [];
for (const rel of REFERENCE_ROOTS) {
  const full = path.join(root, rel);
  if (!fs.existsSync(full)) continue;
  const stat = fs.statSync(full);
  if (stat.isDirectory()) referenceFiles.push(...walk(full));
  else referenceFiles.push(full);
}

const references = new Map();
const baseReferences = new Map();
const assetPattern = /\/assets\/[A-Za-z0-9._~%/+-]+/g;
for (const file of referenceFiles) {
  if (!TEXT_EXT.has(path.extname(file))) continue;
  const text = fs.readFileSync(file, 'utf8');
  for (const raw of text.match(assetPattern) ?? []) {
    const ref = raw.replace(/[.,;:!?)\]}'"]+$/, '');
    if (!ref || ref.includes('*') || ref.includes('$')) continue;
    if (ref.endsWith('/')) continue; // directory mention, not a file
    if (!path.posix.extname(ref)) {
      // A basename used to build responsive variants, e.g. /assets/lab/minilab.
      if (!baseReferences.has(ref)) baseReferences.set(ref, new Set());
      baseReferences.get(ref).add(path.relative(root, file));
      continue;
    }
    if (!references.has(ref)) references.set(ref, new Set());
    references.get(ref).add(path.relative(root, file));
  }
}

const missing = [...references.keys()].filter((ref) => !assetSet.has(ref)).sort();
const coveredByBase = (ref) => [...baseReferences.keys()].some((base) =>
  ref === base || ref.startsWith(`${base}-`) || ref.startsWith(`${base}.`));
const orphans = [...assetSet].filter((ref) => !references.has(ref) && !coveredByBase(ref)).sort();
const orphanBytes = orphans.reduce((sum, ref) => {
  const file = path.join(publicDir, ref.slice(1));
  return sum + (fs.existsSync(file) ? fs.statSync(file).size : 0);
}, 0);

const report = {
  referenced: references.size + baseReferences.size,
  files: assetSet.size,
  missing,
  orphans,
  orphanBytes,
  strict,
};

if (asJson) {
  console.log(JSON.stringify(report, null, 2));
} else {
  console.log(`assets: ${assetSet.size} files, ${references.size + baseReferences.size} referenced paths`);
  if (missing.length) {
    console.error(`\nmissing referenced assets (${missing.length}):`);
    for (const ref of missing) {
      console.error(`  ${ref}`);
      for (const source of references.get(ref)) console.error(`    from ${source}`);
    }
  }
  if (orphans.length) {
    console.log(`\nunreferenced assets (${orphans.length}, ${(orphanBytes / 1024 / 1024).toFixed(2)} MB):`);
    for (const ref of orphans) console.log(`  ${ref}`);
    console.log('  (run with --strict to make these fail; delete only after review)');
  }
  if (!missing.length && !orphans.length) console.log('\nno missing or unreferenced assets');
}

const failed = missing.length > 0 || (strict && orphans.length > 0);
process.exit(failed ? 1 : 0);
