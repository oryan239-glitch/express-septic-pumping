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
};
// --- Request destination: none approved yet. Set to a Pages Function URL (e.g. '/api/request') once approved. ---
const REQUEST_ENDPOINT = '';
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

const LABEL = { pump: 'Pump my septic tank', backup: "I'm experiencing a backup", grease: 'Commercial grease trap service' };
document.querySelectorAll('[data-request]').forEach((box) => {
  const panels = (n) => box.querySelectorAll('.panel').forEach((p) => { p.hidden = p.dataset.panel !== n; });
  const form = box.querySelector('form');
  const pick = (v, focus) => {
    box.querySelectorAll('.choice').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.choice === v)));
    if (v === 'backup') { panels('backup'); if (focus) box.querySelector('[data-panel=backup] a.btn').focus(); return; }
    form.service.value = v; form.querySelector('.picked').textContent = 'Selected: ' + LABEL[v]; panels('form');
    if (focus) form.name.focus();
  };
  box.querySelectorAll('.choice').forEach((b) => b.addEventListener('click', () => pick(b.dataset.choice, true)));
  const pre = new URLSearchParams(location.search).get('service'); if (LABEL[pre]) pick(pre, false);
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const err = form.querySelector('.err'); let bad = null;
    const checks = [['name', (v) => v.trim().length > 1, 'Enter your name.'], ['phone', (v) => v.replace(/\D/g, '').length >= 10, 'Enter a 10-digit phone number.'], ['where', (v) => v.trim().length > 1, 'Enter your city or ZIP.']];
    for (const [n, ok, msg] of checks) { const el = form[n]; const good = ok(el.value); el.setAttribute('aria-invalid', String(!good)); if (!good && !bad) bad = [el, msg]; }
    if (bad) { err.textContent = bad[1]; bad[0].focus(); return; }
    err.textContent = '';
    const data = Object.fromEntries(new FormData(form));
    const summary = `${LABEL[data.service]} — ${data.name}, ${data.phone}, ${data.where}${data.note ? ' — ' + data.note : ''}`;
    if (REQUEST_ENDPOINT) {
      try { const r = await fetch(REQUEST_ENDPOINT, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(data) }); if (r.ok) { panels('sent'); return; } } catch {}
    }
    box.querySelector('.sum').textContent = summary; panels('fallback'); box.querySelector('[data-panel=fallback]').focus?.();
  });
});

// Mobile bottom bar steps aside while typing so it never covers form fields.
const inForm = (el) => el && el.closest && el.closest('form');
document.addEventListener('focusin', (e) => { if (inForm(e.target)) document.body.classList.add('typing'); });
document.addEventListener('focusout', () => setTimeout(() => { if (!inForm(document.activeElement)) document.body.classList.remove('typing'); }, 300));

// Signature motion: the route line draws once when the service-area section scrolls in.
document.querySelectorAll('.route').forEach((svg) => {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window)) return;
  svg.classList.add('draw');
  const io = new IntersectionObserver((es) => es.forEach((x) => { if (x.isIntersecting) { svg.classList.add('on'); io.disconnect(); } }), { threshold: 0.4 });
  io.observe(svg);
});
