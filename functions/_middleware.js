// expresssepticpumping.com ⇄ ServiceTechHub portal (editing tool + Project Showcase at /completed-jobs).
// Safe by default: with STH_* env unset or the portal unreachable, every request is served exactly as built.
import { RENDERER, DEFAULTS, configured, verifyTicket, publishedContent, draftContent, applyContent } from './_lib/sth-connect.js';
import { projectShowcase, addShowcaseNavigation } from './_lib/project-showcase.js';
const noStore = { 'cache-control': 'no-store', 'x-robots-tag': 'noindex, nofollow' };
const isHtml = (r) => (r.headers.get('content-type') || '').includes('text/html');

// Recent-jobs block on the home page is hidden in the static build; reveal it (linking to the showcase) only when the showcase is live.
function revealJobs(res, link) {
  return new HTMLRewriter().on('[data-sth-recent-jobs]', { element(el) { el.removeAttribute('hidden'); } })
    .on('[data-sth-recent-jobs-link]', { element(el) { el.setAttribute('href', link.href); } }).transform(res);
}

export async function onRequest(ctx) {
  { const u = new URL(ctx.request.url); if (u.hostname === 'www.expresssepticpumping.com') { u.hostname = 'expresssepticpumping.com'; u.protocol = 'https:'; return Response.redirect(u.toString(), 301); } }
  const { request, env, next } = ctx;
  const url = new URL(request.url);
  if (!['GET', 'HEAD'].includes(request.method)) return next();
  const p = url.pathname;

  // 1) Project Showcase (needs STH_PORTAL_ORIGIN + STH_WEBSITE_ID; path from STH_SHOWCASE_PATH, default /completed-jobs).
  const sp = env.STH_SHOWCASE_PATH || '/completed-jobs';
  const isShowcase = p === sp || p.startsWith(sp + '/') || p === '/.well-known/sth-showcase';
  if (isShowcase) { const r = await projectShowcase(ctx); return r instanceof Response ? r : next(); }

  const editorOn = configured(env);
  const fresh = url.searchParams.has('sth_check') || /ServiceTechHub-PublishCheck/.test(request.headers.get('user-agent') || '');
  if (editorOn && p === '/api/sth-editor') {
    const t = await verifyTicket(request.headers.get('x-sth-preview'), env.STH_CONNECT_KEY, env.STH_WEBSITE_ID);
    if (!t) return new Response(null, { status: 403, headers: noStore });
    return Response.json({ renderer: RENDERER, websiteId: env.STH_WEBSITE_ID, enabled: true, content: DEFAULTS }, { headers: noStore });
  }

  const res = await next();
  if (!res.ok || !isHtml(res)) return res;
  let out = res, headers = new Headers(res.headers);

  // 2) Editing tool: portal-signed preview or published content.
  if (editorOn) {
    const ticket = request.headers.get('x-sth-preview');
    if (ticket) {
      const t = await verifyTicket(ticket, env.STH_CONNECT_KEY, env.STH_WEBSITE_ID);
      const d = t && (await draftContent(env, ticket));
      if (!t || !d?.content) return new Response(null, { status: 403, headers: noStore });
      out = applyContent(out, d.content);
      for (const [k, v] of Object.entries(noStore)) headers.set(k, v);
      headers.set('x-sth-renderer', RENDERER); headers.set('x-sth-revision', String(d.revision));
    } else {
      const pub = await publishedContent(env, fresh);
      if (pub) { out = applyContent(out, pub.content); headers.set('x-sth-renderer', RENDERER); headers.set('x-sth-published-revision', String(pub.revision)); }
    }
  }

  // 3) Showcase nav link + recent-jobs block, only while the showcase is enabled for this site.
  const link = await projectShowcase(ctx);
  if (link && !(link instanceof Response)) out = revealJobs(addShowcaseNavigation(out, link), link);
  return new Response(out.body, { status: res.status, headers });
}
