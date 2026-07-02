// ============================================================
//  github.js — GitHub REST API client + formatProjects / formatStats
//
//  Uses unauthenticated requests (public data only). Results are
//  cached in the shared state singleton.
// ============================================================

import { state } from './state.js';
import { tStr, getPersonal, getLocale } from './i18n.js';
import { escapeHTML } from './ui.js';

// ---- API helpers ----

async function ghFetch(path) {
  const res = await fetch(`https://api.github.com${path}`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

// ---- Fetchers ----

export async function fetchGitHubProfile() {
  const user = getPersonal()?.githubUser ?? 'Robusr';
  try { state.ghProfileCache = await ghFetch(`/users/${user}`); }
  catch { state.ghProfileCache = null; }
}

export async function fetchGitHubRepos() {
  const user = getPersonal()?.githubUser ?? 'Robusr';
  try {
    const data = await ghFetch(`/users/${user}/repos?per_page=50&sort=updated`);
    state.ghReposCache = {
      originals: data.filter(r => !r.fork),
      forks:     data.filter(r => r.fork),
    };
  } catch { state.ghReposCache = null; }
}

// ---- Formatters ----

/** Build an inline-styled HTML string for the project list. */
export function formatProjects() {
  if (!state.ghReposCache) {
    return `<span class="dim">${escapeHTML(tStr('projectsFailed'))}</span>`;
  }

  const { originals, forks } = state.ghReposCache;
  const lines = [tStr('projectsTitle'), '='.repeat(40), ''];

  if (originals.length === 0 && forks.length === 0) {
    lines.push(tStr('projectsEmpty'));
    return lines.join('\n');
  }

  originals.forEach((r, i) => {
    lines.push(`  <span class="hl">${i + 1}.</span> <span class="bold">${escapeHTML(r.name)}</span>`);
    if (r.description) {
      lines.push(`     <span class="dim">${escapeHTML(r.description)}</span>`);
    }
    lines.push(`     <span class="accent">url: ${escapeHTML(r.html_url)}</span>`);
    const meta = [];
    if (r.language) meta.push(`lang: ${escapeHTML(r.language)}`);
    meta.push(`* ${r.stargazers_count}`);
    meta.push(`fork: ${r.forks_count}`);
    meta.push(`since ${new Date(r.created_at).getFullYear()}`);
    lines.push(`     <span class="dim">${meta.join('  ')}</span>`);
    lines.push('');
  });

  if (forks.length > 0) {
    lines.push('<span class="dim">' + '-'.repeat(40) + '</span>');
    lines.push(`<span class="dim">Forked repositories:</span>`);
    lines.push('');
    forks.forEach((r, i) => {
      const desc = r.description ? ` -- ${r.description}` : '';
      lines.push(`  <span class="dim">${i + 1}.</span> <span class="dim">${escapeHTML(r.name)}</span> <span class="tag">${tStr('forkTag')}</span><span class="dim">${escapeHTML(desc)}</span>`);
      lines.push(`     <span class="accent">url: ${escapeHTML(r.html_url)}</span>`);
      lines.push('');
    });
  }

  return lines.join('\n');
}

/** Build an inline-styled HTML string for the GitHub profile overview. */
export function formatStats() {
  if (!state.ghProfileCache) {
    return `<span class="dim">${escapeHTML(tStr('statsFailed'))}</span>`;
  }

  const p = state.ghProfileCache;
  const locale = getLocale();
  const lines = [tStr('statsTitle'), '='.repeat(36), ''];

  lines.push(`  <span class="bold">${escapeHTML(p.login)}</span>`);
  if (p.name) lines.push(`  ${escapeHTML(p.name)}`);
  if (p.bio)  lines.push(`  <span class="dim">${escapeHTML(p.bio)}</span>`);
  lines.push('');

  lines.push(`  repos: <span class="hl">${p.public_repos}</span>    followers: <span class="hl">${p.followers}</span>    following: <span class="hl">${p.following}</span>`);
  lines.push('');

  if (p.company)  lines.push(`  org:   ${escapeHTML(p.company)}`);
  if (p.location) lines.push(`  loc:   ${escapeHTML(p.location)}`);
  if (p.blog)     lines.push(`  web:   <span class="accent">${escapeHTML(p.blog)}</span>`);
  lines.push(`  url:   <span class="accent">${escapeHTML(p.html_url)}</span>`);
  lines.push(`  since: ${new Date(p.created_at).toLocaleDateString(locale === 'zh' ? 'zh-CN' : 'en-US', { year: 'numeric', month: 'long', day: 'numeric' })}`);

  lines.push('');
  lines.push(`  <span class="dim">Public gists: ${p.public_gists}</span>`);

  return lines.join('\n');
}
