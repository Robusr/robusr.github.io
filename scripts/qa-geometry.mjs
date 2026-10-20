import { chromium } from 'playwright';
import fs from 'node:fs';

const browser = await chromium.launch({ channel: 'chrome' });
const out = {};
for (const [label, path] of [['en', '/'], ['zh', '/zh/']]) {
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto('http://127.0.0.1:4321' + path, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(200);
  out[label] = await page.evaluate(() => {
    const q = (sel) => {
      const el = document.querySelector(sel);
      if (!el) return null;
      const r = el.getBoundingClientRect();
      const cs = getComputedStyle(el);
      return {
        sel,
        top: Math.round(r.top + scrollY),
        bottom: Math.round(r.bottom + scrollY),
        height: Math.round(r.height),
        position: cs.position,
        zIndex: cs.zIndex,
        background: cs.backgroundColor,
      };
    };
    const h1 = document.querySelector('h1');
    const r = h1.getBoundingClientRect();
    const hit = document.elementFromPoint(r.left + 10, Math.max(r.top + 10, 1));
    return {
      scrollY,
      docHeight: document.documentElement.scrollHeight,
      elements: ['.site-header', '.header-inner', '.brand', '.site-nav', '.langs', '.hero', '.hero .eyebrow', 'h1', '.lang-hint'].map(q),
      h1Top: Math.round(r.top),
      elementAtH1Top: hit ? `${hit.tagName}.${String(hit.className).slice(0, 30)}` : null,
    };
  });
  await page.screenshot({ path: `screenshots/${label}-1440-viewport.png` });
  await page.evaluate(() => { const h = document.querySelector('.site-header'); if (h) h.style.position = 'static'; });
  await page.screenshot({ path: `screenshots/${label}-1440-no-sticky.png`, fullPage: true });
  await page.close();
}
await browser.close();
fs.writeFileSync('qa/geometry.json', JSON.stringify(out, null, 2));
console.log(JSON.stringify(out, null, 2));
