import { chromium } from 'playwright';
import fs from 'node:fs';

const BASE = 'http://127.0.0.1:4321';
const OUT = 'screenshots';
const results = { errors: [], shots: [], overflow: [], images: [], tapTargets: [], jsDisabled: null, anchors: [] };

let browser;
try {
  browser = await chromium.launch({ channel: 'chrome' });
} catch (err) {
  console.log('chrome channel failed, falling back to bundled chromium:', err.message);
  browser = await chromium.launch();
}

async function prepare(page) {
  await page.evaluate(async () => {
    if (document.fonts) await document.fonts.ready;
    for (const img of document.images) img.loading = 'eager';
    await Promise.all([...document.images].map((img) => img.complete
      ? Promise.resolve()
      : new Promise((resolve) => {
          img.addEventListener('load', resolve, { once: true });
          img.addEventListener('error', resolve, { once: true });
        })));
    window.scrollTo(0, document.body.scrollHeight);
    await new Promise((r) => setTimeout(r, 300));
    window.scrollTo(0, 0);
  });
  await page.waitForTimeout(400);
}

async function audit(page, label, width) {
  const overflow = await page.evaluate(() => {
    const doc = document.documentElement;
    const bad = [];
    for (const el of document.querySelectorAll('body *')) {
      const r = el.getBoundingClientRect();
      if (r.width > 0 && (r.right > window.innerWidth + 1 || r.left < -1)) {
        if (getComputedStyle(el).position === 'fixed') continue;
        bad.push({ tag: el.tagName, cls: String(el.className).slice(0, 40), right: Math.round(r.right), left: Math.round(r.left) });
      }
    }
    return { scrollWidth: doc.scrollWidth, innerWidth: window.innerWidth, bad: bad.slice(0, 10) };
  });
  results.overflow.push({ label, width, ...overflow });

  const imgs = await page.evaluate(() => [...document.images].map((i) => ({
    src: i.currentSrc.split('/').pop(),
    ok: i.complete && i.naturalWidth > 0,
    alt: i.alt,
    width: i.getAttribute('width'),
    height: i.getAttribute('height'),
  })));
  results.images.push({ label, imgs });

  if (width <= 390) {
    const small = await page.evaluate(() => [...document.querySelectorAll('a, button')]
      .filter((el) => {
        const r = el.getBoundingClientRect();
        const cs = getComputedStyle(el);
        return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && (r.height < 44 || r.width < 44);
      })
      .map((el) => ({
        text: (el.textContent || '').trim().slice(0, 30),
        h: Math.round(el.getBoundingClientRect().height),
        w: Math.round(el.getBoundingClientRect().width),
      }))
      .slice(0, 20));
    results.tapTargets.push({ label, small });
  }
}

const cases = [
  ['en', '/', 1440, 900],
  ['en', '/', 1024, 900],
  ['en', '/', 768, 900],
  ['en', '/', 390, 844],
  ['zh', '/zh/', 1440, 900],
  ['zh', '/zh/', 390, 844],
  ['fr', '/fr/', 1440, 900],
  ['fr', '/fr/', 390, 844],
];

for (const [locale, path, width, height] of cases) {
  const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
  page.on('console', (msg) => { if (msg.type() === 'error') results.errors.push({ label: `${locale}-${width}`, text: msg.text() }); });
  page.on('pageerror', (err) => results.errors.push({ label: `${locale}-${width}`, text: err.message }));
  await page.goto(BASE + path, { waitUntil: 'networkidle' });
  await prepare(page);
  await page.evaluate(() => { const h = document.querySelector('.site-header'); if (h) h.style.position = 'static'; });
  await page.waitForTimeout(100);
  await audit(page, `${locale}-${width}`, width);
  await page.screenshot({ path: `${OUT}/${locale}-${width}.png`, fullPage: true });
  results.shots.push(`${locale}-${width}.png`);
  await page.close();
}

const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
const p1 = await ctx.newPage();
await p1.goto(BASE + '/zh/#about', { waitUntil: 'networkidle' });
results.anchors.push({
  from: '/zh/#about',
  en: await p1.getAttribute('.langs a[data-base="/"]', 'href'),
  fr: await p1.getAttribute('.langs a[data-base="/fr/"]', 'href'),
});
await p1.close();
await ctx.close();

const nojs = await browser.newContext({ viewport: { width: 390, height: 844 }, javaScriptEnabled: false });
const p2 = await nojs.newPage();
await p2.goto(BASE + '/', { waitUntil: 'load' });
const text = await p2.locator('body').innerText();
results.jsDisabled = {
  hasVulcan: text.includes('Vulcan'),
  hasSencillo: text.includes('Sencillo'),
  hasEmail: text.includes('Robusr@outlook.com'),
  sections: await p2.locator('section').count(),
};
await p2.screenshot({ path: `${OUT}/en-390-nojs.png`, fullPage: true });
await nojs.close();

await browser.close();
fs.writeFileSync('qa/capture-report.json', JSON.stringify(results, null, 2));
console.log(JSON.stringify({
  errors: results.errors,
  overflow: results.overflow.map((o) => ({ label: o.label, overflow: o.scrollWidth > o.innerWidth, bad: o.bad.length })),
  images: results.images.map((im) => ({ label: im.label, allLoaded: im.imgs.every((i) => i.ok) })),
  tapTargets: results.tapTargets,
  jsDisabled: results.jsDisabled,
  anchors: results.anchors,
  shots: results.shots,
}, null, 2));
