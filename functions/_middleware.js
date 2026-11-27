// Canonical-host redirect for the www alias. The apex remains untouched.
// Static asset paths are excluded in public/_routes.json so they keep their
// immutable CDN caching; HTML and the GitHub API pass through this middleware.
export async function onRequest(context) {
  const url = new URL(context.request.url);
  if (url.hostname === 'www.robusr.cn') {
    url.protocol = 'https:';
    url.hostname = 'robusr.cn';
    return Response.redirect(url.toString(), 301);
  }
  return context.next();
}
