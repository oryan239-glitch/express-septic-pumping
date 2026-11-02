// Content adapter between expresssepticpumping.com (static, Cloudflare Pages) and the ServiceTechHub portal (Amy + Project Showcase).
// Protocol: the portal's "connected website" v1 (same as Love ALF). Nothing here changes layout or styles:
// it only swaps the TEXT of elements marked data-sth-field="…", and renders /our-work/ from approved published snapshots.
// Env (Pages project settings): STH_PORTAL_ORIGIN, STH_WEBSITE_ID, STH_CONNECT_KEY (>=32 chars, same value as the portal's
// per-site connected key for Express). When any is missing, every page is served exactly as built.
export const RENDERER = 'love-alf-v1'; // connected-protocol id (historic name)
export const PAGES = ['/', '/residential-septic-tank-pumping/', '/commercial-grease-trap-service/', '/service-area/', '/contact/', '/about/', '/faq/'];
// Starting content = the text currently in the static pages (build.py). Must satisfy the portal's contentSchema.
export const DEFAULTS = {
  businessName: 'Express Septic Tank Pumping',
  headline: 'Septic tank pumping in Southwest Florida',
  description: "Need your tank pumped or dealing with a backup? Call Express to talk through what's happening, confirm service at your address, and get pricing.",
  phone: '(239) 451-3261', email: 'expressseptictankpumping@gmail.com',
  address: '23357 Olde Meadowbrook Circle, Estero, FL 34134',
  hours: '',
  services: 'Residential septic tank pumping, commercial septic pumping, grease trap service and septic inspections.',
  heroImage: '', heroImageAlt: '', accent: 'navy',
};
export const FIELDS = ['headline', 'description', 'email', 'address', 'services'];
export function configured(env) {
  const devOk = env.STH_DEV === '1' && /^http:\/\/127\.0\.0\.1:\d+$/.test(env.STH_PORTAL_ORIGIN || ''); // local tests only
  return Boolean(env.STH_PORTAL_ORIGIN && (devOk || /^https:\/\/[a-z0-9.-]+$/.test(env.STH_PORTAL_ORIGIN)) && /^[0-9a-f-]{36}$/.test(env.STH_WEBSITE_ID || '') && (env.STH_CONNECT_KEY || '').length >= 32);
}
const b64u = (buf) => btoa(String.fromCharCode(...new Uint8Array(buf))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
const unb64u = (s) => { s = s.replace(/-/g, '+').replace(/_/g, '/'); while (s.length % 4) s += '='; return Uint8Array.from(atob(s), (c) => c.charCodeAt(0)); };
/** Same checks as the portal's verifyTicket (HMAC-SHA256, 90 s max lifetime, known page). */
export async function verifyTicket(value, key, site) {
  try {
    if (!value || value.length > 2000) return null;
    const [body, sig, extra] = value.split('.');
    if (!body || !sig || extra) return null;
    const k = await crypto.subtle.importKey('raw', new TextEncoder().encode(key), { name: 'HMAC', hash: 'SHA-256' }, false, ['verify']);
    if (!(await crypto.subtle.verify('HMAC', k, unb64u(sig), new TextEncoder().encode(body)))) return null;
    const t = JSON.parse(new TextDecoder().decode(unb64u(body)));
    const now = Math.floor(Date.now() / 1000);
    if (t.site !== site || !/^[0-9a-f-]{36}$/.test(t.actor || '') || !Number.isSafeInteger(t.revision) || t.revision < 0 || !['draft', 'published'].includes(t.view) || !PAGES.includes(t.path) || !Number.isSafeInteger(t.exp) || t.exp < now || t.exp > now + 90) return null;
    return t;
  } catch { return null; }
}
export async function signForTest(ticket, key) { // used by local tests only
  const body = b64u(new TextEncoder().encode(JSON.stringify(ticket)));
  const k = await crypto.subtle.importKey('raw', new TextEncoder().encode(key), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  return `${body}.${b64u(await crypto.subtle.sign('HMAC', k, new TextEncoder().encode(body)))}`;
}
async function portal(env, path, init = {}, ttl = 0) {
  const r = await fetch(`${env.STH_PORTAL_ORIGIN}${path}`, { ...init, redirect: 'manual', cf: ttl ? { cacheTtl: ttl, cacheEverything: true } : { cacheTtl: 0 }, signal: AbortSignal.timeout(6000) });
  return r;
}
export async function publishedContent(env, fresh = false) {
  try { const r = await portal(env, `/api/connected-sites/${env.STH_WEBSITE_ID}`, {}, fresh ? 0 : 10); if (!r.ok) return null; const v = await r.json(); return v && v.content ? v : null; } catch { return null; }
}
export async function draftContent(env, ticketHeader) {
  try { const r = await portal(env, `/api/connected-sites/${env.STH_WEBSITE_ID}/preview`, { headers: { 'x-sth-preview': ticketHeader } }); if (!r.ok) return null; return await r.json(); } catch { return null; }
}
export async function showcaseFeed(env, fresh = false) {
  try { const r = await portal(env, `/api/connected-sites/${env.STH_WEBSITE_ID}/showcase`, {}, fresh ? 0 : 30); if (!r.ok) return null; return await r.json(); } catch { return null; }
}
export function applyContent(res, content) {
  let rw = new HTMLRewriter();
  for (const f of FIELDS) {
    const v = typeof content[f] === 'string' ? content[f] : '';
    if (!v) continue;
    rw = rw.on(`[data-sth-field="${f}"]`, {
      element(el) {
        el.setInnerContent(v); // text only; HTML is escaped
        if (f === 'email' && el.tagName === 'a') el.setAttribute('href', `mailto:${v}`);
      },
    });
  }
  return rw.transform(res);
}
