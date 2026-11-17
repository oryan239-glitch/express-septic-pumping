#!/usr/bin/env python3
"""Build script: generates static pages at repo root from data in this file + src/styles.css."""
import json, os, shutil
BASE="https://expresssepticpumping.com"
NAME="Express Septic Tank Pumping"; PHONE="(239) 451-3261"; TEL="+12394513261"
BOOK="https://book.servicem8.com/request_booking?uuid=019fca12-b6bf-721c-8a2b-41d89e1a1b5b"
EMAIL="expressseptictankpumping@gmail.com"
REVIEW="https://g.page/r/CYxfVw5rrgwLEBM/review"  # write-a-review (Leave a review)
REVIEWS_READ="https://www.google.com/maps?cid=796203008963075980"  # Google Maps listing, place ChIJ2U4mCDcKRGcRjF9XDmuuDAs
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
 ("septic-tank-riser-installation","Septic Tank Riser Installation","Septic Tank Riser Installation | Lee & Collier County | Express Septic","Septic tank riser installation in Southwest Florida: bring your tank lid up to ground level so future pump-outs don't need digging. 6-inch risers $299.99 each. (239) 451-3261.",
  ["A septic tank riser is an extension installed on top of the tank's access opening. It brings the lid up to ground level, so the tank can be found and opened without digging.",
   "Many Southwest Florida tanks have lids buried under soil or grass. Every pump-out then starts with locating the lid and digging down to it. With a riser in place, the next pump-out starts with lifting the lid.",
   "Riser installation is often done during a pump-out, while the lid is already uncovered. Ask about it when you call or book."]),
 ("septic-repair","Septic Repair","Septic Repair | Lee & Collier County | Express Septic Tank Pumping","Septic repair in Southwest Florida. We look at your system first, then quote the repair. Work performed under a FL certified plumbing contractor. (239) 451-3261.",
  ["Express Septic Tank Pumping does septic repairs for homes and businesses across Southwest Florida.",
   "Every repair starts with a look at your system. Once we see what's wrong, we quote the repair before any work starts. Call (239) 451-3261 to set up a visit.",
   "Repair work is performed under Florida Certified Plumbing Contractor Raymond F. Dibble, License #CFC020332, licensed since 1981."]),
 ("drain-field-replacement","Drain Field Replacement","Drain Field Replacement | Lee & Collier County | Express Septic Tank Pumping","Drain field replacement in Southwest Florida. Quoted after we inspect the system. Work performed under a FL certified plumbing contractor. (239) 451-3261.",
  ["Express Septic Tank Pumping does drain field replacement for homes and businesses across Southwest Florida.",
   "We quote drain field replacement after inspecting the system. Call (239) 451-3261 to set up a visit.",
   "The work is performed under FL Certified Plumbing Contractor Raymond F. Dibble, License #CFC020332, licensed since 1981."]),
 ("septic-inspections","Septic Inspections","Septic Inspection for Home Purchase | Fort Myers & Naples | Express Septic","Septic inspection & real estate septic inspection for home purchases in Fort Myers, Naples, Estero & nearby. Septic inspection with pump-out $549.99. Call (239) 451-3261.",
  ["A septic inspection checks the condition of your tank and how the system is working. It's common when buying or selling a home, and a good idea if you're noticing problems.",
   "Buying a home on septic? An inspection helps you understand what you're getting before closing. Selling? Having the system checked ahead of time can help avoid surprises during the sale.",
   "A septic inspection with pump-out is $549.99. Call us to discuss what you need."]),
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
CITY['East Naples']=('Collier County', 'East Naples is the area of Collier County southeast of downtown Naples, along US-41 toward Marco Island, including Lely, Lely Resort and Naples Manor.', 'Many East Naples homes on larger lots off the main sewer lines rely on septic systems.')
CITY['Golden Gate']=('Collier County', 'Golden Gate is a community in Collier County east of Naples; it sits between Naples and the large lots of Golden Gate Estates.', 'Homes in and around Golden Gate that are not on central sewer use septic tanks that need regular pumping. For the Estates, see our Golden Gate Estates page.')
CITY['Marco Island']=('Collier County', "Marco Island is the largest barrier island in Florida's Ten Thousand Islands area, south of Naples.", 'Waterfront and island properties need septic maintenance done right to protect nearby waterways.')
CITY['Immokalee']=('Collier County', 'Immokalee is an agricultural community in inland Collier County, known for its farming industry.', 'Rural homes, farms and businesses around Immokalee often depend on septic systems.')
CITY['Ave Maria']=('Collier County', 'Ave Maria is a planned town in eastern Collier County, home to Ave Maria University.', 'Properties in and around Ave Maria on septic benefit from routine pumping and inspections.')
CITY['North Fort Myers']=('Lee County', 'North Fort Myers lies across the Caloosahatchee River from Fort Myers in Lee County, including neighborhoods like Suncoast Estates, Palmona Park and Lochmoor Waterway Estates.', 'Many North Fort Myers neighborhoods and rural properties use septic tanks.')
CITY['Fort Myers Beach']=('Lee County', 'Fort Myers Beach is a town on Estero Island along the Gulf of Mexico.', 'Beach-area properties on septic need dependable pumping to keep systems working in sandy, low-lying ground.')
CITY['Three Oaks']=('Lee County', 'Three Oaks is a community in southern Lee County near Estero and San Carlos Park.', 'Three Oaks homes on septic should plan pumping every few years.')
CITY['Gateway']=('Lee County', 'Gateway is a planned community in Lee County east of Fort Myers, near Southwest Florida International Airport.', 'We serve Gateway-area homes and businesses that use septic systems.')
CITY['Alva']=('Lee County', 'Alva is a rural community in eastern Lee County along the Caloosahatchee River.', 'Rural Alva homes, ranches and farms commonly rely on septic systems.')
CITY['Buckingham']=('Lee County', 'Buckingham is a rural community in Lee County east of Fort Myers, known for larger acreage lots.', 'Large-lot Buckingham properties typically use septic tanks that need regular pumping.')
CITY['Sanibel']=('Lee County', 'Sanibel is a barrier island city in Lee County known for its beaches, shelling and wildlife refuge.', 'Island properties need careful septic maintenance to protect the surrounding environment.')
CITY['Pine Island']=('Lee County', 'Pine Island is the largest island in Lee County, with communities including Bokeelia, Pineland, St. James City and Matlacha.', 'Many Pine Island homes and businesses use septic systems.')
CITY['Port Charlotte']=('Charlotte County', 'Port Charlotte is a community in Charlotte County, north of the Peace River from Punta Gorda.', 'Many Port Charlotte homes are on septic, so routine pumping helps prevent backups.')
CITY['Punta Gorda']=('Charlotte County', 'Punta Gorda is the county seat of Charlotte County, on Charlotte Harbor.', 'Homes in and around Punta Gorda that use septic systems need regular maintenance.')
CITY['Everglades City']=('Collier County', 'Everglades City is a small town in southern Collier County, a gateway to Everglades National Park and the Ten Thousand Islands, near Chokoloskee and Copeland.', 'Remote properties around Everglades City depend on septic systems and timely pumping.')
CITY['Golden Gate Estates']=('Collier County', 'Golden Gate Estates is a large rural area of eastern Collier County, east of Naples and Golden Gate, laid out on lots that are mostly an acre or more along roads like Golden Gate Blvd, Immokalee Road, Randall Blvd and Everglades Blvd. Orangetree sits at its northern edge.', 'Most Estates homes have no central sewer and use their own well and septic system, so the septic tank is the only thing handling household wastewater.')
CITY['South Fort Myers']=('Lee County', 'South Fort Myers is the unincorporated stretch of Lee County between the city of Fort Myers and San Carlos Park, including Cypress Lake, Iona, Villas, Whiskey Creek, McGregor, Harlem Heights and Pine Manor.', 'Sewer service varies street by street here, and plenty of older homes along the McGregor and Iona corridors still have septic tanks.')
CITY['Fort Myers Shores']=('Lee County', 'Fort Myers Shores is a Lee County community on the south bank of the Caloosahatchee River east of Fort Myers, along Palm Beach Blvd (SR 80), and includes the older riverfront settlement of Olga.', 'Many homes here, especially older riverfront and canal lots and properties toward Olga, are on septic.')
CITY['Tice']=('Lee County', 'Tice is a small, established community just east of the Fort Myers city limits, between Palm Beach Blvd and the Caloosahatchee, near I-75.', 'Tice is largely older single-family homes, and many were built with septic tanks that are now decades old.')
CITY['Corkscrew']=('Lee County', 'The Corkscrew area runs east of I-75 along Corkscrew Road from east Estero toward Corkscrew Swamp, near the Lee and Collier County line.', 'Much of it is rural, large-lot land in Lee County\'s Density Reduction/Groundwater Resource (DR/GR) area, where homes rely on private wells and septic systems.')
CITY['LaBelle']=('Hendry County', 'LaBelle is the county seat of Hendry County, on the Caloosahatchee River east of Alva along SR 80, with Port LaBelle to the northeast and Felda to the south.', 'Ranches, farms and many rural homes around LaBelle and Port LaBelle use septic systems.')
CITY['Charlotte Harbor']=('Charlotte County', 'Charlotte Harbor is a community on the north shore of the Peace River in Charlotte County, along US-41 across the river from Punta Gorda.', 'Many homes here sit on low, waterfront ground close to the harbor and use septic tanks.')
CITY['Harbour Heights']=('Charlotte County', 'Harbour Heights is a residential community in Charlotte County on the north side of the Peace River, east of Port Charlotte off Kings Highway.', 'Homes in Harbour Heights commonly rely on septic tanks.')
CITIES_ALL=list(CITY)
CITY_NOTES={
"Golden Gate Estates":"<h2>Septic in Golden Gate Estates</h2><p>Because there is no central sewer in most of the Estates, every home's tank and drain field carry the full load, and a failed drain field on a well-and-septic lot is a costly fix. The area is low and flat, and the water table rises close to the surface in the summer rainy season, which is why many Estates drain fields are built up as raised mounds. Pumping on schedule keeps solids out of that drain field.</p><p>Septic permits for new systems, repairs and modifications in Collier County go through Florida's onsite sewage program. If you don't know your tank size or location, your permit file is a good place to start, and we can help find the lid on the day of service.</p><p>Large lots mean long driveways and lids that can be far from the house. Let us know about gates, soft ground or a buried lid when you book.</p>",
"South Fort Myers":"<h2>Septic in South Fort Myers</h2><p>South Fort Myers grew over several decades, so sewer service is a patchwork. Some subdivisions are on Lee County Utilities sewer, while many older homes off McGregor Blvd, Iona and Cypress Lake still use septic. If you're not sure which you have, a sewer bill from Lee County Utilities or the city is a quick check; if you don't get one, you likely have a tank.</p><p>Much of this area sits close to the Caloosahatchee, Hendry Creek and Estero Bay, on sandy soil with a shallow water table, so a properly maintained system matters for nearby waterways as well as your yard. Older tanks here may be small by today's standards and fill faster.</p>",
"Fort Myers Shores":"<h2>Septic in Fort Myers Shores and Olga</h2><p>Riverfront and canal lots along the Caloosahatchee often have a high water table, and drain fields there have less room to work in wet months. After heavy summer rains or high water on the river, slow drains are a common sign the system is struggling.</p><p>Many homes here are older, and so are their tanks. If you've just bought a home in Fort Myers Shores or Olga and don't know when the tank was last pumped, it's a good idea to have it pumped and looked at. Septic permits in Lee County go through Florida's onsite sewage program.</p>",
"Tice":"<h2>Septic in Tice</h2><p>Many Tice homes date back decades, and so do their septic tanks. Older tanks are often smaller than today's minimums, so they can fill faster, especially in households with several people. If your tank has never been pumped since you moved in, start there.</p><p>Tice sits near the Caloosahatchee on flat, sandy ground, so heavy summer rain can saturate drain fields. Pumping before the rainy season gives the system more room.</p>",
"Corkscrew":"<h2>Septic along Corkscrew Road</h2><p>Lee County's DR/GR area is meant to protect groundwater and wetlands, which is why lots out here are large and homes are on private wells and septic. Keeping your tank pumped protects your drain field and the water your own well draws from.</p><p>Homes near the Corkscrew Swamp side can see standing water in the rainy season. Long driveways and lids far from the house are common, so tell us about gates and access when you book. Septic permits here go through Florida's onsite sewage program in Lee County.</p>",
"LaBelle":"<h2>Septic around LaBelle</h2><p>Outside the city's sewer lines, homes in LaBelle, Port LaBelle and the surrounding ranch land rely on septic. Rural properties can have older or larger systems, and some have more than one tank, so let us know about outbuildings, barns or a second dwelling when you call.</p><p>LaBelle is in Hendry County, where septic permits go through Florida's onsite sewage program. Low ground near the Caloosahatchee can be wet in the rainy season, so schedule routine pumping before summer if you can. LaBelle is near the edge of our area, so call to confirm scheduling.</p>",
"Charlotte Harbor":"<h2>Septic in Charlotte Harbor</h2><p>Charlotte Harbor is low and close to the water, so drain fields can sit near the water table, especially in summer. Charlotte County has been working to move parts of the county from septic to central sewer, so check whether your street has a sewer connection planned before major septic repairs. Until then, routine pumping protects the system you have.</p><p>Septic permits in Charlotte County go through Florida's onsite sewage program. Charlotte Harbor is near the north edge of our area, so call to confirm scheduling.</p>",
"Harbour Heights":"<h2>Septic in Harbour Heights</h2><p>Harbour Heights has many older single-family homes on septic, on the Peace River side of Charlotte County where the water table can be high in summer. Older tanks can be smaller, and drain fields here can be slow to recover after heavy rain.</p><p>Charlotte County has been expanding central sewer in parts of the county, so ask the county whether a conversion is planned for your street before replacing a system. Septic permits go through Florida's onsite sewage program. Harbour Heights is near the north edge of our area, so call to confirm scheduling.</p>",
}
def slug(c): return "septic-tank-pumping-"+c.lower().replace(" ","-")+"-fl"
FAQ=[("How often should I pump my septic tank?","Most homes need septic tank pumping every 3 to 5 years. Tank size, number of people in the home and water use all affect how often."),
("How much does it cost to pump a septic tank in Florida?","Residential septic pumping starts at $399.99. After-hours pumping is $599.99. Call (239) 451-3261 to confirm for your tank. Your final quote depends on tank size, tank access, and whether the lid needs locating or digging."),
("What are signs my septic tank is full?","Slow drains, gurgling pipes, sewage odors, wet or extra-green spots over the drain field, and backups are common signs."),
("Do you pump commercial septic tanks?","Yes. We provide commercial septic tank pumping for businesses and other properties."),
("Do you pump grease traps?","Yes. We pump grease traps for restaurants and commercial kitchens, one-time or on a recurring schedule. Call (239) 451-3261."),
("Do you do septic repairs?","Yes. We look at the system first, then quote the repair. Call (239) 451-3261. Repair work is performed under Florida Certified Plumbing Contractor Raymond F. Dibble, License #CFC020332."),
("Do you replace drain fields?","Yes. We quote drain field replacement after inspecting the system. Call (239) 451-3261. The work is performed under FL Certified Plumbing Contractor Raymond F. Dibble, License #CFC020332."),
("Do you do septic inspections for real estate?","Yes. We offer septic inspections for buyers, sellers and homeowners. A septic inspection with pump-out is $549.99."),
("What areas do you serve?","Estero, Bonita Springs, Naples, North Naples, Fort Myers, Cape Coral, Lehigh Acres, San Carlos Park and nearby areas of Lee and Collier County."),
("What shouldn't go into a septic system?","Avoid grease, wipes (even 'flushable'), paper towels, feminine products, harsh chemicals and medications. They can clog the system or harm the bacteria that break down waste."),
("What is a septic tank riser?","A riser is an extension installed on top of the tank's access opening that brings the lid up to ground level, so future pump-outs don't need digging to find and open the tank. Express installs 6-inch risers for $299.99 each. Call (239) 451-3261 to confirm what your tank needs."),
("How much does it cost to find and dig up a buried lid?","Locating and digging up a buried lid is $100, plus $50 for each additional hour. A riser avoids digging on future visits."),
("How do I book?","For routine pumping, send a request through our ServiceM8 booking page. We'll contact you to confirm a time; it isn't a confirmed appointment until we do. For a backup, call (239) 451-3261 day or night.")]
PAGES=[]
EXTRA={
"septic-tank-pumping":"<h2>Septic Pumping Near Me</h2><p>We provide septic pumping and septic tank cleaning across Lee and Collier County. Residential septic tank pumping starts at $399.99. After-hours pumping is $599.99. Call to confirm for your tank. Your final quote depends on tank size, tank access, and whether the lid needs locating or digging.</p><h2>Emergency Septic Service</h2><p>Sewage backing up or a tank overflowing? Call <a href='tel:+12394513261'>(239) 451-3261</a> right away and avoid running water until we get there. Night or day, we're available for emergencies. For routine service, we can often make it same day when possible.</p>",
"residential-septic-tank-pumping":"<h2>Residential Septic Service Near Me</h2><p>Residential septic tank cleaning removes built-up sludge and scum so your home's system keeps working.</p><h2>Tank Size FAQs</h2><h3>What size is my septic tank?</h3><p>Many homes have tanks around 750 to 1,500 gallons; larger homes generally have larger tanks. Your permit records or our crew can help confirm the size.</p><h3>Does tank size change how often I pump?</h3><p>Yes. Smaller tanks and larger households need pumping more often. See <a href='/how-often-to-pump-septic-tank/'>how often to pump your septic tank</a>.</p>",
"commercial-septic-tank-pumping":"<h2>Commercial Septic Pumping Near Me</h2><p>Need commercial septic service in Lee or Collier County? Call to discuss your property. Restaurants with grease traps should mention them when you call so we can talk through your needs.</p>",
"septic-tank-riser-installation":"<div class='price-slot'><p class='pp'>Riser installation: $299.99 per riser (6-inch)</p><p>How many risers you need depends on how many access openings your tank has. Call to confirm for your tank.</p></div>@@RISER@@<h2>Why add a riser?</h2><ul><li>No digging to reach the lid on future pump-outs</li><li>You can see where the tank is, so it's easier to keep vehicles and heavy equipment off it</li><li>Easier access for inspections</li></ul><h2>Riser questions</h2><h3>Can you install a riser when you pump my tank?</h3><p>Yes, ask when you call or book. The lid is already uncovered during a pump-out.</p><h3>How many risers do I need?</h3><p>It depends on how many access openings your tank has. Many tanks have more than one. We'll tell you what we see.</p>",
"septic-inspections":"<h2>Septic Inspection for Home Purchase</h2><p>A real estate septic inspection gives buyers and sellers a clearer picture of the system before closing. We serve Fort Myers, Naples and the surrounding area.</p><h2>Septic Inspection Cost</h2><div class='price-slot'><p class='pp'>Septic inspection with pump-out: $549.99</p><p>Call (239) 451-3261 to schedule or to ask about your property.</p></div>",
}
BID=BASE+"/#business"
PROV={"@id":BID}
def schema(extra=None):
  s={"@context":"https://schema.org","@type":["LocalBusiness","Plumber"],"@id":BID,"name":NAME,"legalName":NAME+" LLC","url":BASE+"/","telephone":TEL,"email":EMAIL,"priceRange":"$399.99+","openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],"opens":"00:00","closes":"23:59"}],"image":BASE+"/assets/img/truck-wide-1536.webp","hasMap":REVIEWS_READ,"sameAs":[REVIEWS_READ],
   "address":{"@type":"PostalAddress","streetAddress":"23357 Olde Meadowbrook Circle","addressLocality":"Estero","addressRegion":"FL","postalCode":"34134","addressCountry":"US"},
   "areaServed":[{"@type":"City","name":c+", FL"} for c in CITIES_ALL],
   "makesOffer":[({"@type":"Offer","itemOffered":{"@type":"Service","name":s[1],"url":f"{BASE}/{s[0]}/"},"priceSpecification":{"@type":"PriceSpecification","minPrice":399.99,"priceCurrency":"USD"}} if s[0]=="residential-septic-tank-pumping" else {"@type":"Offer","itemOffered":{"@type":"Service","name":s[1],"url":f"{BASE}/{s[0]}/"}}) for s in SERVICES if s[0] not in ("septic-tank-riser-installation","septic-inspections","septic-repair","drain-field-replacement")]
     +[{"@type":"Offer","itemOffered":{"@type":"Service","name":"Septic Repair","url":BASE+"/septic-repair/","description":"Quoted after we look at the system"}},
        {"@type":"Offer","itemOffered":{"@type":"Service","name":"Drain Field Replacement","url":BASE+"/drain-field-replacement/","description":"Quoted after we inspect the system"}}]
     +[{"@type":"Offer","name":"Septic inspection with pump-out","price":549.99,"priceCurrency":"USD","itemOffered":{"@type":"Service","name":"Septic Inspections","url":BASE+"/septic-inspections/"}}]
     +[{"@type":"Offer","name":"6-inch septic tank riser, installed (each)","price":299.99,"priceCurrency":"USD","itemOffered":{"@type":"Service","name":"Septic Tank Riser Installation","url":BASE+"/septic-tank-riser-installation/"}},
       {"@type":"Offer","name":"Locating and digging up a buried septic tank lid","price":100,"priceCurrency":"USD","description":"$100, plus $50 for each additional hour"},
       {"@type":"Offer","name":"After-hours pumping","price":599.99,"priceCurrency":"USD"},
       {"@type":"Offer","itemOffered":{"@type":"Service","name":"Commercial Grease Trap Service","serviceType":"Grease trap pumping","url":BASE+"/commercial-grease-trap-service/"}}]}
  out=[s]
  if isinstance(extra,list): out+=extra
  elif extra: out.append(extra)
  return "".join(f'<script type="application/ld+json">{json.dumps(o)}</script>' for o in out)
TRUCK_ALT="Express Septic Tank Pumping 4,200-gallon vacuum truck parked at a Southwest Florida home"
HERO_IMG=f'<img src="/assets/img/truck-wide-1024.webp" srcset="/assets/img/truck-wide-640.webp 640w, /assets/img/truck-wide-1024.webp 1024w, /assets/img/truck-wide-1536.webp 1536w" sizes="(min-width:960px) 52vw, 100vw" alt="{TRUCK_ALT}" width="1536" height="960" fetchpriority="high">'
CREW='<figure class="shot crew"><img src="/assets/img/crew-1024.webp" srcset="/assets/img/crew-640.webp 640w, /assets/img/crew-1024.webp 1024w, /assets/img/crew-1500.webp 1500w" sizes="(min-width:960px) 680px, 100vw" alt="Express Septic Tank Pumping crew with the 4,200-gallon vacuum truck" width="1500" height="1125" loading="lazy"></figure>'
LIDS='<figure class="shot"><img src="/assets/img/lids-1024.webp" srcset="/assets/img/lids-640.webp 640w, /assets/img/lids-1024.webp 1024w, /assets/img/lids-1500.webp 1500w" sizes="(min-width:960px) 820px, 100vw" alt="Septic tank lids uncovered and opened for pumping at a Southwest Florida home" width="1500" height="1734" loading="lazy" style="aspect-ratio:auto"></figure>'
RISER='<figure class="shot"><img src="/assets/img/riser-1024.webp" srcset="/assets/img/riser-640.webp 640w, /assets/img/riser-1024.webp 1024w, /assets/img/riser-1500.webp 1500w" sizes="(min-width:960px) 820px, 100vw" alt="Looking down a septic tank riser at the effluent filter" width="1500" height="837" loading="lazy" style="aspect-ratio:auto"></figure>'
EXTRA["septic-tank-riser-installation"]=EXTRA["septic-tank-riser-installation"].replace("@@RISER@@",RISER)
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
  if sid=="septic-tank-riser-installation": return LIDS
  if False:
    return f'<figure class="shot"><img src="/assets/img/truck-wide-1024.webp" srcset="/assets/img/truck-wide-640.webp 640w, /assets/img/truck-wide-1024.webp 1024w" sizes="(min-width:960px) 860px, 100vw" alt="{TRUCK_ALT}" width="1536" height="960" loading="lazy"></figure>'
  if os.path.exists(f"assets/img/{sid}.jpg"):
    return f'<figure class="shot" data-photo-slot="{sid}"><img src="/assets/img/{sid}.jpg" alt="{alt}" loading="lazy" width="1600" height="1000"></figure>'
  return ""
NAVITEMS=[("/residential-septic-tank-pumping/","Residential"),("/commercial-grease-trap-service/","Grease traps"),("/septic-tank-riser-installation/","Risers"),("/septic-repair/","Repairs"),("/service-area/","Service area"),("/about/","About"),("/faq/","FAQ")]
NAVL="".join(f'<a href="{h}">{t}</a>' for h,t in NAVITEMS)
NAV="".join(f'<a href="/{s[0]}/">{s[1]}</a>' for s in SERVICES)+'<a href="/commercial-grease-trap-service/">Commercial Grease Trap Service</a>'
VAL="<p class='values'>Honest, reliable and fair — great customer service is our top priority.</p>"
EMERG="Night or day, we're available for emergencies. Call (239) 451-3261. For routine service, we can often make it same day when possible."
CTA=f'<div class="cta"><a class="btn primary" href="tel:{TEL}">Call {PHONE}</a><a class="btn ghost" href="/contact/#book">Book routine service</a></div>'
AVAIL="Call day or night for a backup. For routine pumping, ask about same-day availability."
PRICE_COND="Your final price depends on tank size, tank access, and whether the lid needs locating or digging. Locating and digging up a buried lid is $100, plus $50 for each additional hour. After-hours pumping is $599.99."
PRICE_PANEL=("<div class='price-panel' id='pricing'><p class='eyebrow'>Pricing</p>"
 "<p class='pp'>Residential pumping from $399.99</p>"
 "<p class='pcond'>"+PRICE_COND+" Call to confirm the price for your tank.</p>"
 "<ul class='plist'><li><span>Buried-lid locating and digging</span> <b>$100, plus $50 for each additional hour</b></li>"
 "<li><span>After-hours pumping</span> <b>$599.99</b></li>"
 "<li><span>Septic inspection with pump-out</span> <b>$549.99</b></li>"
 "<li><span>6-inch risers</span> <b>$299.99 each</b></li></ul></div>")
QUOTES=("<div class='quoteshead'><p class='eyebrow'>Google reviews</p>"
 "<h2><a href='"+REVIEWS_READ+"' rel='noopener'>5.0 stars on Google · 43 reviews</a></h2></div>"
 "<ul class='quotegrid'>"
 "<li class='quotecard'><blockquote><p>Company was great to work with. Very pleasant and professional on the phone and the driver was very knowledgeable and pleasant too. Their pricing was also very reasonable and they were able to service me quickly. Would definitely recommend this company and will use them again.</p></blockquote><p class='qattr'><cite>Michele S.</cite> · Google review</p></li>"
 "<li class='quotecard'><blockquote><p>Excellent septic tank service from start to finish. They were professional, punctual, and very efficient. They explained everything clearly, answered all my questions, and did a great job. The service was excellent, and they left the area clean when they were finished. I highly recommend them to anyone looking for reliable and professional septic tank service. I would definitely use them again.</p></blockquote><p class='qattr'><cite>Isidro P.</cite> · Google review</p></li>"
 "<li class='quotecard'><blockquote><p>Friendly, Professional, and Affordable. I Highly recommend Express Septic Tank Pumping! They worked with my schedule and made the whole process easy.</p></blockquote><p class='qattr'><cite>Allen</cite> · Google review</p></li>"
 "</ul>")
REV=f'<section class="band reviews"><div class="wrap revrow"><div><p class="eyebrow">Reviews</p><h2>See what customers say on Google</h2><p>Our reviews are on our Google Business Profile.</p></div><div class="revlinks"><a class="btn dark" href="{REVIEWS_READ}" rel="noopener">Read our Google reviews</a><a class="txtlink" href="{REVIEW}" rel="noopener">Had a job with us? Leave a review</a></div></div></section>'
ROBOTS={}
LICENSE_URL="https://www.myfloridalicense.com/portalsearches/VerifyLicensee/Results?LicNbr=CFC020332&amp;SearchType=SearchByLicenseNumber"
LICENSE_BODY='Work performed under Florida Certified Plumbing Contractor Raymond F. Dibble, License <a href="'+LICENSE_URL+'" rel="noopener">#CFC020332</a>, licensed since 1981 (45+ years).'
LICENSE_FOOT='Work performed under FL Certified Plumbing Contractor Raymond F. Dibble, License <a href="'+LICENSE_URL+'" rel="noopener">#CFC020332</a>, licensed since 1981.'
def page(path,title,desc,h1,body,extra=None,hero=None,lead=""):
  foot="".join(f'<a href="/{slug(c)}/">{c}</a>' for c in CITIES_ALL[:12])+'<a href="/service-area/">All areas</a>'
  H1A=' data-sth-field="headline"' if path=="/" else ""
  if not hero: body=f'<div class="wrap prose">{body}</div>'
  top=hero if hero else f'<section class="phead"><div class="wrap"><p class="eyebrow">Express Septic Tank Pumping</p><h1>{h1}</h1>{lead}{CTA}</div></section>'
  if hero: top=top.replace("<h1>",f"<h1{H1A}>",1)
  html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-ESN48M0VEZ"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-ESN48M0VEZ');</script>
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{BASE}{path}">{ROBOTS.get(path,"")}<meta name="theme-color" content="#0f1b2d">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{BASE}{path}"><meta property="og:type" content="website"><meta property="og:image" content="{BASE}/assets/img/truck-wide-1536.webp">
{'<link rel="preload" as="image" href="/assets/img/truck-wide-1024.webp" imagesrcset="/assets/img/truck-wide-640.webp 640w, /assets/img/truck-wide-1024.webp 1024w, /assets/img/truck-wide-1536.webp 1536w" imagesizes="100vw">' if hero else ''}
<link rel="stylesheet" href="/styles.css">{schema(extra)}<script src="/site.js" defer></script></head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap bar"><a class="logo" href="/" aria-label="{NAME} home"><span class="mark">EXPRESS</span><span class="sub">Septic Tank Pumping</span></a>
<nav aria-label="Primary">{NAVL}</nav><a class="hcall" href="tel:{TEL}"><span class="lbl">Call</span> {PHONE}</a>
<details class="menu"><summary aria-label="Open menu">Menu</summary><nav aria-label="Mobile">{NAVL}<a href="/contact/">Contact</a><a href="tel:{TEL}">Call {PHONE}</a></nav></details></div></header>
<main id="main">{top}<div class="body">{body}</div>{REV}<section class="band closer"><div class="wrap"><h2>Talk to Express about your tank</h2><p>{AVAIL}</p>{CTA}</div></section></main>
<footer id="contact" class="foot"><div class="wrap fgrid"><div><p class="mark">EXPRESS</p><p>{NAME} LLC<br>23357 Olde Meadowbrook Circle, Estero, FL 34134<br><a href="tel:{TEL}">{PHONE}</a><br><a data-sth-field="email" href="{"mailto:"+EMAIL if EMAIL else "/contact/"}">{EMAIL or "Send a request"}</a></p><p>Open 24 hours, 7 days a week.</p><p>Owner-operated. Licensed &amp; insured. We come to you.</p><p class="dot">USDOT 6673233</p><p class="license-foot">{LICENSE_FOOT}</p></div>
<div><p class="fh">Services</p>{NAV}</div><div><p class="fh">Areas</p>{foot}</div><div><p class="fh">Info</p><a href="/">Home</a><a href="/how-it-works/">How it works</a><a href="/septic-system-maintenance/">Septic maintenance</a><a href="/how-often-to-pump-septic-tank/">How often to pump</a><a href="/completed-jobs/">Completed jobs</a><a href="/about/">About</a><a href="/faq/">FAQ</a><a href="/contact/">Contact</a><a href="/accessibility/">Accessibility</a><a href="/privacy/">Privacy</a><a href="/terms/">Terms</a></div></div></footer>
<div class="mbar" role="region" aria-label="Quick contact"><a class="btn primary" href="tel:{TEL}">Call · {PHONE}</a><a class="btn ghost" href="/contact/#book">Book</a></div></body></html>'''
  html=html.replace("<div class=\"body\"></div>","")
  if 'id="book"' in body: html=html.replace('href="/contact/#book"','href="#book"')
  pre="../"*(path.count("/")-1) or "./"
  html=html.replace('href="/','href="'+pre).replace('src="/','src="'+pre).replace(', /assets',', '+pre+'assets').replace('srcset="/','srcset="'+pre).replace("href='/","href='"+pre).replace('imagesrcset="'+pre,'imagesrcset="'+pre)
  d="."+path; os.makedirs(d,exist_ok=True); open(d+"index.html","w").write(html); PAGES.append(path)
def sec(inner,cls=""): return f'<section class="sec {cls}"><div class="wrap">{inner}</div></section>'
svc_list="<ul class='rows'>"+"".join(f'<li><a href="/{s[0]}/">{s[1]}</a></li>' for s in SERVICES)+"<li><a href='/commercial-grease-trap-service/'>Commercial Grease Trap Service</a></li></ul>"
city_list="<ul class='cities'>"+"".join(f'<li><a href="/{slug(c)}/">{c}</a></li>' for c in CITIES_ALL)+"</ul>"
REQUEST=f'''<div class="book" id="book"><p class="eyebrow">Book or call</p><h2>What do you need?</h2>
<ol class="paths">
<li class="path urgent"><p class="pk">I'm experiencing a backup</p><p>Don't book online. Call now and stop running water until we get there. Day or night.</p><a class="btn primary" href="tel:{TEL}">Call now · {PHONE}</a></li>
<li class="path"><p class="pk">Routine pumping for my home</p><p>Send a request on ServiceM8, the booking system we use. We'll contact you to confirm a time; it isn't booked until we confirm. From $399.99.</p><a class="btn dark" href="{BOOK}" rel="noopener" target="_blank">Book routine service on ServiceM8<span class="sr"> (opens in a new tab)</span> ↗</a></li>
<li class="path"><p class="pk">Grease trap for a restaurant or kitchen</p><p>One-time pump-outs or a recurring schedule. Call to set it up.</p><a class="btn ghost" href="tel:{TEL}">Call {PHONE}</a> <a class="txtlink" href="/commercial-grease-trap-service/">Grease trap service</a></li>
</ol></div>'''
ZIPBOX='''<div class="zip" data-zip><h3>Check your ZIP</h3><form data-zipform novalidate><label for="zipin">5-digit ZIP code</label><div class="zrow"><input id="zipin" inputmode="numeric" maxlength="5" autocomplete="postal-code" pattern="[0-9]{5}"><button class="btn primary" type="submit">Check</button></div></form><p class="zres" aria-live="polite"></p></div>'''
ROUTE='<svg class="route" viewBox="0 0 600 160" aria-hidden="true" focusable="false"><path d="M10 140 C 90 140, 110 40, 200 60 S 330 140, 400 90 S 520 20, 590 30"/><circle cx="10" cy="140" r="5"/><circle cx="590" cy="30" r="5"/></svg>'
HERO=f'''<section class="hero"><div class="wrap hcopy"><p class="eyebrow">Owner-operated in Estero</p><h1>Septic tank pumping in Southwest Florida</h1>
<p class="avail" data-sth-field="description">{AVAIL}</p>
<p class="from">Residential pumping from <strong>$399.99</strong> <a href="#pricing">What affects the price</a></p>
<div class="cta"><a class="btn primary big" href="tel:{TEL}">Call {PHONE}</a><a class="btn ghost" href="#book">Book routine service</a></div></div><figure class="hphoto">{HERO_IMG.replace('sizes="(min-width:960px) 52vw, 100vw"','sizes="(min-width:960px) 56vw, 100vw"')}</figure></section>'''
# ---- Priority city pages (Lehigh Acres first). Local facts are cited to public sources; nothing invented. ----
def A(label,url): return f'<a href="{url}" rel="noopener">{label}</a>'
SRC={
 "fgua":("FGUA, Lehigh Acres service area description","https://fgua.com/docs/systems/System-Description-Lehigh-Acres-Lee.pdf"),
 "leelehigh":("Lee County, Lehigh Acres septic-to-sewer planning document","https://www.leegov.com/dhs/Documents/Grant%20Programs/LeeCountyPD_GPS4.pdf"),
 "estero":("Village of Estero, Septic to Sewer","https://estero-fl.gov/sewer/"),
 "esterotoday":("EsteroToday, Utilities Expansion Program update (2025)","https://esterotoday.com/uepupdate2025/"),
 "bsu":("Bonita Springs Utilities, Sun Village septic-to-sewer","https://bsu.us/sunvillage/"),
 "bsufaq":("Bonita Springs Utilities, Sans Souci FAQ","https://bsu.us/sanssouci-faqs/"),
 "fmcity":("City of Fort Myers Utilities","https://www.cityftmyers.com/utilities"),
 "lcu":("Lee County Utilities","https://www.leegov.com/utilities"),
 "uep":("City of Cape Coral, Utilities Extension Project","https://www.capecoral.gov/departments/public_works/capital_improvements/utilities_extension_project_uep/index.php"),
 "uepn1":("City of Cape Coral, North 1 UEP","https://www.capecoral.gov/departments/public_works/capital_improvements/utilities_extension_project_uep/north_1_uep.php"),
 "epa":("U.S. EPA, How to care for your septic system","https://www.epa.gov/septic/how-care-your-septic-system"),
}
def S(k): return A(*SRC[k])
CITY_PLUS={
"Lehigh Acres":dict(
 title="Septic Tank Cleaning & Pumping Lehigh Acres FL | Express Septic",
 desc="Septic tank cleaning and pumping in Lehigh Acres, FL. Residential pumping from $399.99. Call (239) 451-3261 day or night, or request routine service online.",
 h1="Septic Tank Cleaning &amp; Pumping in Lehigh Acres, FL",
 near=["Fort Myers","Gateway","Buckingham","Alva","Fort Myers Shores","Tice"],
 local=f"<h2>Septic in Lehigh Acres: most homes have a tank</h2><p>Central water and sewer in Lehigh Acres is run by the Florida Governmental Utility Authority (FGUA), which reports about 10,420 wastewater customers here ({S('fgua')}). Lee County has counted 32,879 permitted septic tanks in Lehigh Acres ({S('leelehigh')}). So most Lehigh homes use a septic tank, often alongside a private well.</p><p>Not sure which you have? If you don't pay a sewer charge to FGUA, your home most likely has a septic tank.</p><p>Lee County notes that many Lehigh Acres homes were built from the 1960s through the early 1980s ({S('leelehigh')}). If you own an older home and don't know when the tank was last pumped, start with a pump-out so you know where things stand.</p><p>On a well-and-septic lot, the drain field and your well share the same ground. Pumping on schedule keeps solids out of the drain field. Lehigh is flat, and the summer rainy season raises the water table, so pumping before summer gives the system more room.</p>",
 sewer_q="Is my Lehigh Acres home on septic or sewer?",
 sewer_a="Most Lehigh Acres homes are on septic. FGUA provides sewer to part of the community, about 10,420 wastewater customers, while Lee County counts 32,879 permitted septic tanks in Lehigh Acres. If you don't pay FGUA a sewer charge, you most likely have a septic tank.",
 srcs=["fgua","leelehigh","epa"]),
"Estero":dict(
 title="Septic Tank Pumping Estero, FL | Local, From $399.99 | Express Septic",
 desc="Estero-based septic tank pumping for homes and businesses. Residential pumping from $399.99, risers and grease traps too. Call (239) 451-3261.",
 h1="Septic Tank Pumping in Estero, FL",
 near=["Bonita Springs","San Carlos Park","Three Oaks","Corkscrew","Fort Myers Beach","South Fort Myers"],
 local=f"<h2>Septic in Estero</h2><p>Express is based in Estero, at 23357 Olde Meadowbrook Circle, so Estero homes and businesses are close to home for us.</p><p>The Village of Estero is moving properties from septic to Lee County Utilities sewer through its septic-to-sewer program, aimed in part at protecting the Estero River ({S('estero')}). Early phases include package-plant communities and the Broadway Avenue areas, and the Village treats connection as mandatory once sewer reaches a property ({S('esterotoday')}).</p><p>Until sewer reaches your street, your septic system still needs regular pumping. If you get a notice that sewer is available, ask the Village or Lee County Utilities about the connection and septic abandonment steps.</p>",
 sewer_q="Is Estero switching from septic to sewer?",
 sewer_a="In parts of Estero, yes, over time. The Village of Estero is converting properties to Lee County Utilities sewer in phases. Until sewer reaches your street and you connect, keep pumping your septic tank on schedule.",
 srcs=["estero","esterotoday","epa"]),
"Bonita Springs":dict(
 title="Septic Tank Pumping Bonita Springs, FL | From $399.99 | Express Septic",
 desc="Septic tank pumping in Bonita Springs, FL from nearby Estero. Residential pumping from $399.99, risers and grease traps too. Call (239) 451-3261.",
 h1="Septic Tank Pumping in Bonita Springs, FL",
 near=["Estero","North Naples","Naples","San Carlos Park","Three Oaks","Corkscrew"],
 local=f"<h2>Septic in Bonita Springs</h2><p>Express is based in neighboring Estero, just north of Bonita Springs.</p><p>Central sewer in Bonita Springs is provided by Bonita Springs Utilities (BSU). The City and BSU are converting some neighborhoods from septic to sewer, including Sun Village Estates and the Lake of Sans Souci, partly to cut nutrients reaching groundwater and the Imperial River ({S('bsu')}). Once sewer is available, connection is required within one year ({S('bsufaq')}).</p><p>Many other Bonita Springs homes, especially older neighborhoods and larger lots east of I-75, still use septic tanks that need regular pumping.</p>",
 sewer_q="My Bonita Springs neighborhood is getting sewer. Do I still need pumping?",
 sewer_a="Until your home is connected, yes. Your septic tank keeps working until the switch, so keep it pumped. Bonita Springs Utilities handles the sewer connection, and connection is required within one year once sewer is available.",
 srcs=["bsu","bsufaq","epa"]),
"Fort Myers":dict(
 title="Septic Tank Pumping Fort Myers, FL | From $399.99 | Express Septic",
 desc="Septic tank pumping in Fort Myers, FL for homes and businesses. Residential pumping from $399.99, risers and grease traps too. Call (239) 451-3261.",
 h1="Septic Tank Pumping in Fort Myers, FL",
 near=["South Fort Myers","North Fort Myers","Tice","Fort Myers Shores","Lehigh Acres","Cape Coral"],
 local=f"<h2>Septic in Fort Myers</h2><p>We provide septic tank pumping and septic pump-outs for homes and businesses in Fort Myers and the unincorporated areas around it.</p><p>A Fort Myers mailing address can mean the city or the unincorporated Lee County areas around it. The City of Fort Myers runs utilities inside city limits ({S('fmcity')}). Outside them, some areas are on Lee County Utilities ({S('lcu')}) and many homes still use septic tanks.</p><p>Sewer service can change from one street to the next, especially in older neighborhoods. If you don't get a sewer bill from the city or Lee County Utilities, you likely have a septic tank.</p><p>For area-specific notes, see our pages for <a href=\"/septic-tank-pumping-south-fort-myers-fl/\">South Fort Myers</a>, <a href=\"/septic-tank-pumping-tice-fl/\">Tice</a> and <a href=\"/septic-tank-pumping-fort-myers-shores-fl/\">Fort Myers Shores</a>.</p>",
 sewer_q="How do I know if my Fort Myers home has a septic tank?",
 sewer_a="Check your utility bills. If you don't pay a sewer charge to the City of Fort Myers or Lee County Utilities, your home most likely has a septic tank. Many homes in unincorporated areas with Fort Myers addresses are on septic.",
 srcs=["fmcity","lcu","epa"]),
"Cape Coral":dict(
 title="Septic Tank Pumping Cape Coral, FL | From $399.99 | Express Septic",
 desc="Septic tank pumping in Cape Coral, FL, including the North Cape. Residential pumping from $399.99, risers too. Call (239) 451-3261.",
 h1="Septic Tank Pumping in Cape Coral, FL",
 near=["North Fort Myers","Fort Myers","Pine Island","South Fort Myers","Sanibel","Fort Myers Beach"],
 local=f"<h2>Septic in Cape Coral</h2><p>Until a street is connected to city sewer, homes there still need regular septic tank pumping and septic tank cleaning.</p><p>Cape Coral began as a low-density community built on septic tanks and shallow wells. Through its Utilities Extension Project (UEP), the City has extended water and sewer to nearly all of Cape Coral south of Pine Island Road and is now working north ({S('uep')}). North 1 East construction is expected to finish around the end of 2027, with later North Cape phases still to come ({S('uepn1')}).</p><p>So many North Cape homes still rely on septic tanks. The City notes that failed septic effluent can flow into groundwater and canals ({S('uep')}), which matters on canal-front lots.</p><p>Questions about connecting to city utilities or septic tank abandonment go to the City's Customer Billing Services at (239) 242-3853 ({S('uepn1')}).</p>",
 sewer_q="My Cape Coral area is in the UEP. Do I still need septic pumping?",
 sewer_a="Until your home is connected to city sewer, yes. Your septic system keeps handling your wastewater until then. The City's Customer Billing Services, (239) 242-3853, handles connection and septic abandonment questions.",
 srcs=["uep","uepn1","epa"]),
}
LID_ASK=("<h2>If your lid is buried</h2><p>Many tanks have lids buried under soil or grass. Locating and digging up a buried lid is $100, plus $50 for each additional hour. If you know where the lid is, mark it or tell us when you call.</p>"
 "<p>To skip digging next time, ask about a <a href='/septic-tank-riser-installation/'>6-inch riser</a> ($299.99 each). It brings the lid up to ground level.</p>")
RISER_QA=("What is a septic tank riser?","A riser is an extension installed on top of the tank's access opening. It brings the lid up to ground level, so future pump-outs don't need digging. Express installs 6-inch risers for $299.99 each. Call (239) 451-3261 to confirm what your tank needs.")
def city_faq(c,cp):
  return [(f"How much does septic tank pumping cost in {c}?",f"Residential pumping with Express starts at $399.99. {PRICE_COND} Call (239) 451-3261 to confirm the price for your tank."),
   (cp["sewer_q"],cp["sewer_a"]),
   ("How often should I pump my septic tank?","The U.S. EPA recommends pumping most household tanks every 3 to 5 years. Tank size, household size and water use change that. Pumping before Florida's summer rainy season gives the drain field more room."),
   ("How much does it cost to find and dig up a buried lid?","Locating and digging up a buried lid is $100, plus $50 for each additional hour. A riser avoids digging on future visits."),
   RISER_QA,
   ("Do you do septic repairs?","Yes. We look at the system first, then quote the repair. Call (239) 451-3261. Repair work is performed under Florida Certified Plumbing Contractor Raymond F. Dibble, License #CFC020332."),
   (f"Do you pump grease traps in {c}?","Yes. We pump grease traps for restaurants and commercial kitchens, one-time or on a recurring schedule. Call (239) 451-3261 to set it up."),
   ("Can I book online?","Yes, for routine pumping. Send a request through our ServiceM8 booking page and we'll contact you to confirm a time. It isn't a confirmed appointment until we confirm. For a backup, call (239) 451-3261 day or night.")]
def faq_ld(items): return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in items]}
# Completed jobs: add only real, owner-approved jobs (city, service, month, what was done; never a street address).
# Example: JOBS.append(dict(city="Lehigh Acres", service="Residential septic tank pumping", month="2026-11", summary="..."))
# Owner-supplied jobs (Timemark-stamped photos, Nov 2026). Only what the photos show; no addresses, names or prices.
JOBS=[
 dict(id="cape-coral-2026-11-14",city="Cape Coral",date="November 14, 2026",title="Buried lids, inlet and outlet tees, effluent filter",
   found="Round concrete tank lids were buried.",done="Dug up the lids, exposed the inlet and outlet tees, and pulled and cleaned the effluent filter."),
 dict(id="lehigh-acres-2026-11-13",city="Lehigh Acres",date="November 13, 2026 (night visit)",title="Pump-out through an existing riser",
   found="The tank already had a riser, so no digging was needed.",done="Pumped the tank through the riser. The baffle was visible during the pump-out."),
 dict(id="bonita-springs-2026-11-09",city="Bonita Springs",date="November 9, 2026 (night visit)",title="Buried lid dug out at night",
   found="The round tank lid was buried.",done="Dug out the lid and opened the tank at night."),
 dict(id="lehigh-acres-2026-11-07",city="Lehigh Acres",date="November 7, 2026",title="Buried lids on a two-compartment tank",
   found="Both lids were buried. Before pumping, heavy solids and scum had built up at the inlet.",done="Located the two lids with a probe, dug them up, and pumped the tank."),
 dict(id="lehigh-acres-2026-11-04",city="Lehigh Acres",date="November 4, 2026 (night visit)",title="Night pump-out through a riser",
   found="The tank had a green riser at ground level.",done="Pumped the tank through the riser with the vacuum hose."),
]
# Cities with septic pumping jobs confirmed in ServiceM8 (owner screenshots); city level only.
SERVED_RECENTLY={"Lehigh Acres","Fort Myers","North Fort Myers","Naples"}
def jobs_block(c):
  js=[j for j in JOBS if j["city"]==c]
  served=f"<p>We've done septic tank pumping jobs in {c} recently.</p>" if c in SERVED_RECENTLY else ""
  if not js: return (f"<h2>Recent work in {c}</h2>"+served) if served else ""
  return (f"<h2>Recent jobs in {c}</h2>"+served+"<ul>"+"".join(f"<li><strong>{j['date']}: {j['title']}.</strong> {j['found']} {j['done']} <a href='/completed-jobs/#{j['id']}'>See job</a></li>" for j in js)+"</ul>")
def city_plus_page(c,county,a,b):
  cp=CITY_PLUS[c]; faq=city_faq(c,cp); path=f"/{slug(c)}/"
  quick=(f"<div class='quick'><p class='eyebrow'>Quick answer</p><p><strong>Express Septic Tank Pumping pumps septic tanks in {c}, FL.</strong> Residential pumping starts at $399.99. "
   f"For a backup, call <a href='tel:{TEL}'>{PHONE}</a> day or night. For routine pumping, request a time online and we'll contact you to confirm.</p>"
   f"<ul class='facts'><li><b>Services:</b> residential and commercial septic pumping, septic repairs, drain field replacement, septic tank risers, grease trap pumping, septic inspections</li><li><b>Price:</b> residential pumping from $399.99; after-hours pumping $599.99; septic inspection with pump-out $549.99; 6-inch risers $299.99 each; buried-lid locating/digging $100, plus $50 for each additional hour</li><li><b>Hours:</b> open 24 hours, 7 days a week</li><li><b>Based in:</b> Estero, serving {c} and the rest of {county}</li><li><b>Licensing:</b> work performed under FL Certified Plumbing Contractor Raymond F. Dibble, #CFC020332</li></ul></div>")
  body=(quick+photo(slug(c),f"Septic tank pumping job in {c}, FL")+cp["local"]+jobs_block(c)+
   f"<h2>What septic pumping costs in {c}</h2>"+PRICE_PANEL+LID_ASK+
   f"<h2>Septic services in {c}</h2><ul class='cards'>"+"".join(f'<li><a href="/{s[0]}/">{s[1]}</a></li>' for s in SERVICES)+"<li><a href='/commercial-grease-trap-service/'>Commercial Grease Trap Service</a></li></ul>"
   f"<h2>Signs your tank needs pumping</h2><p>Slow drains, gurgling pipes, sewage odors outside, or soggy, extra-green grass over the drain field. If it's been 3 to 5 years since your last pump-out, or you don't know, it's time to call.</p>"
   +REQUEST+f"<h2>{c} septic questions</h2>"+"".join(f"<h3>{q}</h3><p>{x}</p>" for q,x in faq)+
   "<h2>Nearby areas we serve</h2><ul class='cards'>"+"".join(f'<li><a href="/{slug(x)}/">{x}</a></li>' for x in cp["near"])+"<li><a href='/service-area/'>All areas</a></li></ul>"
   "<p class='srcs'>Sources: "+"; ".join(S(k) for k in cp["srcs"])+".</p>")
  crumbs={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":BASE+"/"},{"@type":"ListItem","position":2,"name":"Service area","item":BASE+"/service-area/"},{"@type":"ListItem","position":3,"name":c,"item":BASE+path}]}
  svc={"@context":"https://schema.org","@type":"Service","name":f"Septic tank pumping in {c}, FL","serviceType":"Septic tank pumping","url":BASE+path,"provider":PROV,"areaServed":{"@type":"City","name":f"{c}, FL","containedInPlace":{"@type":"AdministrativeArea","name":f"{county}, FL"}},"offers":{"@type":"Offer","priceSpecification":{"@type":"PriceSpecification","minPrice":399.99,"priceCurrency":"USD"}}}
  page(path,cp["title"],cp["desc"],cp["h1"],body,[svc,faq_ld(faq),crumbs])
HOME_FAQ=[("How much does septic tank pumping cost?",f"Residential pumping starts at $399.99. {PRICE_COND} Call (239) 451-3261 to confirm for your tank."),RISER_QA,
 ("How often should I pump my septic tank?","The U.S. EPA recommends pumping most household tanks every 3 to 5 years, depending on tank size, household size and water use."),
 ("Do you pump grease traps?","Yes, for restaurants and commercial kitchens, one-time or on a recurring schedule."),
 ("Do you do septic repairs?","Yes. We look at the system first, then quote the repair. Call (239) 451-3261. Repair work is performed under Florida Certified Plumbing Contractor Raymond F. Dibble, License #CFC020332."),
 ("Do you replace drain fields?","Yes. We quote drain field replacement after inspecting the system. Call (239) 451-3261. The work is performed under FL Certified Plumbing Contractor Raymond F. Dibble, License #CFC020332."),
 ("Can I book online?","Yes, for routine pumping: send a request on ServiceM8 and we'll contact you to confirm a time. For a backup, call (239) 451-3261 day or night.")]
page("/","Septic Tank Pumping Southwest Florida | Bonita Springs, Estero, Fort Myers | Express Septic",
 "Owner-operated septic tank pumping in Southwest Florida: Bonita Springs, Estero, Naples, Fort Myers, Cape Coral & Lehigh Acres. Grease trap service too. Call (239) 451-3261.",
 "Septic tank pumping in Southwest Florida",
 sec(f'''<div class="svc"><div class="svch"><p class="eyebrow">What we do</p><h2 id="services">Septic pumping for homes. Grease traps for kitchens.</h2></div>
<ul class="svcl"><li><a href="/residential-septic-tank-pumping/"><b>Residential septic pumping</b><span>We find the lid, pump the tank and tell you what we saw.</span></a></li>
<li><a href="/commercial-grease-trap-service/"><b>Commercial grease trap service</b><span>For restaurants and commercial kitchens. One-time or recurring.</span></a></li>
<li><a href="/commercial-septic-tank-pumping/"><b>Commercial septic pumping</b><span>Offices, rentals, churches and other properties on septic.</span></a></li>
<li><a href="/septic-tank-riser-installation/"><b>Septic tank risers</b><span>Bring the lid up to ground level so future pump-outs don't need digging. 6-inch risers $299.99 each.</span></a></li>
<li><a href="/septic-repair/"><b>Septic repairs</b><span>We look at the system first, then quote the repair.</span></a></li>
<li><a href="/drain-field-replacement/"><b>Drain field replacement</b><span>Quoted after we inspect the system. The work is performed under FL Certified Plumbing Contractor Raymond F. Dibble, License #CFC020332.</span></a></li>
<li><a href="/septic-inspections/"><b>Septic inspections</b><span>For buyers, sellers and homeowners. Inspection with pump-out $549.99.</span></a></li></ul>
</div>''')+sec(PRICE_PANEL,"priceband")+sec(QUOTES,"quotes")+
 f'''<section class="truck"><figure class="tphoto">{SIDE.replace('sizes="(min-width:960px) 680px, 100vw"','sizes="100vw"').replace('<figure class="shot">','').replace('</figure>','')}</figure><div class="wrap tcopy"><p class="eyebrow">The truck</p><h2>4,200 gallons, split tank</h2><p>The tank is split in two: one side for septic, one side for grease, so the two never mix. Licensed &amp; insured · USDOT 6673233.</p></div></section>'''+
 sec(f'''<div class="owner">'''+CREW.replace('alt="Express Septic Tank Pumping crew with the 4,200-gallon vacuum truck"','alt="ORyan Atkinson, owner of Express Septic Tank Pumping (right, in the cap), with a crew member and the Express truck"').replace('sizes="(min-width:960px) 680px, 100vw"','sizes="(min-width:960px) 600px, 100vw"').replace("</figure>","<figcaption>ORyan Atkinson, owner (right, in the cap), with a crew member and the Express truck</figcaption></figure>")+f'''<div><p class="eyebrow">The owner</p><blockquote class="promise">When you call, you're talking to the person who runs the business.</blockquote><p>Express is owned and run by ORyan Atkinson, based in Estero. Licensed &amp; insured. Honest, reliable and fair: great customer service is our top priority.</p><p><a class="btn ghost" href="tel:{TEL}">Call ORyan · {PHONE}</a></p><p><a href="/about/">More about Express</a></p></div></div><div class="cred"><p class="eyebrow">Credentials</p><h2>Licensed &amp; Experienced</h2><p>{LICENSE_BODY}</p><p class="crev"><a class="txtlink" href="{REVIEWS_READ}" rel="noopener">Read our Google reviews</a></p></div>''',"warm")+
 sec("""<div class="workhead"><p class="eyebrow">Recent work</p><h2>Jobs from this month</h2><p>Two recent septic pump-outs from our crew. Customer addresses and names are never shown.</p></div><ul class="workgrid"><li class="workcard"><p class="jdate">November 13, 2026 · Lehigh Acres · night visit</p><h3>Pump-out through an existing riser</h3><p>The tank already had a riser, so no digging was needed. We pumped the tank through the riser; the baffle was visible during the pump-out.</p><a class="txtlink" href="/completed-jobs/#lehigh-acres-2026-11-13">See this job</a></li><li class="workcard"><p class="jdate">November 14, 2026 · Cape Coral</p><h3>Buried lids and effluent filter</h3><p>We dug up buried lids, exposed the inlet and outlet tees, and pulled and cleaned the effluent filter.</p><a class="txtlink" href="/completed-jobs/#cape-coral-2026-11-14">See this job</a></li></ul><p class="more"><a class="txtlink" href="/completed-jobs/">All completed jobs</a></p>""", "work")+
 sec(f'<div class="split"><div><p class="eyebrow">Service area</p><h2>Lee, Collier &amp; Charlotte County</h2><p>Based in Estero, between Bonita Springs and Fort Myers. We also cover LaBelle in Hendry County.</p><p><a href="/service-area/">See every area we serve</a></p></div><div>{city_list}</div></div>',"area")+
 sec(REQUEST,"bookband")+sec("<p class='eyebrow'>FAQ</p><h2>Common questions</h2>"+"".join(f"<h3>{q}</h3><p>{a}</p>" for q,a in HOME_FAQ)+"<p><a href='/faq/'>More septic questions</a></p>","hfaq"),hero=HERO,extra=faq_ld(HOME_FAQ))
RES_EXTRA=("<h2>What happens during a visit</h2>"+LIDS+"<ol><li><strong>We locate the tank.</strong> We find the tank and its lid or access port. If the lid is buried, we dig to reach it: $100, plus $50 for each additional hour.</li><li><strong>We pump it out.</strong> The truck pumps the liquid, sludge and scum out of the tank.</li><li><strong>We tell you what we saw.</strong> You'll hear about anything that looks like it needs attention.</li></ol>"
 "<h2>How to prepare</h2><ul><li>If you know where the lid is, mark it or tell us when you call.</li><li>Make sure the truck can get close: clear the driveway and keep vehicles off the drain field.</li><li>Keep pets inside and unlock any gates.</li><li>Have your last pumping date handy if you know it.</li></ul>"
 "<h2>What affects the price</h2><ul><li>Tank size and how full it is</li><li>Access: how far the truck has to reach and whether the lid is buried and needs locating or digging</li><li>Location within our service area</li><li>After-hours pumping: $599.99</li></ul>"
 "<div class='price-slot'><p class='pp'>Residential septic pumping starting at $399.99</p><p>Your final quote depends on tank size, tank access, and whether the lid needs locating or digging. After-hours pumping is $599.99. Call to confirm for your tank.</p></div>"
 "<p>Call <a href='tel:"+TEL+"'>"+PHONE+"</a> to confirm pricing for your tank.</p>")
EXTRA["residential-septic-tank-pumping"]="<div class='price-slot'><p class='pp'>Residential septic pumping starting at $399.99</p><p>Your final quote depends on tank size, tank access, and whether the lid needs locating or digging. After-hours pumping is $599.99. Call to confirm for your tank.</p></div>"+RES_EXTRA+EXTRA.get("residential-septic-tank-pumping","")
for s in SERVICES:
  body=photo(s[0],s[1]+" job photo")+VAL+"".join(f"<p>{p}</p>" for p in s[4])+EXTRA.get(s[0],"")+("" if s[0] in ("septic-tank-riser-installation","residential-septic-tank-pumping","septic-inspections") else "<h2>Pricing</h2><p>Call for a quote — <a href='tel:"+TEL+"'>"+PHONE+"</a>.</p>")+"<h2>Service Areas</h2>"+city_list+"<h2>Other Services</h2>"+svc_list
  page(f"/{s[0]}/",s[2],s[3],s[1]+" in Southwest Florida",body,{"@context":"https://schema.org","@type":"Service","name":s[1],"serviceType":s[1],"url":f"{BASE}/{s[0]}/","provider":PROV,"areaServed":[{"@type":"City","name":c+", FL"} for c in CITIES_ALL],**({"offers":{"@type":"Offer","name":"6-inch septic tank riser, installed (each)","price":299.99,"priceCurrency":"USD"}} if s[0]=="septic-tank-riser-installation" else {"offers":{"@type":"Offer","priceSpecification":{"@type":"PriceSpecification","minPrice":399.99,"priceCurrency":"USD"}}} if s[0]=="residential-septic-tank-pumping" else {"offers":{"@type":"Offer","name":"Septic inspection with pump-out","price":549.99,"priceCurrency":"USD"}} if s[0]=="septic-inspections" else {"offers":{"@type":"Offer","description":"Quoted after we inspect the system"}} if s[0]=="drain-field-replacement" else {})})
for c,(county,a,b) in CITY.items():
  if c in CITY_PLUS: city_plus_page(c,county,a,b); continue
  near=[x for x in CITIES_ALL if x!=c]
  body=(photo(slug(c),f"Septic tank pumping job in {c}, FL")+VAL+f"<p>Need septic tank pumping in {c}, FL? Express Septic Tank Pumping serves homes and businesses in {c} and across {county}. {a}</p><p>{b}</p>"
   f"<p class='emerg'><strong>Septic emergency in {c}?</strong> "+"Night or day, we\'re available for emergencies. For routine service, we can often make it same day when possible. Call <a href='tel:"+TEL+"'>"+PHONE+"</a>.</p>"
   +CITY_NOTES.get(c,"")+(f"<p><strong>Recent work:</strong> we've done septic tank pumping jobs in {c} recently.</p>" if c in SERVED_RECENTLY else "")+
   f"<h2>Septic Tank Cleaning {c}</h2><p>Septic tank cleaning in {c} removes the sludge and scum that build up over time and helps protect your drain field.</p><h2>Septic Service in {c}, FL</h2><p>For septic service in {c}, FL, tap to call, or book routine pumping online.</p>"
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
CREW_ABOUT=CREW.replace('alt="Express Septic Tank Pumping crew with the 4,200-gallon vacuum truck"','alt="ORyan Atkinson, owner of Express Septic Tank Pumping (right, in the cap), with a crew member and the 4,200-gallon truck"').replace("</figure>","<figcaption>ORyan Atkinson, owner (right, in the cap), with a crew member</figcaption></figure>")
page("/about/","About Express Septic Tank Pumping | Honest, Reliable Septic Service","Express Septic Tank Pumping is an Estero-based septic company built on honesty, reliability, fair rates and great customer service. Call (239) 451-3261.","About Express Septic Tank Pumping",
 CREW_ABOUT+"<p>Express Septic Tank Pumping is a local septic service company based in Estero, Florida, serving homes and businesses across Lee and Collier County.</p><h2>What We Stand For</h2><ul><li><strong>Honesty.</strong> Upfront pricing and straight answers about your system — no surprises.</li><li><strong>Reliability.</strong> We show up on time and do the job right.</li><li><strong>Fairness.</strong> Fair rates for the work you actually need.</li><li><strong>Customer service.</strong> Treating customers right is our top priority.</li></ul><h2>Licensed &amp; Experienced</h2><p>"+LICENSE_BODY+"</p><h2>Our Services</h2>"+svc_list+"<p>See <a href='/how-it-works/'>how it works</a>.</p>")
page("/commercial-grease-trap-service/","Commercial Grease Trap Service & Pumping | Southwest Florida | Express Septic",
 "Grease trap pumping for restaurants and commercial kitchens in Lee & Collier County. One-time or recurring service from Express Septic. Call (239) 451-3261.",
 "Commercial grease trap service",
 REAR+"<p>Restaurants and commercial kitchens need their grease traps pumped before fats, oils and grease build up and cause backups, odors or problems with the drain line. Express pumps grease traps for businesses across Southwest Florida.</p>"
 +SIDE+"<p>Our 4,200-gallon truck has a split tank, one side for septic and one side for grease, so grease trap loads and septic loads never mix.</p>"
 "<h2>One-time or recurring</h2><p>Some businesses call us when a trap is full. Most are better off on a recurring schedule based on how much cooking they do and the size of the trap. Tell us about your kitchen and we'll talk through how often makes sense.</p>"
 "<p><a class='btn primary' href='tel:"+TEL+"'>Call about recurring service · "+PHONE+"</a></p>"
 "<h2>Signs your grease trap needs service</h2><ul><li>Slow sinks or floor drains in the kitchen</li><li>Grease or odors around the trap lid</li><li>It's been longer than your usual schedule since the last pump-out</li></ul>"
 "<h2>What to have ready when you call</h2><ul><li>Business name and address</li><li>Where the trap is and how it's accessed</li><li>Trap size, if you know it</li><li>When it was last pumped</li></ul>"
 "<h2>Other services</h2>"+svc_list,
 {"@context":"https://schema.org","@type":"Service","name":"Commercial Grease Trap Service","serviceType":"Grease trap pumping","description":"Grease trap pumping for restaurants and commercial kitchens, one-time or on a recurring schedule.","url":BASE+"/commercial-grease-trap-service/","audience":{"@type":"BusinessAudience","name":"Restaurants and commercial kitchens"},"provider":PROV,"areaServed":[{"@type":"City","name":c+", FL"} for c in CITIES_ALL]})
counties={}
for c,(co,_,_) in CITY.items(): counties.setdefault(co,[]).append(c)
page("/service-area/","Septic Pumping Service Area | Lee, Collier, Charlotte & Hendry | Express Septic",
 "Express Septic Tank Pumping serves Bonita Springs, Estero, Fort Myers, Cape Coral, Lehigh Acres, Naples and more. Check your ZIP or call (239) 451-3261.",
 "Where we work",
 JOB+"<p>Express is based in Estero, between Bonita Springs and Fort Myers, and works across Lee, Collier and Charlotte County, plus LaBelle in Hendry County. Check your ZIP below, or call to confirm service at your address.</p>"+ZIPBOX+ROUTE+
 "".join(f"<h2>{co}</h2><ul class='cities'>"+"".join(f'<li><a href="/{slug(c)}/">{c}</a></li>' for c in cs)+"</ul>" for co,cs in counties.items()))
page("/contact/","Contact & Request Septic Service | Express Septic Tank Pumping",
 "Call Express Septic Tank Pumping at (239) 451-3261, book online, or request septic pumping or grease trap service.",
 "Contact Express",
 f"<p>The fastest way to reach us is by phone: <a href='tel:{TEL}'>{PHONE}</a>. We're open 24 hours, 7 days a week. {AVAIL}</p><p>Email: <a href='mailto:{EMAIL}'>{EMAIL}</a></p>"+REQUEST+
 "<h2>Mailing address</h2><p>Express Septic Tank Pumping LLC<br>23357 Olde Meadowbrook Circle, Estero, FL 34134</p>")
faqhtml="".join(f"<h2>{q}</h2><p>{a}</p>" for q,a in FAQ)
page("/faq/","Septic Tank FAQ | How Often to Pump, Cost & Signs | Express Septic","Answers to common septic tank questions: how often to pump, signs your tank is full, cost and what areas Express Septic Tank Pumping serves.","Septic Tank Pumping FAQ",faqhtml,
 {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]})
page("/privacy/","Privacy Policy | Express Septic Tank Pumping","Privacy policy for Express Septic Tank Pumping website visitors and customers.","Privacy Policy",
 f"<p>Express Septic Tank Pumping respects your privacy. Information you give us by phone, through our online booking provider (ServiceM8) or by text is used only to schedule and provide service, send quotes and invoices, and communicate with you about your job.</p><p>We do not sell your personal information. Mobile phone numbers and SMS consent are not shared with third parties for marketing purposes.</p><p>This site does not use advertising trackers. Online booking is handled by ServiceM8 under its own privacy policy.</p><p>Questions? Call {PHONE}.</p>")
page("/terms/","Terms of Service | Express Septic Tank Pumping","Terms of service for the Express Septic Tank Pumping website and services.","Terms of Service",
 f"<p>By using this website you agree to these terms. Content is general information about septic systems and is not a substitute for an on-site evaluation.</p><p>Quotes are provided after discussing your property and needs. Scheduling is subject to availability.</p><p>If you opt in to text messages, message and data rates may apply. Reply STOP to opt out or HELP for help.</p><p>Contact: {NAME}, 23357 Olde Meadowbrook Circle, Estero, FL 34134, {PHONE}.</p>")
page("/accessibility/","Accessibility Statement | Express Septic Tank Pumping","Accessibility information for the Express Septic Tank Pumping website, and how to reach us if you need help using it.","Accessibility",
 "<p>Express Septic Tank Pumping wants this website to be usable by all customers, including people who use assistive technology or browse on a phone.</p>"
 "<p>Pages include a skip-to-content link, visible keyboard focus, text that can be resized, and buttons large enough to tap. We keep writing in plain language and put the phone number on every page so you can call if something on the site gets in the way.</p>"
 "<p>If you have trouble using this website, call <a href='tel:"+TEL+"'>"+PHONE+"</a> or email <a href='mailto:"+EMAIL+"'>"+EMAIL+"</a> and we will help.</p>")

page("/completed-jobs/","Completed Septic Jobs in Southwest Florida | Express Septic Tank Pumping","Recent septic jobs by Express Septic Tank Pumping in Lehigh Acres, Cape Coral and Bonita Springs: buried lids, risers, effluent filters and pump-outs.","Completed jobs",
 "<p>Recent jobs from our crew, with the city, date, what we found and what we did. Customer addresses and names are never shown.</p><p>We've also done septic tank pumping jobs recently in Fort Myers, North Fort Myers and Naples.</p>"+
 "".join(f"<section class='job' id='{j['id']}'><h2>{j['city']}: {j['title']}</h2><p class='jdate'>{j['date']}</p><p><strong>What we found:</strong> {j['found']}</p><p><strong>What we did:</strong> {j['done']}</p><p><a href='/{slug(j['city'])}/'>Septic service in {j['city']}</a></p></section>" for j in JOBS)+
 "<p>Need your tank pumped? Call <a href='tel:"+TEL+"'>"+PHONE+"</a> or see <a href='/residential-septic-tank-pumping/'>residential septic pumping</a>.</p>",
 {"@context":"https://schema.org","@type":"ItemList","name":"Completed septic jobs","itemListElement":[{"@type":"ListItem","position":k+1,"url":f"{BASE}/completed-jobs/#{j['id']}","name":f"{j['city']}: {j['title']}"} for k,j in enumerate(JOBS)]})
ROBOTS["/404/"]='<meta name="robots" content="noindex">'
page("/404/","Page not found | Express Septic Tank Pumping","Page not found.","Page not found","<p>That page doesn't exist. Try the <a href='/'>home page</a>, <a href='/service-area/'>service area</a>, or call <a href='tel:"+TEL+"'>"+PHONE+"</a>.</p>")
PAGES.remove("/404/")
h=open("404/index.html").read().replace('<link rel="canonical" href="'+BASE+'/404/">','').replace('<meta property="og:url" content="'+BASE+'/404/">','').replace('href="../','href="/').replace('src="../','src="/').replace(', ../',', /').replace('srcset="../','srcset="/').replace("href='../","href='/")
open("404.html","w").write(h); shutil.rmtree("404")
shutil.copy("src/styles.css","styles.css"); shutil.copy("src/site.js","site.js")
open("sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{BASE}{p}</loc></url>" for p in PAGES)+"</urlset>\n")
# Sitemap index: static pages + ServiceTechHub Project Showcase (served by functions/ once configured)
open("sitemap-index.xml","w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><sitemap><loc>{BASE}/sitemap.xml</loc></sitemap></sitemapindex>\n')
open("robots.txt","w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap-index.xml\nSitemap: {BASE}/sitemap.xml\n")
print("\n".join(PAGES))
# llms.txt: plain-text facts for AI assistants (same NAP and prices as the pages).
LL=[f"# {NAME}","",f"> Owner-operated septic tank pumping company based in Estero, Florida, serving Lee, Collier and Charlotte County plus LaBelle (Hendry County). Residential septic pumping starts at $399.99.","",
"## Contact",f"- Business: {NAME} LLC",f"- Address: 23357 Olde Meadowbrook Circle, Estero, FL 34134",f"- Phone: {PHONE}","- Hours: open 24 hours, 7 days a week",f"- Email: {EMAIL}",
f"- Online requests: {BOOK} (a request; the business contacts the customer to confirm a time)",f"- Google reviews: {REVIEWS_READ}","",
"## Services and prices",f"- [Residential septic tank pumping]({BASE}/residential-septic-tank-pumping/): from $399.99. {PRICE_COND}",
f"- [Septic tank riser installation]({BASE}/septic-tank-riser-installation/): 6-inch risers $299.99 each. A riser brings the tank lid up to ground level so future pump-outs don't need digging.",
"- Buried lid locating and digging: $100, plus $50 for each additional hour",
"- After-hours pumping: $599.99",
f"- [Commercial grease trap service]({BASE}/commercial-grease-trap-service/): restaurants and commercial kitchens, one-time or recurring. Call for a quote.",
f"- [Septic repair]({BASE}/septic-repair/): quoted after we look at the system. Repair work performed under Florida Certified Plumbing Contractor Raymond F. Dibble, License #CFC020332.",
f"- [Drain field replacement]({BASE}/drain-field-replacement/): quoted after we inspect the system. The work is performed under FL Certified Plumbing Contractor Raymond F. Dibble, License #CFC020332.",
f"- [Commercial septic tank pumping]({BASE}/commercial-septic-tank-pumping/): call for a quote.",f"- [Septic inspections]({BASE}/septic-inspections/): septic inspection with pump-out $549.99.","",
"## Credentials","- Work performed under Florida Certified Plumbing Contractor Raymond F. Dibble, License #CFC020332, licensed since 1981.","- USDOT 6673233. Truck: 4,200-gallon split tank, one side for septic and one for grease.","",
"## Main service-area pages"]+[f"- [{c}, FL]({BASE}/{slug(c)}/)" for c in CITY_PLUS]+[f"- [All areas]({BASE}/service-area/)","",
"## More",f"- [Completed jobs]({BASE}/completed-jobs/)",f"- [FAQ]({BASE}/faq/)",f"- [How often to pump]({BASE}/how-often-to-pump-septic-tank/)",f"- [About]({BASE}/about/)",""]
open("llms.txt","w").write("\n".join(LL))
