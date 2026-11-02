#!/usr/bin/env python3
"""Build script: generates static pages at repo root from data in this file + src/styles.css."""
import json, os, shutil
BASE="https://expresssepticpumping.com"
NAME="Express Septic Tank Pumping"; PHONE="(239) 451-3261"; TEL="+12394513261"
BOOK="https://book.servicem8.com/request_booking?uuid=019fca12-b6bf-721c-8a2b-41d89e1a1b5b"
EMAIL="expressseptictankpumping@gmail.com"
REVIEW="https://g.page/r/CYxfVw5rrgwLEBM/review"
CITIES_ALL=["Estero","Bonita Springs","Naples","North Naples","Fort Myers","Cape Coral","Lehigh Acres","San Carlos Park"]
SERVICES=[
 ("septic-tank-pumping","Septic Tank Pumping","Septic Tank Pumping & Septic Tank Cleaning | SW Florida | Express Septic","Septic tank pumping, septic pumping & septic tank cleaning near you in Estero, Naples, Fort Myers & nearby. Ask about septic tank pumping cost: (239) 451-3261.",
  ["Septic tank pumping removes the sludge and scum that build up in your tank over time. If solids are left too long they can flow into the drain field, which is the most expensive part of a septic system to repair.",
   "Most households should have the tank pumped every 3 to 5 years, depending on tank size and how many people live in the home. Homes with garbage disposals, frequent guests or older systems may need service more often.",
   "Warning signs you're overdue: slow drains, gurgling pipes, sewage odors in the yard, soggy or extra-green grass over the drain field, or toilets that back up."]),
 ("residential-septic-tank-pumping","Residential Septic Tank Pumping","Residential Septic Tank Pumping & Cleaning | SW Florida | Express Septic","Residential septic tank pumping and residential septic tank cleaning near you in Lee & Collier County. Residential septic service: (239) 451-3261.",
  ["Our residential septic tank pumping service is built for homeowners. We locate the tank lid, pump out the full tank, and let you know what we see so you can plan ahead.",
   "Regular pumping protects your drain field, prevents backups inside the house and helps your system last longer. It's also a smart step before buying or selling a home, before a big family gathering, or after a heavy rainy season.",
   "Tip: keep a record of every pumping date. It helps you stay on schedule and shows buyers the system has been maintained."]),
 ("commercial-septic-tank-pumping","Commercial Septic Tank Pumping","Commercial Septic Tank Pumping & Septic Service | SW Florida","Commercial septic tank pumping and commercial septic service near you for businesses in Lee & Collier County. Call (239) 451-3261 for a quote.",
  ["Businesses on septic need a reliable pumping schedule. Commercial systems often see heavier use than homes, so solids build up faster and a backup can shut down your operation.",
   "We pump septic tanks for offices, retail sites, churches, rental properties, farms and other commercial properties. Call us to set up a schedule that fits your usage.",
   "Keeping a steady pumping schedule helps avoid emergency calls, odors near customers and costly drain field damage."]),
 ("septic-inspections","Septic Inspections","Septic Inspection for Home Purchase | Fort Myers & Naples | Express Septic","Septic inspection & real estate septic inspection for home purchases in Fort Myers, Naples, Estero & nearby. Septic inspection cost: call (239) 451-3261.",
  ["A septic inspection checks the condition of your tank and how the system is working. It's common when buying or selling a home, and a good idea if you're noticing problems.",
   "Buying a home on septic? An inspection helps you understand what you're getting before closing. Selling? Having the system checked ahead of time can help avoid surprises during the sale.",
   "Call us to discuss what kind of inspection you need and we'll give you a quote."]),
]
CITY={
 "Estero":("Lee County","Estero sits between Fort Myers and Bonita Springs along US-41 and I-75. Our address is right here in Estero, so local homes and businesses are close to home for our crew.","Many Estero properties, from older homes to rural lots east of I-75, rely on septic systems that need regular pumping."),
 "Bonita Springs":("Lee County","Bonita Springs is at the southern end of Lee County, bordering Estero to the north and Collier County to the south.","Parts of Bonita Springs, especially older neighborhoods and larger lots east of I-75, still use septic tanks."),
 "Naples":("Collier County","Naples is the largest city area in Collier County, on the Gulf of Mexico.","Many homes in the Naples area outside central sewer service, including Golden Gate Estates and other larger-lot areas, use septic systems."),
 "North Naples":("Collier County","North Naples covers the northern part of the Naples area in Collier County, just south of Bonita Springs.","North Naples homes on septic benefit from a regular pumping schedule, especially in Florida's rainy season when high water tables put extra stress on drain fields."),
 "Fort Myers":("Lee County","Fort Myers is the county seat of Lee County, on the Caloosahatchee River.","Plenty of Fort Myers homes and businesses, particularly in unincorporated areas around the city, are on septic tanks."),
 "Cape Coral":("Lee County","Cape Coral is known for its hundreds of miles of canals and is one of the largest cities by area in Florida.","Many Cape Coral homes still use septic systems while the city continues expanding its utility network, so routine pumping matters."),
 "Lehigh Acres":("Lee County","Lehigh Acres is a large community in eastern Lee County, east of Fort Myers.","A large share of Lehigh Acres homes are on septic tanks and private wells, making regular pumping and inspections especially important."),
 "San Carlos Park":("Lee County","San Carlos Park is a community in Lee County between Fort Myers and Estero, near Florida Gulf Coast University.","Homes in San Carlos Park on septic systems should be pumped every few years to protect their drain fields."),
}
CITY['East Naples']=('Collier County', 'East Naples is the area of Collier County southeast of downtown Naples, along US-41 toward Marco Island.', 'Many East Naples homes on larger lots off the main sewer lines rely on septic systems.')
CITY['Golden Gate']=('Collier County', 'Golden Gate is a community in Collier County east of Naples; nearby Golden Gate Estates is known for its large wooded lots.', 'Golden Gate Estates homes are widely on septic tanks and private wells, so regular pumping protects the system.')
CITY['Marco Island']=('Collier County', "Marco Island is the largest barrier island in Florida's Ten Thousand Islands area, south of Naples.", 'Waterfront and island properties need septic maintenance done right to protect nearby waterways.')
CITY['Immokalee']=('Collier County', 'Immokalee is an agricultural community in inland Collier County, known for its farming industry.', 'Rural homes, farms and businesses around Immokalee often depend on septic systems.')
CITY['Ave Maria']=('Collier County', 'Ave Maria is a planned town in eastern Collier County, home to Ave Maria University.', 'Properties in and around Ave Maria on septic benefit from routine pumping and inspections.')
CITY['North Fort Myers']=('Lee County', 'North Fort Myers lies across the Caloosahatchee River from Fort Myers in Lee County.', 'Many North Fort Myers neighborhoods and rural properties use septic tanks.')
CITY['Fort Myers Beach']=('Lee County', 'Fort Myers Beach is a town on Estero Island along the Gulf of Mexico.', 'Beach-area properties on septic need dependable pumping to keep systems working in sandy, low-lying ground.')
CITY['Three Oaks']=('Lee County', 'Three Oaks is a community in southern Lee County near Estero and San Carlos Park.', 'Three Oaks homes on septic should plan pumping every few years.')
CITY['Gateway']=('Lee County', 'Gateway is a planned community in Lee County east of Fort Myers, near Southwest Florida International Airport.', 'We serve Gateway-area homes and businesses that use septic systems.')
CITY['Alva']=('Lee County', 'Alva is a rural community in eastern Lee County along the Caloosahatchee River.', 'Rural Alva homes, ranches and farms commonly rely on septic systems.')
CITY['Buckingham']=('Lee County', 'Buckingham is a rural community in Lee County east of Fort Myers, known for larger acreage lots.', 'Large-lot Buckingham properties typically use septic tanks that need regular pumping.')
CITY['Sanibel']=('Lee County', 'Sanibel is a barrier island city in Lee County known for its beaches, shelling and wildlife refuge.', 'Island properties need careful septic maintenance to protect the surrounding environment.')
CITY['Pine Island']=('Lee County', 'Pine Island is the largest island in Lee County, with communities including Bokeelia, Pineland, St. James City and Matlacha.', 'Many Pine Island homes and businesses use septic systems.')
CITY['Port Charlotte']=('Charlotte County', 'Port Charlotte is a community in Charlotte County, north of the Peace River from Punta Gorda.', 'Many Port Charlotte homes are on septic, so routine pumping helps prevent backups.')
CITY['Punta Gorda']=('Charlotte County', 'Punta Gorda is the county seat of Charlotte County, on Charlotte Harbor.', 'Homes in and around Punta Gorda that use septic systems need regular maintenance.')
CITY['Everglades City']=('Collier County', 'Everglades City is a small town in southern Collier County, a gateway to Everglades National Park and the Ten Thousand Islands.', 'Remote properties around Everglades City depend on septic systems and timely pumping.')
CITIES_ALL=list(CITY)
def slug(c): return "septic-tank-pumping-"+c.lower().replace(" ","-")+"-fl"
FAQ=[("How often should I pump my septic tank?","Most homes need septic tank pumping every 3 to 5 years. Tank size, number of people in the home and water use all affect how often."),
("How much does it cost to pump a septic tank in Florida?","Residential septic pumping starts at $399.99; call (239) 451-3261 to confirm for your tank. Your final quote depends on tank size, tank access, whether the lid needs locating or digging, and after-hours visits."),
("What are signs my septic tank is full?","Slow drains, gurgling pipes, sewage odors, wet or extra-green spots over the drain field, and backups are common signs."),
("Do you pump commercial septic tanks?","Yes. We provide commercial septic tank pumping for businesses and other properties."),
("Do you do septic inspections for real estate?","Yes. We offer septic inspections for buyers, sellers and homeowners."),
("What areas do you serve?","Estero, Bonita Springs, Naples, North Naples, Fort Myers, Cape Coral, Lehigh Acres, San Carlos Park and nearby areas of Lee and Collier County."),
("What shouldn't go into a septic system?","Avoid grease, wipes (even 'flushable'), paper towels, feminine products, harsh chemicals and medications. They can clog the system or harm the bacteria that break down waste."),
("How do I book?","Tap Book Online to request a time, or call (239) 451-3261.")]
PAGES=[]
EXTRA={
"septic-tank-pumping":"<h2>Septic Pumping Near Me</h2><p>We provide septic pumping and septic tank cleaning across Lee and Collier County. Residential septic tank pumping starts at $399.99; call to confirm for your tank. Your final quote depends on tank size, tank access, whether the lid needs locating or digging, and after-hours visits.</p><h2>Emergency Septic Service</h2><p>Sewage backing up or a tank overflowing? Call <a href='tel:+12394513261'>(239) 451-3261</a> right away and avoid running water until we get there. Night or day, we're available for emergencies. For routine service, we can often make it same day when possible.</p>",
"residential-septic-tank-pumping":"<h2>Residential Septic Service Near Me</h2><p>Residential septic tank cleaning removes built-up sludge and scum so your home's system keeps working.</p><h2>Tank Size FAQs</h2><h3>What size is my septic tank?</h3><p>Many homes have tanks around 750 to 1,500 gallons; larger homes generally have larger tanks. Your permit records or our crew can help confirm the size.</p><h3>Does tank size change how often I pump?</h3><p>Yes. Smaller tanks and larger households need pumping more often. See <a href='/how-often-to-pump-septic-tank/'>how often to pump your septic tank</a>.</p>",
"commercial-septic-tank-pumping":"<h2>Commercial Septic Pumping Near Me</h2><p>Need commercial septic service in Lee or Collier County? Call to discuss your property. Restaurants with grease traps should mention them when you call so we can talk through your needs.</p>",
"septic-inspections":"<h2>Septic Inspection for Home Purchase</h2><p>A real estate septic inspection gives buyers and sellers a clearer picture of the system before closing. We serve Fort Myers, Naples and the surrounding area.</p><h2>Septic Inspection Cost</h2><p>Cost depends on the property and type of inspection. Call (239) 451-3261 for a quote.</p>",
}
def schema(extra=None):
  s={"@context":"https://schema.org","@type":["LocalBusiness","Plumber"],"name":NAME,"url":BASE+"/","telephone":TEL,"email":EMAIL,"priceRange":"$399.99+",
   "address":{"@type":"PostalAddress","streetAddress":"23357 Olde Meadowbrook Circle","addressLocality":"Estero","addressRegion":"FL","postalCode":"34134","addressCountry":"US"},
   "areaServed":[{"@type":"City","name":c+", FL"} for c in CITIES_ALL],
   "makesOffer":[({"@type":"Offer","itemOffered":{"@type":"Service","name":s[1]},"priceSpecification":{"@type":"PriceSpecification","minPrice":399.99,"priceCurrency":"USD"}} if s[0]=="residential-septic-tank-pumping" else {"@type":"Offer","itemOffered":{"@type":"Service","name":s[1]}}) for s in SERVICES]}
  out=[s]
  if extra: out.append(extra)
  return "".join(f'<script type="application/ld+json">{json.dumps(o)}</script>' for o in out)
TRUCK_ALT="Express Septic Tank Pumping 4,200-gallon vacuum truck parked at a Southwest Florida home"
HERO_IMG=f'<img src="/assets/img/truck-wide-1024.webp" srcset="/assets/img/truck-wide-640.webp 640w, /assets/img/truck-wide-1024.webp 1024w, /assets/img/truck-wide-1536.webp 1536w" sizes="(min-width:960px) 52vw, 100vw" alt="{TRUCK_ALT}" width="1536" height="960" fetchpriority="high">'
CREW='<figure class="shot crew"><img src="/assets/img/crew-1024.webp" srcset="/assets/img/crew-640.webp 640w, /assets/img/crew-1024.webp 1024w, /assets/img/crew-1500.webp 1500w" sizes="(min-width:960px) 680px, 100vw" alt="Express Septic Tank Pumping crew with the 4,200-gallon vacuum truck" width="1500" height="1125" loading="lazy"></figure>'
LIDS='<figure class="shot"><img src="/assets/img/lids-1024.webp" srcset="/assets/img/lids-640.webp 640w, /assets/img/lids-1024.webp 1024w, /assets/img/lids-1500.webp 1500w" sizes="(min-width:960px) 820px, 100vw" alt="Septic tank lids uncovered and opened for pumping at a Southwest Florida home" width="1500" height="1734" loading="lazy" style="aspect-ratio:auto"></figure>'
RISER='<figure class="shot"><img src="/assets/img/riser-1024.webp" srcset="/assets/img/riser-640.webp 640w, /assets/img/riser-1024.webp 1024w, /assets/img/riser-1500.webp 1500w" sizes="(min-width:960px) 820px, 100vw" alt="Looking down a septic tank riser at the effluent filter" width="1500" height="837" loading="lazy" style="aspect-ratio:auto"></figure>'
JOB='<figure class="shot"><img src="/assets/img/job-830.webp" srcset="/assets/img/job-640.webp 640w, /assets/img/job-830.webp 830w" sizes="(min-width:960px) 820px, 100vw" alt="Express Septic Tank Pumping truck pumping a residential septic tank in Southwest Florida" width="830" height="960" fetchpriority="high" style="aspect-ratio:auto"></figure>'
WIDE='<figure class="shot"><img src="/assets/img/wide-job-830.webp" srcset="/assets/img/wide-job-640.webp 640w, /assets/img/wide-job-830.webp 830w" sizes="(min-width:960px) 820px, 100vw" alt="Vacuum hose running from the Express truck to an opened septic tank" width="830" height="960" loading="lazy" style="aspect-ratio:auto"></figure>'
HOSE='<figure class="shot"><img src="/assets/img/hose-776.webp" srcset="/assets/img/hose-640.webp 640w, /assets/img/hose-776.webp 776w" sizes="(min-width:960px) 820px, 100vw" alt="Septic tank being pumped through the vacuum hose" width="776" height="960" loading="lazy" style="aspect-ratio:auto"></figure>'
OUTLET='<figure class="shot"><img src="/assets/img/outlet-720.webp" srcset="/assets/img/outlet-640.webp 640w, /assets/img/outlet-720.webp 720w" sizes="(min-width:960px) 820px, 100vw" alt="Opened septic tank outlet with effluent filter" width="720" height="960" loading="lazy" style="aspect-ratio:auto"></figure>'
REAR='<figure class="shot"><img src="/assets/img/rear-1024.webp" srcset="/assets/img/rear-640.webp 640w, /assets/img/rear-1024.webp 1024w, /assets/img/rear-1500.webp 1500w" sizes="(min-width:960px) 820px, 100vw" alt="Express septic and grease pumping truck at the curb" width="1500" height="2000" loading="lazy" style="aspect-ratio:auto"></figure>'
SIDE='<figure class="shot"><img src="/assets/img/side-1024.webp" srcset="/assets/img/side-640.webp 640w, /assets/img/side-1024.webp 1024w, /assets/img/side-1436.webp 1436w" sizes="(min-width:960px) 680px, 100vw" alt="Express Septic Tank Pumping 4,200-gallon septic and grease trap truck" width="1436" height="900" loading="lazy"></figure>'
def photo(sid,alt):
  # Photo slots stay hidden until a real photo exists at assets/img/<slot>.jpg (see PHOTO-SLOTS.md).
  if sid=="septic-tank-pumping": return LIDS+WIDE
  if sid=="septic-inspections": return HOSE+OUTLET
  if sid=="how-it-works": return RISER+HOSE+OUTLET
  if sid=="septic-system-maintenance": return RISER
  if sid.startswith("septic-tank-pumping-") and sid.endswith("-fl"):
    i=[slug(c) for c in CITIES_ALL].index(sid); return [WIDE,HOSE,OUTLET,LIDS,JOB,RISER][i%6].replace('fetchpriority="high"','loading="lazy"')
  if sid=="residential-septic-tank-pumping": return JOB
  if False:
    return f'<figure class="shot"><img src="/assets/img/truck-wide-1024.webp" srcset="/assets/img/truck-wide-640.webp 640w, /assets/img/truck-wide-1024.webp 1024w" sizes="(min-width:960px) 860px, 100vw" alt="{TRUCK_ALT}" width="1536" height="960" loading="lazy"></figure>'
  if os.path.exists(f"assets/img/{sid}.jpg"):
    return f'<figure class="shot" data-photo-slot="{sid}"><img src="/assets/img/{sid}.jpg" alt="{alt}" loading="lazy" width="1600" height="1000"></figure>'
  return ""
NAVITEMS=[("/residential-septic-tank-pumping/","Residential"),("/commercial-grease-trap-service/","Grease traps"),("/service-area/","Service area"),("/about/","About"),("/faq/","FAQ")]
NAVL="".join(f'<a href="{h}">{t}</a>' for h,t in NAVITEMS)
NAV="".join(f'<a href="/{s[0]}/">{s[1]}</a>' for s in SERVICES)+'<a href="/commercial-grease-trap-service/">Commercial Grease Trap Service</a>'
VAL="<p class='values'>Honest, reliable and fair — great customer service is our top priority.</p>"
EMERG="Night or day, we're available for emergencies. Call (239) 451-3261. For routine service, we can often make it same day when possible."
CTA=f'<div class="cta"><a class="btn primary" href="tel:{TEL}">Call Express <span class="num">{PHONE}</span></a><a class="btn ghost" href="/contact/#request">Request service</a></div>'
REV=f'<section class="band reviews"><div class="wrap"><p class="eyebrow">Reviews</p><h2>Read what customers say on Google</h2><p>Our reviews live on our Google Business Profile, where you can read them in full or leave your own.</p><a class="btn ghost" href="{REVIEW}" rel="noopener">Open our Google reviews</a></div></section>'
def page(path,title,desc,h1,body,extra=None,hero=None,lead=""):
  foot="".join(f'<a href="/{slug(c)}/">{c}</a>' for c in CITIES_ALL[:12])+'<a href="/service-area/">All areas</a>'
  H1A=' data-sth-field="headline"' if path=="/" else ""
  if not hero: body=f'<div class="wrap prose">{body}</div>'
  top=hero if hero else f'<section class="phead"><div class="wrap"><p class="eyebrow">Express Septic Tank Pumping</p><h1>{h1}</h1>{lead}{CTA}</div></section>'
  if hero: top=top.replace("<h1>",f"<h1{H1A}>",1)
  html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{BASE}{path}"><meta name="theme-color" content="#0f1b2d">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{BASE}{path}"><meta property="og:type" content="website"><meta property="og:image" content="{BASE}/assets/img/truck-wide-1536.webp">
{'<link rel="preload" as="image" href="/assets/img/truck-wide-1024.webp" imagesrcset="/assets/img/truck-wide-640.webp 640w, /assets/img/truck-wide-1024.webp 1024w, /assets/img/truck-wide-1536.webp 1536w" imagesizes="(min-width:960px) 52vw, 100vw">' if hero else ''}
<link rel="stylesheet" href="/styles.css">{schema(extra)}<script src="/site.js" defer></script></head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap bar"><a class="logo" href="/" aria-label="{NAME} home"><span class="mark">EXPRESS</span><span class="sub">Septic Tank Pumping</span></a>
<nav aria-label="Primary">{NAVL}</nav><a class="hcall" href="tel:{TEL}"><span class="lbl">Call</span> {PHONE}</a>
<details class="menu"><summary aria-label="Open menu">Menu</summary><nav aria-label="Mobile">{NAVL}<a href="/contact/">Contact</a><a href="tel:{TEL}">Call {PHONE}</a></nav></details></div></header>
<main id="main">{top}<div class="body">{body}</div>{REV}<section class="band closer"><div class="wrap"><h2>Talk to Express about your tank</h2><p>{EMERG}</p>{CTA}</div></section></main>
<footer id="contact" class="foot"><div class="wrap fgrid"><div><p class="mark">EXPRESS</p><p>{NAME} LLC<br>23357 Olde Meadowbrook Circle, Estero, FL 34134<br><a href="tel:{TEL}">{PHONE}</a><br><a data-sth-field="email" href="{"mailto:"+EMAIL if EMAIL else "/contact/"}">{EMAIL or "Send a request"}</a></p><p>Owner-operated. Licensed &amp; insured. We come to you.</p><p class="dot">USDOT 6673233</p></div>
<div><p class="fh">Services</p>{NAV}</div><div><p class="fh">Areas</p>{foot}</div><div><p class="fh">Info</p><a href="/">Home</a><a href="/how-it-works/">How it works</a><a href="/septic-system-maintenance/">Septic maintenance</a><a href="/how-often-to-pump-septic-tank/">How often to pump</a><a href="/about/">About</a><a href="/faq/">FAQ</a><a href="/contact/">Contact</a><a href="/privacy/">Privacy</a><a href="/terms/">Terms</a></div></div></footer>
<div class="mbar" role="region" aria-label="Quick contact"><a class="btn primary" href="tel:{TEL}">Call Express</a><a class="btn ghost" href="/contact/#request">Request service</a></div></body></html>'''
  html=html.replace("<div class=\"body\"></div>","")
  pre="../"*(path.count("/")-1) or "./"
  html=html.replace('href="/','href="'+pre).replace('src="/','src="'+pre).replace(', /assets',', '+pre+'assets').replace('srcset="/','srcset="'+pre).replace("href='/","href='"+pre).replace('imagesrcset="'+pre,'imagesrcset="'+pre)
  d="."+path; os.makedirs(d,exist_ok=True); open(d+"index.html","w").write(html); PAGES.append(path)
def sec(inner,cls=""): return f'<section class="sec {cls}"><div class="wrap">{inner}</div></section>'
svc_list="<ul class='rows'>"+"".join(f'<li><a href="/{s[0]}/">{s[1]}</a></li>' for s in SERVICES)+"<li><a href='/commercial-grease-trap-service/'>Commercial Grease Trap Service</a></li></ul>"
city_list="<ul class='cities'>"+"".join(f'<li><a href="/{slug(c)}/">{c}</a></li>' for c in CITIES_ALL)+"</ul>"
REQUEST=f'''<div class="req" id="request" data-request>
<h2>Request service</h2><p class="muted">Pick what you need. We'll carry it through.</p>
<div class="choices" role="group" aria-label="What do you need?">
<button type="button" class="choice" data-choice="pump" aria-pressed="false"><b>Pump my septic tank</b><span>Routine pumping for a home</span></button>
<button type="button" class="choice" data-choice="backup" aria-pressed="false"><b>I'm experiencing a backup</b><span>Call now — fastest way to reach us</span></button>
<button type="button" class="choice" data-choice="grease" aria-pressed="false"><b>Commercial grease trap service</b><span>One-time or recurring</span></button></div>
<div class="panel" data-panel="backup" hidden><p class="big">Call Express now at <a href="tel:{TEL}">{PHONE}</a>.</p><p>{EMERG}</p><a class="btn primary" href="tel:{TEL}">Call {PHONE}</a></div>
<form class="panel" data-panel="form" hidden novalidate><input type="hidden" name="service">
<p class="picked" aria-live="polite"></p>
<label>Name<input name="name" autocomplete="name" required></label>
<label>Phone<input name="phone" type="tel" autocomplete="tel" inputmode="tel" required></label>
<label>City or ZIP<input name="where" autocomplete="postal-code" required></label>
<label>Note <span class="muted">(optional)</span><textarea name="note" rows="3"></textarea></label>
<p class="err" role="alert"></p><button class="btn primary" type="submit">Continue to book with ServiceM8</button><p class="muted">Or call <a href="tel:{TEL}">{PHONE}</a>.</p></form>
<div class="panel" data-panel="fallback" hidden role="status" tabindex="-1"><p class="big">Almost done: finish your request on our ServiceM8 booking page.</p><p>Your request hasn't been sent yet. ServiceM8 opened in a new tab; enter these details there:</p><p><strong class="sum"></strong></p><div class="cta"><a class="btn primary" data-sm8 href="{BOOK}" target="_blank" rel="noopener">Continue to book with ServiceM8</a><a class="btn ghost" href="tel:{TEL}">Or call {PHONE}</a></div></div>
<noscript><p>Call <a href="tel:{TEL}">{PHONE}</a> or <a href="{BOOK}">book online</a>.</p></noscript></div>'''
ZIPBOX='''<div class="zip" data-zip><h3>Check your ZIP</h3><form data-zipform novalidate><label for="zipin">5-digit ZIP code</label><div class="zrow"><input id="zipin" inputmode="numeric" maxlength="5" autocomplete="postal-code" pattern="[0-9]{5}"><button class="btn primary" type="submit">Check</button></div></form><p class="zres" aria-live="polite"></p></div>'''
ROUTE='<svg class="route" viewBox="0 0 600 160" aria-hidden="true" focusable="false"><path d="M10 140 C 90 140, 110 40, 200 60 S 330 140, 400 90 S 520 20, 590 30"/><circle cx="10" cy="140" r="5"/><circle cx="590" cy="30" r="5"/></svg>'
HERO=f'''<section class="hero"><div class="wrap hgrid"><div class="hcopy"><p class="eyebrow">Owner-operated • Southwest Florida</p><h1>Septic tank pumping in Southwest Florida</h1>
<p class="lede" data-sth-field="description">Need your tank pumped or dealing with a backup? Call Express to talk through what's happening, confirm service at your address, and get pricing.</p>{CTA}<p class="lic">Licensed &amp; insured</p><p class="note">{EMERG}</p></div>
<figure class="hphoto">{HERO_IMG}<figcaption><span>UNIT 4200</span><span>Split tank · Septic &amp; grease</span></figcaption></figure></div></section>'''
page("/","Septic Tank Pumping Southwest Florida | Bonita Springs, Estero, Fort Myers | Express Septic",
 "Owner-operated septic tank pumping in Southwest Florida: Bonita Springs, Estero, Naples, Fort Myers, Cape Coral & Lehigh Acres. Grease trap service too. Call (239) 451-3261.",
 "Septic tank pumping in Southwest Florida",
 sec(f'''<div class="split"><div><p class="eyebrow">What we do</p><h2 id="services">Two jobs, done right</h2></div><div class="two">
<a class="feat" href="/residential-septic-tank-pumping/"><span class="k">Homes</span><b>Residential septic pumping</b><span>We find the lid, pump the tank and tell you what we saw.</span></a>
<a class="feat" href="/commercial-grease-trap-service/"><span class="k">Businesses</span><b>Commercial grease trap service</b><span>One-time pump-outs or a recurring schedule for kitchens.</span></a></div></div>
<div class="price-slot"><p class="pp">Residential septic pumping starting at $399.99</p><p>Your final quote depends on tank size, tank access, whether the lid needs locating or digging, and after-hours visits. Call to confirm for your tank.</p></div><p class="more">Also: <a href="/commercial-septic-tank-pumping/">commercial septic pumping</a> · <a href="/septic-inspections/">septic inspections</a> · <a href="/septic-tank-pumping/">septic tank cleaning</a></p>''')+
 sec(f'''<div class="split"><div><p class="eyebrow">The truck</p><h2>A 4,200-gallon split-tank truck</h2></div><div><p>Our truck carries 4,200 gallons split into separate compartments, so it's set up for both septic and grease trap work. In plain terms: one trip can handle a full household tank, and grease stays separate from septic.</p><dl class="spec"><div><dt>Capacity</dt><dd>4,200 gal</dd></div><div><dt>Tank</dt><dd>Split</dd></div><div><dt>Work</dt><dd>Septic · Grease</dd></div><div><dt>Coverage</dt><dd>Licensed &amp; insured</dd></div><div><dt>USDOT</dt><dd>6673233</dd></div></dl></div></div>'''.replace("<div><p>Our truck","<div>"+SIDE+"<p>Our truck",1),"ink")+
 sec(f'''<div class="split"><div><p class="eyebrow">The owner</p><h2>Meet O'Ryan Atkinson</h2></div><div>'''+CREW.replace('alt="Express Septic Tank Pumping crew with the 4,200-gallon vacuum truck"','alt="ORyan Atkinson, owner of Express Septic Tank Pumping"').replace("</figure>","<figcaption>ORyan Atkinson, owner of Express Septic Tank Pumping</figcaption></figure>")+f'''<p>Express is owner-operated. When you call, you're talking to the person who runs the business. Express is licensed &amp; insured. Honest, reliable and fair — great customer service is our top priority.</p><p><a href="/about/">More about Express</a></p></div></div>''')+
 f'<section class="sec" data-sth-recent-jobs hidden><div class="wrap"><p class="eyebrow">Recent jobs</p><h2>Completed jobs</h2><p>Photos and notes from recent work around Southwest Florida.</p><a class="btn ghost" data-sth-recent-jobs-link href="/completed-jobs/">See completed jobs</a></div></section>'+
 sec(f'<div class="split"><div><p class="eyebrow">Service area</p><h2>Lee, Collier &amp; Charlotte County</h2><p>Based in Estero, between Bonita Springs and Fort Myers.</p></div><div>{ZIPBOX}</div></div>{ROUTE}<p><a href="/service-area/">See every area we serve</a></p>',"area")+
 sec(REQUEST),hero=HERO)
RES_EXTRA=("<h2>What happens during a visit</h2>"+LIDS+"<ol><li><strong>We locate the tank.</strong> We find the tank and its lid or access port. If the lid is buried, we may need to dig to reach it.</li><li><strong>We pump it out.</strong> The truck pumps the liquid, sludge and scum out of the tank.</li><li><strong>We tell you what we saw.</strong> You'll hear about anything that looks like it needs attention.</li></ol>"
 "<h2>How to prepare</h2><ul><li>If you know where the lid is, mark it or tell us when you call.</li><li>Make sure the truck can get close: clear the driveway and keep vehicles off the drain field.</li><li>Keep pets inside and unlock any gates.</li><li>Have your last pumping date handy if you know it.</li></ul>"
 "<h2>What affects the price</h2><ul><li>Tank size and how full it is</li><li>Access: how far the truck has to reach and whether the lid is buried and needs locating or digging</li><li>Location within our service area</li><li>Timing: after-hours or emergency visits can affect the quote</li></ul>"
 "<div class='price-slot'><p class='pp'>Residential septic pumping starting at $399.99</p><p>Your final quote depends on tank size, tank access, whether the lid needs locating or digging, and after-hours visits. Call to confirm for your tank.</p></div>"
 "<p>Call <a href='tel:"+TEL+"'>"+PHONE+"</a> to confirm pricing for your tank.</p>")
EXTRA["residential-septic-tank-pumping"]="<div class='price-slot'><p class='pp'>Residential septic pumping starting at $399.99</p><p>Your final quote depends on tank size, tank access, whether the lid needs locating or digging, and after-hours visits. Call to confirm for your tank.</p></div>"+RES_EXTRA+EXTRA.get("residential-septic-tank-pumping","")
for s in SERVICES:
  body=photo(s[0],s[1]+" job photo")+VAL+"".join(f"<p>{p}</p>" for p in s[4])+EXTRA.get(s[0],"")+"<h2>Pricing</h2><p>Call for a quote — <a href='tel:"+TEL+"'>"+PHONE+"</a>.</p><h2>Service Areas</h2>"+city_list+"<h2>Other Services</h2>"+svc_list
  page(f"/{s[0]}/",s[2],s[3],s[1]+" in Southwest Florida",body,{"@context":"https://schema.org","@type":"Service","name":s[1],"provider":{"@type":"LocalBusiness","name":NAME},"areaServed":[c+", FL" for c in CITIES_ALL]})
for c,(county,a,b) in CITY.items():
  near=[x for x in CITIES_ALL if x!=c]
  body=(photo(slug(c),f"Septic tank pumping job in {c}, FL")+VAL+f"<p>Need septic tank pumping in {c}, FL? Express Septic Tank Pumping serves homes and businesses in {c} and across {county}. {a}</p><p>{b}</p>"
   f"<p class='emerg'><strong>Septic emergency in {c}?</strong> "+"Night or day, we\'re available for emergencies. For routine service, we can often make it same day when possible. Call <a href='tel:"+TEL+"'>"+PHONE+"</a>.</p>"
   f"<h2>Septic Tank Cleaning {c}</h2><p>Septic tank cleaning in {c} removes the sludge and scum that build up over time and helps protect your drain field.</p><h2>Septic Service in {c}, FL</h2><p>For septic service in {c}, FL, tap to call or book online.</p>"
   f"<h2>Septic Services in {c}</h2><ul class='cards'>"+"".join(f'<li><a href="/{s[0]}/">{s[1]} in {c}</a></li>' for s in SERVICES)+"</ul>"
   f"<h2>Signs Your {c} Septic Tank Needs Pumping</h2><p>Slow drains, gurgling, odors outside, or soggy ground over the drain field. If it's been 3–5 years since your last pump-out, it's time to call.</p>"
   f"<p><a href='/'>Back to Express Septic Tank Pumping home</a> · Call <a href='tel:{TEL}'>{PHONE}</a> for a quote in {c}.</p>"
   "<h2>Nearby Areas We Serve</h2><ul class='cards'>"+"".join(f'<li><a href="/{slug(x)}/">{x}</a></li>' for x in near)+"</ul>")
  if c=="Lehigh Acres":
    page(f"/{slug(c)}/","Septic Tank Cleaning Lehigh Acres | Septic Service Lehigh Acres FL","Septic tank cleaning and septic service in Lehigh Acres, FL from Express Septic Tank Pumping. Residential, commercial & inspections. (239) 451-3261.","Septic Tank Cleaning &amp; Septic Service in Lehigh Acres, FL",body.replace("Need septic tank pumping in","Need septic tank cleaning or septic service in"));continue
  page(f"/{slug(c)}/",f"Septic Tank Pumping {c}, FL | Express Septic Tank Pumping",
   f"Septic tank pumping in {c}, FL for homes & businesses. Residential, commercial pumping & septic inspections. Call (239) 451-3261 or book online.",
   f"Septic Tank Pumping in {c}, FL",body)

page("/septic-system-maintenance/","Septic System Maintenance Tips | Southwest Florida | Express Septic","Septic system maintenance guide: how often to pump, what not to flush, water use, drain field care and warning signs. Call (239) 451-3261.","Septic System Maintenance Guide",
 photo("septic-system-maintenance","Septic system maintenance")+
 "<h2>How Often to Pump Your Septic Tank</h2><p>Most homes should pump every 3 to 5 years. The right interval depends on household size, tank size and water use. Larger families or smaller tanks need pumping more often. See <a href='/septic-tank-pumping/'>septic tank pumping</a>.</p>"
 "<h2>What Not to Flush or Pour Down Drains</h2><ul><li>Wipes (including 'flushable' wipes), paper towels, diapers and feminine products</li><li>Cooking grease, fats and oils</li><li>Coffee grounds and large amounts of food scraps</li><li>Paint, solvents, harsh chemicals and medications</li><li>Excessive bleach or antibacterial cleaners that kill helpful bacteria</li></ul>"
 "<h2>Water Use Tips</h2><ul><li>Fix leaky toilets and faucets quickly</li><li>Spread laundry loads through the week</li><li>Use high-efficiency fixtures and appliances</li><li>Send roof gutters and runoff away from the drain field</li></ul>"
 "<h2>Drain Field Care</h2><ul><li>Don't park or drive vehicles on the drain field</li><li>Don't plant trees or large shrubs nearby; roots can damage pipes. Grass is best</li><li>Don't build structures or pave over it</li></ul>"
 "<h2>Warning Signs of Problems</h2><p>Slow drains, gurgling pipes, sewage odors, soggy or extra-green grass over the drain field, and backups in toilets or drains. Call right away if you notice these.</p>"
 "<h2>Why Regular Inspections Help</h2><p>An inspection can catch problems early, before they turn into costly repairs, and gives you a record of your system's condition. Learn about <a href='/septic-inspections/'>septic inspections</a>.</p>"
 "<p>See <a href='/how-it-works/'>how our service works</a> and <a href='/how-often-to-pump-septic-tank/'>how often to pump your septic tank</a>.</p><h2>Our Services</h2>"+svc_list)
page("/how-it-works/","How Septic Pumping Service Works | Express Septic Tank Pumping","How booking septic tank pumping with Express Septic works: call or book online, we schedule, pump your tank and walk you through what we found.","How Our Septic Service Works",
 photo("how-it-works","Express Septic technician at work")+
 "<ol><li><strong>Call or book online.</strong> Tap to call (239) 451-3261 or use Book Online.</li><li><strong>Get a quote and schedule.</strong> Tell us about your property and we'll quote and set a time.</li><li><strong>We locate and pump the tank.</strong> Our crew finds the tank lid and pumps the tank.</li><li><strong>We share what we saw.</strong> We let you know about anything that needs attention.</li></ol>"
 "<p>Keep your system healthy between visits with our <a href='/septic-system-maintenance/'>septic maintenance tips</a> and our guide to <a href='/how-often-to-pump-septic-tank/'>how often to pump your septic tank</a>.</p><h2>Our Services</h2>"+svc_list)

page("/how-often-to-pump-septic-tank/","How Often Should You Pump Your Septic Tank? | Express Septic","How often to pump a septic tank: EPA says every 3-5 years for most homes. See our pumping frequency chart by tank size and household size.","How Often Should You Pump Your Septic Tank?",
 "<p>The U.S. EPA recommends that most household septic tanks be pumped every 3 to 5 years, and that systems be inspected by a professional at least every 3 years. Your exact schedule depends on tank size, how many people live in the home and how much water you use.</p>"
 "<h2>Septic Pumping Frequency Chart</h2><p>Estimated years between pumpings, based on a widely published university extension estimate. A general guide only; an inspection tells you what your tank actually needs.</p>"+"<div class='tw'><table><tr><th>Tank size</th><th>1 person</th><th>2 people</th><th>3 people</th><th>4 people</th><th>5 people</th><th>6 people</th></tr><tr><td>500 gal</td><td>5.8 yrs</td><td>2.6 yrs</td><td>1.5 yrs</td><td>1.0 yrs</td><td>0.7 yrs</td><td>0.4 yrs</td></tr><tr><td>750 gal</td><td>9.1 yrs</td><td>4.2 yrs</td><td>2.6 yrs</td><td>1.8 yrs</td><td>1.3 yrs</td><td>1.0 yrs</td></tr><tr><td>1,000 gal</td><td>12.4 yrs</td><td>5.9 yrs</td><td>3.7 yrs</td><td>2.6 yrs</td><td>2.0 yrs</td><td>1.5 yrs</td></tr><tr><td>1,250 gal</td><td>15.6 yrs</td><td>7.5 yrs</td><td>4.8 yrs</td><td>3.4 yrs</td><td>2.6 yrs</td><td>2.0 yrs</td></tr><tr><td>1,500 gal</td><td>18.9 yrs</td><td>9.1 yrs</td><td>5.9 yrs</td><td>4.2 yrs</td><td>3.3 yrs</td><td>2.6 yrs</td></tr></table></div>"+
 "<h2>Factors That Change How Often You Pump</h2><ul><li><strong>Garbage disposal:</strong> adds solids; the EPA notes disposals can significantly increase sludge and scum, so pump more often.</li><li><strong>Water use:</strong> heavy laundry, long showers and leaks push more water through the tank.</li><li><strong>Household size:</strong> more people means faster buildup.</li><li><strong>Seasonal and rental homes in Southwest Florida:</strong> snowbird homes and vacation rentals can see heavy use in season and with guests, so rentals may need pumping more often than household size suggests.</li><li><strong>Florida rainy season:</strong> high water tables stress drain fields, so a pumped tank helps.</li></ul>"
 "<h2>Signs Your Tank Is Due Now</h2><ul><li>Slow drains or gurgling pipes</li><li>Sewage odors inside or outside</li><li>Soggy ground or extra-green grass over the drain field</li><li>Toilets or drains backing up</li><li>More than 3–5 years since the last pump-out, or you don't know</li></ul>"
 "<p>Read our <a href='/septic-system-maintenance/'>septic system maintenance guide</a> or see <a href='/how-it-works/'>how our service works</a>.</p><h2>Our Services</h2>"+svc_list)
page("/about/","About Express Septic Tank Pumping | Honest, Reliable Septic Service","Express Septic Tank Pumping is an Estero-based septic company built on honesty, reliability, fair rates and great customer service. Call (239) 451-3261.","About Express Septic Tank Pumping",
 CREW+"<p>Express Septic Tank Pumping is a local septic service company based in Estero, Florida, serving homes and businesses across Lee and Collier County.</p><h2>What We Stand For</h2><ul><li><strong>Honesty.</strong> Upfront pricing and straight answers about your system — no surprises.</li><li><strong>Reliability.</strong> We show up on time and do the job right.</li><li><strong>Fairness.</strong> Fair rates for the work you actually need.</li><li><strong>Customer service.</strong> Treating customers right is our top priority.</li></ul><h2>Our Services</h2>"+svc_list+"<p>See <a href='/how-it-works/'>how it works</a>.</p>")
page("/commercial-grease-trap-service/","Commercial Grease Trap Service & Pumping | Southwest Florida | Express Septic",
 "Grease trap pumping for restaurants and commercial kitchens in Lee & Collier County. One-time or recurring service from Express Septic. Call (239) 451-3261.",
 "Commercial grease trap service",
 REAR+"<p>Restaurants and commercial kitchens need their grease traps pumped before fats, oils and grease build up and cause backups, odors or problems with the drain line. Express pumps grease traps for businesses across Southwest Florida.</p>"
 +SIDE+"<p>Our 4,200-gallon split-tank truck keeps grease separate from septic loads, so we can handle grease trap work and septic work on the same truck.</p>"
 "<h2>One-time or recurring</h2><p>Some businesses call us when a trap is full. Most are better off on a recurring schedule based on how much cooking they do and the size of the trap. Tell us about your kitchen and we'll talk through how often makes sense.</p>"
 "<p><a class='btn primary' href='/contact/?service=grease#request'>Ask about recurring service</a></p>"
 "<h2>Signs your grease trap needs service</h2><ul><li>Slow sinks or floor drains in the kitchen</li><li>Grease or odors around the trap lid</li><li>It's been longer than your usual schedule since the last pump-out</li></ul>"
 "<h2>What to have ready when you call</h2><ul><li>Business name and address</li><li>Where the trap is and how it's accessed</li><li>Trap size, if you know it</li><li>When it was last pumped</li></ul>"
 "<h2>Other services</h2>"+svc_list,
 {"@context":"https://schema.org","@type":"Service","name":"Commercial Grease Trap Service","provider":{"@type":"LocalBusiness","name":NAME},"areaServed":[c+", FL" for c in CITIES_ALL]})
counties={}
for c,(co,_,_) in CITY.items(): counties.setdefault(co,[]).append(c)
page("/service-area/","Septic Pumping Service Area | Lee, Collier & Charlotte County | Express Septic",
 "Express Septic Tank Pumping serves Bonita Springs, Estero, Fort Myers, Cape Coral, Lehigh Acres, Naples and more. Check your ZIP or call (239) 451-3261.",
 "Where we work",
 JOB+"<p>Express is based in Estero, between Bonita Springs and Fort Myers, and works across Lee, Collier and Charlotte County. Check your ZIP below, or call to confirm service at your address.</p>"+ZIPBOX+ROUTE+
 "".join(f"<h2>{co}</h2><ul class='cities'>"+"".join(f'<li><a href="/{slug(c)}/">{c}</a></li>' for c in cs)+"</ul>" for co,cs in counties.items()))
page("/contact/","Contact & Request Septic Service | Express Septic Tank Pumping",
 "Call Express Septic Tank Pumping at (239) 451-3261, book online, or request septic pumping or grease trap service.",
 "Contact Express",
 f"<p>The fastest way to reach us is by phone: <a href='tel:{TEL}'>{PHONE}</a>. {EMERG}</p><p>You can also <a href='{BOOK}' rel='noopener'>book online through ServiceM8</a> or email <a href='mailto:{EMAIL}'>{EMAIL}</a>.</p>"+REQUEST+
 "<h2>Mailing address</h2><p>Express Septic Tank Pumping LLC<br>23357 Olde Meadowbrook Circle, Estero, FL 34134</p>")
faqhtml="".join(f"<h2>{q}</h2><p>{a}</p>" for q,a in FAQ)
page("/faq/","Septic Tank FAQ | How Often to Pump, Cost & Signs | Express Septic","Answers to common septic tank questions: how often to pump, signs your tank is full, cost and what areas Express Septic Tank Pumping serves.","Septic Tank Pumping FAQ",faqhtml,
 {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]})
page("/privacy/","Privacy Policy | Express Septic Tank Pumping","Privacy policy for Express Septic Tank Pumping website visitors and customers.","Privacy Policy",
 f"<p>Express Septic Tank Pumping respects your privacy. Information you give us by phone, through our online booking provider (ServiceM8) or by text is used only to schedule and provide service, send quotes and invoices, and communicate with you about your job.</p><p>We do not sell your personal information. Mobile phone numbers and SMS consent are not shared with third parties for marketing purposes.</p><p>This site does not use advertising trackers. Online booking is handled by ServiceM8 under its own privacy policy.</p><p>Questions? Call {PHONE}.</p>")
page("/terms/","Terms of Service | Express Septic Tank Pumping","Terms of service for the Express Septic Tank Pumping website and services.","Terms of Service",
 f"<p>By using this website you agree to these terms. Content is general information about septic systems and is not a substitute for an on-site evaluation.</p><p>Quotes are provided after discussing your property and needs. Scheduling is subject to availability.</p><p>If you opt in to text messages, message and data rates may apply. Reply STOP to opt out or HELP for help.</p><p>Contact: {NAME}, 23357 Olde Meadowbrook Circle, Estero, FL 34134, {PHONE}.</p>")
shutil.copy("src/styles.css","styles.css"); shutil.copy("src/site.js","site.js")
open("sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{BASE}{p}</loc></url>" for p in PAGES)+"</urlset>\n")
# Sitemap index: static pages + ServiceTechHub Project Showcase (served by functions/ once configured)
open("sitemap-index.xml","w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><sitemap><loc>{BASE}/sitemap.xml</loc></sitemap><sitemap><loc>{BASE}/completed-jobs/sitemap.xml</loc></sitemap></sitemapindex>\n')
open("robots.txt","w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap-index.xml\nSitemap: {BASE}/sitemap.xml\nSitemap: {BASE}/completed-jobs/sitemap.xml\n")
print("\n".join(PAGES))
