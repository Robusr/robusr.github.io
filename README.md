# robusr.cn

**Personal homepage of Robusr Guo (郭沫晗)**: a robotics engineering student at HUST who turns real-world problems into working hardware, then builds AI tools that shorten the distance from an idea to a part.

**English** · [简体中文](README.zh.md) · [Français](README.fr.md)

> Five selected projects, a six-row journey, awards and media, and a short essay on moving from building machines to building tools.

![Homepage preview](public/og/og-default-v3.png)

| | |
|---|---|
| **Live site** | <https://robusr.cn> |
| **Hosting** | Cloudflare Pages, deployed from `main` |
| **Stack** | Astro 7, static output, no client framework |
| **Locales** | English `/`, 简体中文 `/zh/`, Français `/fr/` |
| **Design** | single-column editorial layout, 880 px max width, one deep-teal accent |
| **Quality gates** | `npm run verify`, build-time GitHub sync, Playwright, Lighthouse |

---

## Pages

| Route | Language | Notes |
|---|---|---|
| `/` | English | Default entry, `x-default` |
| `/zh/` | 简体中文 | `lang="zh-Hans"` |
| `/fr/` | Français | `lang="fr"` |
| `/404.html` | English | `noindex`, missing-sheet layout, links to all three languages |

All versions share one content model and the same section order. With JavaScript enabled, switching language preserves the current anchor. There is no automatic redirect from browser language.

## What the page contains

- **Mini Lab (00):** a full-width photo of the bedroom workbench directly after the Hero, before Selected Work, set on a paper mat with a `Fig. 00` caption in each language.
- **Selected Work:** Vulcan, Hsiwu, DustArrow X, OnesArm, and Anteportal Labs · Sencillo, in that fixed order. Each project opens with a four-panel A–D carousel (one 880 px panel at a time; swipe and snap on mobile) and a click-to-enlarge lightbox; every panel keeps its own localized caption. Animated panels are silent looping MP4/WebM with posters, paused by `prefers-reduced-motion` or the motion control. All five sets are redrawn: Vulcan (system loop, deployment, operator workflow, contract), Hsiwu (three-segment wing, analog chain, lead screw, bench evidence), DustArrow (modular bays, deployment, actual Gobi launch, telemetry), OnesArm (modular layers, FCF, 24 layouts + MATLAB, FEA), and Sencillo (force flow, layout, error budget, constraint compiler). The DustArrow launch panel uses the owner-provided *Young Edison* footage, credited to Shanghai TV. The body below pairs the project narrative with a Tech / Evidence / GitHub spec table. Repository cards still show live GitHub stars, forks, last push, and the latest release tag, with a build-time snapshot fallback.
- **Journey:** six rows from a bedroom workshop in 2018 to HUST in 2026.
- **Awards & Media:** 38th CASTIC first prize, 37th CASTIC second prize, and the Shanghai TV *Young Edison* feature.
- **More Work:** four repositories, one line each.
- **About:** three short paragraphs and a pull quote on October Sky, the sugar-propellant ignition that started it all, the floor lamp borrowed from his art-teacher father, the von Kármán curve, modular rocket PCB assembly, LoRa packet-loss tests, and the ink tones that connect engineering to meaning.
- **Contact:** email, GitHub, Anteportal Labs, location, language links, and the signature.
- **Background:** two hand-drawn personal IP illustrations, a collage portrait anchored bottom-right and a standing figure bottom-left, over a warm paper wash with a faint drafting dot grid in the margins. The standing figure appears from 1200 px up; mobile uses a 480 px version of the portrait.

## Stack

| Area | Choice |
|---|---|
| Framework | Astro 7, static output, no client framework |
| Styling | native CSS custom properties, no utility framework |
| Type | self-hosted, preloaded Inter variable WOFF2; system CJK stack |
| Images | 20 project plates at 1600×900 WebP; 10 silent MP4/WebM loops with 800 px posters and 800 px print stills; A plates use focus scans, Hsiwu C / DustArrow B / OnesArm C use repository CAD or MATLAB composites, and DustArrow C uses the actual launch footage; portrait at 260 and 512 px, Mini Lab at 480/960/1440 px with a 1440 px JPEG fallback, two transparent line-art IP assets sized for their display slots; WebP, with JPEG fallbacks |
| Icons | paper-field SVG favicon with an ink robotic-arm line drawing, hollow joints, a C gripper, and a teal base accent; 16/32/180 px PNG fallbacks and a web manifest |
| JavaScript | about 6 KB uncompressed of progressive enhancement (carousel, lightbox, motion control, live GitHub) |
| GitHub data | build-time snapshot from the GitHub API; edge-cached `/api/github` refresh through a Cloudflare Pages Function |
| Privacy | no analytics, cookies, third-party fonts, or embeds; GitHub requests leave from Cloudflare, not the visitor's browser |
| Print | A4 print stylesheet with a print-only cover: hides navigation, backgrounds, and live metadata; keeps all four panels, dates, and outbound URLs; print-only images load at 800 px, the cover upgrades to 960 px on `beforeprint` |
| Social | 1200×630 OG cards per locale, built around the Mini Lab plate and localized taglines |
| Deployment | Cloudflare Pages and Pages Functions, Git integration, Node 22 |
| CI | GitHub Actions runs `npm run verify` on pushes and pull requests |

## Local development

Requirements: Node.js 22.12 or newer and npm 9.6 or newer.

```bash
npm ci
npm run dev       # http://localhost:4321
npm run build     # sync GitHub stats, then render static output in dist/
npm run preview   # preview dist/ at http://localhost:4321
npm run check     # content, locale, asset, and GitHub snapshot consistency
npm run sync:github # refresh the checked-in GitHub snapshot
npm run typecheck # astro check
npm run verify    # check + typecheck + build
```

`npm run verify` syncs the GitHub snapshot, runs the content check, the type check, and the build; the build refreshes the snapshot again and produces four HTML pages. `dist/` is ignored by git and rebuilt in CI. `npm run sync:github` and `npm run build` keep the existing snapshot when GitHub is unreachable; set `GITHUB_TOKEN` to raise the API rate limit. The live `/api/github` endpoint is served by Cloudflare Pages Functions and is not part of `astro preview`; the page falls back to the snapshot there.

## Content model

All visible copy is data-driven.

| Path | Purpose |
|---|---|
| `src/data/profile.json` | Name, positioning, intro, status, links, portrait, portrait caption, About paragraphs, and pull quote |
| `src/data/projects.json` | Five featured projects with per-locale copy, tech, evidence, and status |
| `src/data/project-figures.json` | A/B/C/D panel captions, labels, source notes, and image/video/poster paths |
| `src/data/timeline.json` | Six Journey rows |
| `src/data/awards.json` | Three award and media rows |
| `src/data/more-work.json` | Four secondary projects |
| `src/data/mini-lab.json` | Mini Lab title, figure label, caption, alt text, and image dimensions |
| `src/data/github.json` | Generated snapshot: stars, forks, last push, and latest release for each tracked repository |
| `src/i18n/en.json`, `zh.json`, `fr.json` | UI labels, meta titles, and descriptions |
| `content/copy-en.md` | English source manuscript |
| `content/copy-zh.md`, `copy-fr.md` | Chinese and French translations |
| `content/glossary.md` | Shared terminology |

English is the source of truth. When editing:

1. Change the English manuscript and `src/data` together.
2. Update the Chinese and French fields in the same commit.
3. Keep section counts, numbers, links, and image paths identical across locales.
4. Run `npm run sync:github` after adding, renaming, or removing a tracked repository.
5. Run `npm run verify` and check all three routes.

`src/data/github.json` is generated; do not hand-edit it. `npm run sync:github` reads the featured and More Work repository links, then records stars, forks, last push, and the latest release. The `prebuild` hook refreshes it before every build and keeps the old file if GitHub is unreachable.

## Project structure

```text
.
├── src/
│   ├── components/   Header, Hero, MiniLab, PrintCover, ProjectList, Journey, Awards, MoreWork, About, Footer, LanguageSwitcher
│   ├── data/         profile, projects, project-figures, timeline, awards, more-work, mini-lab, generated GitHub snapshot
│   ├── i18n/         en, zh, fr, and shared types
│   ├── layouts/      Base.astro with head, hreflang, and JSON-LD
│   ├── pages/        index, zh/index, fr/index, 404, sitemap.xml, robots.txt
│   ├── scripts/      progressive enhancement and live GitHub refresh
│   └── styles/       tokens.css, global.css
├── figures/          editable SVG sources, Vulcan plate generator, render and animation scripts
├── functions/        Cloudflare Pages Function for /api/github
├── public/           images, hand-drawn IP art, mini lab photo, favicon set, OG cards, manifest, _headers, _redirects
├── content/          copy manuscripts and glossary
├── scripts/          content check, GitHub sync, OG/IP/Mini Lab/portrait/project figure generators, and QA helpers
├── qa/               Lighthouse, consistency, and layout reports
├── screenshots/      full-page captures at 1440, 1024, 768, and 390 px
├── Robusr IP/        source scans for the background artwork
├── .github/          verify workflow
└── .nvmrc            Node version for local builds
```

## Verification

| Check | Result |
|---|---|
| Build and checks | `npm run verify` passes: content check, `astro check` with 0 errors, 4 pages built |
| GitHub sync | Snapshot covers 8 repositories; Vulcan resolves to v1.3.0; `/api/github` returned 24 public repositories and the Vulcan release in a local handler test; a mocked endpoint updated the card to 99 stars and v9.9.9 in a Playwright check on 2026-11-26 |
| Production | `/`, `/zh/`, `/fr/` return 200; HTTP redirects to HTTPS; `www` returns 200 and still needs a 301 |
| Lighthouse mobile, local preview (2026-11-27) | EN 98/100/100/100, ZH 97/100/100/100, FR 98/100/100/100; LCP 2.3–2.4 s; CLS 0–0.001; 864–905 KiB |
| Lighthouse mobile, production (2026-10-22) | EN 97/100/92/100, ZH 98/100/92/100, FR 99/100/92/100 |
| LCP / CLS, production | LCP 1.8–2.2 s; CLS 0–0.069, measured before the portrait `aspect-ratio` fix |
| Layout widths | 1440, 1024, 768, and 390 px, no horizontal overflow; carousel is 4 panels / 4 tabs per project; 10 loops total (Vulcan 2, Hsiwu 2, DustArrow 3, OnesArm 2, Sencillo 1) |
| JavaScript disabled | all content readable; GitHub cards use the build-time snapshot |
| Mini Lab assets | 480/960/1440 WebP and a 1440 JPEG fallback; EXIF stripped; caption and alt text in three languages |
| Project figures | Five plates × four panels, all redrawn and audited as editable SVG at the web figure scale; Sencillo is design-target material; OnesArm uses v2 material only; the DustArrow launch excerpt is owner-provided and credited to Shanghai TV, Young Edison S8 |
| Project motion | 10 silent MP4/WebM loops: Vulcan A/C, Hsiwu A/C, DustArrow A/B/C, OnesArm A/C, Sencillo A; focus scans plus CAD, MATLAB, and actual-launch composites; posters for reduced motion |
| OG and print | v3 1200×630 OG cards for EN/ZH/FR with the Mini Lab plate; A4 print CSS with a print-only cover (10 pages in the 2026-11-27 test) keeps all four panels, dates, and outbound URLs while hiding navigation and live metadata |
| Visual system | Plate carousel with A–D anchors and lightbox, portrait and project frames, spec tables, section ticks, localized OG cards, print cover, and a missing-sheet 404 page |
| Icons | SVG favicon plus 16/32/180 px PNGs and a manifest; checked at 16/32/64/180 px on light and dark tab backgrounds |
| Outbound links | GitHub and media links return 200 |

The 2026-11-27 Lighthouse figures are from the local preview of the carousel/video build. Production figures are the 2026-10-22 run and predate the live GitHub module; re-run after deploy. Production Best Practices is 92 because Cloudflare still injects the Web Analytics beacon and the CSP blocks it. Email Address Obfuscation and Managed robots.txt are also still applied at the edge, so the live page differs from the local build. These are zone settings, not repository settings. Production results are in `qa/lighthouse-live-summary.json`.

Full evidence: [QA.md](QA.md). Screenshots: [screenshots/](screenshots/). Raw Lighthouse reports: [qa/](qa/).

The QA scripts use Playwright, installed separately with `npm install --no-save playwright@1.64.1`. The OG image is regenerated with `python3 scripts/make-og.py`; the background art is regenerated from `Robusr IP/` with `python3 scripts/make-ip-assets.py`; the Mini Lab photo is regenerated with `python3 scripts/make-minilab-assets.py /path/to/minilab.jpeg`; the portrait is regraded with `python3 scripts/make-portrait-assets.py`. The new plates are built with `python3 figures/build_vulcan.py` and `python3 figures/build_batch.py`, rendered with `node figures/render.mjs`, focus-scans encoded with `node figures/animate_batch.mjs`, and source-video composites assembled with ffmpeg. The legacy `scripts/make-project-figures.py` remains for the old repository plates. The figure scripts require Pillow, and the Mini Lab and portrait scripts strip EXIF metadata; the portrait script reads the v2 512 px file and writes v3 assets. Source repository assets, the owner-provided launch excerpt, and Sencillo design-target renders are not committed.

## Deployment

Production is Cloudflare Pages at <https://robusr.cn>. The project builds with `npm run build` and publishes `dist/`. `astro.config.mjs` sets the canonical site; canonical URLs, hreflang, Open Graph, JSON-LD, `sitemap.xml`, and `robots.txt` derive from it.

1. Connect the repository to Cloudflare Pages.
2. Set build command `npm run build`, output directory `dist`, and `NODE_VERSION=22`.
3. Add `robusr.cn` as a custom domain and enable HTTPS.
4. Push to `main`. Cloudflare Pages rebuilds automatically.

Cloudflare Pages deploys the `functions/` directory alongside `dist/`, so `/api/github` works without a separate worker. The function reads public repository metadata with a 10-minute edge cache; set an optional `GITHUB_TOKEN` environment variable to raise GitHub's rate limit. Without Functions, or when the endpoint fails, the page keeps the build-time snapshot.

`public/_headers` adds security and cache headers. Cloudflare Pages cannot redirect by host from `_redirects`, so that file only documents the limitation. `www.robusr.cn` currently resolves and returns 200; configure a Redirect Rule to send it to the apex with a 301. GitHub Pages is retired; disable the Pages site in repository settings if it is still enabled. See [DEPLOY.md](DEPLOY.md).

## Content rules

- Assets under `/assets/` and `/og/` are cached for one year. When an image changes, write it to a new filename and update every reference.
- Every number, award, link, and project status must trace back to the info library or a public source.
- Sencillo figures are design targets and must stay labeled as such.
- Star and fork counts refresh at build time and from `/api/github`; the static snapshot in `src/data/github.json` is the no-JavaScript fallback. Never hand-edit it; run `npm run sync:github`.
- When visible content changes, update `contentDate` in `src/data/profile.json`; `sitemap.xml` uses it as `lastmod`.
- Run `npm run verify` before pushing. The same command runs in GitHub Actions.
- Do not add family details, addresses, birthdays, scores, rankings, or private relationships; the art-teacher sentence in About is the owner-requested exception.
- Do not use TV stills, competition logos, third-party paper figures, or unverified accounts; the single authorized DustArrow launch excerpt (Fig. 03C) is credited to Shanghai TV, Young Edison S8. Sencillo figures are owner-supplied design-target material.

## Documentation

| Document | Purpose |
|---|---|
| [DELIVERY.md](DELIVERY.md) | Chinese delivery report |
| [DEPLOY.md](DEPLOY.md) | Cloudflare Pages, domain, DNS, HTTPS, and rollback |
| [QA.md](QA.md) | Consistency, accessibility, link, Lighthouse, and production evidence |
| [content-inventory.md](content-inventory.md) | Audited facts and link checks |
| [CONTENT_GAPS.md](CONTENT_GAPS.md) | Unresolved content |
| [CONTENT_CONFLICTS.md](CONTENT_CONFLICTS.md) | Conflicts and resolutions |

## Credits

Portrait and the two line-art personal IP illustrations provided by Robusr. Both drawings are used as low-opacity background art. All project plates are redrawn from the repository READMEs, repository renders, and installed-add-in or CAD captures; the UI and models remain the projects' own. OnesArm uses v2 material only. Sencillo figures are design-target illustrations supplied by the owner. The DustArrow launch excerpt is from the owner-provided *Young Edison* episode and is credited to Shanghai TV, Young Edison S8. The Mini Lab photograph is provided by Robusr; the published copies have EXIF metadata removed. The site does not use other TV stills, competition logos, or third-party paper figures. GitHub stars, forks, last-push dates, and release tags come from the public GitHub API and are cached at the edge.
