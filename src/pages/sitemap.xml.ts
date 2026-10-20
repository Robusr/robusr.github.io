import type { APIRoute } from 'astro';
import profile from '../data/profile.json';

const PATHS = [
  { path: '/', priority: '1.0' },
  { path: '/zh/', priority: '0.9' },
  { path: '/fr/', priority: '0.9' },
] as const;

export const GET: APIRoute = ({ site }) => {
  const base = (site ?? new URL('https://robusr.cn')).origin;
  const body = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${PATHS.map(({ path, priority }) => `  <url>
    <loc>${base}${path}</loc>
    <lastmod>${profile.snapshotDate}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>${priority}</priority>
  </url>`).join('\n')}
</urlset>
`;

  return new Response(body, {
    headers: {
      'Content-Type': 'application/xml; charset=utf-8',
      'Cache-Control': 'public, max-age=3600',
    },
  });
};
