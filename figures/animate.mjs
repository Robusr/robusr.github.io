import { chromium } from 'playwright-core';
import fs from 'fs';
import path from 'path';
import { execFileSync } from 'child_process';

const chrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const root = '/Users/robusr/Desktop/Redraw/robusr.github.io';
const renderDir = path.join(root, 'figures/render');
const frameRoot = path.join(root, 'figures/frames');
fs.mkdirSync(renderDir, { recursive: true });
fs.mkdirSync(frameRoot, { recursive: true });

const DURATION = 6.4;
const FPS = 25;
const POSTER_T = 5.2;

const A = {
  'a-focus1': [{ t: 0, o: 1 }, { t: 1.0, o: 0 }],
  'a-focus2': [{ t: 0, o: 0 }, { t: 1.0, o: 1 }, { t: 1.8, o: 0 }],
  'a-focus3': [{ t: 0, o: 0 }, { t: 1.8, o: 1 }, { t: 2.6, o: 0 }],
  'a-focus4': [{ t: 0, o: 0 }, { t: 2.6, o: 1 }, { t: 3.4, o: 0 }],
  'a-focus5': [{ t: 0, o: 0 }, { t: 3.4, o: 1 }, { t: 4.2, o: 0 }],
  'a-focus6': [{ t: 0, o: 0 }, { t: 4.2, o: 1 }, { t: 5.2, o: 0 }],
  'a-focus7': [{ t: 0, o: 0 }, { t: 4.2, o: 1 }, { t: 5.2, o: 0 }],
  'a-render-img': [{ t: 0, s: 1.0 }, { t: 6.0, s: 1.035 }],
};

const C = {
  'c-focus1': [{ t: 0, o: 1 }, { t: 1.8, o: 0 }],
  'c-focus2': [{ t: 0, o: 0 }, { t: 1.8, o: 1 }, { t: 3.6, o: 0 }],
  'c-focus3': [{ t: 0, o: 0 }, { t: 3.6, o: 1 }, { t: 5.0, o: 0 }],
  'c-render-img': [{ t: 0, s: 1.0 }, { t: 5.8, s: 1.05 }],
};

const SYMBOLS = ['o', 'x', 'y', 's', 'd'];

function fillTimeline(tl) {
  for (const keys of Object.values(tl)) {
    keys.sort((a, b) => a.t - b.t);
    for (const p of SYMBOLS) {
      let has = false;
      for (const k of keys) if (k[p] !== undefined) has = true;
      if (!has) continue;
      let last;
      for (const k of keys) {
        if (k[p] !== undefined) last = k[p];
        else k[p] = last;
      }
    }
  }
  return tl;
}
fillTimeline(A); fillTimeline(C);

function htmlFor(svg, timeline) {
  return `<!doctype html><html><head><meta charset="utf-8"><style>
    @font-face { font-family: Inter; src: url('/figures/fonts/inter-latin-wght-normal.woff2') format('woff2'); font-weight: 100 900; font-style: normal; }
    html, body { margin: 0; background: #FBFBF9; }
    #stage { width: 1600px; height: 900px; overflow: hidden; }
    #stage svg { display: block; width: 1600px; height: 900px; }
  </style></head><body><div id="stage">${svg.replace(/^<\?xml[^>]*>\s*/, '')}</div>
  <script>
  const LAYERS = ${JSON.stringify(timeline)};
  const DURATION = ${DURATION};
  const ease = u => u < 0.5 ? 2 * u * u : 1 - Math.pow(-2 * u + 2, 2) / 2;
  function val(keys, t, prop, dflt) {
    if (!keys.length) return dflt;
    if (t <= keys[0].t) return keys[0][prop] ?? dflt;
    if (t >= keys[keys.length - 1].t) return keys[keys.length - 1][prop] ?? dflt;
    let i = 0;
    while (i < keys.length - 1 && keys[i + 1].t < t) i++;
    const a = keys[i], b = keys[i + 1];
    const pa = a[prop] ?? dflt, pb = b[prop] ?? pa;
    const u = (t - a.t) / Math.max(1e-6, b.t - a.t);
    const e = ease(Math.min(1, Math.max(0, u)));
    return pa + (pb - pa) * e;
  }
  window.setTime = (t) => {
    for (const [id, keys] of Object.entries(LAYERS)) {
      const el = document.getElementById(id);
      if (!el) continue;
      const o = val(keys, t, 'o', 1);
      el.style.opacity = String(o);
      const x = val(keys, t, 'x', 0), y = val(keys, t, 'y', 0), s = val(keys, t, 's', 1);
      if (x !== 0 || y !== 0 || s !== 1) {
        el.style.transform = 'translate(' + x + 'px,' + y + 'px) scale(' + s + ')';
        el.style.transformOrigin = 'center';
        el.style.transformBox = 'fill-box';
      } else {
        el.style.transform = '';
      }
      if (keys.some(k => k.d !== undefined)) {
        const d = val(keys, t, 'd', 1);
        el.querySelectorAll('line,path').forEach(n => {
          n.style.strokeDasharray = '1';
          n.style.strokeDashoffset = String(d);
        });
      }
    }
  };
  window.setTime(0);
  </script></body></html>`;
}

const videos = [
  { name: 'vulcan-a', tl: A },
  { name: 'vulcan-c', tl: C },
];

const browser = await chromium.launch({ executablePath: chrome, headless: true });
for (const { name, tl } of videos) {
  const svg = fs.readFileSync(path.join(root, 'figures/src', `${name}.svg`), 'utf8');
  const htmlPath = path.join(renderDir, `${name}.html`);
  fs.writeFileSync(htmlPath, htmlFor(svg, tl));
  const frameDir = path.join(frameRoot, name);
  fs.rmSync(frameDir, { recursive: true, force: true });
  fs.mkdirSync(frameDir, { recursive: true });
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1 });
  await page.goto(`http://127.0.0.1:8789/figures/render/${name}.html`, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);
  const total = Math.round(DURATION * FPS);
  for (let i = 0; i < total; i++) {
    const t = i / FPS;
    await page.evaluate((t) => window.setTime(t), t);
    await page.waitForTimeout(16);
    await page.screenshot({ path: path.join(frameDir, `${String(i).padStart(4, '0')}.png`) });
    if (i % 40 === 0) console.log(name, 'frame', i, '/', total);
  }
  await page.evaluate((t) => window.setTime(t), POSTER_T);
  await page.waitForTimeout(50);
  await page.screenshot({ path: path.join(renderDir, `${name}-poster.png`) });
  await page.close();
  console.log(name, 'captured', total, 'frames');
  const mp4 = path.join(renderDir, `${name}.mp4`);
  const webm = path.join(renderDir, `${name}.webm`);
  execFileSync('ffmpeg', ['-y', '-framerate', String(FPS), '-i', path.join(frameDir, '%04d.png'),
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '20', '-pix_fmt', 'yuv420p',
    '-movflags', '+faststart', '-an', mp4], { stdio: 'ignore' });
  execFileSync('ffmpeg', ['-y', '-framerate', String(FPS), '-i', path.join(frameDir, '%04d.png'),
    '-c:v', 'libvpx-vp9', '-crf', '34', '-b:v', '0', '-row-mt', '1', '-an', webm], { stdio: 'ignore' });
  console.log(name, 'encoded', fs.statSync(mp4).size, fs.statSync(webm).size);
}
await browser.close();
