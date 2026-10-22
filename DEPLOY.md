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

The apex and `www` hosts each serve a certificate covering that host. Keep both custom domains attached, or remove `www` if a redirect rule is not desired.

## 3. www

`www.robusr.cn` currently resolves through Cloudflare and returns 200 with the same site. Its canonical tag points to `https://robusr.cn/`, but the host still needs a 301. Cloudflare Pages `_redirects` only supports path redirects, so a host rule in that file does nothing. `public/_redirects` now records this limitation instead of carrying a rule.

Create a Redirect Rule on the zone:

1. Open **Rules → Redirect Rules → Create rule**.
2. Set the expression to `http.host eq "www.robusr.cn"`.
3. Use a dynamic redirect with the expression `concat("https://robusr.cn", http.request.uri.path)`, preserve the query string, and use status `301`.
4. Alternatively, create a Bulk Redirect with source `https://www.robusr.cn/*` and target `https://robusr.cn/$1`, preserving the query string, status `301`.
5. Verify that `https://www.robusr.cn/zh/` returns a 301 to `https://robusr.cn/zh/`.

Until the rule exists, `www` serves a duplicate of the site. Search engines should consolidate on the canonical URL, but the redirect is still the correct fix.

## 4. Headers, redirects, and zone features

`public/_headers` is copied to `dist/_headers` and applies to every route:

- `X-Content-Type-Options: nosniff`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `X-Frame-Options: DENY`
- `Permissions-Policy` with camera, microphone, and geolocation disabled
- `Strict-Transport-Security` for one year
- `Content-Security-Policy` restricted to the site origin. `'unsafe-inline'` is required because Astro inlines the small enhancement script.
- one-year immutable caching for `/_astro/*`, `/assets/*`, `/og/*`, and `/favicon.svg`

Three Cloudflare zone features modify the response after the build. The site policy is to keep all three off:

| Feature | Dashboard path | API |
|---|---|---|
| Email Address Obfuscation | Security → Settings → Scrape Shield → Email Address Obfuscation → Off | `PATCH /zones/{zone_id}/settings/email_obfuscation` with `{"value":"off"}` |
| Managed robots.txt | AI Crawl Control → Directives → Managed robots.txt → Off, or Security → Bots on older accounts | `PUT /zones/{zone_id}/bot_management` with the current config and `is_robots_txt_managed: false` |
| Web Analytics / RUM | Analytics & Logs → Web Analytics → Manage Site → Advanced Options → JS Snippet injection → Off | `PATCH /zones/{zone_id}/settings/rum` with `{"value":"off"}` |

Audit on 2026-10-22: all three features are still active. Email obfuscation rewrites the two `mailto:` links and injects `email-decode.min.js`; Managed robots.txt prepends 134 lines and a Content-Signal policy; RUM still injects the beacon for browser user agents, even though `curl` does not show it. The local preview has none of them.

For the Bot Management call, read the current config first and send it back with only `is_robots_txt_managed` changed. If the API rejects read-only fields, remove them before the PUT.

```bash
TOKEN=...  # Zone:Read, Zone Settings:Edit, Bot Management:Edit
ZONE_ID=$(curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.cloudflare.com/client/v4/zones?name=robusr.cn" | jq -r '.result[0].id')

curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/bot_management" \
  > /tmp/bot-management.json
jq '.result | .is_robots_txt_managed = false' /tmp/bot-management.json \
  > /tmp/bot-management-update.json
curl -s -X PUT -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  --data @/tmp/bot-management-update.json \
  "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/bot_management"

curl -s -X PATCH -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  --data '{"value":"off"}' \
  "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/email_obfuscation"
curl -s -X PATCH -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  --data '{"value":"off"}' \
  "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/rum"
```

Verify after the change:

```bash
curl -s https://robusr.cn/ | grep -E '__cf_email__|email-decode' || echo "email obfuscation off"
curl -s https://robusr.cn/robots.txt | grep -c 'Cloudflare Managed'  # expect 0
curl -s https://robusr.cn/ | grep -c 'cloudflareinsights'          # expect 0
```

The repository currently has no Cloudflare credentials. Until these settings are changed, the live site keeps the email placeholder without JavaScript, the managed robots block, and the CSP console error that lowers Best Practices to 92. Local Lighthouse scores 100 for Best Practices because these edge features are absent.


## 5. Retire GitHub Pages

The repository used to publish to `https://robusr.github.io` through GitHub Actions and legacy branch builds. That host now returns 404, but the Pages setting is still enabled in repository settings.

1. Confirm that `https://robusr.cn/`, `/zh/`, `/fr/`, `/sitemap.xml`, and `/robots.txt` are correct.
2. In repository settings, open **Pages** and remove the site, or set the source to **None**.
3. The old workflow file has been removed from the repository.
4. Keep `https://robusr.github.io` only as a redirect if needed. Do not point canonical, Open Graph, or JSON-LD URLs back to it.

## 6. Verify

```bash
curl -sSI https://robusr.cn/ | grep -Ei 'HTTP/|strict-transport|cache-control'
curl -sSI https://robusr.cn/zh/
curl -sSI https://www.robusr.cn/zh/ | grep -Ei 'HTTP/|location'
curl -sS https://robusr.cn/sitemap.xml
curl -sS https://robusr.cn/robots.txt
curl -sS https://robusr.cn/ | grep -Eo '<link rel="canonical"[^>]*>|<meta property="og:url"[^>]*>'
```

Expected: `200` on all three locales, a `301` from `www.robusr.cn/zh/` to `robusr.cn/zh/`, canonical and Open Graph URLs on `https://robusr.cn`, `Sitemap: https://robusr.cn/sitemap.xml`, and a `404` status for an unknown path. Until the redirect rule is created, the `www` request returns `200`.

## 7. Rollback

Cloudflare Pages keeps every deployment. Open **Deployments**, select a previous build, and choose **Rollback**. The site is static, so rollback does not involve data migrations. A revert commit on `main` triggers a new build.
