# Deploying to GitHub Pages

The repository is a GitHub Pages user site: `Robusr/robusr.github.io`. Astro builds at the repository root with the default base `/`, and the workflow uploads `dist/` as the Pages artifact.

## 1. Push the branch

```bash
git push -u origin feat/homepage
```

Open a pull request. Review the screenshots in `screenshots/` and the QA notes in `QA.md` first.

## 2. Enable Pages

After merging to `main`, in the repository settings:

1. Settings → Pages.
2. Source: **GitHub Actions** (not “Deploy from a branch”).
3. Run the workflow, or push to `main` again. `.github/workflows/deploy.yml` builds and deploys automatically.

The first deployment publishes to `https://robusr.github.io/`.

## 3. Custom domain (optional, not performed)

`robusr.cn` returned no DNS answer when checked on 2026-10-20. Do not add a CNAME until the domain resolves.

When the domain is ready:

1. At the DNS provider, point the apex domain to GitHub Pages:
   - `A` records: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `AAAA` records: `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`
2. Add a `CNAME` record for `www` pointing to `robusr.github.io`.
3. Create `public/CNAME` containing exactly:

   ```text
   robusr.cn
   ```

4. If the canonical host changes, update `site` in `astro.config.mjs`, the `SITE` constant in `src/layouts/Base.astro`, `public/robots.txt`, `public/sitemap.xml`, and the Contact link if one is added.
5. Re-enable “Enforce HTTPS” after the certificate is issued.

DNS changes, HTTPS enforcement, and production deploys are intentionally left to the repository owner.

## 4. Rollback

Redeploy a previous commit from the Actions tab, or revert the merge commit on `main`. The site is fully static, so rollback does not involve data migrations.
