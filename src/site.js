/* Express Septic: ZIP checker, guided request, route line. No dependencies. */
document.documentElement.classList.add('js');
// --- Service-area ZIPs: PENDING OWNER APPROVAL. Edit/confirm before launch. ---
const ZIPS_APPROVED = false;
const ZIPS = {
  'Bonita Springs': ['34134','34135','34136'],
  'Estero': ['33928','33929'],
  'Fort Myers': ['33901','33905','33907','33908','33912','33913','33916','33919','33966','33967'],
  'Cape Coral': ['33904','33909','33914','33990','33991','33993'],
  'Lehigh Acres': ['33936','33971','33972','33973','33974','33976'],
  'Golden Gate Estates': ['34117','34120'],
  'LaBelle': ['33935','33440'],
  'Sanibel': ['33957'],
  'Captiva': ['33924'],
  'Charlotte Harbor': ['33980'],
  'Harbour Heights': ['33983'],
  'Alva': ['33920'],
  // Fort Myers Shores/Tice (33905), South Fort Myers (33907/33908/33919) and Corkscrew (33928/33967) fall under ZIPs listed above.
};
// Requests go to ServiceM8's booking page (owner-approved). No in-site submission, so never a fake 'sent'.
const PHONE = '(239) 451-3261';
const cityFor = (z) => Object.keys(ZIPS).find((c) => ZIPS[c].includes(z));

document.querySelectorAll('[data-zipform]').forEach((f) => f.addEventListener('submit', (e) => {
  e.preventDefault();
  const inp = f.querySelector('input'), out = f.parentNode.querySelector('.zres'), z = inp.value.trim();
  if (!/^\d{5}$/.test(z)) { inp.setAttribute('aria-invalid', 'true'); out.textContent = 'Enter a 5-digit ZIP code.'; return; }
  inp.removeAttribute('aria-invalid');
  const c = cityFor(z);
  out.textContent = c
    ? (ZIPS_APPROVED ? `Yes, ${z} (${c}) is in our service area. Call ${PHONE} to schedule.` : `${z} is in ${c}, an area we work in. Call ${PHONE} to confirm service at your address.`)
    : `Call ${PHONE} to confirm service at your address.`;
}));

// Signature motion: the route line draws once when the service-area section scrolls in.
document.querySelectorAll('.route').forEach((svg) => {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window)) return;
  svg.classList.add('draw');
  const io = new IntersectionObserver((es) => es.forEach((x) => { if (x.isIntersecting) { svg.classList.add('on'); io.disconnect(); } }), { threshold: 0.4 });
  io.observe(svg);
});

// --- GA4 lead events (uses the existing G-ESN48M0VEZ tag; adds no second tag). ---
// phone_call_click: any tel: link. book_request_click: ServiceM8 request link (off-site; the request itself
// can't be seen by GA4). email_click: mailto. book_section_click: on-site "Book" buttons that open the booking choices.
(function () {
  const where = (a) => { const z = a.closest('.mbar,.top,.hero,.phead,.book,.closer,.foot,.quick,.svc,.need,.feat,.price,.process,.revsec,.areasec,.contact,.owner,.hfaq,.prose,.work,.price-panel,.priceband,.cred,.quotes,.standapart,.edu'); return z ? (z.className.split(' ')[0] || z.tagName.toLowerCase()) : 'body'; };
  document.addEventListener('click', (e) => {
    const a = e.target.closest && e.target.closest('a[href]'); if (!a || typeof window.gtag !== 'function') return;
    // No PII: only where the link sits, the page path and the site domain. Clicks are intent, not confirmed leads.
    const h = a.getAttribute('href') || '', p = { link_location: where(a), page_path: location.pathname, site_domain: location.hostname, transport_type: 'beacon' };
    if (h.startsWith('tel:')) gtag('event', 'phone_call_click', p);
    else if (h.startsWith('sms:')) gtag('event', 'sms_click', p);
    else if (h.includes('book.servicem8.com')) gtag('event', 'book_request_click', p);
    else if (h.startsWith('mailto:')) gtag('event', 'email_click', p);
    else if (/#book$/.test(h)) gtag('event', 'book_section_click', p);
  }, { capture: true });
})();

// --- Sticky call bar: hidden while the page's own call button is on screen; never sits over a form or the booking frame. ---
(function () {
  const bar = document.querySelector('.mbar'); if (!bar || !('IntersectionObserver' in window)) return;
  const anchor = document.querySelector('[data-hero-cta]') || document.querySelector('.phead .cta');
  const blockers = document.querySelectorAll('form, iframe, .quote-wrap, .zip, .contact');
  let anchorVisible = !!anchor, blocking = new Set();
  const sync = () => { const off = anchorVisible || blocking.size > 0; bar.classList.toggle('off', off); bar.setAttribute('aria-hidden', off ? 'true' : 'false'); bar.querySelectorAll('a').forEach((a) => off ? a.setAttribute('tabindex', '-1') : a.removeAttribute('tabindex')); };
  if (anchor) new IntersectionObserver((es) => { es.forEach((e) => { anchorVisible = e.isIntersecting || e.boundingClientRect.top > 0; }); sync(); }).observe(anchor);
  const bo = new IntersectionObserver((es) => { es.forEach((e) => { e.isIntersecting ? blocking.add(e.target) : blocking.delete(e.target); }); sync(); }, { rootMargin: '0px 0px -10% 0px' });
  blockers.forEach((b) => bo.observe(b));
  document.addEventListener('focusin', (e) => { if (e.target.matches && e.target.matches('input,select,textarea')) { blocking.add(e.target); sync(); } });
  document.addEventListener('focusout', (e) => { if (blocking.delete(e.target)) sync(); });
  sync();
})();
// --- Subtle entrance: sections fade up once. Skipped with reduced motion; content is never hidden without JS. ---
(function () {
  if (!('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const els = document.querySelectorAll('.sec .shead, .feat figure, .steps, .revs, .price .pcall');
  const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -8% 0px' });
  els.forEach((el) => { const r = el.getBoundingClientRect(); if (r.top < innerHeight) return; el.classList.add('rv'); io.observe(el); });
})();
