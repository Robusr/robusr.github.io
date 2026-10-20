# QA

Date: 2026-10-20. Build: Astro 7.4.1, Node 25.4.0, static output. Tests run against `astro preview` at `http://127.0.0.1:4321`.

Production host switched to <https://robusr.cn> on 2026-10-21. Production checks are recorded below.

## Build

- `npm run build` completes with 4 pages: `/`, `/zh/`, `/fr/`, `/404.html`.
- No errors or warnings during rendering; no runtime console errors or page errors in Chromium.
- Output size: 1.4 MB total. HTML: EN 19,021 B, ZH 18,414 B, FR 19,941 B, 404 3,273 B.
- CSS, fonts, and the enhancement script are bundled locally. The build has no third-party script, font CDN, analytics, or iframe. Cloudflare injects an email-decode script at the edge; see Known limitations.

## Production checks (2026-10-21)

Deployed commit: `50eb6c9`. The live HTML matches the local build except for the Cloudflare email-decode script and rewritten links.

| Check | Result |
|---|---|
| `/`, `/zh/`, `/fr/` | 200 |
| `/zh` without trailing slash | 308 to `/zh/` |
| `/404.html` | 308 to `/` |
| Unknown path | 404 with the custom page |
| HTTP to HTTPS | 301 |
| IPv6 | 200 |
| TLS certificate | valid to 2027-01-18, covers `robusr.cn` |
| `www.robusr.cn` | no DNS record; see `DEPLOY.md` |
| Canonical, hreflang, OG, JSON-LD | `https://robusr.cn` in all three locales |
| `sitemap.xml`, `robots.txt` | 200; sitemap lists only `robusr.cn` URLs |
| `_headers` | HSTS, CSP, X-Frame-Options, Permissions-Policy, and immutable asset caching present |
| GitHub Pages | `https://robusr.github.io/` returns 404; the Pages setting is still enabled |

Live Playwright, 390, 768, and 1440 px:

- All three locales report the correct `lang`.
- `scrollWidth === innerWidth` at every viewport.
- 1 `h1`, 6 `h2`, 5 `h3`, and 5 `.section` elements plus the hero.
- No image is missing alt text, width, or height.
- The skip link is the first focusable element.
- From `/zh/#about`, the language links are `/#about` and `/fr/#about`.
- The English language hint appears for a `zh-CN` browser.
- With JavaScript disabled, all sections and project copy remain readable. The email link becomes `/cdn-cgi/l/email-protection` and the footer shows `[email protected]`.

### Lighthouse live

| Locale | Performance | Accessibility | Best Practices | SEO | FCP | LCP | Speed Index | CLS | TBT | Transfer |
|---|---|---|---|---|---|---|---|---|---|---|
| EN | 96 | 100 | 92 | 100 | 1.6 s | 2.0 s | 4.3 s | 0 | 0 ms | 183 KiB |
| ZH | 96 | 100 | 92 | 100 | 1.6 s | 2.1 s | 4.4 s | 0 | 0 ms | 201 KiB |
| FR | 96 | 100 | 92 | 100 | 1.6 s | 2.0 s | 4.4 s | 0 | 0 ms | 183 KiB |

Best Practices is 92 because `errors-in-console` records the CSP-blocked Cloudflare Web Analytics beacon. The beacon transferred 0 bytes. Performance is 96 because Speed Index is 4.3 to 4.4 s; LCP is 2.0 to 2.1 s. Accessibility and SEO remain 100.

### Pending Cloudflare zone changes

Three edge features are still applied but are not in the repository:

| Feature | Current effect | Desired state |
|---|---|---|
| Email Address Obfuscation | Rewrites two `mailto:` links and injects `email-decode.min.js`; no-JS users see `[email protected]` | Off |
| Managed robots.txt | Prepends 134 lines and a Content-Signal policy to `robots.txt` | Off |
| Web Analytics / RUM | Injects `static.cloudflareinsights.com/beacon.min.js`, which the CSP blocks; this is the Best Practices 92 cause | Off |

The owner chose to disable all three. The audit machine has no Cloudflare credentials, so the changes are pending dashboard access or a scoped API token. Exact steps are in `DEPLOY.md`.

`public/_headers` sets one year immutable caching for hashed assets and adds HSTS, CSP, and framing headers. The live CSS response confirms `max-age=31536000, immutable`.


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

With JavaScript disabled at 390 px, all six sections and the hero, contact, and project copy remain readable. Navigation and language links are plain anchors. This check ran on the local preview. On Cloudflare, Email Address Obfuscation replaces the email address with `[email protected]`; see Known limitations.

## Links and assets

- All GitHub profile, repository, organization, and Kankanews links returned HTTP 200 on 2026-10-20.
- `https://robusr.cn` resolves through Cloudflare and returns 200; it is the production host. `https://www.robusr.cn` still has no DNS record.
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
- Canonical, hreflang, Open Graph, JSON-LD, `sitemap.xml`, and `robots.txt` derive from `site` in `astro.config.mjs`.
- hreflang set with `x-default` pointing to `/`.
- `robots.txt` allows all and references the sitemap.
- `sitemap.xml` lists the three locales with lastmod 2026-10-20.
- JSON-LD `Person` includes name, alternateName, url, image, jobTitle, alumniOf, sameAs, email.
- 404 page is `noindex, follow` and links to all three languages.

## Known limitations

- Production is Cloudflare Pages at `https://robusr.cn`. Canonical, hreflang, Open Graph, JSON-LD, sitemap, and robots use that host.
- Cloudflare Email Address Obfuscation rewrites `mailto:` links and injects `/cdn-cgi/scripts/.../email-decode.min.js`. With JavaScript disabled, the footer shows `[email protected]` and the email link does not open a mail client. This feature is pending removal.
- Cloudflare Managed robots.txt and Web Analytics are also pending removal. The beacon is blocked by the CSP, so it transfers no data, but it lowers Best Practices to 92 and logs a console error.
- ZH LCP is 2.1 s, slightly above the 2.0 s target. EN and FR are at 2.0 s.
- Chinese and French copy need a native technical review before publishing.
- The 37th CASTIC second prize is medium-confidence; see `CONTENT_CONFLICTS.md`.
- The OG image is shared across locales and uses English copy, which the brief permits.
- Local Lighthouse reports are in `qa/lighthouse-*.json`; live results are in `qa/lighthouse-live-summary.json`.


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
