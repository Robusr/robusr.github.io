import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const errors = [];
const locales = ['en', 'zh', 'fr'];

const read = (file) => JSON.parse(fs.readFileSync(path.join(root, file), 'utf8'));
const exists = (file) => fs.existsSync(path.join(root, file));
const isLocalized = (value) =>
  value && locales.every((locale) => typeof value[locale] === 'string' && value[locale].trim().length > 0);
const isIsoDate = (value) => typeof value === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(value) && !Number.isNaN(Date.parse(value));
const isIsoTimestamp = (value) => typeof value === 'string' && /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$/.test(value) && !Number.isNaN(Date.parse(value));

function keyPaths(value, prefix = '') {
  if (value === null || typeof value !== 'object' || Array.isArray(value)) return [prefix];
  return Object.keys(value).flatMap((key) => keyPaths(value[key], prefix ? `${prefix}.${key}` : key));
}

const i18n = Object.fromEntries(locales.map((locale) => [locale, read(`src/i18n/${locale}.json`)]));
const enKeys = keyPaths(i18n.en).sort();

for (const locale of ['zh', 'fr']) {
  const keys = keyPaths(i18n[locale]).sort();
  const missing = enKeys.filter((key) => !keys.includes(key));
  const extra = keys.filter((key) => !enKeys.includes(key));
  if (missing.length) errors.push(`${locale}.json missing keys: ${missing.join(', ')}`);
  if (extra.length) errors.push(`${locale}.json extra keys: ${extra.join(', ')}`);
}

const profile = read('src/data/profile.json');
for (const field of ['name', 'label', 'positioning', 'intro', 'status', 'location', 'lastUpdated']) {
  if (!isLocalized(profile[field])) errors.push(`profile.${field} must have en, zh, and fr strings`);
}
for (const locale of locales) {
  if (!Array.isArray(profile.about?.[locale]) || profile.about[locale].length < 1 || profile.about[locale].length > 3) {
    errors.push(`profile.about.${locale} must contain one to three paragraphs`);
  }
  if (!profile.portrait?.alt?.[locale]) errors.push(`profile.portrait.alt.${locale} is missing`);
}
for (const key of ['webp', 'webpSmall', 'jpg']) {
  if (!exists(`public${profile.portrait[key]}`)) errors.push(`portrait file missing: ${profile.portrait[key]}`);
}
for (const field of ['snapshotDate', 'contentDate']) {
  if (!isIsoDate(profile[field])) errors.push(`profile.${field} must be an ISO date`);
}
if (isIsoDate(profile.snapshotDate) && isIsoDate(profile.contentDate) && profile.contentDate < profile.snapshotDate) {
  errors.push('profile.contentDate must not precede snapshotDate');
}
for (const asset of ['robusr-ip-v2.webp', 'robusr-ip-480.webp', 'robusr-standing.webp', 'robusr-standing-640.webp']) {
  if (!exists(`public/assets/brand/${asset}`)) errors.push(`background art missing: ${asset}`);
}

const miniLab = read('src/data/mini-lab.json');
for (const field of ['title', 'caption', 'alt']) {
  if (!isLocalized(miniLab[field])) errors.push(`mini-lab.${field} must have en, zh, and fr strings`);
}
if (!/^\/assets\/lab\/[A-Za-z0-9-]+$/.test(miniLab.image?.base ?? '')) {
  errors.push('mini-lab.image.base must point into /assets/lab/');
}
for (const suffix of ['-480.webp', '-960.webp', '-1440.webp', '-1440.jpg']) {
  if (!exists(`public${miniLab.image?.base}${suffix}`)) errors.push(`mini lab image missing: ${miniLab.image?.base}${suffix}`);
}
if (!Number.isInteger(miniLab.image?.width) || !Number.isInteger(miniLab.image?.height)) {
  errors.push('mini-lab.image.width and height must be integers');
}

const projects = read('src/data/projects.json');
const github = read('src/data/github.json');
if (!isIsoTimestamp(github.fetchedAt)) errors.push('github.fetchedAt must be an ISO timestamp');
if (projects.length !== 5) errors.push(`projects.json must contain five projects, found ${projects.length}`);
const orders = projects.map((project) => project.order).sort((a, b) => a - b).join(',');
if (orders !== '1,2,3,4,5') errors.push(`project order must be 1..5, found ${orders}`);
for (const project of projects) {
  const id = project.id ?? project.name;
  for (const field of ['category', 'tagline', 'summary', 'evidence', 'alt']) {
    if (!isLocalized(project[field])) errors.push(`${id}.${field} must have en, zh, and fr strings`);
  }
  if (!i18n.en.status?.[project.statusKey]) errors.push(`${id} uses unknown statusKey: ${project.statusKey}`);
  if (!i18n.en.exit?.[project.exitKey]) errors.push(`${id} uses unknown exitKey: ${project.exitKey}`);
  if (!/^https:\/\//.test(project.href ?? '')) errors.push(`${id}.href must be an absolute https URL`);
  if (project.repo !== null && !/^[A-Za-z0-9_.-]+$/.test(project.repo ?? '')) {
    errors.push(`${id}.repo must be null or a GitHub repository name`);
  }
  if (project.repo) {
    const stats = github.repos?.[project.repo];
    if (!stats) {
      errors.push(`github.json missing featured repository: ${project.repo}`);
    } else {
      if (!Number.isInteger(stats.stars) || stats.stars < 0) errors.push(`github ${project.repo}.stars must be a non-negative integer`);
      if (!Number.isInteger(stats.forks) || stats.forks < 0) errors.push(`github ${project.repo}.forks must be a non-negative integer`);
      if (!isIsoTimestamp(stats.pushedAt)) errors.push(`github ${project.repo}.pushedAt must be an ISO timestamp`);
      if (stats.release) {
        if (typeof stats.release.tag !== 'string' || !stats.release.tag.trim()) {
          errors.push(`github ${project.repo}.release.tag is required`);
        }
        if (!/^https:\/\//.test(stats.release.url ?? '')) {
          errors.push(`github ${project.repo}.release.url must be an absolute https URL`);
        }
      }
    }
  }
  for (const suffix of ['-480.webp', '-960.webp', '-960.jpg']) {
    if (!exists(`public${project.image}${suffix}`)) errors.push(`${id} image missing: ${project.image}${suffix}`);
  }
}

const timeline = read('src/data/timeline.json');
if (timeline.length !== 6) errors.push(`timeline.json must contain six rows, found ${timeline.length}`);
for (const row of timeline) {
  if (!/^\d{4}(–\d{4})?$/.test(row.year)) errors.push(`timeline year format: ${row.year}`);
  if (!isLocalized(row.event)) errors.push(`timeline ${row.year} event must have en, zh, and fr strings`);
}

const awards = read('src/data/awards.json');
if (awards.length !== 3) errors.push(`awards.json must contain three rows, found ${awards.length}`);
for (const award of awards) {
  if (!isLocalized(award.title)) errors.push(`award ${award.year} title must have en, zh, and fr strings`);
  if (!isLocalized(award.detail)) errors.push(`award ${award.year} detail must have en, zh, and fr strings`);
  if (award.href && !/^https:\/\//.test(award.href)) errors.push(`award ${award.year} href must be https`);
}

const moreWork = read('src/data/more-work.json');
if (moreWork.length !== 4) errors.push(`more-work.json must contain four items, found ${moreWork.length}`);
for (const item of moreWork) {
  if (!isLocalized(item.desc)) errors.push(`${item.name} desc must have en, zh, and fr strings`);
  if (!isLocalized(item.meta)) errors.push(`${item.name} meta must have en, zh, and fr strings`);
  if (!/^https:\/\//.test(item.href ?? '')) errors.push(`${item.name}.href must be an absolute https URL`);
  const repo = /^https:\/\/github\.com\/Robusr\/([^/?#]+)\/?$/.exec(item.href ?? '')?.[1];
  if (repo && !github.repos?.[repo]) errors.push(`github.json missing repository for more-work item ${item.name}: ${repo}`);
}

if (errors.length) {
  console.error(`Content check failed with ${errors.length} issue(s):`);
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}

console.log(`Content check passed: 3 locales, ${projects.length} projects, ${timeline.length} timeline rows, ${awards.length} awards, ${moreWork.length} more-work items, ${Object.keys(github.repos ?? {}).length} GitHub repositories.`);
