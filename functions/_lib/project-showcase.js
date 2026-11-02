/** Install alongside an existing Pages middleware; see README.md. Public content only, no service keys. */
export async function projectShowcase(ctx) {
  const { env, request } = ctx;
  const portal = env.STH_PORTAL_ORIGIN, id = env.STH_WEBSITE_ID, path = env.STH_SHOWCASE_PATH || '/completed-jobs';
  if (!/^https:\/\/[a-z0-9.-]+$/.test(portal || '') || !/^[0-9a-f-]{36}$/.test(id || '') || !/^\/[a-z0-9]+(?:-[a-z0-9]+)*$/.test(path)) return null;
  const url = new URL(request.url);
  if (!['GET', 'HEAD'].includes(request.method)) return null;
  if (url.pathname === '/.well-known/sth-showcase') return Response.json({ version: 1, websiteId: id, path }, { headers: { 'Cache-Control': 'no-store' } });
  const isProject = url.pathname === path || url.pathname.startsWith(path + '/');
  const tail = isProject ? url.pathname.slice(path.length) : '';
  const endpoint = `${portal}/api/connected-sites/${id}/showcase/pages${tail}`;
  try {
    // No cookies or credentials leave the customer's website. No edge cache can retain an unpublished job.
    const upstream = await fetch(endpoint + (isProject ? url.search : ''), {
      redirect: 'manual', signal: AbortSignal.timeout(10000),
      headers: { 'User-Agent': request.headers.get('user-agent') || 'Showcase-Website', 'Cache-Control': 'no-cache' },
      cf: { cacheTtl: 0 },
    });
    if (upstream.status === 404) return isProject ? new Response('Not found', { status: 404, headers: { 'Cache-Control': 'no-store' } }) : null;
    const matching = upstream.headers.get('x-sth-showcase-origin') === url.origin && upstream.headers.get('x-sth-showcase-path') === path;
    if (!matching) {
      if (!isProject) return null;
      return new Response('Projects are temporarily unavailable. Please try again shortly.', { status: 503, headers: { 'Cache-Control': 'no-store' } });
    }
    if (isProject) {
      const headers = new Headers(upstream.headers);
      headers.set('Cache-Control', 'no-store');
      return new Response(request.method === 'HEAD' ? null : upstream.body, { status: upstream.status, headers });
    }
    // The caller can insert this link in its existing desktop/mobile navigation without changing the homepage layout.
    return { href: path + '/', label: decodeURIComponent(upstream.headers.get('x-sth-showcase-label') || 'Completed%20Jobs') };
  } catch {
    return isProject ? new Response('Projects are temporarily unavailable. Please try again shortly.', { status: 503, headers: { 'Cache-Control': 'no-store' } }) : null;
  }
}

/** Drop-in middleware for Pages sites without another middleware. Use the helpers when composing. */
export async function onRequest(ctx) {
  const url = new URL(ctx.request.url), path = ctx.env.STH_SHOWCASE_PATH || '/completed-jobs';
  const isProject = url.pathname === path || url.pathname.startsWith(path + '/');
  if (isProject || url.pathname === '/.well-known/sth-showcase') return (await projectShowcase(ctx)) || ctx.next();
  const response = await ctx.next();
  if (!response.ok || !(response.headers.get('content-type') || '').includes('text/html')) return response;
  const link = await projectShowcase(ctx);
  if (!link || link instanceof Response) return response;
  return addShowcaseNavigation(response, link);
}

export function addShowcaseNavigation(response, link) {
  // Mark the site's existing desktop/mobile nav with data-sth-showcase-nav when it uses other selectors.
  return new HTMLRewriter().on('nav[aria-label="Primary"], nav[aria-label="Mobile"], nav[aria-label="Main navigation"], [data-sth-showcase-nav]', {
    element(element) {
      const escape = s => s.replace(/[&<>"']/g, c => ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;' })[c]);
      element.append(`<a href="${escape(link.href)}">${escape(link.label)}</a>`, { html: true });
    },
  }).transform(response);
}
