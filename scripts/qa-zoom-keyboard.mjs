import { chromium } from 'playwright';
import fs from 'node:fs';

const browser = await chromium.launch({ channel: 'chrome' });
const out = {};

// 200% browser zoom proxy: 720 CSS px on a 1440 device
const zoom = await browser.newPage({ viewport: { width: 720, height: 450 } });
await zoom.goto('http://127.0.0.1:4321/', { waitUntil: 'networkidle' });
await zoom.evaluate(() => document.fonts.ready);
const zoomMetrics = await zoom.evaluate(() => ({
  scrollWidth: document.documentElement.scrollWidth,
  innerWidth: window.innerWidth,
  scrollHeight: document.documentElement.scrollHeight,
  overflow: document.documentElement.scrollWidth > window.innerWidth,
}));
await zoom.screenshot({ path: 'screenshots/en-720-zoom-200.png', fullPage: true });
out.zoom200 = zoomMetrics;
await zoom.close();

// Keyboard walk
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
await page.goto('http://127.0.0.1:4321/', { waitUntil: 'networkidle' });
const stops = [];
for (let i = 0; i < 14; i++) {
  await page.keyboard.press('Tab');
  stops.push(await page.evaluate(() => {
    const el = document.activeElement;
    const cs = getComputedStyle(el);
    return {
      tag: el.tagName,
      text: (el.textContent || '').trim().slice(0, 28),
      href: el.getAttribute('href'),
      outline: cs.outlineStyle !== 'none' && cs.outlineWidth !== '0px',
    };
  }));
}
out.keyboard = stops;
await page.close();

await browser.close();
fs.writeFileSync('qa/zoom-keyboard.json', JSON.stringify(out, null, 2));
console.log(JSON.stringify(out, null, 2));
