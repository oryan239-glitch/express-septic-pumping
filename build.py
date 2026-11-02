#!/usr/bin/env python3
"""Build script: generates static pages at repo root from data in this file + src/styles.css."""
import json, os, shutil
BASE="https://expresssepticpumping.com"
NAME="Express Septic Tank Pumping"; PHONE="(239) 451-3261"; TEL="+12394513261"
BOOK="https://book.servicem8.com/request_booking?uuid=019fca12-b6bf-721c-8a2b-41d89e1a1b5b"
REVIEW="https://g.page/r/CYxfVw5rrgwLEBM/review"
CITIES_ALL=["Estero","Bonita Springs","Naples","North Naples","Fort Myers","Cape Coral","Lehigh Acres","San Carlos Park"]
SERVICES=[
 ("septic-tank-pumping","Septic Tank Pumping","Septic Tank Pumping in Southwest Florida | Express Septic","Septic tank pumping in Estero, Bonita Springs, Naples, Fort Myers & nearby. Licensed local crew, tap to call (239) 451-3261 or book online.",
  ["Septic tank pumping removes the sludge and scum that build up in your tank over time. If solids are left too long they can flow into the drain field, which is the most expensive part of a septic system to repair.",
   "Most households should have the tank pumped every 3 to 5 years, depending on tank size and how many people live in the home. Homes with garbage disposals, frequent guests or older systems may need service more often.",
   "Warning signs you're overdue: slow drains, gurgling pipes, sewage odors in the yard, soggy or extra-green grass over the drain field, or toilets that back up."]),
 ("residential-septic-tank-pumping","Residential Septic Tank Pumping","Residential Septic Tank Pumping | Homes in SW Florida","Residential septic tank pumping for homes in Estero, Naples, Fort Myers, Cape Coral, Lehigh Acres & more. Call for a quote: (239) 451-3261.",
  ["Our residential septic tank pumping service is built for homeowners. We locate the tank lid, pump out the full tank, and let you know what we see so you can plan ahead.",
   "Regular pumping protects your drain field, prevents backups inside the house and helps your system last longer. It's also a smart step before buying or selling a home, before a big family gathering, or after a heavy rainy season.",
   "Tip: keep a record of every pumping date. It helps you stay on schedule and shows buyers the system has been maintained."]),
 ("commercial-septic-tank-pumping","Commercial Septic Tank Pumping","Commercial Septic Tank Pumping | Businesses in SW Florida","Commercial septic tank pumping for businesses, offices, churches & properties in Lee and Collier County. Call (239) 451-3261 for a quote.",
  ["Businesses on septic need a reliable pumping schedule. Commercial systems often see heavier use than homes, so solids build up faster and a backup can shut down your operation.",
   "We pump septic tanks for offices, retail sites, churches, rental properties, farms and other commercial properties. Call us to set up a schedule that fits your usage.",
   "Keeping a steady pumping schedule helps avoid emergency calls, odors near customers and costly drain field damage."]),
 ("septic-inspections","Septic Inspections","Septic Tank Inspection | Real Estate & Routine | Express Septic","Septic tank inspections for home buyers, sellers and owners in Estero, Naples, Fort Myers & nearby. Book online or call (239) 451-3261.",
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
("How much does septic tank pumping cost?","Price depends on tank size, location and access. Call (239) 451-3261 for a quote."),
("What are signs my septic tank is full?","Slow drains, gurgling pipes, sewage odors, wet or extra-green spots over the drain field, and backups are common signs."),
("Do you pump commercial septic tanks?","Yes. We provide commercial septic tank pumping for businesses and other properties."),
("Do you do septic inspections for real estate?","Yes. We offer septic inspections for buyers, sellers and homeowners."),
("What areas do you serve?","Estero, Bonita Springs, Naples, North Naples, Fort Myers, Cape Coral, Lehigh Acres, San Carlos Park and nearby areas of Lee and Collier County."),
("What shouldn't go into a septic system?","Avoid grease, wipes (even 'flushable'), paper towels, feminine products, harsh chemicals and medications. They can clog the system or harm the bacteria that break down waste."),
("How do I book?","Tap Book Online to request a time, or call (239) 451-3261.")]
PAGES=[]
def schema(extra=None):
  s={"@context":"https://schema.org","@type":["LocalBusiness","Plumber"],"name":NAME,"url":BASE+"/","telephone":TEL,
   "address":{"@type":"PostalAddress","streetAddress":"23357 Olde Meadowbrook Circle","addressLocality":"Estero","addressRegion":"FL","postalCode":"34134","addressCountry":"US"},
   "areaServed":[{"@type":"City","name":c+", FL"} for c in CITIES_ALL],
   "makesOffer":[{"@type":"Offer","itemOffered":{"@type":"Service","name":s[1]}} for s in SERVICES]}
  out=[s]
  if extra: out.append(extra)
  return "".join(f'<script type="application/ld+json">{json.dumps(o)}</script>' for o in out)
def photo(sid,alt): return f'<figure class="photo" data-photo-slot="{sid}"><img src="/assets/img/{sid}.jpg" alt="{alt}" loading="lazy" width="800" height="500" onerror="this.parentNode.classList.add(\'empty\')"><figcaption>Photo: {alt}</figcaption></figure>'
NAV="".join(f'<a href="/{s[0]}/">{s[1]}</a>' for s in SERVICES)
CTA=f'<div class="cta"><a class="btn call" href="tel:{TEL}">Call {PHONE}</a><a class="btn book" href="{BOOK}" rel="noopener">Book Online</a></div>'
REV=f'<section class="reviews"><h2>Customer Reviews</h2><p>See what our customers say about Express Septic Tank Pumping on Google, or leave us a review.</p><a class="btn" href="{REVIEW}" rel="noopener">Read &amp; Leave a Google Review</a></section>'
def page(path,title,desc,h1,body,extra=None):
  foot="".join(f'<a href="/{slug(c)}/">{c}</a>' for c in CITIES_ALL)
  html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{BASE}{path}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{BASE}{path}"><meta property="og:type" content="website">
<link rel="stylesheet" href="/styles.css">{schema(extra)}</head><body>
<header><a class="logo" href="/">{NAME}</a><nav>{NAV}<a href="/faq/">FAQ</a></nav><a class="hcall" href="tel:{TEL}">{PHONE}</a></header>
<main><h1>{h1}</h1>{CTA}{body}{REV}{CTA}</main>
<footer><div><strong>{NAME}</strong><br>23357 Olde Meadowbrook Circle, Estero, FL 34134<br><a href="tel:{TEL}">{PHONE}</a><br>Service-area business — we come to you.</div>
<div><strong>Services</strong>{NAV}</div><div><strong>Areas</strong>{foot}</div><div><strong>Info</strong><a href="/">Home</a><a href="/faq/">FAQ</a><a href="/privacy/">Privacy</a><a href="/terms/">Terms</a></div></footer>
<a class="sticky" href="tel:{TEL}">Tap to Call {PHONE}</a></body></html>'''
  pre="../"*(path.count("/")-1) or "./"
  html=html.replace('href="/','href="'+pre).replace('src="/','src="'+pre).replace("href='/","href='"+pre)
  d="."+path; os.makedirs(d,exist_ok=True); open(d+"index.html","w").write(html); PAGES.append(path)
svc_list="<ul class='cards'>"+"".join(f'<li><a href="/{s[0]}/"><strong>{s[1]}</strong></a></li>' for s in SERVICES)+"</ul>"
city_list="<ul class='cards'>"+"".join(f'<li><a href="/{slug(c)}/">Septic Tank Pumping {c}</a></li>' for c in CITIES_ALL)+"</ul>"
# Home
page("/","Septic Tank Pumping Estero, Bonita Springs, Naples & Fort Myers | Express Septic",
 "Express Septic Tank Pumping: residential & commercial septic tank pumping and inspections in Estero, Bonita Springs, Naples & Fort Myers. Call (239) 451-3261.",
 "Septic Tank Pumping in Estero, Bonita Springs, Naples &amp; Fort Myers",
 photo("home-hero","Express Septic pump truck on a job")+
 "<p>Express Septic Tank Pumping provides septic tank pumping, septic cleaning and septic inspections for homes and businesses across Southwest Florida. Based in Estero, we serve Bonita Springs, Naples, North Naples, Fort Myers, Cape Coral, Lehigh Acres and San Carlos Park.</p>"
 "<h2>Our Septic Services</h2>"+svc_list+
 "<h2>Why Regular Septic Pumping Matters</h2><p>Pumping your septic tank every 3–5 years keeps solids out of your drain field, prevents backups and sewage odors, and helps your system last. Florida's high water table and heavy summer rains make maintenance even more important.</p>"
 +photo("home-job-1","Septic tank being pumped")+
 "<h2>Pricing</h2><p>Every tank and property is different. Call <a href='tel:"+TEL+"'>"+PHONE+"</a> for a quote.</p>"
 "<h2>Areas We Serve</h2>"+city_list)
for s in SERVICES:
  body=photo(s[0],s[1]+" job photo")+"".join(f"<p>{p}</p>" for p in s[4])+"<h2>Pricing</h2><p>Call for a quote — <a href='tel:"+TEL+"'>"+PHONE+"</a>.</p><h2>Service Areas</h2>"+city_list+"<h2>Other Services</h2>"+svc_list
  page(f"/{s[0]}/",s[2],s[3],s[1]+" in Southwest Florida",body,{"@context":"https://schema.org","@type":"Service","name":s[1],"provider":{"@type":"LocalBusiness","name":NAME},"areaServed":[c+", FL" for c in CITIES_ALL]})
for c,(county,a,b) in CITY.items():
  near=[x for x in CITIES_ALL if x!=c]
  body=(photo(slug(c),f"Septic tank pumping job in {c}, FL")+f"<p>Need septic tank pumping in {c}, FL? Express Septic Tank Pumping serves homes and businesses in {c} and across {county}. {a}</p><p>{b}</p>"
   f"<h2>Septic Services in {c}</h2><ul class='cards'>"+"".join(f'<li><a href="/{s[0]}/">{s[1]} in {c}</a></li>' for s in SERVICES)+"</ul>"
   f"<h2>Signs Your {c} Septic Tank Needs Pumping</h2><p>Slow drains, gurgling, odors outside, or soggy ground over the drain field. If it's been 3–5 years since your last pump-out, it's time to call.</p>"
   f"<p><a href='/'>Back to Express Septic Tank Pumping home</a> · Call <a href='tel:{TEL}'>{PHONE}</a> for a quote in {c}.</p>"
   "<h2>Nearby Areas We Serve</h2><ul class='cards'>"+"".join(f'<li><a href="/{slug(x)}/">{x}</a></li>' for x in near)+"</ul>")
  page(f"/{slug(c)}/",f"Septic Tank Pumping {c}, FL | Express Septic Tank Pumping",
   f"Septic tank pumping in {c}, FL for homes & businesses. Residential, commercial pumping & septic inspections. Call (239) 451-3261 or book online.",
   f"Septic Tank Pumping in {c}, FL",body)
faqhtml="".join(f"<h2>{q}</h2><p>{a}</p>" for q,a in FAQ)
page("/faq/","Septic Tank FAQ | How Often to Pump, Cost & Signs | Express Septic","Answers to common septic tank questions: how often to pump, signs your tank is full, cost and what areas Express Septic Tank Pumping serves.","Septic Tank Pumping FAQ",faqhtml,
 {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]})
page("/privacy/","Privacy Policy | Express Septic Tank Pumping","Privacy policy for Express Septic Tank Pumping website visitors and customers.","Privacy Policy",
 f"<p>Express Septic Tank Pumping respects your privacy. Information you give us by phone, through our online booking provider (ServiceM8) or by text is used only to schedule and provide service, send quotes and invoices, and communicate with you about your job.</p><p>We do not sell your personal information. Mobile phone numbers and SMS consent are not shared with third parties for marketing purposes.</p><p>This site does not use advertising trackers. Online booking is handled by ServiceM8 under its own privacy policy.</p><p>Questions? Call {PHONE}.</p>")
page("/terms/","Terms of Service | Express Septic Tank Pumping","Terms of service for the Express Septic Tank Pumping website and services.","Terms of Service",
 f"<p>By using this website you agree to these terms. Content is general information about septic systems and is not a substitute for an on-site evaluation.</p><p>Quotes are provided after discussing your property and needs. Scheduling is subject to availability.</p><p>If you opt in to text messages, message and data rates may apply. Reply STOP to opt out or HELP for help.</p><p>Contact: {NAME}, 23357 Olde Meadowbrook Circle, Estero, FL 34134, {PHONE}.</p>")
shutil.copy("src/styles.css","styles.css")
open("sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{BASE}{p}</loc></url>" for p in PAGES)+"</urlset>\n")
open("robots.txt","w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
print("\n".join(PAGES))
