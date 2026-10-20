# QA

Date: 2026-10-20. Build: Astro 7.4.1, Node 25.4.0, static output. Tests run against `astro preview` at `http://127.0.0.1:4321`.

## Build

- `npm run build` completes with 4 pages: `/`, `/zh/`, `/fr/`, `/404.html`.
- No errors or warnings during rendering; no runtime console errors or page errors in Chromium.
- Output size: 1.4 MB total. HTML: EN 19,021 B, ZH 18,414 B, FR 19,941 B, 404 3,273 B.
- CSS, fonts, and the enhancement script are bundled locally. No third-party script, font CDN, analytics, or iframe.

## Three-language consistency

| Check | Result |
|---|---|
| Sections per page | 6 in each locale |
| Featured projects | 5, same order: Vulcan → Hsiwu → DustArrow X → OnesArm → Sencillo |
| Project repository links | Identical set and order in all three |
| Journey rows | 6, same years: 2018, 2019–2022, 2023, 2023, 2024, 2025–2026 |
| Awards rows | 3, same years |
| More Work rows | 6, same names and links |
| Images and srcsets | Identical paths in all three |
| Key metrics | 23, 8, 40, 10, 9, 32, 24, 450, 5052, 0.8, 30, 8/8, 2², 3! present in all three |
| `aria-current` | Marks English / 中文 / Français correctly |
| hreflang | 4 links per page: en, zh-Hans, fr, x-default |
| Canonical | Self-referencing per locale |
| French typography | 17 non-breaking spaces before `:` and in numeric formatting; decimal comma preserved (`0,8 mm`) |
| Chinese typography | Half-width spaces between Chinese and Latin text |

Detailed machine output: `qa/consistency.json`, `qa/capture-report.json`.

## Responsive layout

Tested at 1440, 1024, 768, and 390 px, plus a 720 px viewport as a 200% zoom proxy on a 1440 px display.

- No horizontal overflow at any width (`scrollWidth === innerWidth`), no element crossing the viewport, no text truncation observed.
- Desktop: hero is two columns (text + 260 px portrait); project rows are image-left / text-right.
- Tablet and mobile: single column, full-width project images, portrait after the intro, max 200 px.
- Mobile header uses a second row of text navigation rather than a hamburger; header is static below 640 px and sticky above.
- Sticky header geometry at 1440 px: header bottom 111 px, hero h1 top 229 px; no overlap. Full-page screenshots were captured with `position: static` on the header to avoid a known Chromium full-page capture artifact; viewport screenshots verify the real sticky state.
- Tap targets: all standalone links and buttons measure at least 44 × 44 px on mobile. One exception: the inline “watch the feature” link inside the Awards paragraph (16 px high) is an inline text link, covered by the WCAG 2.5.8 inline exception.

Screenshots:

- `screenshots/en-1440.png`, `en-1024.png`, `en-768.png`, `en-390.png`
- `screenshots/zh-1440.png`, `zh-390.png`
- `screenshots/fr-1440.png`, `fr-390.png`
- `screenshots/en-720-zoom-200.png` — 200% zoom proxy
- `screenshots/en-390-nojs.png` — JavaScript disabled
- `screenshots/en-1440-viewport.png` — sticky header state

## Accessibility

- Lighthouse Accessibility: 100 for EN, ZH, FR.
- One `h1`, six `h2`, five `h3`; no skipped heading levels; no duplicate IDs.
- Skip link is the first focusable element and jumps to `#main`.
- Keyboard walk at 1440 px: Skip to content → language hint links and dismiss → brand → Work / Journey / About / Contact → language switch → GitHub / Email / Anteportal Labs. Every stop shows a visible focus outline.
- All images have descriptive localized alt text plus `width` and `height`. The portrait is preloaded; project images use `loading="lazy"`.
- `prefers-reduced-motion` disables transitions and image scaling. No autoplay, parallax, or scroll-triggered animation.
- Language switch preserves the current anchor: `/zh/#about` offers `/#about` and `/fr/#about`.
- No automatic language redirect. The English page shows a dismissible “Also available in 中文 / Français” bar only when the browser language is Chinese or French; dismissal is stored in `sessionStorage`.

## JavaScript disabled

With JavaScript disabled at 390 px, all six sections and the hero, contact, and project copy remain readable. Navigation, language links, and email link are plain anchors. Verified text includes Vulcan, Sencillo, and the email address.

## Links and assets

- All GitHub profile, repository, organization, and Kankanews links returned HTTP 200 on 2026-10-20.
- `https://robusr.cn` returned 000 (no DNS response) and is not used anywhere.
- Local routes `/`, `/zh/`, `/fr/`, `/404.html`, `/sitemap.xml`, `/robots.txt`, `/og/og-default.png`, and `/favicon.svg` return 200 with correct content types.
- No broken in-page anchors in any locale.

## Lighthouse (mobile, simulated throttling)

| Locale | Performance | Accessibility | Best Practices | SEO | LCP | CLS | Transfer |
|---|---|---|---|---|---|---|---|
| EN | 100 | 100 | 100 | 100 | 1.6 s | 0.001 | 179 KiB |
| ZH | 100 | 100 | 100 | 100 | 1.7 s | 0 | 197 KiB |
| FR | 100 | 100 | 100 | 100 | 1.4 s | 0.001 | 179 KiB |

Targets from the brief: all four categories ≥ 95, LCP < 2.0 s, CLS < 0.05. All met. Raw reports: `qa/lighthouse-en-mobile.json`, `qa/lighthouse-zh-mobile.json`, `qa/lighthouse-fr-mobile.json`; summary: `qa/lighthouse-summary.json`.

Lighthouse ran against a local preview with Chrome headless and simulated mobile throttling; scores on Pages/CDN may differ slightly.

## SEO and metadata

- Per-page title, description, canonical, OG and Twitter tags.
- hreflang set with `x-default` pointing to `/`.
- `robots.txt` allows all and references the sitemap.
- `sitemap.xml` lists the three locales with lastmod 2026-10-20.
- JSON-LD `Person` includes name, alternateName, url, image, jobTitle, alumniOf, sameAs, email.
- 404 page is `noindex, follow` and links to all three languages.

## Known limitations

- `robusr.cn` is unverified, so canonical URLs use `https://robusr.github.io`.
- Chinese and French copy need a native technical review before publishing.
- The 37th CASTIC second prize is medium-confidence; see `CONTENT_CONFLICTS.md`.
- The OG image is shared across locales and uses English copy, which the brief permits.
- Lighthouse results are local; production results require a deployed URL.

## Reproduce

```bash
npm ci
npm run build
npm run preview -- --host 127.0.0.1 --port 4321
npm install --no-save playwright@1.64.1   # QA tooling only, not a site dependency
node scripts/qa-capture.mjs
node scripts/qa-zoom-keyboard.mjs
CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  npx lighthouse http://127.0.0.1:4321/ --only-categories=performance,accessibility,best-practices,seo \
  --output=json --output-path=qa/lighthouse-en-mobile.json
python3 scripts/make-og.py               # requires Pillow
```

The preview server was stopped after testing.
