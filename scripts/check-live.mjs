#!/usr/bin/env node
/**
 * Small production smoke check. Not part of `verify` because it needs network.
 * Run after a deploy: `npm run check:live`.
 */
const APEX = 'https://robusr.cn';
const checks = [
  { label: 'apex EN', url: `${APEX}/`, status: 200 },
  { label: 'apex ZH', url: `${APEX}/zh/`, status: 200 },
  { label: 'apex FR', url: `${APEX}/fr/`, status: 200 },
  { label: 'apex API', url: `${APEX}/api/github`, status: 200, json: true },
  { label: 'apex v3 asset', url: `${APEX}/assets/projects/plates/v3/onesarm-a-poster-800.webp`, status: 200 },
  { label: 'www root 301', url: 'https://www.robusr.cn/', status: 301, location: `${APEX}/` },
  { label: 'www path/query 301', url: 'https://www.robusr.cn/zh/?x=1', status: 301, location: `${APEX}/zh/?x=1` },
  { label: 'www API 301', url: 'https://www.robusr.cn/api/github', status: 301, location: `${APEX}/api/github` },
];

let failed = 0;
for (const check of checks) {
  try {
    const res = await fetch(check.url, {
      redirect: 'manual',
      headers: { 'user-agent': 'robusr-site-smoke/1.0' },
      signal: AbortSignal.timeout(20_000),
    });
    const location = res.headers.get('location');
    const type = res.headers.get('content-type') ?? '';
    const problems = [];
    if (res.status !== check.status) problems.push(`status ${res.status}, expected ${check.status}`);
    if (check.location && location !== check.location) problems.push(`location ${location ?? '(none)'}, expected ${check.location}`);
    if (check.json && !type.includes('application/json')) problems.push(`content-type ${type || '(none)'}, expected JSON`);
    if (problems.length) {
      failed++;
      console.log(`FAIL ${check.label}: ${problems.join('; ')}`);
    } else {
      console.log(`ok   ${check.label} (${res.status}${location ? ` → ${location}` : ''})`);
    }
  } catch (error) {
    failed++;
    console.log(`FAIL ${check.label}: ${error.message}`);
  }
}
process.exit(failed ? 1 : 0);
