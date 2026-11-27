#!/usr/bin/env node
/**
 * Copy selected plate files to a new immutable version directory and point
 * project-figures.json at the copies.
 *
 * Example:
 *   node scripts/version-plate.mjs --from v2 --to v3 --prefix onesarm-b --prefix onesarm-c
 *
 * Existing target files are left alone unless --force is passed. No files are
 * deleted. Use --dry-run to preview.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const platesDir = path.join(root, 'public/assets/projects/plates');
const dataFile = path.join(root, 'src/data/project-figures.json');

const args = process.argv.slice(2);
const value = (name) => {
  const i = args.indexOf(name);
  return i >= 0 ? args[i + 1] : undefined;
};
const from = value('--from');
const to = value('--to');
const force = args.includes('--force');
const dryRun = args.includes('--dry-run');
const prefixes = [];
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--prefix' && args[i + 1]) prefixes.push(args[i + 1]);
  if (args[i].startsWith('--prefix=')) prefixes.push(args[i].slice('--prefix='.length));
}

if (!from || !to || !prefixes.length) {
  console.error('usage: node scripts/version-plate.mjs --from v2 --to v3 --prefix onesarm-b [--prefix ...] [--force] [--dry-run]');
  process.exit(2);
}
for (const version of [from, to]) {
  if (!/^[a-z0-9][a-z0-9-]*$/.test(version)) {
    console.error(`invalid version: ${version}`);
    process.exit(2);
  }
}
if (from === to) {
  console.error('--from and --to must differ');
  process.exit(2);
}

const fromDir = path.join(platesDir, from);
const toDir = path.join(platesDir, to);
if (!fs.existsSync(fromDir)) {
  console.error(`missing source directory: ${path.relative(root, fromDir)}`);
  process.exit(1);
}
const matches = fs.readdirSync(fromDir)
  .filter((name) => fs.statSync(path.join(fromDir, name)).isFile())
  .filter((name) => prefixes.some((prefix) => name.startsWith(prefix)))
  .sort();
if (!matches.length) {
  console.error(`no files in ${from} match: ${prefixes.join(', ')}`);
  process.exit(1);
}

if (!dryRun) fs.mkdirSync(toDir, { recursive: true });
const copied = [];
const existing = [];
for (const name of matches) {
  const source = path.join(fromDir, name);
  const target = path.join(toDir, name);
  if (fs.existsSync(target) && !force) {
    existing.push(name);
    continue;
  }
  if (!dryRun) fs.copyFileSync(source, target);
  copied.push(name);
}

const available = new Set([...copied, ...existing]);
const data = JSON.parse(fs.readFileSync(dataFile, 'utf8'));
const oldPrefix = `/assets/projects/plates/${from}/`;
const newPrefix = `/assets/projects/plates/${to}/`;
let rewritten = 0;
const visit = (node) => {
  if (Array.isArray(node)) return node.map(visit);
  if (node && typeof node === 'object') {
    for (const key of Object.keys(node)) node[key] = visit(node[key]);
    return node;
  }
  if (typeof node === 'string' && node.startsWith(oldPrefix)) {
    const name = node.slice(oldPrefix.length);
    if (available.has(name)) {
      rewritten++;
      return newPrefix + name;
    }
  }
  return node;
};
const next = visit(data);
if (!dryRun && rewritten) fs.writeFileSync(dataFile, `${JSON.stringify(next, null, 2)}\n`);

console.log(`from ${from} to ${to}`);
console.log(`copied ${copied.length}${dryRun ? ' (dry run)' : ''}${existing.length ? `, kept ${existing.length} existing` : ''}`);
for (const name of copied) console.log(`  + ${name}`);
for (const name of existing) console.log(`  = ${name} (already exists)`);
console.log(`project-figures.json references ${dryRun ? 'would change' : 'changed'}: ${rewritten}`);
