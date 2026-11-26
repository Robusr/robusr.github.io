import { chromium } from 'playwright-core';
import fs from 'fs';
import path from 'path';
import { execFileSync } from 'child_process';

const chrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const root = '/Users/robusr/Desktop/Redraw/robusr.github.io';
const renderDir = path.join(root, 'figures/render');
const frameRoot = path.join(root, 'figures/frames');
const DURATION = 6.4, FPS = 25, POSTER_T = 5.2;
fs.mkdirSync(renderDir, { recursive: true });
fs.mkdirSync(frameRoot, { recursive: true });

function focus(name, count, times) {
  const t = {};
  for (let i = 1; i <= count; i++) {
    const on = times[i - 1][0], off = times[i - 1][1];
    t[`${name}-focus${i}`] = [{ t: 0, o: 0 }, { t: on, o: 1 }, { t: off, o: 0 }];
  }
  return t;
}

const JOBS = [
  { name: 'hsiwu-a', tl: focus('h-a', 4, [[0, 1.4], [1.4, 2.9], [2.9, 4.4], [4.4, 5.4]]) },
  { name: 'dustarrow-a', tl: focus('d-a', 3, [[0, 1.8], [1.8, 3.4], [3.4, 5.2]]) },
  { name: 'onesarm-a', tl: focus('o-a', 2, [[0, 2.2], [2.2, 4.6]]) },
  { name: 'sencillo-a', tl: focus('s-a', 3, [[0, 2.2], [2.2, 4.0], [4.0, 5.4]]) },
];

function htmlFor(svg, timeline) {
  return `<!doctype html><html><head><meta charset="utf-8"><style>
    @font-face { font-family: Inter; src: url('/figures/fonts/inter-latin-wght-normal.woff2') format('woff2'); font-weight: 100 900; font-style: normal; }
    html, body { margin: 0; background: #FBFBF9; }
    #stage { width: 1600px; height: 900px; overflow: hidden; }
    #stage svg { display: block; width: 1600px; height: 900px; }
  </style></head><body><div id="stage">${svg.replace(/^<\?xml[^>]*>\s*/, '')}</div>
  <script>
  const LAYERS = ${JSON.stringify(timeline)};
  const ease = u => u < 0.5 ? 2*u*u : 1 - Math.pow(-2*u+2, 2)/2;
  function val(keys, t, prop, dflt) {
    if (!keys.length) return dflt;
    if (t <= keys[0].t) return keys[0][prop] ?? dflt;
    if (t >= keys[keys.length-1].t) return keys[keys.length-1][prop] ?? dflt;
    let i = 0; while (i < keys.length-1 && keys[i+1].t < t) i++;
    const a = keys[i], b = keys[i+1];
    const pa = a[prop] ?? dflt, pb = b[prop] ?? pa;
    const u = (t - a.t) / Math.max(1e-6, b.t - a.t);
    return pa + (pb - pa) * ease(Math.min(1, Math.max(0, u)));
  }
  window.setTime = (t) => {
    for (const [id, keys] of Object.entries(LAYERS)) {
      const el = document.getElementById(id); if (!el) continue;
      el.style.opacity = String(val(keys, t, 'o', 1));
    }
  };
  window.setTime(0);
  </script></body></html>`;
}

const browser = await chromium.launch({ executablePath: chrome, headless: true });
for (const { name, tl } of JOBS) {
  const svg = fs.readFileSync(path.join(root, 'figures/src', `${name}.svg`), 'utf8');
  fs.writeFileSync(path.join(renderDir, `${name}.html`), htmlFor(svg, tl));
  const frameDir = path.join(frameRoot, name);
  fs.rmSync(frameDir, { recursive: true, force: true });
  fs.mkdirSync(frameDir, { recursive: true });
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1 });
  await page.goto(`http://127.0.0.1:8789/figures/render/${name}.html`, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(250);
  const total = Math.round(DURATION * FPS);
  for (let i = 0; i < total; i++) {
    await page.evaluate((t) => window.setTime(t), i / FPS);
    await page.waitForTimeout(12);
    await page.screenshot({ path: path.join(frameDir, `${String(i).padStart(4, '0')}.png`) });
  }
  await page.evaluate((t) => window.setTime(t), POSTER_T);
  await page.waitForTimeout(30);
  await page.screenshot({ path: path.join(renderDir, `${name}-poster.png`) });
  await page.close();
  const mp4 = path.join(renderDir, `${name}.mp4`);
  const webm = path.join(renderDir, `${name}.webm`);
  execFileSync('ffmpeg', ['-y', '-framerate', String(FPS), '-i', path.join(frameDir, '%04d.png'),
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '20', '-pix_fmt', 'yuv420p',
    '-movflags', '+faststart', '-an', mp4], { stdio: 'ignore' });
  execFileSync('ffmpeg', ['-y', '-framerate', String(FPS), '-i', path.join(frameDir, '%04d.png'),
    '-c:v', 'libvpx-vp9', '-crf', '36', '-b:v', '0', '-row-mt', '1', '-an', webm], { stdio: 'ignore' });
  console.log(name, 'frames', total, 'mp4', fs.statSync(mp4).size, 'webm', fs.statSync(webm).size);
}
await browser.close();
