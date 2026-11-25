const USER = 'Robusr';
const FEATURED = ['Vulcan', 'Hsiwu', 'DustArrow', 'OnesArm'];
const CACHE_SECONDS = 600;

const json = (body, status = 200) => new Response(JSON.stringify(body), {
  status,
  headers: {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': status === 200
      ? `public, max-age=300, s-maxage=${CACHE_SECONDS}`
      : 'no-store',
    'X-Content-Type-Options': 'nosniff',
  },
});

export async function onRequestGet({ env = {} } = {}) {
  const headers = {
    Accept: 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28',
    'User-Agent': 'robusr.cn-site',
  };
  if (env.GITHUB_TOKEN) headers.Authorization = `Bearer ${env.GITHUB_TOKEN}`;

  const fetchJson = async (url) => {
    const response = await fetch(url, {
      headers,
      cf: { cacheTtl: CACHE_SECONDS, cacheEverything: true },
    });
    if (!response.ok) throw new Error(`GitHub responded ${response.status}`);
    return response.json();
  };

  try {
    const [list, ...releaseResults] = await Promise.all([
      fetchJson(`https://api.github.com/users/${USER}/repos?per_page=100&sort=pushed&direction=desc`),
      ...FEATURED.map((name) =>
        fetchJson(`https://api.github.com/repos/${USER}/${name}/releases/latest`).catch(() => null)),
    ]);

    const repos = {};
    for (const repo of list) {
      repos[repo.name] = {
        stars: repo.stargazers_count,
        forks: repo.forks_count,
        pushedAt: repo.pushed_at,
      };
    }

    const releases = {};
    FEATURED.forEach((name, index) => {
      const release = releaseResults[index];
      if (release?.tag_name) {
        releases[name] = {
          tag: release.tag_name,
          publishedAt: release.published_at,
          url: release.html_url,
        };
      }
    });

    return json({ fetchedAt: new Date().toISOString(), repos, releases });
  } catch {
    return json({ error: 'github_unavailable' }, 502);
  }
}
