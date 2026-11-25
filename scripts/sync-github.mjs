import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const SNAPSHOT = 'src/data/github.json';
const USER = 'Robusr';

const readJson = (file) => JSON.parse(fs.readFileSync(path.join(root, file), 'utf8'));
const repoFromHref = (href) => {
  const match = /^https:\/\/github\.com\/Robusr\/([^/?#]+)\/?$/.exec(href ?? '');
  return match ? decodeURIComponent(match[1]) : null;
};

const projects = readJson('src/data/projects.json');
const moreWork = readJson('src/data/more-work.json');
const featured = projects.filter((project) => project.repo);
const tracked = [...new Set([
  ...featured.map((project) => project.repo),
  ...moreWork.map((item) => repoFromHref(item.href)).filter(Boolean),
])];

const headers = {
  Accept: 'application/vnd.github+json',
  'X-GitHub-Api-Version': '2022-11-28',
  'User-Agent': 'robusr.cn-site',
};
if (process.env.GITHUB_TOKEN) headers.Authorization = `Bearer ${process.env.GITHUB_TOKEN}`;

async function api(url) {
  const response = await fetch(url, { headers });
  if (!response.ok) throw new Error(`${response.status} ${response.statusText} for ${url}`);
  return response.json();
}

function fail(message) {
  console.warn(`GitHub sync skipped: ${message}`);
  if (fs.existsSync(path.join(root, SNAPSHOT))) {
    console.warn(`Keeping the existing ${SNAPSHOT} snapshot.`);
    process.exit(0);
  }
  console.error('No snapshot exists yet. Run this script with network access before building.');
  process.exit(1);
}

async function main() {
  const existing = fs.existsSync(path.join(root, SNAPSHOT)) ? readJson(SNAPSHOT) : null;

  let list;
  try {
    list = await api(`https://api.github.com/users/${USER}/repos?per_page=100&sort=pushed&direction=desc`);
  } catch (error) {
    fail(error.message);
  }

  const byName = new Map(list.map((repo) => [repo.name, repo]));
  const missing = tracked.filter((name) => !byName.has(name));
  if (missing.length) fail(`repositories not found: ${missing.join(', ')}`);

  const repos = Object.fromEntries(tracked.map((name) => {
    const repo = byName.get(name);
    return [name, {
      stars: repo.stargazers_count,
      forks: repo.forks_count,
      pushedAt: repo.pushed_at,
    }];
  }));

  const releaseResults = await Promise.all(featured.map(async (project) => {
    try {
      const release = await api(`https://api.github.com/repos/${USER}/${project.repo}/releases/latest`);
      return [project.repo, {
        tag: release.tag_name,
        publishedAt: release.published_at,
        url: release.html_url,
      }];
    } catch (error) {
      if (!String(error.message).startsWith('404')) {
        console.warn(`Release lookup failed for ${project.repo}: ${error.message}`);
      }
      return [project.repo, existing?.repos?.[project.repo]?.release ?? null];
    }
  }));

  for (const [name, release] of releaseResults) {
    if (release) repos[name].release = release;
  }

  const previous = existing ? JSON.stringify(existing.repos) : null;
  if (previous === JSON.stringify(repos)) {
    console.log(`GitHub snapshot already current: ${tracked.length} repositories.`);
    return;
  }

  const payload = { fetchedAt: new Date().toISOString(), repos };
  fs.writeFileSync(path.join(root, SNAPSHOT), `${JSON.stringify(payload, null, 2)}\n`);
  console.log(`GitHub snapshot updated: ${tracked.length} repositories, ${releaseResults.filter(([, release]) => release).length} release(s).`);
}

main();
