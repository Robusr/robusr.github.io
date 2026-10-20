# Content gaps

Items marked `[待补充]` are not invented on the page. None of them blocks the build.

1. **Custom domain resolved.** `robusr.cn` resolves through Cloudflare and is the production host. Canonical, hreflang, sitemap, robots, and JSON-LD are configured to use `https://robusr.cn`. `www.robusr.cn` still has no DNS record; see `DEPLOY.md`.
2. **Portrait variety.** Only one user-provided photo exists (beach portrait). The hero uses a square crop. A more formal portrait would be useful for press or applications, but the current photo is acceptable for a personal homepage.
3. **Native review of translations.** Chinese and French were written from the English source. A native technical reviewer should read `content/copy-zh.md` and `content/copy-fr.md` before publishing.
4. **More Work descriptions.** The six one-line descriptions come from English GitHub repo descriptions; official Chinese and French descriptions were not in the library and were translated here.
5. **37th CASTIC prize level.** The DustArrow repo confirms participation and the TV feature but not the prize level; the second prize comes from personal materials and search summaries. See `CONTENT_CONFLICTS.md`.
6. **Sencillo details.** No public repo, images, or measured results exist. All figures are labeled design targets. `[待补充]` Photos, measured results, or a product page when available.
7. **Media beyond one link.** Only the Kankanews feature is linked. Sohu and other reports were not used because they are secondary aggregations.
8. **Optional GitHub Profile README sync.** `05-profile-readme-draft.md` is a ready draft, but this repository does not modify `Robusr/Robusr`. The user must decide whether to sync.
9. **OG images per language.** A single English OG image is shared by all three pages, which the brief allows.
10. **No analytics.** Deliberately omitted; the brief forbids third-party tracking. Cloudflare Web Analytics is currently injected by the zone but blocked by the CSP. Disable RUM so the policy and the Lighthouse score agree.
