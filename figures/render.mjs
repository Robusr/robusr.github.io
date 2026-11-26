import { chromium } from 'playwright-core';
import fs from 'fs';
import path from 'path';

const chrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const root = '/Users/robusr/Desktop/Redraw/robusr.github.io';
const outDir = path.join(root, 'figures/render');
fs.mkdirSync(outDir, { recursive: true });

const names = process.argv.slice(2);
const targets = names.length ? names : ['vulcan-a', 'vulcan-b', 'vulcan-c', 'vulcan-d'];

const browser = await chromium.launch({ executablePath: chrome, headless: true });
for (const name of targets) {
  const svg = fs.readFileSync(path.join(root, 'figures/src', `${name}.svg`), 'utf8')
    .replace(/^<\?xml[^>]*>\s*/, '');
  const html = `<!doctype html><html><head><meta charset="utf-8"><style>
    @font-face { font-family: Inter; src: url('/figures/fonts/inter-latin-wght-normal.woff2') format('woff2'); font-weight: 100 900; font-style: normal; }
    html, body { margin: 0; background: #FBFBF9; }
    #stage { width: 1600px; height: 900px; overflow: hidden; }
    #stage svg { display: block; width: 1600px; height: 900px; }
  </style></head><body><div id="stage">${svg}</div></body></html>`;
  fs.writeFileSync(path.join(outDir, `${name}.html`), html);
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1 });
  await page.goto(`http://127.0.0.1:8789/figures/render/${name}.html`, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(250);
  await page.screenshot({ path: path.join(outDir, `${name}.png`) });
  console.log('rendered', name);
  await page.close();
}
await browser.close();
