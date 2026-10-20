# Deploying to Cloudflare Pages

Production: <https://robusr.cn>
Hosting: Cloudflare Pages, static output
Source: `main`

The site is fully static. `npm run build` writes four HTML pages plus assets to `dist/`. `astro.config.mjs` sets `site: 'https://robusr.cn'`; canonical URLs, hreflang, Open Graph, JSON-LD, `sitemap.xml`, and `robots.txt` derive from it.

## 1. Build settings

| Setting | Value |
|---|---|
| Framework preset | Astro |
| Build command | `npm run build` |
| Build output directory | `dist` |
| Node version | `NODE_VERSION=22` in the Pages project; `.nvmrc` covers local tools |

`package.json` declares `node >= 22.12.0`. Astro 7 supports Node 20.19 and newer or 22.12 and newer.

## 2. Custom domain

1. Add `robusr.cn` as a custom domain on the Pages project.
2. Point the apex at the Pages project using the custom domain flow and keep it proxied through Cloudflare.
3. Enable **Always Use HTTPS**. Cloudflare issues the edge certificate automatically.
4. Purge the Cloudflare cache after the first deployment.

The current certificate covers `robusr.cn` only. Add `www` before relying on that host.

## 3. www

`www.robusr.cn` has no DNS record today. To add it:

1. Create a proxied `CNAME` for `www` pointing to the Pages project hostname.
2. Add `www.robusr.cn` as a custom domain on the same Pages project.
3. `public/_redirects` already contains `https://www.robusr.cn/* https://robusr.cn/:splat 301`. Keep it, or use a Cloudflare Redirect Rule with the same target.
4. Verify that `https://www.robusr.cn/zh/` returns a 301 to `https://robusr.cn/zh/`.

## 4. Headers, redirects, and zone features

`public/_headers` is copied to `dist/_headers` and applies to every route:

- `X-Content-Type-Options: nosniff`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `X-Frame-Options: DENY`
- `Permissions-Policy` with camera, microphone, and geolocation disabled
- `Strict-Transport-Security` for one year
- `Content-Security-Policy` restricted to the site origin. `'unsafe-inline'` is required because Astro inlines the small enhancement script.
- one-year immutable caching for `/_astro/*`, `/assets/*`, `/og/*`, and `/favicon.svg`

Two Cloudflare zone features change the response after the build:

- **Email Address Obfuscation** rewrites `mailto:` links and injects `/cdn-cgi/scripts/.../email-decode.min.js`. With JavaScript disabled, the footer shows `[email protected]` and the email link does not open a mail client. Disable it under Scrape Shield if no-JavaScript email access matters.
- **Managed robots.txt** prepends a policy that blocks GPTBot, ClaudeBot, Google-Extended, Baiduspider, and other crawlers. Review it under Security, Bots if that policy is not intended. The repository's `robots.txt` endpoint remains correct underneath.

## 5. Retire GitHub Pages

The repository used to publish to `https://robusr.github.io` through GitHub Actions and legacy branch builds. That copy is still reachable and duplicates the site.

1. Confirm that `https://robusr.cn/`, `/zh/`, `/fr/`, `/sitemap.xml`, and `/robots.txt` are correct.
2. In repository settings, open **Pages** and remove the site, or set the source to **None**.
3. The old workflow file has been removed from the repository.
4. Keep `https://robusr.github.io` only as a redirect if needed. Do not point canonical, Open Graph, or JSON-LD URLs back to it.

## 6. Verify

```bash
curl -sSI https://robusr.cn/ | grep -Ei 'HTTP/|strict-transport|cache-control'
curl -sSI https://robusr.cn/zh/
curl -sS https://robusr.cn/sitemap.xml
curl -sS https://robusr.cn/robots.txt
curl -sS https://robusr.cn/ | grep -Eo '<link rel="canonical"[^>]*>|<meta property="og:url"[^>]*>'
```

Expected: `200` on all three locales, canonical and Open Graph URLs on `https://robusr.cn`, `Sitemap: https://robusr.cn/sitemap.xml`, and a `404` status for an unknown path.

## 7. Rollback

Cloudflare Pages keeps every deployment. Open **Deployments**, select a previous build, and choose **Rollback**. The site is static, so rollback does not involve data migrations. A revert commit on `main` triggers a new build.
