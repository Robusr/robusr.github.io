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
  if (!Array.isArray(profile.about?.[locale]) || profile.about[locale].length !== 2) {
    errors.push(`profile.about.${locale} must contain two paragraphs`);
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
for (const asset of ['robusr-ip-v2.webp', 'robusr-ip-480.webp', 'robusr-standing.webp']) {
  if (!exists(`public/assets/brand/${asset}`)) errors.push(`background art missing: ${asset}`);
}

const projects = read('src/data/projects.json');
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
if (moreWork.length !== 6) errors.push(`more-work.json must contain six items, found ${moreWork.length}`);
for (const item of moreWork) {
  if (!isLocalized(item.desc)) errors.push(`${item.name} desc must have en, zh, and fr strings`);
  if (!isLocalized(item.meta)) errors.push(`${item.name} meta must have en, zh, and fr strings`);
  if (!/^https:\/\//.test(item.href ?? '')) errors.push(`${item.name}.href must be an absolute https URL`);
}

if (errors.length) {
  console.error(`Content check failed with ${errors.length} issue(s):`);
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}

console.log(`Content check passed: 3 locales, ${projects.length} projects, ${timeline.length} timeline rows, ${awards.length} awards, ${moreWork.length} more-work items.`);
