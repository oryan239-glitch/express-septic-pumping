#!/usr/bin/env python3
"""Build script: generates static pages at repo root from data in this file + src/styles.css."""
import json, os, shutil, re, html as htmllib
from datetime import date
TODAY=date.today().isoformat()
def plain(s):
  return re.sub(r'<[^>]+>','',s)
def crumbs_ld(items):
  return {'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':i,'name':n,'item':u} for i,(n,u) in enumerate(items,1)]}
def crumbs_html(items):
  out=[]
  for i,(name,url) in enumerate(items):
    safe=htmllib.escape(name)
    if i==len(items)-1: out.append(f'<li aria-current="page"><span>{safe}</span></li>')
    else: out.append(f'<li><a href="{url}">{safe}</a></li>')
  return '<nav class="crumbs" aria-label="Breadcrumb"><ol>'+''.join(out)+'</ol></nav>'
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
 ("lift-station-pumping","Lift Station Pumping","Lift Station Pumping in Lee & Collier County | Express Septic","Express Septic Tank Pumping pumps lift stations in Estero and across Southwest Florida. Work is quoted after we inspect the system. Call (239) 451-3261.",
  ["Express Septic Tank Pumping pumps lift stations for homes and businesses in Estero and across Lee, Collier, and Charlotte County, plus LaBelle. Lift station work is quoted after we inspect the system. Call (239) 451-3261."]),
 ("grease-trap-pumping","Grease Trap & Interceptor Pumping","Grease Trap & Interceptor Pumping in Lee, Collier & Charlotte County | Express Septic","Grease trap and interceptor pumping for restaurants and food service in Fort Myers, Cape Coral, Bonita Springs, Naples, Estero and across Lee, Collier and Charlotte County. $695 for a 1,000-gallon grease trap or interceptor; other sizes are quoted. Call (239) 451-3261.",
  ["Express Septic Tank Pumping pumps grease traps and interceptors for restaurants and food service in Fort Myers, Cape Coral, Bonita Springs, Naples, Estero and across Lee, Collier, and Charlotte County, plus LaBelle. We pump in-ground grease interceptors and indoor traps. $695 for a 1,000-gallon grease trap or interceptor; other sizes are quoted. We can set up a recurring pump-out schedule. Call (239) 451-3261.",
   "Our 4,200-gallon truck has a split tank, one side for septic and one side for grease, so grease trap loads and septic loads never mix."]),
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
CITY['Captiva']=('Lee County', 'Captiva is a barrier-island community in Lee County, north of Sanibel, reached from the mainland by the Sanibel Causeway and from Sanibel by the Blind Pass Bridge.', 'Island properties on Captiva need careful septic maintenance to protect the surrounding waters.')
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
"Sanibel":"<p>Captiva is the next island north of Sanibel, across the Blind Pass Bridge. See our page for <a href='/septic-tank-pumping-captiva-fl/'>septic tank pumping on Captiva</a>.</p>",
"Captiva":"<h2>Septic tank pumping on Captiva Island</h2><p>Captiva is a barrier-island community in Lee County, just north of <a href='/septic-tank-pumping-sanibel-fl/'>Sanibel</a>. From the mainland you reach Captiva by the Sanibel Causeway, then the Blind Pass Bridge from Sanibel. This page is for Captiva Island, the island connected by road from Sanibel.</p>",
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
("Do you pump grease traps?","Yes. We pump <a href='/grease-trap-pumping/'>grease traps and interceptors</a> for restaurants and food service, including in-ground interceptors and indoor traps, one-time or on a recurring schedule. $695 for a 1,000-gallon grease trap or interceptor; other sizes are quoted. Call (239) 451-3261."),
("Do you pump grease interceptors?","Yes. We pump in-ground grease interceptors and indoor traps for restaurants and food service. $695 for a 1,000-gallon grease trap or interceptor; other sizes are quoted. Call (239) 451-3261. See <a href='/grease-trap-pumping/'>grease trap and interceptor pumping</a>."),
("How much does grease trap pumping cost?","$695 for a 1,000-gallon grease trap or interceptor; other sizes are quoted. Call (239) 451-3261."),
("How often does a grease interceptor need pumping in Lee County?","<a href='https://www.leegov.com/bocc/Ordinances/14-24.pdf' rel='noopener'>Lee County Ordinance 14-24</a> requires grease interceptors to be fully pumped at least every 90 calendar days. Indoor grease traps must be cleaned at least weekly or whenever grease and solids exceed 20% of the unit volume. We can set up a recurring pump-out schedule. Call (239) 451-3261."),
("Do you do septic repairs?","Yes. We look at the system first, then quote the repair. Call (239) 451-3261. Repair work is performed under Florida Certified Plumbing Contractor Raymond F. Dibble, License #CFC020332."),
("Do you replace drain fields?","Yes. We quote drain field replacement after inspecting the system. Call (239) 451-3261. The work is performed under FL Certified Plumbing Contractor Raymond F. Dibble, License #CFC020332."),
("Do you pump lift stations?","Yes. <a href='/lift-station-pumping/'>Lift station work</a> is quoted after we inspect the system. Call (239) 451-3261."),
("Do you do septic inspections for real estate?","Yes. We offer septic inspections for buyers, sellers and homeowners. A septic inspection with pump-out is $549.99."),
("What areas do you serve?","Estero, Bonita Springs, Naples, North Naples, Fort Myers, Cape Coral, Lehigh Acres, San Carlos Park and nearby areas of Lee and Collier County."),
("What shouldn't go into a septic system?","Avoid grease, wipes (even 'flushable'), paper towels, feminine products, harsh chemicals and medications. They can clog the system or harm the bacteria that break down waste."),
("What is a septic tank riser?","A riser is an extension installed on top of the tank's access opening that brings the lid up to ground level, so future pump-outs don't need digging to find and open the tank. Express installs 6-inch risers for $299.99 each. Call (239) 451-3261 to confirm what your tank needs."),
("How much does it cost to find and dig up a buried lid?","Locating and digging up a buried lid is $100, plus $50 for each additional hour. A riser avoids digging on future visits."),
("How often should I clean my septic effluent filter?","If your tank has an effluent filter, it should be checked and cleaned at every pump-out and whenever drains slow. Express can advise on a schedule for your system. See <a href='/septic-filter-care/'>effluent filter care</a>. Call (239) 451-3261."),
("Where is the septic effluent filter?","The effluent filter is in the outlet side of the tank, under the lid. A <a href='/septic-tank-riser-installation/'>6-inch riser</a> ($299.99 each) brings the lid up to ground level so the filter is easier to reach. Call (239) 451-3261."),
("What happens if the effluent filter is dirty?","A dirty filter can cause backups or slow drains, and wastewater can be pushed back into the house. Express cleans your filter at no charge on pump-outs and can show you how to keep it clean. See <a href='/septic-filter-care/'>effluent filter care</a>."),
("How does soil bacteria protect a drain field?","Healthy bacteria in the soil break down effluent after it leaves the tank. Harsh chemicals, solids and grease overload can hurt that process. See <a href='/septic-bacteria-drain-field/'>why good bacteria protect your septic tank and drain field</a> and <a href='/drain-field-replacement/'>drain field replacement</a>."),
("Do you clean the effluent filter when you pump?","Yes. We clean your filter at no charge on pump-outs and show you how to keep it clean."),
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
   "makesOffer":[({"@type":"Offer","itemOffered":{"@type":"Service","name":s[1],"url":f"{BASE}/{s[0]}/"},"priceSpecification":{"@type":"PriceSpecification","minPrice":399.99,"priceCurrency":"USD"}} if s[0]=="residential-septic-tank-pumping" else {"@type":"Offer","itemOffered":{"@type":"Service","name":s[1],"url":f"{BASE}/{s[0]}/"}}) for s in SERVICES if s[0] not in ("septic-tank-riser-installation","septic-inspections","septic-repair","drain-field-replacement","lift-station-pumping","grease-trap-pumping")]
     +[{"@type":"Offer","itemOffered":{"@type":"Service","name":"Septic Repair","url":BASE+"/septic-repair/","description":"Quoted after we look at the system"}},
        {"@type":"Offer","itemOffered":{"@type":"Service","name":"Drain Field Replacement","url":BASE+"/drain-field-replacement/","description":"Quoted after we inspect the system"}},
        {"@type":"Offer","itemOffered":{"@type":"Service","name":"Lift Station Pumping","url":BASE+"/lift-station-pumping/","description":"Quoted after we inspect the system"}},
        {"@type":"Offer","itemOffered":{"@type":"Service","name":"Grease Trap & Interceptor Pumping","url":BASE+"/grease-trap-pumping/"},"price":695,"priceCurrency":"USD","description":"1,000 gallons"}]
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
NAV="".join(f'<a href="/{s[0]}/">{htmllib.escape(s[1])}</a>' for s in SERVICES)+'<a href="/commercial-grease-trap-service/">Commercial Grease Trap Service</a>'
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
def page(path,title,desc,h1,body,extra=None,hero=None,lead="",trail=None,canonical=None):
  foot="".join(f'<a href="/{slug(c)}/">{c}</a>' for c in CITIES_ALL[:12])+'<a href="/service-area/">All areas</a>'
  H1A=' data-sth-field="headline"' if path=="/" else ""
  if not hero: body=f'<div class="wrap prose">{body}</div>'
  crumb=(crumbs_html(trail) if trail else "")
  canon=canonical or (BASE+path)
  et,ed,eh=htmllib.escape(title,True),htmllib.escape(desc,True),htmllib.escape(h1)
  top=hero if hero else f'<section class="phead"><div class="wrap">{crumb}<p class="eyebrow">Express Septic Tank Pumping</p><h1>{eh}</h1>{lead}{CTA}</div></section>'
  if hero: top=top.replace("<h1>",f"<h1{H1A}>",1)
  doc=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-ESN48M0VEZ"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-ESN48M0VEZ');</script>
<title>{et}</title><meta name="description" content="{ed}"><link rel="canonical" href="{canon}">{ROBOTS.get(path,"")}<meta name="theme-color" content="#0f1b2d">
<meta property="og:title" content="{et}"><meta property="og:description" content="{ed}"><meta property="og:url" content="{BASE}{path}"><meta property="og:type" content="website"><meta property="og:image" content="{BASE}/assets/img/truck-wide-1536.webp">
{'<link rel="preload" as="image" href="/assets/img/truck-wide-1024.webp" imagesrcset="/assets/img/truck-wide-640.webp 640w, /assets/img/truck-wide-1024.webp 1024w, /assets/img/truck-wide-1536.webp 1536w" imagesizes="100vw">' if hero else ''}
<link rel="stylesheet" href="/styles.css">{schema(extra)}<script src="/site.js" defer></script></head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap bar"><a class="logo" href="/" aria-label="{NAME} home"><span class="mark">EXPRESS</span><span class="sub">Septic Tank Pumping</span></a>
<nav aria-label="Primary">{NAVL}</nav><a class="hcall" href="tel:{TEL}"><span class="lbl">Call</span> {PHONE}</a>
<details class="menu"><summary aria-label="Open menu">Menu</summary><nav aria-label="Mobile">{NAVL}<a href="/contact/">Contact</a><a href="tel:{TEL}">Call {PHONE}</a></nav></details></div></header>
<main id="main">{top}<div class="body">{body}</div>{REV}<section class="band closer"><div class="wrap"><h2>Talk to Express about your tank</h2><p>{AVAIL}</p>{CTA}</div></section></main>
<footer id="contact" class="foot"><div class="wrap fgrid"><div><p class="mark">EXPRESS</p><p>{NAME} LLC<br>23357 Olde Meadowbrook Circle, Estero, FL 34134<br><a href="tel:{TEL}">{PHONE}</a><br><a data-sth-field="email" href="{"mailto:"+EMAIL if EMAIL else "/contact/"}">{EMAIL or "Send a request"}</a></p><p>Open 24 hours, 7 days a week.</p><p>Owner-operated. Licensed &amp; insured. We come to you.</p><p class="dot">USDOT 6673233</p><p class="license-foot">{LICENSE_FOOT}</p></div>
<div><p class="fh">Services</p>{NAV}</div><div><p class="fh">Areas</p>{foot}</div><div><p class="fh">Info</p><a href="/">Home</a><a href="/how-it-works/">How it works</a><a href="/septic-system-maintenance/">Septic maintenance</a><a href="/septic-filter-care/">Filter care</a><a href="/septic-bacteria-drain-field/">Good bacteria</a><a href="/first-time-septic-owner/">First-time septic guide</a><a href="/septic-maintenance-checklist/">Maintenance checklist</a><a href="/how-often-to-pump-septic-tank/">How often to pump</a><a href="/emergency-septic-backup/">Emergency backup</a><a href="/hurricane-and-flood-septic-prep/">Hurricane and flood prep</a><a href="/completed-jobs/">Completed jobs</a><a href="/about/">About</a><a href="/faq/">FAQ</a><a href="/contact/">Contact</a><a href="/accessibility/">Accessibility</a><a href="/privacy/">Privacy</a><a href="/terms/">Terms</a></div></div></footer>
<div class="mbar" role="region" aria-label="Quick contact"><a class="btn primary" href="tel:{TEL}">Call · {PHONE}</a><a class="btn ghost" href="/contact/#book">Book</a></div></body></html>'''
  doc=doc.replace("<div class=\"body\"></div>","")
  if 'id="book"' in body: doc=doc.replace('href="/contact/#book"','href="#book"')
  pre="../"*(path.count("/")-1) or "./"
  doc=doc.replace('href="/','href="'+pre).replace('src="/','src="'+pre).replace(', /assets',', '+pre+'assets').replace('srcset="/','srcset="'+pre).replace("href='/","href='"+pre).replace('imagesrcset="'+pre,'imagesrcset="'+pre)
  d="."+path; os.makedirs(d,exist_ok=True); open(d+"index.html","w").write(doc); PAGES.append(path)
def sec(inner,cls=""): return f'<section class="sec {cls}"><div class="wrap">{inner}</div></section>'
svc_list="<ul class='rows'>"+"".join(f'<li><a href="/{s[0]}/">{htmllib.escape(s[1])}</a></li>' for s in SERVICES)+"<li><a href='/commercial-grease-trap-service/'>Commercial Grease Trap Service</a></li></ul>"
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
 title="Septic Tank Pumping in Bonita Springs, FL | Septic Tank Cleaning | Express Septic",
 desc="Septic tank pumping and septic tank cleaning in Bonita Springs, FL, from nearby Estero. Residential pumping starts at $399.99 (standard 1–3 bed). Open 24 hours. Call (239) 451-3261.",
 h1="Septic Tank Pumping in Bonita Springs, FL",
 near=["Estero","North Naples","Naples","San Carlos Park","Three Oaks","Corkscrew"],
 trail=[("Home","/"),("Service area","/service-area/"),("Bonita Springs","/septic-tank-pumping-bonita-springs-fl/")],
 price_a=f"Residential pumping with Express starts at $399.99 (standard 1–3 bed). {PRICE_COND} Call (239) 451-3261 to confirm the price for your tank.",
 quick=(f"<div class='quick'><p class='eyebrow'>Quick answer</p><p><strong>Express Septic Tank Pumping provides septic tank pumping and septic tank cleaning in Bonita Springs, FL.</strong> Bonita Springs is in southern Lee County, bordering Estero to the north and Collier County to the south. We are based in neighboring Estero. Residential pumping starts at $399.99 (standard 1–3 bed). We are open 24 hours, 7 days a week. For a backup or after-hours emergency, call <a href='tel:{TEL}'>{PHONE}</a>; after-hours pumping is $599.99. For routine pumping, request a time online and we'll contact you to confirm.</p>"
  "<ul class='facts'><li><b>Services:</b> residential and commercial septic pumping, septic repairs, drain field replacement, <a href='/lift-station-pumping/'>lift station pumping</a>, septic tank risers, <a href='/grease-trap-pumping/'>grease trap and interceptor pumping</a>, septic inspections, <a href='/septic-filter-care/'>effluent filter care</a></li><li><b>Price:</b> residential pumping starts at $399.99 (standard 1–3 bed); after-hours pumping $599.99; septic inspection with pump-out $549.99; 6-inch risers $299.99 each; buried-lid locating/digging $100, plus $50 for each additional hour</li><li><b>Hours:</b> open 24 hours, 7 days a week</li><li><b>Based in:</b> Estero, serving Bonita Springs and the rest of Lee County</li><li><b>Licensing:</b> work performed under FL Certified Plumbing Contractor Raymond F. Dibble, #CFC020332</li></ul></div>"),
 local=f"<h2>Do you pump septic tanks in Bonita Springs?</h2><p>Yes. Express pumps septic tanks for homes and businesses in Bonita Springs, and septic tank cleaning here is the same service: we empty the sludge and scum from the tank so it does not overflow into the drain field.</p><h2>Where in Bonita Springs do you work?</h2><p>Express is based in neighboring Estero, just north of Bonita Springs along US-41 and I-75. We serve Bonita Springs neighborhoods on both sides of I-75, including older parts of the city and larger lots east of I-75, and we also serve nearby <a href=\"/septic-tank-pumping-estero-fl/\">Estero</a>, <a href=\"/septic-tank-pumping-north-naples-fl/\">North Naples</a>, <a href=\"/septic-tank-pumping-three-oaks-fl/\">Three Oaks</a> and <a href=\"/septic-tank-pumping-san-carlos-park-fl/\">San Carlos Park</a>.</p><h2>Is Bonita Springs switching from septic to sewer?</h2><p>In some neighborhoods, yes, over time. Central sewer in Bonita Springs is provided by Bonita Springs Utilities (BSU). The City and BSU are converting some neighborhoods from septic to sewer, including Sun Village Estates and the Lake of Sans Souci, partly to cut nutrients reaching groundwater and the Imperial River ({S('bsu')}). Once sewer is available, connection is required within one year ({S('bsufaq')}).</p><p>Many other Bonita Springs homes, especially older neighborhoods and larger lots east of I-75, still use septic tanks that need regular pumping. Until your home is connected, keep the tank pumped on schedule.</p><h2>Do you offer 24-hour septic pumping in Bonita Springs?</h2><p>Yes. Express is open 24 hours, 7 days a week. For a backup, call <a href='tel:{TEL}'>{PHONE}</a> day or night and stop running water until we arrive. After-hours pumping is $599.99.</p>",
 sewer_q="My Bonita Springs neighborhood is getting sewer. Do I still need pumping?",
 sewer_a="Until your home is connected, yes. Your septic tank keeps working until the switch, so keep it pumped. Bonita Springs Utilities handles the sewer connection, and connection is required within one year once sewer is available.",
 faq_extra=[
  ("Do you do septic tank cleaning in Bonita Springs?","Yes. Septic tank cleaning and septic tank pumping are the same service: we empty the tank of sludge and scum. Residential pumping starts at $399.99 (standard 1–3 bed). Call (239) 451-3261."),
  ("Do you offer 24-hour emergency pumping in Bonita Springs?","Yes. Express is open 24 hours, 7 days a week. For a backup, call (239) 451-3261 day or night. After-hours pumping is $599.99."),
  ("Do you clean the effluent filter when you pump a Bonita Springs tank?","Yes. We clean your filter at no charge on pump-outs and can show you how to keep it clean. See <a href='/septic-filter-care/'>effluent filter care</a>.")
 ],
 svc_enriched=True,
 srcs=["bsu","bsufaq","epa"]),
"Fort Myers":dict(
 title="Septic Tank Pumping in Fort Myers, FL | Septic Tank Cleaning | Express Septic",
 desc="Septic tank pumping and septic tank cleaning in Fort Myers, FL, including unincorporated Lee County areas with a Fort Myers address. Residential pumping starts at $399.99 (standard 1–3 bed). Open 24 hours. Call (239) 451-3261.",
 h1="Septic Tank Pumping in Fort Myers, FL",
 near=["South Fort Myers","North Fort Myers","Tice","Fort Myers Shores","Lehigh Acres","Cape Coral"],
 trail=[("Home","/"),("Service area","/service-area/"),("Fort Myers","/septic-tank-pumping-fort-myers-fl/")],
 price_a=f"Residential pumping with Express starts at $399.99 (standard 1–3 bed). {PRICE_COND} Call (239) 451-3261 to confirm the price for your tank.",
 quick=(f"<div class='quick'><p class='eyebrow'>Quick answer</p><p><strong>Express Septic Tank Pumping provides septic tank pumping and septic tank cleaning in Fort Myers, FL.</strong> We serve homes and businesses in the city, the county seat of Lee County on the Caloosahatchee River, and in the unincorporated Lee County areas that use a Fort Myers address. Residential pumping starts at $399.99 (standard 1–3 bed). We are open 24 hours, 7 days a week. For a backup or after-hours emergency, call <a href='tel:{TEL}'>{PHONE}</a>; after-hours pumping is $599.99. For routine pumping, request a time online and we'll contact you to confirm.</p>"
  "<ul class='facts'><li><b>Services:</b> residential and commercial septic pumping, septic repairs, drain field replacement, <a href='/lift-station-pumping/'>lift station pumping</a>, septic tank risers, <a href='/grease-trap-pumping/'>grease trap and interceptor pumping</a>, septic inspections, <a href='/septic-filter-care/'>effluent filter care</a></li><li><b>Price:</b> residential pumping starts at $399.99 (standard 1–3 bed); after-hours pumping $599.99; septic inspection with pump-out $549.99; 6-inch risers $299.99 each; buried-lid locating/digging $100, plus $50 for each additional hour</li><li><b>Hours:</b> open 24 hours, 7 days a week</li><li><b>Based in:</b> Estero, serving Fort Myers and the rest of Lee County</li><li><b>Licensing:</b> work performed under FL Certified Plumbing Contractor Raymond F. Dibble, #CFC020332</li></ul></div>"),
 local=f"<h2>Do you pump septic tanks in Fort Myers?</h2><p>Yes. Express pumps septic tanks for homes and businesses in Fort Myers and the unincorporated areas around it. Septic tank cleaning in Fort Myers is the same service: we empty the sludge and scum from the tank so it does not overflow into the drain field.</p><h2>Which parts of Fort Myers do you serve?</h2><p>We serve Fort Myers and nearby communities, including <a href=\"/septic-tank-pumping-south-fort-myers-fl/\">South Fort Myers</a> (McGregor Boulevard, Iona, Cypress Lake and Villas), <a href=\"/septic-tank-pumping-tice-fl/\">Tice</a>, <a href=\"/septic-tank-pumping-fort-myers-shores-fl/\">Fort Myers Shores</a>, <a href=\"/septic-tank-pumping-gateway-fl/\">Gateway</a> and <a href=\"/septic-tank-pumping-buckingham-fl/\">Buckingham</a>. Across the Caloosahatchee River, see our page for <a href=\"/septic-tank-pumping-north-fort-myers-fl/\">North Fort Myers</a>. We also serve <a href=\"/septic-tank-pumping-cape-coral-fl/\">Cape Coral</a> and <a href=\"/septic-tank-pumping-lehigh-acres-fl/\">Lehigh Acres</a>.</p><h2>How do I know if my Fort Myers home is on septic?</h2><p>A Fort Myers mailing address can mean the city or unincorporated Lee County. The City of Fort Myers runs utilities inside city limits ({S('fmcity')}). Outside them, some areas are on Lee County Utilities ({S('lcu')}) and many homes still use septic tanks. Sewer service can change from one street to the next, especially in older neighborhoods. If you don't get a sewer bill from the city or Lee County Utilities, you likely have a septic tank.</p><h2>Do you offer 24-hour septic pumping in Fort Myers?</h2><p>Yes. Express is open 24 hours, 7 days a week. For a backup, call <a href='tel:{TEL}'>{PHONE}</a> day or night and stop running water until we arrive. After-hours pumping is $599.99.</p>",
 sewer_q="How do I know if my Fort Myers home has a septic tank?",
 sewer_a="Check your utility bills. If you don't pay a sewer charge to the City of Fort Myers or Lee County Utilities, your home most likely has a septic tank. Many homes in unincorporated areas with Fort Myers addresses are on septic.",
 faq_extra=[
  ("Do you do septic tank cleaning in Fort Myers?","Yes. Septic tank cleaning and septic tank pumping are the same service: we empty the tank of sludge and scum. Residential pumping starts at $399.99 (standard 1–3 bed). Call (239) 451-3261."),
  ("Do you offer 24-hour emergency pumping in Fort Myers?","Yes. Express is open 24 hours, 7 days a week. For a backup, call (239) 451-3261 day or night. After-hours pumping is $599.99."),
  ("Do you serve South Fort Myers, Tice and Fort Myers Shores?","Yes. We pump septic tanks in those communities and have pages for <a href='/septic-tank-pumping-south-fort-myers-fl/'>South Fort Myers</a>, <a href='/septic-tank-pumping-tice-fl/'>Tice</a> and <a href='/septic-tank-pumping-fort-myers-shores-fl/'>Fort Myers Shores</a>."),
  ("Do you clean the effluent filter when you pump a Fort Myers tank?","Yes. We clean your filter at no charge on pump-outs and can show you how to keep it clean. See <a href='/septic-filter-care/'>effluent filter care</a>.")
 ],
 svc_enriched=True,
 srcs=["fmcity","lcu","epa"]),
"Cape Coral":dict(
 title="Septic Tank Pumping in Cape Coral, FL | Septic Tank Cleaning | Express Septic",
 desc="Septic tank pumping and septic tank cleaning in Cape Coral, FL, including the North Cape. Residential pumping starts at $399.99 (standard 1–3 bed). Open 24 hours. Call (239) 451-3261.",
 h1="Septic Tank Pumping in Cape Coral, FL",
 near=["North Fort Myers","Fort Myers","Pine Island","South Fort Myers","Sanibel","Fort Myers Beach"],
 trail=[("Home","/"),("Service area","/service-area/"),("Cape Coral","/septic-tank-pumping-cape-coral-fl/")],
 price_a=f"Residential pumping with Express starts at $399.99 (standard 1–3 bed). {PRICE_COND} Call (239) 451-3261 to confirm the price for your tank.",
 quick=(f"<div class='quick'><p class='eyebrow'>Quick answer</p><p><strong>Express Septic Tank Pumping provides septic tank pumping and septic tank cleaning in Cape Coral, FL, including the North Cape.</strong> Cape Coral is in Lee County, across the Caloosahatchee River from Fort Myers. Residential pumping starts at $399.99 (standard 1–3 bed). We are open 24 hours, 7 days a week. For a backup or after-hours emergency, call <a href='tel:{TEL}'>{PHONE}</a>; after-hours pumping is $599.99. For routine pumping, request a time online and we'll contact you to confirm.</p>"
  "<ul class='facts'><li><b>Services:</b> residential and commercial septic pumping, septic repairs, drain field replacement, <a href='/lift-station-pumping/'>lift station pumping</a>, septic tank risers, <a href='/grease-trap-pumping/'>grease trap and interceptor pumping</a>, septic inspections, <a href='/septic-filter-care/'>effluent filter care</a></li><li><b>Price:</b> residential pumping starts at $399.99 (standard 1–3 bed); after-hours pumping $599.99; septic inspection with pump-out $549.99; 6-inch risers $299.99 each; buried-lid locating/digging $100, plus $50 for each additional hour</li><li><b>Hours:</b> open 24 hours, 7 days a week</li><li><b>Based in:</b> Estero, serving Cape Coral and the rest of Lee County</li><li><b>Licensing:</b> work performed under FL Certified Plumbing Contractor Raymond F. Dibble, #CFC020332</li></ul></div>"),
 local=f"<h2>Do you pump septic tanks in Cape Coral?</h2><p>Yes. Express pumps septic tanks for homes and businesses in Cape Coral, including the North Cape. Septic tank cleaning in Cape Coral is the same service: we empty the sludge and scum from the tank so it does not overflow into the drain field. Until a street is connected to city sewer, homes there still need regular pumping.</p><h2>Which parts of Cape Coral still use septic?</h2><p>Cape Coral began as a low-density community built on septic tanks and shallow wells. Through its Utilities Extension Project (UEP), the City has extended water and sewer to nearly all of Cape Coral south of Pine Island Road and is now working north ({S('uep')}). North 1 East construction is expected to finish around the end of 2027, with later North Cape phases still to come ({S('uepn1')}).</p><p>So many North Cape homes still rely on septic tanks. The City notes that failed septic effluent can flow into groundwater and canals ({S('uep')}), which matters on canal-front lots. We also serve nearby <a href=\"/septic-tank-pumping-north-fort-myers-fl/\">North Fort Myers</a>, <a href=\"/septic-tank-pumping-fort-myers-fl/\">Fort Myers</a> and <a href=\"/septic-tank-pumping-pine-island-fl/\">Pine Island</a>.</p><p>Questions about connecting to city utilities or septic tank abandonment go to the City's Customer Billing Services at (239) 242-3853 ({S('uepn1')}).</p><h2>Do you offer 24-hour septic pumping in Cape Coral?</h2><p>Yes. Express is open 24 hours, 7 days a week. For a backup, call <a href='tel:{TEL}'>{PHONE}</a> day or night and stop running water until we arrive. After-hours pumping is $599.99.</p>",
 sewer_q="My Cape Coral area is in the UEP. Do I still need septic pumping?",
 sewer_a="Until your home is connected to city sewer, yes. Your septic system keeps handling your wastewater until then. The City's Customer Billing Services, (239) 242-3853, handles connection and septic abandonment questions.",
 faq_extra=[
  ("Do you do septic tank cleaning in Cape Coral?","Yes. Septic tank cleaning and septic tank pumping are the same service: we empty the tank of sludge and scum. Residential pumping starts at $399.99 (standard 1–3 bed). Call (239) 451-3261."),
  ("Do you pump septic tanks in North Cape Coral?","Yes. Many North Cape homes still use septic tanks while the City's Utilities Extension Project works north of Pine Island Road. Call (239) 451-3261."),
  ("Do you offer 24-hour emergency pumping in Cape Coral?","Yes. Express is open 24 hours, 7 days a week. For a backup, call (239) 451-3261 day or night. After-hours pumping is $599.99."),
  ("Do you clean the effluent filter when you pump a Cape Coral tank?","Yes. We clean your filter at no charge on pump-outs and can show you how to keep it clean. See <a href='/septic-filter-care/'>effluent filter care</a>.")
 ],
 svc_enriched=True,
 srcs=["uep","uepn1","epa"]),
}
LID_ASK=("<h2>If your lid is buried</h2><p>Many tanks have lids buried under soil or grass. Locating and digging up a buried lid is $100, plus $50 for each additional hour. If you know where the lid is, mark it or tell us when you call.</p>"
 "<p>To skip digging next time, ask about a <a href='/septic-tank-riser-installation/'>6-inch riser</a> ($299.99 each). It brings the lid up to ground level.</p>")
RISER_QA=("What is a septic tank riser?","A riser is an extension installed on top of the tank's access opening. It brings the lid up to ground level, so future pump-outs don't need digging. Express installs 6-inch risers for $299.99 each. Call (239) 451-3261 to confirm what your tank needs.")
def city_faq(c,cp):
  price_a=cp.get("price_a") or f"Residential pumping with Express starts at $399.99. {PRICE_COND} Call (239) 451-3261 to confirm the price for your tank."
  return [(f"How much does septic tank pumping cost in {c}?",price_a),
   (cp["sewer_q"],cp["sewer_a"]),
   ("How often should I pump my septic tank?","The U.S. EPA recommends pumping most household tanks every 3 to 5 years. Tank size, household size and water use change that. Pumping before Florida's summer rainy season gives the drain field more room."),
   ("How much does it cost to find and dig up a buried lid?","Locating and digging up a buried lid is $100, plus $50 for each additional hour. A riser avoids digging on future visits."),
   RISER_QA,
   ("Do you do septic repairs?","Yes. We look at the system first, then quote the repair. Call (239) 451-3261. Repair work is performed under Florida Certified Plumbing Contractor Raymond F. Dibble, License #CFC020332."),
   (f"Do you pump grease traps in {c}?","Yes. We pump grease traps for restaurants and commercial kitchens, one-time or on a recurring schedule. Call (239) 451-3261 to set it up."),
   ("Can I book online?","Yes, for routine pumping. Send a request through our ServiceM8 booking page and we'll contact you to confirm a time. It isn't a confirmed appointment until we confirm. For a backup, call (239) 451-3261 day or night.")]
def faq_ld(items): return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":plain(a)}} for q,a in items]}
# Completed jobs: add only real, owner-approved jobs (city, service, month, what was done; never a street address).
# Example: JOBS.append(dict(city="Lehigh Acres", service="Residential septic tank pumping", month="2026-11", summary="..."))
# Owner-supplied jobs (Timemark-stamped photos, Nov 2026). Only what the photos show; no addresses, names or prices.
JOBS=[
 dict(id="lehigh-acres-2026-11-17",city="Lehigh Acres",date="November 17, 2026",title="Residential pump-out, system was backing up",
   found="The septic system was backing up.",done="Residential pump-out."),
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
def job_shots(j, limit=None):
  photos=list(j.get("photos") or [])
  if limit is not None: photos=photos[:limit]
  if not photos: return ""
  figs="".join(f"<figure class='jobshot'><img src='{p['src']}' srcset='{p.get('srcset',p['src'])}' sizes='(min-width:960px) 560px, 100vw' alt='{p['alt']}' width='{p.get('w',1200)}' height='{p.get('h',900)}' loading='lazy'>"+(f"<figcaption>{p['cap']}</figcaption>" if p.get('cap') else "")+"</figure>" for p in photos)
  return f"<div class='jobshots'>{figs}</div>"
def attach_job_photos():
  # Attach processed WebP files if present (never invent captions beyond the approved wording).
  specs={
    "lehigh-acres-2026-11-17":[
      ("lehigh-acres-2026-11-17-inlet.webp","Opened inlet side of a septic tank in Lehigh Acres during a November 2026 residential pump-out, with scum and solids visible. No street address is shown.","Lehigh Acres pump-out, Nov 2026: system was backing up"),
      ("lehigh-acres-2026-11-17-inlet-2.webp","Opened inlet side of a septic tank in Lehigh Acres during a November 2026 residential pump-out. No street address is shown.","Lehigh Acres pump-out, Nov 2026: system was backing up"),
      ("lehigh-acres-2026-11-17-outlet.webp","Outlet side of a septic tank in Lehigh Acres during a November 2026 residential pump-out, showing the effluent filter housing. No street address is shown.","Outlet side with effluent filter"),
      ("lehigh-acres-2026-11-17-outlet-2.webp","Outlet side of a septic tank in Lehigh Acres during a November 2026 residential pump-out, with the effluent filter housing visible. No street address is shown.","Outlet side with effluent filter"),
    ]
  }
  for j in JOBS:
    out=[]
    for fn,alt,cap in specs.get(j["id"],[]):
      path=f"assets/img/jobs/{fn}"
      if os.path.exists(path):
        w,h=1200,900
        try:
          from PIL import Image
          with Image.open(path) as im:
            w,h=im.size
        except Exception:
          pass
        out.append(dict(src="/"+path, alt=alt, cap=cap, w=w, h=h))
    if out:
      j["photos"]=out
attach_job_photos()
def jobs_block(c):
  js=[j for j in JOBS if j["city"]==c]
  served=f"<p>We've done septic tank pumping jobs in {c} recently.</p>" if c in SERVED_RECENTLY else ""
  if not js: return (f"<h2>Recent work in {c}</h2>"+served) if served else ""
  return (f"<h2>Recent jobs in {c}</h2>"+served+"<ul>"+"".join(f"<li><strong>{j['date']}: {j['title']}.</strong> {j['found']} {j['done']} <a href='/completed-jobs/#{j['id']}'>See job</a></li>"+job_shots(j) for j in js)+"</ul>")
def city_svc_cards(c, extra=True):
  cards="".join(f'<li><a href="/{s[0]}/">{htmllib.escape(s[1])}</a></li>' for s in SERVICES)
  extra_l="<li><a href='/septic-filter-care/'>Septic filter care</a></li>" if extra else ""
  return (f"<h2>Septic services in {c}</h2>"
   +(f"<p>Septic tank pumping and septic tank cleaning in {c}, plus related service pages:</p>" if extra else "")
   +"<ul class='cards'>"+cards+extra_l+"<li><a href='/commercial-grease-trap-service/'>Commercial Grease Trap Service</a></li></ul>")
def city_plus_page(c,county,a,b):
  cp=CITY_PLUS[c]; faq=list(city_faq(c,cp))+list(cp.get("faq_extra") or []); path=f"/{slug(c)}/"
  quick=(cp["quick"] if "quick" in cp else
   (f"<div class='quick'><p class='eyebrow'>Quick answer</p><p><strong>Express Septic Tank Pumping pumps septic tanks in {c}, FL.</strong> Residential pumping starts at $399.99. "
   f"For a backup, call <a href='tel:{TEL}'>{PHONE}</a> day or night. For routine pumping, request a time online and we'll contact you to confirm.</p>"
   f"<ul class='facts'><li><b>Services:</b> residential and commercial septic pumping, septic repairs, drain field replacement, <a href='/lift-station-pumping/'>lift station pumping</a>, septic tank risers, <a href='/grease-trap-pumping/'>grease trap and interceptor pumping</a>, septic inspections</li><li><b>Price:</b> residential pumping from $399.99; after-hours pumping $599.99; septic inspection with pump-out $549.99; 6-inch risers $299.99 each; buried-lid locating/digging $100, plus $50 for each additional hour</li><li><b>Hours:</b> open 24 hours, 7 days a week</li><li><b>Based in:</b> Estero, serving {c} and the rest of {county}</li><li><b>Licensing:</b> work performed under FL Certified Plumbing Contractor Raymond F. Dibble, #CFC020332</li></ul></div>"))
  body=(quick+photo(slug(c),f"Septic tank pumping job in {c}, FL")+cp["local"]+jobs_block(c)+
   f"<h2>What septic pumping costs in {c}</h2>"+PRICE_PANEL+LID_ASK+
   (cp["svc_cards"] if "svc_cards" in cp else city_svc_cards(c) if cp.get("svc_enriched") else (f"<h2>Septic services in {c}</h2><ul class='cards'>"+"".join(f'<li><a href="/{s[0]}/">{htmllib.escape(s[1])}</a></li>' for s in SERVICES)+"<li><a href='/commercial-grease-trap-service/'>Commercial Grease Trap Service</a></li></ul>"))
   +f"<h2>Signs your tank needs pumping</h2><p>Slow drains, gurgling pipes, sewage odors outside, or soggy, extra-green grass over the drain field. If it's been 3 to 5 years since your last pump-out, or you don't know, it's time to call.</p>"
   +REQUEST+f"<h2>{c} septic questions</h2>"+"".join(f"<h3>{q}</h3><p>{x}</p>" for q,x in faq)+
   "<h2>Nearby areas we serve</h2><ul class='cards'>"+"".join(f'<li><a href="/{slug(x)}/">{x}</a></li>' for x in cp["near"])+"<li><a href='/service-area/'>All areas</a></li></ul>"
   "<p class='srcs'>Sources: "+"; ".join(S(k) for k in cp["srcs"])+".</p>")
  crumbs={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":BASE+"/"},{"@type":"ListItem","position":2,"name":"Service area","item":BASE+"/service-area/"},{"@type":"ListItem","position":3,"name":c,"item":BASE+path}]}
  svc={"@context":"https://schema.org","@type":"Service","name":f"Septic tank pumping in {c}, FL","serviceType":"Septic tank pumping","url":BASE+path,"provider":PROV,"areaServed":{"@type":"City","name":f"{c}, FL","containedInPlace":{"@type":"AdministrativeArea","name":f"{county}, FL"}},"offers":{"@type":"Offer","priceSpecification":{"@type":"PriceSpecification","minPrice":399.99,"priceCurrency":"USD"}}}
  page(path,cp["title"],cp["desc"],cp["h1"],body,[svc,faq_ld(faq),crumbs],trail=cp.get("trail"))
HOME_FAQ=[("How much does septic tank pumping cost?",f"Residential pumping starts at $399.99. {PRICE_COND} Call (239) 451-3261 to confirm for your tank."),RISER_QA,
 ("How often should I pump my septic tank?","The U.S. EPA recommends pumping most household tanks every 3 to 5 years, depending on tank size, household size and water use."),
 ("Do you pump grease traps?","Yes. We pump <a href='/grease-trap-pumping/'>grease traps and interceptors</a> for restaurants and food service, including in-ground interceptors and indoor traps, one-time or on a recurring schedule. $695 for a 1,000-gallon grease trap or interceptor; other sizes are quoted. Call (239) 451-3261."),
 ("Do you pump grease interceptors?","Yes. We pump in-ground grease interceptors and indoor traps for restaurants and food service. $695 for a 1,000-gallon grease trap or interceptor; other sizes are quoted. Call (239) 451-3261."),
("How much does grease trap pumping cost?","$695 for a 1,000-gallon grease trap or interceptor; other sizes are quoted. Call (239) 451-3261."),
 ("How often does a grease interceptor need pumping in Lee County?","<a href='https://www.leegov.com/bocc/Ordinances/14-24.pdf' rel='noopener'>Lee County Ordinance 14-24</a> requires grease interceptors to be fully pumped at least every 90 calendar days. Indoor grease traps must be cleaned at least weekly or whenever grease and solids exceed 20% of the unit volume. We can set up a recurring pump-out schedule. Call (239) 451-3261."),
 ("Do you do septic repairs?","Yes. We look at the system first, then quote the repair. Call (239) 451-3261. Repair work is performed under Florida Certified Plumbing Contractor Raymond F. Dibble, License #CFC020332."),
 ("Do you replace drain fields?","Yes. We quote drain field replacement after inspecting the system. Call (239) 451-3261. The work is performed under FL Certified Plumbing Contractor Raymond F. Dibble, License #CFC020332."),
 ("Do you pump lift stations?","Yes. <a href='/lift-station-pumping/'>Lift station work</a> is quoted after we inspect the system. Call (239) 451-3261."),
 ("How often should I clean my septic effluent filter?","If your tank has an effluent filter, it should be checked and cleaned at every pump-out and whenever drains slow. Express can advise on a schedule for your system. See <a href='/septic-filter-care/'>effluent filter care</a>. Call (239) 451-3261."),
 ("What happens if the effluent filter is dirty?","A dirty filter can cause backups or slow drains, and wastewater can be pushed back into the house. Express cleans your filter at no charge on pump-outs and can show you how to keep it clean."),
 ("How does soil bacteria protect a drain field?","Healthy bacteria in the soil break down effluent after it leaves the tank. Harsh chemicals, solids and grease overload can hurt that process. See <a href='/septic-bacteria-drain-field/'>why good bacteria protect your septic tank and drain field</a>."),
 ("Can I book online?","Yes, for routine pumping: send a request on ServiceM8 and we'll contact you to confirm a time. For a backup, call (239) 451-3261 day or night.")]

STANDAPART=("""<div class="aparthead"><p class="eyebrow">How we stand apart</p>
<h2>What you can expect from Express</h2></div>
<ul class="apartgrid">
<li><h3>If we commit to a same-day pump-out</h3><p>We keep working into the night until every scheduled job is done.</p></li>
<li><h3>We pump both compartments</h3><p>We pump both the inlet and the outlet compartments. Some companies only pump the inlet.</p></li>
<li><h3>Filter cleaning at no charge</h3><p>We clean your filter at no charge on pump-outs and show you how to keep it clean.</p></li>
</ul>""")
EDU=("""<div class="eduhead"><p class="eyebrow">Septic care</p>
<h2>Protect your system between pump-outs</h2></div>
<ul class="edugrid">
<li><h3>First time with a septic system?</h3><p>If you just moved from city sewer, bought a new-build home, or this is your first house on a septic tank, start with a complete guide: how the system works, first steps after you move in, what not to flush, and when to call.</p><a class="txtlink" href="/first-time-septic-owner/">First-time septic guide</a></li>
<li><h3>Effluent filter care</h3><p>If your tank has an effluent filter, it should be checked and cleaned at every pump-out and whenever drains slow. A dirty filter can cause backups or slow drains, and wastewater can be pushed back into the house. We clean your filter at no charge on pump-outs and can show you how to keep it clean.</p><a class="txtlink" href="/septic-filter-care/">How to care for your filter</a></li>
<li><h3>Healthy bacteria protect the tank and drain field</h3><p>Anaerobic bacteria in the tank break down solids. Aerobic bacteria and the biomat in drain-field soil treat effluent before it reaches groundwater. Harsh chemicals, grease and solids overload can hurt that process.</p><p><a class="txtlink" href="/septic-bacteria-drain-field/">Why good bacteria matter</a> <a class="txtlink" href="/drain-field-replacement/">Drain field replacement</a></p></li>
</ul>""")
def work_card(jid, blurb):
  j=next(x for x in JOBS if x["id"]==jid)
  return f"<li class='workcard'>{job_shots(j, limit=1)}<p class='jdate'>{j['date']} · {j['city']}</p><h3>{j['title']}</h3><p>{blurb}</p><a class='txtlink' href='/completed-jobs/#{j['id']}'>See this job</a></li>"
WORK_SEC=("<div class='workhead'><p class='eyebrow'>Recent work</p><h2>Jobs from this month</h2><p>Recent septic pump-outs from our crew. Customer addresses and names are never shown.</p></div><ul class='workgrid'>"
 +work_card("lehigh-acres-2026-11-17","Lehigh Acres pump-out, Nov 2026: system was backing up.")
 +work_card("cape-coral-2026-11-14","We dug up buried lids, exposed the inlet and outlet tees, and pulled and cleaned the effluent filter.")
 +"</ul><p class='more'><a class='txtlink' href='/completed-jobs/'>All completed jobs</a></p>")

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
<li><a href="/lift-station-pumping/"><b>Lift station pumping</b><span>Quoted after we inspect the system.</span></a></li>
<li><a href="/grease-trap-pumping/"><b>Grease trap &amp; interceptor pumping</b><span>For restaurants and food service, including in-ground interceptors and indoor traps. $695 for a 1,000-gallon grease trap or interceptor; other sizes are quoted.</span></a></li>
<li><a href="/septic-inspections/"><b>Septic inspections</b><span>For buyers, sellers and homeowners. Inspection with pump-out $549.99.</span></a></li></ul><p class='more'>We also have dedicated septic tank pumping pages for <a href='/septic-tank-pumping-fort-myers-fl/'>Fort Myers</a>, <a href='/septic-tank-pumping-cape-coral-fl/'>Cape Coral</a> and <a href='/septic-tank-pumping-bonita-springs-fl/'>Bonita Springs</a>.</p>
</div>''')+sec(PRICE_PANEL,"priceband")+sec(QUOTES,"quotes")+sec(STANDAPART,"standapart")+sec(EDU,"edu")+
 f'''<section class="truck"><figure class="tphoto">{SIDE.replace('sizes="(min-width:960px) 680px, 100vw"','sizes="100vw"').replace('<figure class="shot">','').replace('</figure>','')}</figure><div class="wrap tcopy"><p class="eyebrow">The truck</p><h2>4,200 gallons, split tank</h2><p>The tank is split in two: one side for septic, one side for grease, so the two never mix. Licensed &amp; insured · USDOT 6673233.</p></div></section>'''+
 sec(f'''<div class="owner">'''+CREW.replace('alt="Express Septic Tank Pumping crew with the 4,200-gallon vacuum truck"','alt="ORyan Atkinson, owner of Express Septic Tank Pumping (right, in the cap), with a crew member and the Express truck"').replace('sizes="(min-width:960px) 680px, 100vw"','sizes="(min-width:960px) 600px, 100vw"').replace("</figure>","<figcaption>ORyan Atkinson, owner (right, in the cap), with a crew member and the Express truck</figcaption></figure>")+f'''<div><p class="eyebrow">The owner</p><blockquote class="promise">When you call, you're talking to the person who runs the business.</blockquote><p>Express is owned and run by ORyan Atkinson, based in Estero. Licensed &amp; insured. Honest, reliable and fair: great customer service is our top priority.</p><p><a class="btn ghost" href="tel:{TEL}">Call ORyan · {PHONE}</a></p><p><a href="/about/">More about Express</a></p></div></div><div class="cred"><p class="eyebrow">Credentials</p><h2>Licensed &amp; Experienced</h2><p>{LICENSE_BODY}</p><p class="crev"><a class="txtlink" href="{REVIEWS_READ}" rel="noopener">Read our Google reviews</a></p></div>''',"warm")+
 sec(WORK_SEC, "work")+
 sec(f'<div class="split"><div><p class="eyebrow">Service area</p><h2>Lee, Collier &amp; Charlotte County</h2><p>Based in Estero, between Bonita Springs and Fort Myers. We also cover LaBelle in Hendry County.</p><p><a href="/service-area/">See every area we serve</a></p></div><div>{city_list}</div></div>',"area")+
 sec(REQUEST,"bookband")+sec("<p class='eyebrow'>FAQ</p><h2>Common questions</h2>"+"".join(f"<h3>{q}</h3><p>{a}</p>" for q,a in HOME_FAQ)+"<p><a href='/faq/'>More septic questions</a></p>","hfaq"),hero=HERO,extra=faq_ld(HOME_FAQ))
RES_EXTRA=("<h2>What happens during a visit</h2>"+LIDS+"<ol><li><strong>We locate the tank.</strong> We find the tank and its lid or access port. If the lid is buried, we dig to reach it: $100, plus $50 for each additional hour.</li><li><strong>We pump it out.</strong> The truck pumps the liquid, sludge and scum out of the tank.</li><li><strong>We tell you what we saw.</strong> You'll hear about anything that looks like it needs attention.</li></ol>"
 "<h2>How to prepare</h2><ul><li>If you know where the lid is, mark it or tell us when you call.</li><li>Make sure the truck can get close: clear the driveway and keep vehicles off the drain field.</li><li>Keep pets inside and unlock any gates.</li><li>Have your last pumping date handy if you know it.</li></ul>"
 "<h2>What affects the price</h2><ul><li>Tank size and how full it is</li><li>Access: how far the truck has to reach and whether the lid is buried and needs locating or digging</li><li>Location within our service area</li><li>After-hours pumping: $599.99</li></ul>"
 "<div class='price-slot'><p class='pp'>Residential septic pumping starting at $399.99</p><p>Your final quote depends on tank size, tank access, and whether the lid needs locating or digging. After-hours pumping is $599.99. Call to confirm for your tank.</p></div>"
 "<p>Call <a href='tel:"+TEL+"'>"+PHONE+"</a> to confirm pricing for your tank.</p>")
EXTRA["residential-septic-tank-pumping"]="<div class='price-slot'><p class='pp'>Residential septic pumping starting at $399.99</p><p>Your final quote depends on tank size, tank access, and whether the lid needs locating or digging. After-hours pumping is $599.99. Call to confirm for your tank.</p></div>"+RES_EXTRA+EXTRA.get("residential-septic-tank-pumping","")

LIFT_FAQ=[
 ("Do you pump lift stations?","Yes. Lift station work is quoted after we inspect the system. Call (239) 451-3261."),
 ("How is lift station work quoted?","Lift station work is quoted after we inspect the system. Call (239) 451-3261 to set up a visit."),
 ("Where do you pump lift stations?","We're based in Estero and serve Lee, Collier and Charlotte County, plus LaBelle in Hendry County. Call (239) 451-3261."),
]
GREASE_FAQ=[
 ("How much does grease trap pumping cost?","$695 for a 1,000-gallon grease trap or interceptor; other sizes are quoted. Call (239) 451-3261."),
 ("Do you pump grease interceptors?","Yes. We pump in-ground grease interceptors and indoor traps for restaurants and food service. $695 for a 1,000-gallon grease trap or interceptor; other sizes are quoted. Call (239) 451-3261."),
 ("How often does a grease interceptor need pumping in Lee County?","Lee County Ordinance 14-24 requires grease interceptors to be fully pumped at least every 90 calendar days. Indoor grease traps must be cleaned at least weekly or whenever grease and solids exceed 20% of the unit volume. We can set up a recurring pump-out schedule. Call (239) 451-3261."),
 ("Do you pump grease traps?","Yes. We pump grease traps and interceptors for restaurants and food service, one-time or on a recurring schedule. $695 for a 1,000-gallon grease trap or interceptor; other sizes are quoted. Call (239) 451-3261."),
 ("Do you keep grease and septic loads separate?","Yes. Our 4,200-gallon truck has a split tank, one side for septic and one side for grease, so the two never mix."),
]
BACTERIA_FAQ=[
 ("What do bacteria do in a septic tank?","Anaerobic bacteria in the tank break down solids. Heavier material settles as sludge, and lighter material, including grease, floats as scum. Wastewater in the middle, called effluent, leaves the tank toward the drain field."),
 ("How do bacteria in the drain field treat wastewater?","Aerobic bacteria in the drain-field soil, and a thin living layer called the biomat, treat effluent after it leaves the tank and before it moves farther toward groundwater."),
 ("What can kill or overload good septic bacteria?","Bleach and harsh cleaners in large amounts, antibacterial soaps, drain openers, antibiotics and other medications that are flushed, grease, wipes, heavy garbage-disposal use, and too much water at once, such as doing all the laundry in one day."),
 ("What are signs the bacterial balance is off?","Odors, slow drains, soggy spots in the yard, and unusually lush grass over the drain field. These can have other causes too. If you notice them, call (239) 451-3261."),
 ("Do I need septic tank additives?","A healthy septic system normally gets the bacteria it needs from everyday household waste. Additives are not a substitute for regular pumping. See the U.S. EPA SepticSmart page at https://www.epa.gov/septic."),
 ("How does pumping help the drain field?","Regular pumping removes sludge and scum that bacteria cannot fully break down, so solids are less likely to leave the tank and overload the drain field."),
 ("Do you clean the effluent filter when you pump?","Yes. We clean your filter at no charge on pump-outs and can show you how to keep it clean. A clean filter helps keep solids out of the drain field. See <a href='/septic-filter-care/'>effluent filter care</a>."),
]
FILTER_FAQ=[
 ("How often should I clean my septic effluent filter?","If your tank has an effluent filter, it should be checked and cleaned at every pump-out and whenever drains slow. Express can advise on a schedule for your system. Call (239) 451-3261."),
 ("Where is the septic effluent filter?","The effluent filter is in the outlet side of the tank, under the lid. A 6-inch riser ($299.99 each) brings the lid up to ground level so the filter is easier to reach."),
 ("What happens if the effluent filter is dirty?","A dirty filter can cause backups or slow drains, and wastewater can be pushed back into the house. Express cleans your filter at no charge on pump-outs and can show you how to keep it clean."),
 ("How does soil bacteria protect a drain field?","Healthy bacteria in the soil break down effluent after it leaves the tank. Harsh chemicals, solids and grease overload can hurt that process. See <a href='/septic-bacteria-drain-field/'>why good bacteria protect your septic tank and drain field</a>."),
 ("Do you clean the effluent filter when you pump?","Yes. We clean your filter at no charge on pump-outs and show you how to keep it clean."),
]
def faq_html(items, heading_tag="h3"):
  return "".join(f"<{heading_tag}>{q}</{heading_tag}><p>{a}</p>" for q,a in items)
EXTRA["drain-field-replacement"]=(
 "<p>Keeping good bacteria healthy in the tank and the drain-field soil helps protect a drain field before it fails. See <a href='/septic-bacteria-drain-field/'>why good bacteria protect your septic tank and drain field</a>.</p>"
)
EXTRA["lift-station-pumping"]=(
 "<h2>What is lift station pumping?</h2>"
 "<p>A lift station is a pump that moves wastewater when it cannot flow by gravity. Express pumps lift stations in our service area. We quote the work after we inspect the system.</p>"
 "<h2>Do you pump lift stations?</h2>"
 "<p>Yes. Lift station work is quoted after we inspect the system. Call <a href='tel:"+TEL+"'>"+PHONE+"</a>.</p>"
 "<h2>How is lift station work quoted?</h2>"
 "<p>Lift station work is quoted after we inspect the system. Call <a href='tel:"+TEL+"'>"+PHONE+"</a> to set up a visit.</p>"
 "<h2>Where do you pump lift stations?</h2>"
 "<p>We're based in Estero and serve Lee, Collier and Charlotte County, plus LaBelle in Hendry County. See our <a href='/service-area/'>service area</a>.</p>"
 "<h2>Lift station questions</h2>"+faq_html(LIFT_FAQ)
)
LEE_ORD='<a href="https://www.leegov.com/bocc/Ordinances/14-24.pdf" rel="noopener">Lee County Ordinance 14-24</a>'
FL_STATUTE='<a href="https://www.flsenate.gov/Laws/Statutes/2026/403.0741" rel="noopener">Florida Statute 403.0741</a>'
EXTRA["grease-trap-pumping"]=(
 "<h2>Do you pump grease interceptors?</h2>"
 "<p>Yes. We pump in-ground grease interceptors and indoor traps for restaurants and food service in Fort Myers, Cape Coral, Bonita Springs, Naples, Estero and across Lee, Collier, and Charlotte County, plus LaBelle. $695 for a 1,000-gallon grease trap or interceptor; other sizes are quoted. We can set up a recurring pump-out schedule. Call <a href='tel:"+TEL+"'>"+PHONE+"</a>.</p>"
 "<h2>Where do you pump grease traps and interceptors?</h2>"
 "<p>This is our main page for grease trap and interceptor pumping in Southwest Florida. We serve restaurants and food-service kitchens in Lee, Collier and Charlotte County, plus LaBelle in Hendry County, including Fort Myers, Cape Coral, Bonita Springs, Naples and Estero.</p>"
 "<h2>How often does a grease interceptor need pumping in Lee County?</h2>"
 "<p>"+LEE_ORD+" requires grease interceptors to be fully pumped at least every 90 calendar days. Indoor grease traps must be cleaned at least weekly or whenever grease and solids exceed 20% of the unit volume. We can set up a recurring pump-out schedule that fits your kitchen.</p>"
 "<h2>What Florida law says about grease waste manifests</h2>"
 "<p>"+FL_STATUTE+" requires a signed grease waste service manifest for every pump-out.</p>"
 "<h2>How much does grease trap pumping cost?</h2>"
 "<p>$695 for a 1,000-gallon grease trap or interceptor; other sizes are quoted. Call <a href='tel:"+TEL+"'>"+PHONE+"</a>.</p>"
 "<h2>How do you keep grease and septic separate?</h2>"
 "<p>Our 4,200-gallon truck has a split tank, one side for septic and one side for grease, so grease trap loads and septic loads never mix.</p>"
 "<p>A shorter overview is on our <a href='/commercial-grease-trap-service/'>commercial grease trap service</a> page. This page is the main one for grease trap and interceptor pumping in Southwest Florida.</p>"
 "<h2>Grease trap and interceptor questions</h2>"+faq_html(GREASE_FAQ)+
 '<p class="srcs">Sources: '+LEE_ORD+'; '+FL_STATUTE+'.</p>'
)

for s in SERVICES:
  intro="" if s[0] in ("lift-station-pumping","grease-trap-pumping") else VAL
  no_generic_price=s[0] in ("septic-tank-riser-installation","residential-septic-tank-pumping","septic-inspections","lift-station-pumping","grease-trap-pumping")
  body=photo(s[0],s[1]+" job photo")+intro+"".join(f"<p>{p}</p>" for p in s[4])+EXTRA.get(s[0],"")+("" if no_generic_price else "<h2>Pricing</h2><p>Call for a quote — <a href='tel:"+TEL+"'>"+PHONE+"</a>.</p>")+"<h2>Service Areas</h2>"+city_list+"<h2>Other Services</h2>"+svc_list
  offers=({"offers":{"@type":"Offer","name":"6-inch septic tank riser, installed (each)","price":299.99,"priceCurrency":"USD"}} if s[0]=="septic-tank-riser-installation" else {"offers":{"@type":"Offer","priceSpecification":{"@type":"PriceSpecification","minPrice":399.99,"priceCurrency":"USD"}}} if s[0]=="residential-septic-tank-pumping" else {"offers":{"@type":"Offer","name":"Septic inspection with pump-out","price":549.99,"priceCurrency":"USD"}} if s[0]=="septic-inspections" else {"offers":{"@type":"Offer","description":"Quoted after we inspect the system"}} if s[0] in ("drain-field-replacement","lift-station-pumping") else {"offers":{"@type":"Offer","price":695,"priceCurrency":"USD","description":"1,000 gallons"}} if s[0]=="grease-trap-pumping" else {})
  svc={"@context":"https://schema.org","@type":"Service","name":s[1],"serviceType":s[1],"url":f"{BASE}/{s[0]}/","provider":PROV,"areaServed":[{"@type":"City","name":c+", FL"} for c in CITIES_ALL],**offers}
  extra=svc; trail=None
  if s[0]=="lift-station-pumping":
    extra=[svc,faq_ld(LIFT_FAQ),crumbs_ld([("Home",BASE+"/"),("Lift Station Pumping",BASE+"/lift-station-pumping/")])]
    trail=[("Home","/"),("Lift Station Pumping","/lift-station-pumping/")]
  elif s[0]=="grease-trap-pumping":
    extra=[svc,faq_ld(GREASE_FAQ),crumbs_ld([("Home",BASE+"/"),("Grease Trap & Interceptor Pumping",BASE+"/grease-trap-pumping/")])]
    trail=[("Home","/"),("Grease Trap & Interceptor Pumping","/grease-trap-pumping/")]
  page(f"/{s[0]}/",s[2],s[3],s[1]+" in Southwest Florida",body,extra,trail=trail)
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
  if c=="Captiva":
    cap_path="/septic-tank-pumping-captiva-fl/"
    cap_faq=[
     ("Do you pump septic tanks on Captiva?","Yes. Express pumps septic tanks on Captiva Island in Lee County. Residential pumping starts at $399.99 (standard 1–3 bed). Call (239) 451-3261."),
     ("Do you offer 24-hour pumping on Captiva?","Yes. Express is open 24 hours, 7 days a week. For a backup, call (239) 451-3261 day or night. After-hours pumping is $599.99."),
     ("Do you also serve Sanibel?","Yes. See our page for <a href='/septic-tank-pumping-sanibel-fl/'>septic tank pumping on Sanibel</a>."),
    ]
    cap_body=(
     "<div class='quick'><p class='eyebrow'>Quick answer</p><p><strong>Express Septic Tank Pumping provides septic tank pumping and septic tank cleaning on Captiva Island in Lee County.</strong> "
     "Captiva sits north of Sanibel and is reached from the mainland by the Sanibel Causeway, then the Blind Pass Bridge from Sanibel. "
     f"Residential pumping starts at $399.99 (standard 1–3 bed). We are open 24 hours, 7 days a week. For a backup or after-hours emergency, call <a href='tel:{TEL}'>{PHONE}</a>; after-hours pumping is $599.99. For routine pumping, request a time online and we'll contact you to confirm.</p></div>"
     +photo(slug(c),f"Septic tank pumping job in {c}, FL")
     +"<h2>Do you pump septic tanks on Captiva?</h2>"
     "<p>Yes. Express pumps septic tanks for homes and businesses on Captiva Island. Septic tank cleaning on Captiva is the same service: we empty the sludge and scum from the tank so it does not overflow into the drain field. Island properties need careful septic maintenance to protect the surrounding waters.</p>"
     "<h2>How do you get to Captiva for a pump-out?</h2>"
     "<p>Our crew reaches Captiva from the mainland by the Sanibel Causeway, then continues north from <a href='/septic-tank-pumping-sanibel-fl/'>Sanibel</a> across the Blind Pass Bridge. This page covers Captiva Island, the island connected by road from Sanibel.</p>"
     "<h2>Do you offer 24-hour septic pumping on Captiva?</h2>"
     f"<p>Yes. Express is open 24 hours, 7 days a week. For a backup, call <a href='tel:{TEL}'>{PHONE}</a> day or night and stop running water until we arrive. After-hours pumping is $599.99.</p>"
     +f"<h2>What septic pumping costs on Captiva</h2>"+PRICE_PANEL
     +city_svc_cards("Captiva")
     +"<h2>Captiva septic questions</h2>"+"".join(f"<h3>{q}</h3><p>{x}</p>" for q,x in cap_faq)
     +"<h2>Nearby areas we serve</h2><ul class='cards'>"
     +"".join(f"<li><a href='/{slug(x)}/'>{x}</a></li>" for x in ["Sanibel","Fort Myers Beach","Pine Island","Cape Coral","Fort Myers"])
     +"<li><a href='/service-area/'>All areas</a></li></ul>")
    cap_crumbs={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":BASE+"/"},{"@type":"ListItem","position":2,"name":"Service area","item":BASE+"/service-area/"},{"@type":"ListItem","position":3,"name":"Captiva","item":BASE+cap_path}]}
    cap_svc={"@context":"https://schema.org","@type":"Service","name":"Septic tank pumping in Captiva, FL","serviceType":"Septic tank pumping","url":BASE+cap_path,"provider":PROV,"areaServed":{"@type":"City","name":"Captiva, FL","containedInPlace":{"@type":"AdministrativeArea","name":"Lee County, FL"}},"offers":{"@type":"Offer","priceSpecification":{"@type":"PriceSpecification","minPrice":399.99,"priceCurrency":"USD"}}}
    page(cap_path,"Septic Tank Pumping in Captiva, FL | Express Septic",
     "Septic tank pumping and septic tank cleaning on Captiva Island, FL, north of Sanibel in Lee County. Residential pumping starts at $399.99 (standard 1–3 bed). Open 24 hours. Call (239) 451-3261.",
     "Septic Tank Pumping in Captiva, FL",cap_body,
     [cap_svc,faq_ld(cap_faq),cap_crumbs],
     trail=[("Home","/"),("Service area","/service-area/"),("Captiva","/septic-tank-pumping-captiva-fl/")])
    continue
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

FILTER_PHOTOS=""
_j=next((x for x in JOBS if x["id"]=="lehigh-acres-2026-11-17"), None)
if _j:
  _out=[p for p in (_j.get("photos") or []) if "effluent filter" in (p.get("cap") or "").lower() or "outlet side" in (p.get("cap") or "").lower()]
  FILTER_PHOTOS=job_shots({"photos":_out} if _out else {"photos":[]})

page("/septic-bacteria-drain-field/","Why Good Bacteria Protect Your Septic Tank and Drain Field | Express Septic",
 "Anaerobic bacteria in the tank and aerobic bacteria in the drain field treat wastewater before it reaches groundwater. What helps, what hurts, and why pumping and filter cleaning matter. Call (239) 451-3261.",
 "Why good bacteria protect your septic tank and drain field",
 "<p>Good bacteria do two jobs in a septic system. In the tank, anaerobic bacteria break down solids. In the drain field, aerobic bacteria and a living layer called the biomat treat effluent before it reaches groundwater. Regular pumping and a clean effluent filter help protect that balance. Express cleans your filter at no charge on pump-outs.</p>"
 "<h2>What do anaerobic bacteria do in the septic tank?</h2>"
 "<p>Wastewater from the house flows into the tank. Anaerobic bacteria, which work without oxygen, break down some of the solids. Heavier material settles to the bottom as sludge. Lighter material, including grease, floats to the top as scum. The clearer wastewater in the middle, called effluent, moves on to the drain field.</p>"
 "<h2>How do aerobic bacteria and the biomat treat effluent in the drain field?</h2>"
 "<p>Effluent leaving the tank still needs treatment. In the drain-field soil, aerobic bacteria, which need oxygen, continue breaking down what remains. A thin, living layer called the biomat forms in the soil around the drain-field pipes. Together, the soil bacteria and the biomat treat effluent before it moves farther through the soil and toward groundwater.</p>"
 "<h2>Why does this matter in Southwest Florida?</h2>"
 "<p>Much of Southwest Florida has sandy soils and a high water table, especially in the rainy season. Sandy soil can let water move quickly, and a high water table leaves less unsaturated soil between the drain field and groundwater. That makes it more important to keep bacteria in the tank and the drain-field biomat healthy, and to pump the tank so solids and grease do not overload the field.</p>"
 "<h2>What kills or overloads septic bacteria?</h2>"
 "<p>Some household products and habits can kill helpful bacteria or send more solids and water to the drain field than it can treat:</p>"
 "<ul><li>Bleach and harsh cleaners in large amounts</li><li>Antibacterial soaps</li><li>Drain openers</li><li>Antibiotics and other medications flushed down the toilet or drain</li><li>Grease</li><li>Wipes, even ones labeled flushable</li><li>Heavy use of a garbage disposal</li><li>Too much water at once, such as doing all the laundry in one day</li></ul>"
 "<p>See our <a href='/septic-system-maintenance/'>septic system maintenance</a> tips for more on what not to flush or pour down drains.</p>"
 "<h2>What are signs the bacterial balance is off?</h2>"
 "<p>Odors, slow drains, soggy spots in the yard, and unusually lush grass over the drain field can mean the system is out of balance. Those signs can also have other causes. If you notice them, call <a href='tel:"+TEL+"'>"+PHONE+"</a>.</p>"
 "<h2>What daily habits help?</h2>"
 "<ul><li>Keep grease, wipes, paper towels, and medications out of the drains and toilet</li><li>Use household cleaners in normal amounts rather than large amounts of bleach or drain opener</li><li>Spread laundry loads through the week instead of doing them all in one day</li><li>Go easy on the garbage disposal</li><li>Have the tank pumped on a regular schedule, and have the effluent filter cleaned when the tank is pumped</li></ul>"
 "<h2>Why does regular pumping matter for bacteria?</h2>"
 "<p>Bacteria in the tank cannot fully break down all of the solids. Regular <a href='/septic-tank-pumping/'>septic tank pumping</a> removes the sludge and scum that build up so those solids are less likely to leave the tank and reach the drain field, where they can clog soil and harm the biomat.</p>"
 "<h2>How does effluent filter cleaning help?</h2>"
 "<p>If your tank has an effluent filter, a clean filter helps keep solids out of the drain field so soil bacteria and the biomat can do their job. Express cleans your filter at no charge on pump-outs and can show you how to keep it clean. See <a href='/septic-filter-care/'>effluent filter care</a>.</p>"
 "<h2>Do septic tank additives replace pumping?</h2>"
 "<p>A healthy septic system normally gets the bacteria it needs from everyday household waste. Additives are not a substitute for regular pumping. The U.S. EPA's <a href='https://www.epa.gov/septic' rel='noopener'>SepticSmart guidance</a> is a good place to read more about caring for a septic system.</p>"
 "<h2>Questions about septic bacteria</h2>"+faq_html(BACTERIA_FAQ)+
 '<p class="srcs">Source: <a href="https://www.epa.gov/septic" rel="noopener">U.S. EPA, Septic systems (SepticSmart)</a>.</p>',
 [faq_ld(BACTERIA_FAQ), crumbs_ld([("Home",BASE+"/"),("Good bacteria and the drain field",BASE+"/septic-bacteria-drain-field/")])],
 trail=[("Home","/"),("Good bacteria and the drain field","/septic-bacteria-drain-field/")])

page("/septic-filter-care/","Septic Filter Care and Drain Field Tips | Express Septic",
 "How to care for a septic effluent filter, why a riser makes it easier to clean, what a dirty filter can cause, and how healthy soil bacteria help protect the drain field. Call (239) 451-3261.",
 "Septic filter care and drain field protection",
 "<p>If your septic tank has an effluent filter, keeping it clean helps wastewater leave the tank as it should. This page explains how to access the filter, when to check it, and how healthy bacteria in the soil help protect the drain field.</p>"
 "<h2>How often should I clean my septic effluent filter?</h2>"
 "<p>If your tank has an effluent filter, it should be checked and cleaned at every pump-out and whenever drains slow. Express can advise on a schedule for your system. Call <a href='tel:"+TEL+"'>"+PHONE+"</a>.</p>"
 "<h2>How do I access the effluent filter?</h2>"
 "<p>The effluent filter is in the outlet side of the tank, under the lid.</p>"
 +FILTER_PHOTOS+
 "<h2>Why does a riser help?</h2>"
 "<p>A <a href='/septic-tank-riser-installation/'>6-inch riser</a> ($299.99 each) brings the lid up to ground level, so the filter is easier to reach on later visits without digging.</p>"
 "<h2>What can happen with a dirty filter?</h2>"
 "<p>A dirty filter can cause backups or slow drains, and wastewater can be pushed back into the house. Express cleans your filter at no charge on pump-outs and can show you how to keep it clean.</p>"
 "<h2 id='drain-field'>How healthy soil bacteria protect the drain field</h2>"
 "<p>Healthy bacteria in the soil break down effluent after it leaves the tank, which helps protect the drain field. Harsh chemicals, solids and grease overload can hurt that process. Read more about <a href='/septic-bacteria-drain-field/'>why good bacteria protect your septic tank and drain field</a>. If a drain field has already failed, see <a href='/drain-field-replacement/'>drain field replacement</a>.</p>"
 "<h2>Filter and drain field questions</h2>"+faq_html(FILTER_FAQ),
 [faq_ld(FILTER_FAQ), crumbs_ld([("Home",BASE+"/"),("Septic filter care",BASE+"/septic-filter-care/")])],
 trail=[("Home","/"),("Septic filter care","/septic-filter-care/")])

page("/how-it-works/","How Septic Pumping Service Works | Express Septic Tank Pumping","How booking septic tank pumping with Express Septic works: call or book online, we schedule, pump your tank and walk you through what we found.","How Our Septic Service Works",
 photo("how-it-works","Express Septic technician at work")+
 "<ol><li><strong>Call or book online.</strong> Tap to call (239) 451-3261 or use Book Online.</li><li><strong>Get a quote and schedule.</strong> Tell us about your property and we'll quote and set a time.</li><li><strong>We locate and pump the tank.</strong> Our crew finds the tank lid and pumps the tank.</li><li><strong>We share what we saw.</strong> We let you know about anything that needs attention.</li></ol>"
 "<p>Keep your system healthy between visits with our <a href='/septic-system-maintenance/'>septic maintenance tips</a> and our guide to <a href='/how-often-to-pump-septic-tank/'>how often to pump your septic tank</a>.</p><h2>Our Services</h2>"+svc_list)

# --- Batch 1 educational guides (unique audience pages) ---
def guide(path, title, desc, h1, body, faq, crumb):
  p=path if path.endswith("/") else path+"/"
  page(p, title, desc, h1, body+"<h2>"+crumb+" questions</h2>"+faq_html(faq),
    [faq_ld(faq), crumbs_ld([("Home",BASE+"/"),(crumb,BASE+p)])],
    trail=[("Home","/"),(crumb,p)])

FT_FAQ=[
 ("What should I do first if I just moved into a house with a septic tank?","Find the tank and its lids, ask for pumping and inspection records, and schedule a pump-out if you don't know when it was last serviced. A septic inspection with pump-out is $549.99. Call (239) 451-3261."),
 ("How often should a first-time owner pump the tank?","The U.S. EPA's SepticSmart guidance is that most household tanks are pumped every 3 to 5 years. Household size, tank size, and water use change that. See <a href='/how-often-to-pump-septic-tank/'>how often to pump</a>."),
 ("Where is the effluent filter and how often should I clean it?","If your tank has one, it is in the outlet side, under the lid. Check and clean it at every pump-out and whenever drains slow. Express cleans the filter at no charge on pump-outs. See <a href='/septic-filter-care/'>effluent filter care</a>."),
 ("What should never go down a septic drain?","Wipes, even those labeled flushable, grease and oil, large amounts of bleach or harsh cleaners, medications, paint, and feminine products. Septic-safe, biodegradable toilet paper is a better choice than thick or 'flushable' wipes."),
 ("Does Express pump both compartments of the tank?","Yes. We pump both the inlet and the outlet compartments and clean your effluent filter at no charge on pump-outs."),
 ("What does residential pumping cost?","Residential pumping starts at $399.99 (standard 1–3 bed). After-hours pumping is $599.99. A septic inspection with pump-out is $549.99. 6-inch risers are $299.99 each. Locating and digging a buried lid is $100, plus $50 for each additional hour. Repairs and drain field work are quoted after we inspect the system."),
]
guide("/first-time-septic-owner/","First Time With a Septic System? The Complete Guide | Express Septic",
 "A complete guide for Southwest Florida homeowners new to septic systems: how the tank and drain field work, first steps after you move in, what not to flush, and when to call. Pumping starts at $399.99. Call (239) 451-3261.",
 "First time with a septic system? The complete guide",
 "<p><strong>If you just moved from city sewer, bought a new-build home, or this is your first house on a septic tank, start here.</strong> A septic system treats wastewater on your property instead of sending it to a municipal plant. In Southwest Florida, many homes in and around Estero, Bonita Springs, Fort Myers, Cape Coral, Naples, and Lehigh Acres use one. This guide covers how the system works, what to do in the first weeks, and how to keep it healthy. Call <a href='tel:"+TEL+"'>"+PHONE+"</a> or <a href='"+BOOK+"' rel='noopener' target='_blank'>book routine service on ServiceM8</a> when you are ready for a pump-out or inspection.</p>"
 "<h2>How does a septic system work?</h2>"
 "<p>Wastewater from toilets, sinks, showers, and laundry flows into an underground tank. Inside the tank, heavier solids settle in the inlet compartment as sludge. Lighter material, including grease, floats as scum. Wastewater in the middle, called effluent, moves into the outlet compartment and then out to the drain field.</p>"
 "<p>If the tank has an effluent filter, it sits in the outlet side, under the lid, and helps keep solids from leaving the tank. From there, effluent soaks into the drain field. Bacteria in the soil, including a living layer called the biomat, treat it before it moves farther toward groundwater. For a fuller explanation, see <a href='/septic-bacteria-drain-field/'>why good bacteria protect your tank and drain field</a>.</p>"
 "<h2>How often should I pump a septic tank?</h2>"
 "<p>The <a href='https://www.epa.gov/septic' rel='noopener'>U.S. EPA SepticSmart guidance</a> is that most household tanks are pumped every 3 to 5 years. That is a general range, not a fixed schedule for every home. A larger household, a smaller tank, a garbage disposal, or heavy water use can mean you need service sooner. Snowbird and rental homes can also fill faster when they are occupied. We do not guess your interval from a chart alone; household size and tank size are the starting point, and an inspection shows what your tank actually needs. See <a href='/how-often-to-pump-septic-tank/'>how often to pump your septic tank</a> for more detail.</p>"
 "<p>Residential pumping starts at $399.99 (standard 1–3 bed). After-hours pumping is $599.99.</p>"
 "<h2>What should I do first after moving into a house with a septic system?</h2>"
 "<ol><li><strong>Find the tank and lids.</strong> Lids can be buried under grass or soil. Locating and digging up a buried lid is $100, plus $50 for each additional hour. If you know where the lid is, mark it or tell us when you call.</li>"
 "<li><strong>Ask for records.</strong> Previous pumping dates, permits, and inspection reports tell you whether the system is current or overdue.</li>"
 "<li><strong>Schedule a pump-out, and an inspection if you do not know the system's condition.</strong> A septic inspection with pump-out is $549.99. That is a practical first step when records are missing, especially after a purchase.</li>"
 "<li><strong>Ask about risers.</strong> A <a href='/septic-tank-riser-installation/'>6-inch riser</a> ($299.99 each) brings the lid up to ground level so later visits do not start with digging.</li></ol>"
 "<h2>How do I care for the effluent filter?</h2>"
 "<p>If your tank has an effluent filter, it should be checked and cleaned at every pump-out and whenever drains slow. There is no single calendar interval that fits every house. A dirty filter can cause backups or slow drains, and wastewater can be pushed back into the house. Express cleans your filter at no charge on pump-outs and can show you how to keep it clean. See <a href='/septic-filter-care/'>effluent filter care</a>.</p>"
 "<h2>What should never go down the drains or toilet?</h2>"
 "<ul><li>Wipes, including ones labeled flushable</li><li>Cooking grease, fats, and oil</li><li>Bleach and harsh cleaners in large amounts, which can kill helpful bacteria</li><li>Medications</li><li>Paint and solvents</li><li>Feminine products, paper towels, and diapers</li></ul>"
 "<p>Septic-safe, biodegradable toilet paper is easier on the system than thick wipes. For habits that protect bacteria, see <a href='/septic-bacteria-drain-field/'>good bacteria and the drain field</a> and our <a href='/septic-system-maintenance/'>maintenance tips</a>.</p>"
 "<h2>What are the drain field do's and don'ts?</h2>"
 "<ul><li>Do not park, drive, or build on the drain field</li><li>Do not plant trees or large shrubs over it; grass is the better cover</li><li>Divert roof gutters and runoff away from the field</li><li>Do not drain a swimming pool or spa onto the field; a large volume of chlorinated water can overload it</li><li>A garbage disposal adds solids, so you may need pumping more often</li><li>A water softener can send extra water into the system when it recharges; factor that into how often you pump</li></ul>"
 "<p>If the field is already soggy or backing up, see <a href='/drain-field-not-draining/'>what to do when a drain field is not draining</a>. Replacement, if it is needed, is <a href='/drain-field-replacement/'>quoted after we inspect the system</a>.</p>"
 "<h2>How should I use water in a septic home?</h2>"
 "<p>Spread laundry through the week instead of running many loads in one day. Fix leaky toilets and faucets. A sudden flood of water can push solids toward the drain field before they have time to settle in the tank.</p>"
 "<h2>What warning signs mean I should call?</h2>"
 "<ul><li>Sewage odors inside or outside</li><li>Gurgling pipes</li><li>Slow drains</li><li>Wet spots or unusually lush grass over the drain field</li><li>Toilets or drains backing up</li><li>An alarm, if your system has one</li></ul>"
 "<p>If you have a backup now, do not book online. Stop running water and call <a href='tel:"+TEL+"'>"+PHONE+"</a>. After-hours pumping is $599.99. See <a href='/emergency-septic-backup/'>emergency septic backup service</a>.</p>"
 "<h2>What is different about septic systems in Southwest Florida?</h2>"
 "<p>Much of this area has sandy soil and a high water table, especially in the rainy season. That leaves less room between the drain field and groundwater, so a full tank or a saturated yard can show problems sooner. After a hurricane or flood, wait until standing water recedes before using the system, then have it checked. Snowbirds returning to a house that sat unused should confirm when the tank was last pumped before filling it with several days of heavy use. See <a href='/hurricane-and-flood-septic-prep/'>hurricane and flood septic prep</a> and <a href='/snowbird-seasonal-septic/'>seasonal and snowbird septic care</a>.</p>"
 "<h2>Why does Express pump both the inlet and the outlet?</h2>"
 "<p>Some companies pump only the inlet compartment. Express pumps both the inlet and the outlet so sludge and scum are removed from the whole tank, and we clean your effluent filter at no charge on pump-outs. We are based in Estero, at 23357 Olde Meadowbrook Circle, and serve homes across Lee, Collier, and Charlotte County, plus LaBelle. Browse area pages for <a href='/septic-tank-pumping-fort-myers-fl/'>Fort Myers</a>, <a href='/septic-tank-pumping-cape-coral-fl/'>Cape Coral</a>, <a href='/septic-tank-pumping-bonita-springs-fl/'>Bonita Springs</a>, <a href='/septic-tank-pumping-estero-fl/'>Estero</a>, <a href='/septic-tank-pumping-naples-fl/'>Naples</a>, and <a href='/septic-tank-pumping-lehigh-acres-fl/'>Lehigh Acres</a>, or see the <a href='/faq/'>FAQ</a>.</p>"
 "<h2>What does service cost for a new septic owner?</h2>"
 "<ul><li>Residential pumping starts at $399.99 (standard 1–3 bed)</li><li>After-hours pumping is $599.99</li><li>Septic inspection with pump-out is $549.99</li><li>6-inch risers are $299.99 each</li><li>Locating and digging a buried lid is $100, plus $50 for each additional hour</li><li>Repairs and drain field work are quoted after we inspect the system</li></ul>"
 "<p><a class='btn primary' href='tel:"+TEL+"'>Call "+PHONE+"</a> <a class='btn ghost' href='"+BOOK+"' rel='noopener' target='_blank'>Book routine service on ServiceM8<span class='sr'> (opens in a new tab)</span></a></p>",
 FT_FAQ, "First-time septic guide")

RE_FAQ=[
 ("When should a listing mention a septic inspection?","If the home is on a septic tank and the last pump-out or inspection is unknown, recommend a septic inspection with pump-out before or during the inspection period. That service is $549.99. Call (239) 451-3261."),
 ("Can Express work on a short closing timeline?","Call and tell us the contract dates. Routine work can often be requested through ServiceM8; a backup is not something to book online. We confirm times after we hear from you."),
 ("What should I tell buyers who have only lived on city sewer?","Point them to our <a href='/first-time-septic-owner/'>first-time septic guide</a> and to a professional inspection, not to guesses about the tank's condition."),
 ("Do you provide a report I can share with both sides?","After an inspection with pump-out, we tell you what we saw. Share that conversation and any written notes with your clients and their inspectors as you normally would for other property reports."),
]
guide("/septic-guide-for-realtors/","Septic Guide for Southwest Florida Realtors | Express Septic",
 "A practical septic briefing for Realtors in Lee, Collier, and Charlotte County: when to recommend a $549.99 inspection with pump-out, what to tell first-time buyers, and how to reach Express at (239) 451-3261.",
 "Septic guide for Realtors",
 "<p><strong>If you list or sell homes on septic in Southwest Florida, your clients often need a clear next step more than a lecture on tanks.</strong> This page is written for agents. It covers when to suggest a pump-out or inspection, how to help buyers who have only known city sewer, and how to reach Express without slowing a contract. It is not legal advice about disclosure; your broker and the parties' attorneys handle that.</p>"
 "<h2>When should I recommend a septic inspection?</h2>"
 "<p>Recommend one when the property has a septic tank and the file has no recent pumping record, the buyers are uncertain, or the listing is in an area where many lots are still on tanks rather than central sewer. A <a href='/septic-inspections/'>septic inspection with pump-out</a> is $549.99. That visit is the cleanest way for both sides to see the tank, not a substitute for a general home inspection.</p>"
 "<h2>How do I talk about septic with first-time buyers?</h2>"
 "<p>Many buyers moving to Estero, Bonita Springs, or unincorporated Lee and Collier County are leaving municipal sewer for the first time. Send them to the <a href='/first-time-septic-owner/'>first-time owner guide</a> so they can read about lids, filters, and drain fields at their own pace. On a showing, it is enough to say the home treats wastewater on site, records should be requested, and Express can inspect and pump if they want a current look.</p>"
 "<h2>What belongs in the file besides the marketing remarks?</h2>"
 "<p>Ask the seller for the last pumping date, any risers already installed, and whether the lids are buried. If the lid is buried, locating and digging it is $100, plus $50 for each additional hour, which is useful to mention so a buyer is not surprised on service day. A riser at $299.99 each can be a simple improvement to note in negotiations. For a longer checklist aimed at the parties themselves, use <a href='/buying-or-selling-a-home-with-septic/'>buying or selling a home with a septic tank</a>.</p>"
 "<h2>How do I schedule around a closing date?</h2>"
 "<p>Call <a href='tel:"+TEL+"'>"+PHONE+"</a> and give us the inspection deadline or closing date. For routine pumping or a planned inspection, clients can also <a href='"+BOOK+"' rel='noopener' target='_blank'>request a time on ServiceM8</a>. We contact them to confirm; a request is not a booked appointment until we confirm. If a occupied house has a backup, they should call, not book online.</p>"
 "<h2>Where do you work?</h2>"
 "<p>Express is based in Estero and serves Lee, Collier, and Charlotte County, plus LaBelle. We pump tanks for listings and purchases across those areas, including Fort Myers, Cape Coral, Naples, Lehigh Acres, and the islands. We do not quote drain field replacement or repairs until we inspect the system.</p>"
 "<p><a class='btn primary' href='tel:"+TEL+"'>Call "+PHONE+"</a></p>",
 RE_FAQ, "Realtor septic guide")

BS_FAQ=[
 ("Should I get a septic inspection before closing?","If the home has a septic tank and you do not have recent records, yes, an inspection with pump-out is a sound step. That service is $549.99. Call (239) 451-3261."),
 ("Is a pump-out the same as an inspection?","A pump-out empties the tank. An inspection with pump-out is a visit that includes pumping and a look at the system so you hear what we saw. Buyers and sellers often want that combined visit."),
 ("Who usually pays for the pump-out in a sale?","That is a contract question, not a rule we set. Either party can schedule and pay. We just need access to the lids and a contact who can confirm the appointment."),
 ("What if nobody can find the lid before closing?","We can locate and dig a buried lid for $100, plus $50 for each additional hour. Tell us before the visit if the lid has not been opened in years."),
]
guide("/buying-or-selling-a-home-with-septic/","Buying or Selling a Home With a Septic Tank in SWFL | Express Septic",
 "Pre-sale septic pump-outs and inspections for buyers and sellers in Southwest Florida. Inspection with pump-out is $549.99. Call (239) 451-3261 or request a time on ServiceM8.",
 "Buying or selling a home with a septic tank",
 "<p><strong>If you are buying or selling a Southwest Florida home that uses a septic tank, a current pump-out and inspection is often the missing piece in the due-diligence file.</strong> This page is for the buyer and the seller, not for agents (agents can start with the <a href='/septic-guide-for-realtors/'>Realtor septic guide</a>). The goal is simple: know when the tank was last pumped, see its condition before closing, and avoid inheriting a surprise.</p>"
 "<h2>Why schedule a pump-out before or during the inspection period?</h2>"
 "<p>A tank that has not been opened in years can hide a full sludge layer, a dirty outlet filter, or a lid no one can find. Waiting until after closing leaves the new owner to discover that on a holiday weekend. A <a href='/septic-inspections/'>septic inspection with pump-out</a> is $549.99 and gives both sides a current look. Residential pumping alone starts at $399.99 (standard 1–3 bed) if you only need the tank emptied and already know the system.</p>"
 "<h2>What should a buyer request from the seller?</h2>"
 "<p>Ask for pumping receipts, any county or state permits, and notes about risers or prior repairs. If those papers do not exist, treat the system as unknown and schedule the inspection visit. Buyers who have never owned a septic system can read the <a href='/first-time-septic-owner/'>first-time owner guide</a> in parallel so terms like outlet filter and drain field are familiar before walkthrough.</p>"
 "<h2>What should a seller do before listing?</h2>"
 "<p>Have the tank pumped if it is due, or if you cannot prove the last service date. If lids are buried, budget for locating and digging at $100, plus $50 for each additional hour, or install a <a href='/septic-tank-riser-installation/'>riser</a> ($299.99 each) so future access is easier to show. A tidy, recently serviced tank is easier to explain than a yard with no idea where the lid is.</p>"
 "<h2>What happens on the appointment?</h2>"
 "<p>We find the lid, pump the tank, and tell you what we saw. If the tank has an effluent filter, we clean it at no charge on that pump-out. We do not invent a clean bill of health for a drain field we have not been asked to evaluate in depth; drain field replacement, if it ever comes up, is quoted only after we inspect the system.</p>"
 "<h2>How do I book around a closing date?</h2>"
 "<p>Call <a href='tel:"+TEL+"'>"+PHONE+"</a> with your inspection deadline, or <a href='"+BOOK+"' rel='noopener' target='_blank'>request routine service on ServiceM8</a>. We confirm the time before it is set. If the house is already backing up, skip the booking form and call; after-hours pumping is $599.99.</p>",
 BS_FAQ, "Buying or selling with septic")

BU_FAQ=[
 ("Can crews drive or stage materials on a drain field?","No. Parking, storing fill, or running equipment over the field can compact soil and damage pipes. Mark the field before work starts and keep traffic off it."),
 ("Do you pump tanks on active job sites?","Yes, when we can reach the lids safely. Call (239) 451-3261 with access notes, gate codes, and where the tank is relative to the work."),
 ("Is construction pumping priced like a house pump-out?","Residential pumping starts at $399.99 (standard 1–3 bed). Work tied to a construction site is discussed when we see access and tank size. Drain field and repair work are quoted after inspection."),
 ("Who should be on site when you arrive?","Someone who can show lid locations, unlock gates, and confirm buried utilities in the work area."),
]
guide("/septic-service-for-builders-and-contractors/","Septic Service for Builders and Contractors in SWFL | Express Septic",
 "Pumping and access guidance for builders, remodelers, and site contractors working around septic tanks and drain fields in Lee, Collier, and Charlotte County. Call (239) 451-3261.",
 "Septic service for builders and contractors",
 "<p><strong>If you are building, remodeling, or running a crew on a lot that already has a septic tank, the drain field is the part of the yard that cannot be treated like extra staging space.</strong> This page is for general contractors, excavation crews, and trade partners who need the tank pumped or need to keep the field intact while other work happens. Express pumps tanks; we quote other system work only after we inspect.</p>"
 "<h2>How do I protect the drain field during construction?</h2>"
 "<p>Find out where the tank and drain field are before the first delivery of fill or equipment. Do not park trucks, store block, or cut a temporary road across the field. Compacted soil and broken laterals are much harder to undo than a marked-off corner of the lot. If you are not sure where the field is, stop and have it located rather than guessing with a skid steer.</p>"
 "<h2>When should a job site call for pumping?</h2>"
 "<p>Call when a temporary facility is on the existing tank, when a house has been occupied through a remodel, or when the tank must be opened before other trades close up the yard. Tell us about mud, fences, and overhead work so we can reach the lids. Buried-lid locating and digging is $100, plus $50 for each additional hour.</p>"
 "<h2>How do new-construction and remodel access differ?</h2>"
 "<p>On a remodel, the tank is often already in a finished yard, sometimes with landscaping over the lids. On an open pad, the risk is equipment traffic more than hidden lids. In both cases we need a clear path for the hose and a contact who knows the lot. We pump both the inlet and outlet compartments when we pump, and we clean an effluent filter at no charge if the tank has one.</p>"
 "<h2>Can you coordinate with the plumber or the owner?</h2>"
 "<p>Yes. Have the site supervisor or the property owner call <a href='tel:"+TEL+"'>"+PHONE+"</a> with the address and the preferred window. Routine visits can also be requested through <a href='"+BOOK+"' rel='noopener' target='_blank'>ServiceM8</a>. If a drain field is already failing, do not assume a pump-out will finish the project; <a href='/drain-field-replacement/'>drain field work is quoted after inspection</a>.</p>",
 BU_FAQ, "Builders and contractors")

PM_FAQ=[
 ("Can you put several properties on a recurring pump-out schedule?","Yes. Call (239) 451-3261 with the addresses and last service dates, and we can set a schedule that you track for the board or owner."),
 ("What should tenants be told about the septic system?","A short house rule: no wipes, grease, or paint down the drains, and call management immediately if drains slow or an odor appears. Our <a href='/first-time-septic-owner/'>first-time guide</a> can be shared as background."),
 ("What does after-hours service cost if a unit backs up at night?","After-hours pumping is $599.99. For a backup, the occupant should stop running water and call us or you should call on their behalf. Do not use the online booking form for an active backup."),
 ("Do HOAs need anything different than a single rental house?","The plumbing is the same idea, but you may be coordinating common-area systems or many lots. Keep a shared log of pump dates and lid locations so a turnover in the board does not lose the map."),
]
guide("/septic-for-property-managers-and-hoas/","Septic Service for Property Managers and HOAs in SWFL | Express Septic",
 "Recurring septic pump-outs, tenant guidance, and after-hours backup service for property managers and HOA boards in Southwest Florida. After-hours pumping is $599.99. Call (239) 451-3261.",
 "Septic service for property managers and HOAs",
 "<p><strong>Property managers and HOA boards are usually the ones who get the call when a tenant or a resident has a slow drain on a Friday night.</strong> This page is about keeping pumping dates, lid locations, and after-hours contacts in one place so you are not starting from zero at each turnover. Express can pump on a recurring schedule and respond when a unit backs up. After-hours pumping is $599.99.</p>"
 "<h2>How should I track septic service across multiple addresses?</h2>"
 "<p>Keep a simple log: address, tank access notes, last pump-out date, and whether a riser is already in place. When a board or owner changes, that log is what you hand off. If dates are missing, treat the tank as overdue and schedule a visit rather than guessing. Residential pumping starts at $399.99 (standard 1–3 bed). An inspection with pump-out is $549.99 when the history is a blank page.</p>"
 "<h2>What belongs in a tenant or resident handout?</h2>"
 "<p>A short list works better than a manual: no wipes (including flushable labels), no grease, no paint or medications down the toilet, and a phone number to call if drains gurgle or the yard is soggy. Point people who want more detail to the <a href='/first-time-septic-owner/'>first-time septic guide</a>. You do not need to teach soil bacteria on move-in day; you need fewer emergency calls.</p>"
 "<h2>How do after-hours backups work for a managed property?</h2>"
 "<p>Tell occupants to stop running water and to call you or <a href='tel:"+TEL+"'>"+PHONE+"</a> directly. Online booking is for routine work, not an active backup. We are open 24 hours, 7 days a week. After-hours pumping is $599.99. More detail is on the <a href='/emergency-septic-backup/'>emergency backup</a> page.</p>"
 "<h2>Can an HOA set a neighborhood-wide pumping reminder?</h2>"
 "<p>Yes, as a policy or a reminder letter, even if each lot is a separate system. A shared calendar for older sections of a community, especially where lids are buried, reduces the number of 'we cannot find the tank' visits. Locating and digging a buried lid is $100, plus $50 for each additional hour. A riser at $299.99 each is often the longer-term fix for those lots.</p>"
 "<p><a class='btn primary' href='tel:"+TEL+"'>Call "+PHONE+"</a> <a class='btn ghost' href='"+BOOK+"' rel='noopener' target='_blank'>Book routine service on ServiceM8<span class='sr'> (opens in a new tab)</span></a></p>",
 PM_FAQ, "Property managers and HOAs")

LL_FAQ=[
 ("Do short-term rentals need pumping more often?","They can. Guest turnover and weekend occupancy can load a tank faster than a full-time household of the same bedroom count. Track actual use and pump on a tighter schedule if the house stays busy. Call (239) 451-3261."),
 ("What house rules help protect a septic tank in an Airbnb?","No wipes, no grease down the kitchen sink, and a note to call the host if drains slow. Put the rule where guests see it, not only in a buried listing paragraph."),
 ("What if a guest reports a backup after checkout?","Treat it as a backup: stop water use, and call us. After-hours pumping is $599.99. Online booking is for planned pump-outs, not an active backup."),
 ("Should I pump between long gaps in reservations?","If the home will sit, or if a packed season is about to start, check the last pump date and schedule service before guests arrive. See also <a href='/snowbird-seasonal-septic/'>seasonal septic care</a>."),
]
guide("/septic-for-landlords-and-short-term-rentals/","Septic Care for Landlords and Airbnb Hosts in SWFL | Express Septic",
 "Septic pumping and guest-use guidance for landlords and short-term rental hosts in Southwest Florida. Busy rentals can need service sooner. After-hours backups are $599.99. Call (239) 451-3261.",
 "Septic care for landlords and Airbnb hosts",
 "<p><strong>A rental or Airbnb on a septic tank has a different risk profile than a family that lives in the house all year.</strong> Guests do not know your rules, weekend groups can run a lot of water, and a backup during a stay becomes your emergency, not theirs. This page is for landlords and hosts. Property managers handling many units may prefer <a href='/septic-for-property-managers-and-hoas/'>the managers and HOA page</a>.</p>"
 "<h2>Why can a short-term rental need pumping sooner?</h2>"
 "<p>The EPA's general 3 to 5 year range for household tanks still applies as a starting point, but a house that sleeps more people on weekends than it was sized for will fill faster. So will a kitchen that sees vacation cooking and a bathroom where guests use wipes. Keep a pump-out date on your turnover calendar, not only in a folder you open when something fails. Residential pumping starts at $399.99 (standard 1–3 bed).</p>"
 "<h2>What should I put in the guest book?</h2>"
 "<p>Three lines are enough: do not flush wipes or paper towels, do not pour grease down the sink, and text the host if a drain is slow or the yard smells. You can link the <a href='/first-time-septic-owner/'>first-time owner guide</a> in a welcome email for long-term tenants who are new to septic. For a one-night stay, the three lines in the bathroom matter more.</p>"
 "<h2>How should I plan around busy season and empty weeks?</h2>"
 "<p>Pump before a heavy reservation stretch if the last service was a long time ago. If the house will sit for months, note the date you return or the next check-in, and do not wait until the afternoon guests arrive. That pattern is close to what snowbird owners do; the <a href='/snowbird-seasonal-septic/'>seasonal return page</a> covers houses that go empty part of the year.</p>"
 "<h2>What do I do if a guest has a backup?</h2>"
 "<p>Ask them to stop using water. Call <a href='tel:"+TEL+"'>"+PHONE+"</a>. After-hours pumping is $599.99. We are open 24 hours. Do not send them to the online booking form while sewage is backing up. Details are on <a href='/emergency-septic-backup/'>emergency septic backup</a>.</p>",
 LL_FAQ, "Landlords and short-term rentals")

CL_FAQ=[
 ("Is this the same as the how-often-to-pump page?","No. That page explains the 3 to 5 year range and the factors that change it. This checklist is a season-by-season list of tasks for Southwest Florida homes. Use both."),
 ("What should I do before the rainy season?","If a pump-out is due, schedule it before summer rains raise the water table. Walk the drain field after a storm later, but do not wait for standing water to think about a full tank."),
 ("What belongs on a monthly once-over?","Look and listen: odors, slow drains, soggy ground, unusually green grass over the field. You do not need to open the tank every month."),
 ("When should the effluent filter be cleaned?","At every pump-out and whenever drains slow. Express cleans it at no charge when we pump. There is no separate monthly interval that fits every house."),
]
guide("/septic-maintenance-checklist/","Southwest Florida Septic Maintenance Checklist | Express Septic",
 "A season-by-season septic checklist for Southwest Florida homes: before rainy season, before guests or snowbird return, and monthly walk-arounds. Call (239) 451-3261 for a pump-out.",
 "Southwest Florida septic maintenance checklist",
 "<p><strong>This is a task list, not another explanation of how often most tanks are pumped.</strong> The <a href='/how-often-to-pump-septic-tank/'>how often to pump</a> page already covers the U.S. EPA SepticSmart 3 to 5 year range and the factors that shorten it. The <a href='/septic-system-maintenance/'>maintenance tips</a> page covers what not to flush. Use this checklist to plan the year in a climate with a rainy season, holiday guests, and houses that sit part of the year.</p>"
 "<h2>What should I do before the summer rainy season?</h2>"
 "<p>If you are due for pumping, or you cannot remember the last date, schedule it before the water table rises. A tank with room in it gives the drain field a better chance when the yard is already wet. Residential pumping starts at $399.99 (standard 1–3 bed). Walk the field after a typical rain later in the season so you know what 'normal wet' looks like for your lot.</p>"
 "<h2>What should I do before guests, holidays, or snowbird return?</h2>"
 "<p>Check the last pump-out date. If a full house is about to arrive and the tank is overdue, pump first. If you are coming back after months away, do the same before you run laundry and showers all day. The <a href='/snowbird-seasonal-septic/'>snowbird page</a> is written for that return; this checklist is the reminder to put it on the calendar.</p>"
 "<h2>What is worth a monthly walk-around?</h2>"
 "<p>Odors, gurgling, slow drains, soggy spots, and grass that is much greener over the drain field than the rest of the yard. You are not opening lids every month. You are noticing change. If something looks wrong, call <a href='tel:"+TEL+"'>"+PHONE+"</a> rather than adding more water to the system.</p>"
 "<h2>What belongs on the annual service visit?</h2>"
 "<p>A pump-out when it is due, filter cleaning (included at no charge when Express pumps), and a conversation about access. If the lid is still buried, consider a riser at $299.99 each so the next visit is faster. If you want a written look at the system as well, an inspection with pump-out is $549.99.</p>"
 "<h2>Where do I go for habits, not dates?</h2>"
 "<p>For what never to flush, water use, and drain field care, stay with the <a href='/septic-system-maintenance/'>maintenance guide</a>. For bacteria, bleach, and additives, use <a href='/septic-bacteria-drain-field/'>good bacteria and the drain field</a>. This page stays on timing.</p>"
 "<p><a class='btn primary' href='tel:"+TEL+"'>Call "+PHONE+"</a> <a class='btn ghost' href='"+BOOK+"' rel='noopener' target='_blank'>Book routine service on ServiceM8<span class='sr'> (opens in a new tab)</span></a></p>",
 CL_FAQ, "Maintenance checklist")

DF_FAQ=[
 ("Does a soggy drain field always mean the field has failed?","No. A full tank, a dirty outlet filter, or a high water table after heavy rain can also leave the yard wet. We start by looking at the tank. Drain field replacement is quoted only after we inspect the system."),
 ("What should I do today if the yard is soggy over the field?","Cut back water use, do not run extra laundry, and call (239) 451-3261. Do not drive on the wet area and do not add fill or more pipe on your own."),
 ("Will a pump-out fix a drain field that is not draining?","It can help if the tank is full and solids or a clogged filter are part of the problem. It will not rebuild a field that has already failed. We will tell you what we see."),
 ("When is replacement even on the table?","Only after an inspection. We do not quote drain field replacement over the phone from a description of wet grass."),
]
guide("/drain-field-not-draining/","Drain Field Not Draining in Southwest Florida | Express Septic",
 "What to do when a septic drain field is soggy, smelly, or not taking water in Southwest Florida. A pump-out may help if the tank is full; replacement is quoted after inspection. Call (239) 451-3261.",
 "What to do when a drain field is not draining",
 "<p><strong>If wastewater is pooling over the drain field, the grass there is suddenly lush and wet, or drains in the house are slow at the same time, stop adding water and call.</strong> This page is about that problem, not a general maintenance overview. A wet field in Southwest Florida can mean a full tank, a dirty filter, a high water table after rain, or a field that is no longer taking water. Those are different problems, and they are not diagnosed from a photo alone.</p>"
 "<h2>What are the signs the field is not taking water?</h2>"
 "<p>Standing water or persistently soggy soil over the drain field, sewage odor in the yard, extra-green grass in that footprint, and slow or backing-up fixtures inside the house can show up together. After a heavy rain, some yards are wet everywhere; a field problem is more likely when the wet or smelly area sits over the drain field and stays after the rest of the lot dries.</p>"
 "<h2>What should I do before anyone arrives?</h2>"
 "<p>Stop laundry, long showers, and dishwasher runs. Do not drive or park on the wet area. Do not trench, add gravel, or 'air out' the field with a homemade fix. Call <a href='tel:"+TEL+"'>"+PHONE+"</a>. If sewage is already backing up inside, treat it as a <a href='/emergency-septic-backup/'>backup</a> and call day or night. After-hours pumping is $599.99.</p>"
 "<h2>Can pumping the tank help a field that looks failed?</h2>"
 "<p>Sometimes. If the tank is full, sludge is escaping, or the effluent filter is clogged, emptying the tank and cleaning the filter can take pressure off the field. Express pumps both compartments and cleans the filter at no charge on pump-outs. If the field itself has failed, a pump-out will not make the soil work like new. <a href='/drain-field-replacement/'>Drain field replacement is quoted after we inspect the system</a>.</p>"
 "<h2>Why is this more common in the rainy season here?</h2>"
 "<p>Sandy soils and a high water table leave less unsaturated soil under many Southwest Florida yards when summer storms sit over the area. A field that was marginal in dry weather can start to show at the surface in those weeks. That is a reason to pump when you are due, not a reason to assume every wet yard needs a new field. For how soil bacteria and the biomat treat effluent, see <a href='/septic-bacteria-drain-field/'>good bacteria and the drain field</a>.</p>",
 DF_FAQ, "Drain field not draining")

EM_FAQ=[
 ("What does after-hours septic pumping cost?","After-hours pumping is $599.99. Call (239) 451-3261. Do not use the online booking form while a backup is happening."),
 ("What should I do until someone arrives?","Stop running water, including laundry and showers. Do not keep flushing 'to see if it cleared.' If sewage is on the floor, keep people and pets away from it."),
 ("Are you open at night and on weekends?","Yes. Express is open 24 hours, 7 days a week for this kind of call."),
 ("Is after-hours service the same as a routine pump-out?","The work is still pumping the tank. The after-hours price is $599.99. Routine residential pumping starts at $399.99 (standard 1–3 bed) when it is not an after-hours emergency visit."),
]
guide("/emergency-septic-backup/","Emergency and After-Hours Septic Backup Pumping in SWFL | Express Septic",
 "Sewage backing up? Stop running water and call Express at (239) 451-3261, day or night. After-hours septic pumping is $599.99. Online booking is for routine service only.",
 "Emergency and after-hours septic backup pumping",
 "<p><strong>If sewage is coming back up a drain or toilet, stop running water and call <a href='tel:"+TEL+"'>"+PHONE+"</a> now.</strong> Do not request a time on the booking form while a backup is in progress. Express is open 24 hours, 7 days a week. After-hours pumping is $599.99.</p>"
 "<h2>What counts as a backup that should be called in immediately?</h2>"
 "<p>Wastewater rising in a shower, toilet, or floor drain; sewage on the floor; or a sudden, strong sewage odor with fixtures that will not drain. Gurgling alone is a warning, but standing sewage is an emergency visit, not a 'maybe next week' pump-out.</p>"
 "<h2>What should I do in the house while I wait?</h2>"
 "<p>Turn off anything that adds water: laundry, dishwashers, ice makers, and showers. Avoid flushing. Keep children and pets away from spilled sewage. If you can, note whether one fixture is affected or several, and whether the problem started after heavy rain. That information helps when you call, but it should not delay the call.</p>"
 "<h2>What will we do when we arrive?</h2>"
 "<p>We access the tank and pump it, including both the inlet and outlet compartments, and we clean the effluent filter at no charge if the tank has one. A pump-out often relieves a backup caused by a full tank. If the drain field is not taking water, we will tell you what we see; further work is quoted after inspection, not invented on the spot.</p>"
 "<h2>How is after-hours pricing different from a planned visit?</h2>"
 "<p>After-hours pumping is $599.99. Planned residential pumping starts at $399.99 (standard 1–3 bed). If you have a slow drain but no backup, you can still call, or you can <a href='"+BOOK+"' rel='noopener' target='_blank'>request a routine time on ServiceM8</a> once it is clearly not an active overflow. For wet yards without an indoor overflow, see <a href='/drain-field-not-draining/'>drain field not draining</a>.</p>",
 EM_FAQ, "Emergency septic backup")

CO_FAQ=[
 ("Do you pump septic tanks at churches, schools, and RV parks?","Yes. We provide commercial septic tank pumping for churches, schools, RV parks, and similar properties in our service area. Call (239) 451-3261 to talk through the tank and the schedule."),
 ("Is the residential $399.99 starting price for a large commercial tank?","No. Residential pumping starts at $399.99 for a standard 1–3 bedroom home. Commercial tanks and busier sites are quoted for that system and its use."),
 ("Can we set a recurring schedule around services, school terms, or seasonal occupancy?","Yes. Tell us when the property is busiest so pump-outs are not left until a weekend event or a full park weekend."),
 ("What if we have a backup during an event?","Call (239) 451-3261. After-hours pumping is $599.99. Do not use the online booking form during an active backup."),
]
guide("/commercial-septic-churches-schools-rv-parks/","Commercial Septic Pumping for Churches, Schools, and RV Parks | Express Septic",
 "Commercial septic tank pumping for churches, schools, and RV parks in Southwest Florida. Quoted for your tank and use. After-hours backups are $599.99. Call (239) 451-3261.",
 "Commercial septic pumping for churches, schools, and RV parks",
 "<p><strong>Churches, schools, and RV parks put a different kind of load on a septic tank than a single-family house.</strong> Use often clusters around services, school days, weekends, or seasonal occupancy, then drops. This page is for those sites. It is not a restaurant grease-trap guide; kitchens with interceptors should use <a href='/grease-trap-pumping/'>grease trap and interceptor pumping</a>. General commercial pumping background is also on <a href='/commercial-septic-tank-pumping/'>commercial septic tank pumping</a>.</p>"
 "<h2>Why do these properties need a planned schedule instead of 'every few years'?</h2>"
 "<p>A church that is quiet on weekdays and full on Sunday, a school with long breaks, or an RV park that fills in winter can send a lot of water through the tank in a short window. The EPA's household 3 to 5 year range is not a good sole guide here. We set a recurring pump-out around how the property is actually used, then adjust if events or occupancy change.</p>"
 "<h2>How is this priced?</h2>"
 "<p>Commercial pumping is quoted for your tank size and use. The published residential starting price of $399.99 applies to a standard 1–3 bedroom home, not automatically to a large commercial tank. After-hours pumping is $599.99 if you have a backup outside routine hours. We will ask about access, tank size if you know it, and the last service date when you call <a href='tel:"+TEL+"'>"+PHONE+"</a>.</p>"
 "<h2>What should a facilities manager have ready?</h2>"
 "<p>Gate codes, lid locations, a contact who can meet the truck, and any rules about working around worship times, school pickup, or campers. If lids are buried in a lawn or gravel lot, locating and digging is $100, plus $50 for each additional hour. A riser at $299.99 each is often worth it on a site that will be pumped on a regular route.</p>"
 "<h2>What about dump stations or unusually heavy weekend use?</h2>"
 "<p>Tell us if the tank receives waste from an RV dump station or from a hall that hosts large events. Those details change how often the tank needs to be emptied. We pump inlet and outlet compartments and can set reminders so the next event does not start with a full tank.</p>",
 CO_FAQ, "Churches, schools, and RV parks")

HU_FAQ=[
 ("Should I always pump the tank before every named storm?","Not automatically. If a pump-out is already due, or the tank is close to full, pumping before a storm can help. If the tank was recently emptied, a special trip is not a rule we invent for every forecast. Call (239) 451-3261 if you are unsure."),
 ("Can I use the septic system while the yard is flooded?","Do not use it while standing water covers the tank or drain field. Wait until the water recedes, then have the system checked before you return to normal use."),
 ("What should I do after a hurricane or flood?","Stay off a saturated drain field, watch for electrical hazards if you have pumps or an alarm, and call us when you can reach the lids safely. We will tell you what we see; we do not quote a repair from a storm photo alone."),
 ("Is after-hours pumping available during storm recovery?","We are open 24 hours, 7 days a week. After-hours pumping is $599.99. Call (239) 451-3261."),
]
guide("/hurricane-and-flood-septic-prep/","Hurricane and Flood Septic Prep in Southwest Florida | Express Septic",
 "What to do with a septic system before and after a hurricane or flood in Southwest Florida: when to pump, when not to use a flooded system, and how to reach Express at (239) 451-3261.",
 "Hurricane and flood septic prep",
 "<p><strong>A hurricane or a long flood changes how you should treat a septic system, but it does not require a special ritual for every storm on the map.</strong> This page is about when to pump beforehand, what not to do while the yard is underwater, and how to come back to the system safely. It is not a promise of emergency response times, and it is not a rule that every house must be pumped the day a watch is issued.</p>"
 "<h2>What should I do before a storm if I have time?</h2>"
 "<p>If the tank is due, or you know it is close to full, schedule a pump-out before heavy rain if we can reach you. A tank with room in it is less likely to overflow when the water table rises. Residential pumping starts at $399.99 (standard 1–3 bed). If you just had the tank pumped, you do not need a second trip just because a forecast changed. Call <a href='tel:"+TEL+"'>"+PHONE+"</a> if you want a straight answer for your last service date.</p>"
 "<h2>What should I do while the lot is flooded?</h2>"
 "<p>Do not run water into a system whose tank or drain field is under standing water. Keep vehicles off the field. If you have a pump, alarm, or electrical components at a lift station, treat water and power as a safety issue and do not wade in to inspect them yourself. More on indoor backups is at <a href='/emergency-septic-backup/'>emergency septic backup</a>.</p>"
 "<h2>What should I do after the water goes down?</h2>"
 "<p>Wait until you can reach the lids without standing in floodwater. Then have the system checked before you return to full household use, especially if the house took on water or the field stayed submerged. We pump both compartments when we pump, and we clean the effluent filter at no charge. Damage beyond a full tank, including drain field work, is quoted after we inspect, not estimated from a storm report.</p>"
 "<h2>Why does flooding matter so much here?</h2>"
 "<p>Southwest Florida yards often sit on sandy soil with a water table that is already high in the rainy season. A storm surge or long rain on top of that can saturate a drain field that was working in dry weather. Pumping when you are due is one of the few steps you can take in advance. Afterward, patience and an inspection matter more than rushing water through a still-soggy field.</p>",
 HU_FAQ, "Hurricane and flood prep")

SN_FAQ=[
 ("When should a snowbird pump, before leaving or after coming back?","If a pump-out is due, do it before you leave, or as soon as you return and before several days of heavy use. Call (239) 451-3261 and tell us which end of the season you are in."),
 ("The house sat empty for months. Can I just start using everything?","Check the last pump date first. If you do not know it, schedule a pump-out or an inspection with pump-out ($549.99) before you run many loads of laundry and long showers."),
 ("Do seasonal homes follow the same 3 to 5 year range?","That EPA range is still a starting point, but months of empty time plus a busy winter can change when the tank actually needs service. Track occupancy, not only the calendar."),
 ("The lid is buried and I am only in town for a short stay. What then?","Tell us that when you call. Locating and digging a buried lid is $100, plus $50 for each additional hour. A riser at $299.99 each makes the next return easier."),
]
guide("/snowbird-seasonal-septic/","Snowbird and Seasonal Septic Care in Southwest Florida | Express Septic",
 "Septic guidance for snowbirds and seasonal residents in Southwest Florida: when to pump before you leave or after you return, and what to do if the house sat empty. Call (239) 451-3261.",
 "Snowbird and seasonal septic care",
 "<p><strong>If you spend only part of the year in a Southwest Florida home on a septic tank, the calendar that matters is your occupancy, not a year-round household's routine.</strong> This page is for snowbirds, seasonal residents, and anyone who closes a house for months and then returns to showers, laundry, and company. It is not the same problem as a weekend Airbnb; hosts can see <a href='/septic-for-landlords-and-short-term-rentals/'>landlords and short-term rentals</a>.</p>"
 "<h2>Should I pump before I leave or when I get back?</h2>"
 "<p>If a pump-out is already due, have it done before you lock up, so the tank is not sitting full through the off months and you are not hunting for a truck the afternoon you land. If you ran out of time in the spring, schedule service as soon as you return and before you fill the house with several days of water use. Residential pumping starts at $399.99 (standard 1–3 bed). Call <a href='tel:"+TEL+"'>"+PHONE+"</a> or <a href='"+BOOK+"' rel='noopener' target='_blank'>request a routine visit on ServiceM8</a> ahead of your flight when you can.</p>"
 "<h2>What is risky about coming back to a house that sat empty?</h2>"
 "<p>The tank may still be holding sludge from last season. A week of catching-up laundry and long showers can push that load toward the drain field. If you have no record of the last pump-out, treat the system as unknown: an inspection with pump-out is $549.99. If the lid is buried after a summer of grass growth, locating and digging is $100, plus $50 for each additional hour.</p>"
 "<h2>How do I plan around a short stay?</h2>"
 "<p>Book the visit before you arrive, leave a gate code or a neighbor who can meet the truck, and consider a riser ($299.99 each) if every visit starts with a shovel. A <a href='/septic-maintenance-checklist/'>seasonal checklist</a> can sit on the fridge for the next departure. If you return to a backup, skip the form and call; after-hours pumping is $599.99.</p>"
 "<h2>Does a high water table change the off-season plan?</h2>"
 "<p>If you leave at the start of the rainy season and the tank is already due, pump before you go. Sandy soil and a high water table are harder on a drain field when the tank is full and storms pass over an empty house you cannot watch. That is timing, not a different kind of tank. For storm-specific steps, use <a href='/hurricane-and-flood-septic-prep/'>hurricane and flood septic prep</a>.</p>",
 SN_FAQ, "Snowbird and seasonal septic")

page("/how-often-to-pump-septic-tank/","How Often Should You Pump Your Septic Tank? | Express Septic","How often to pump a septic tank: EPA says every 3-5 years for most homes. See our pumping frequency chart by tank size and household size.","How Often Should You Pump Your Septic Tank?",
 "<p>The U.S. EPA recommends that most household septic tanks be pumped every 3 to 5 years, and that systems be inspected by a professional at least every 3 years. Your exact schedule depends on tank size, how many people live in the home and how much water you use.</p>"
 "<h2>Septic Pumping Frequency Chart</h2><p>Estimated years between pumpings, based on a widely published university extension estimate. A general guide only; an inspection tells you what your tank actually needs.</p>"+"<div class='tw'><table><tr><th>Tank size</th><th>1 person</th><th>2 people</th><th>3 people</th><th>4 people</th><th>5 people</th><th>6 people</th></tr><tr><td>500 gal</td><td>5.8 yrs</td><td>2.6 yrs</td><td>1.5 yrs</td><td>1.0 yrs</td><td>0.7 yrs</td><td>0.4 yrs</td></tr><tr><td>750 gal</td><td>9.1 yrs</td><td>4.2 yrs</td><td>2.6 yrs</td><td>1.8 yrs</td><td>1.3 yrs</td><td>1.0 yrs</td></tr><tr><td>1,000 gal</td><td>12.4 yrs</td><td>5.9 yrs</td><td>3.7 yrs</td><td>2.6 yrs</td><td>2.0 yrs</td><td>1.5 yrs</td></tr><tr><td>1,250 gal</td><td>15.6 yrs</td><td>7.5 yrs</td><td>4.8 yrs</td><td>3.4 yrs</td><td>2.6 yrs</td><td>2.0 yrs</td></tr><tr><td>1,500 gal</td><td>18.9 yrs</td><td>9.1 yrs</td><td>5.9 yrs</td><td>4.2 yrs</td><td>3.3 yrs</td><td>2.6 yrs</td></tr></table></div>"+
 "<h2>Factors That Change How Often You Pump</h2><ul><li><strong>Garbage disposal:</strong> adds solids; the EPA notes disposals can significantly increase sludge and scum, so pump more often.</li><li><strong>Water use:</strong> heavy laundry, long showers and leaks push more water through the tank.</li><li><strong>Household size:</strong> more people means faster buildup.</li><li><strong>Seasonal and rental homes in Southwest Florida:</strong> snowbird homes and vacation rentals can see heavy use in season and with guests, so rentals may need pumping more often than household size suggests.</li><li><strong>Florida rainy season:</strong> high water tables stress drain fields, so a pumped tank helps.</li></ul>"
 "<h2>Signs Your Tank Is Due Now</h2><ul><li>Slow drains or gurgling pipes</li><li>Sewage odors inside or outside</li><li>Soggy ground or extra-green grass over the drain field</li><li>Toilets or drains backing up</li><li>More than 3–5 years since the last pump-out, or you don't know</li></ul>"
 "<p>Read our <a href='/septic-system-maintenance/'>septic system maintenance guide</a> or see <a href='/how-it-works/'>how our service works</a>.</p><h2>Our Services</h2>"+svc_list)
CREW_ABOUT=CREW.replace('alt="Express Septic Tank Pumping crew with the 4,200-gallon vacuum truck"','alt="ORyan Atkinson, owner of Express Septic Tank Pumping (right, in the cap), with a crew member and the 4,200-gallon truck"').replace("</figure>","<figcaption>ORyan Atkinson, owner (right, in the cap), with a crew member</figcaption></figure>")
page("/about/","About Express Septic Tank Pumping | Honest, Reliable Septic Service","Express Septic Tank Pumping is an Estero-based septic company built on honesty, reliability, fair rates and great customer service. Call (239) 451-3261.","About Express Septic Tank Pumping",
 CREW_ABOUT+"<p>Express Septic Tank Pumping is a local septic service company based in Estero, Florida, serving homes and businesses across Lee and Collier County.</p><h2>What We Stand For</h2><ul><li><strong>Honesty.</strong> Upfront pricing and straight answers about your system — no surprises.</li><li><strong>Reliability.</strong> We show up on time and do the job right.</li><li><strong>Fairness.</strong> Fair rates for the work you actually need.</li><li><strong>Customer service.</strong> Treating customers right is our top priority.</li></ul><h2>Licensed &amp; Experienced</h2><p>"+LICENSE_BODY+"</p><h2>Our Services</h2>"+svc_list+"<p>See <a href='/how-it-works/'>how it works</a>.</p>")
page("/commercial-grease-trap-service/","Commercial Grease Trap Service in Southwest Florida | Express Septic",
 "A short overview of commercial grease trap service for restaurants in Fort Myers, Cape Coral, Bonita Springs, Naples, Estero and across Lee, Collier and Charlotte County. See our main grease trap and interceptor pumping page for full details. Call (239) 451-3261.",
 "Commercial grease trap service in Southwest Florida",
 REAR+"<p><strong>This is a short overview.</strong> Our main page for restaurants and food service is <a href='/grease-trap-pumping/'>grease trap and interceptor pumping</a>, covering in-ground interceptors and indoor traps in Fort Myers, Cape Coral, Bonita Springs, Naples, Estero and across Lee, Collier and Charlotte County, plus LaBelle.</p>"
 "<p>Restaurants and commercial kitchens need their grease traps pumped before fats, oils and grease build up and cause backups, odors or problems with the drain line. Express can set up a one-time pump-out or a recurring schedule. $695 for a 1,000-gallon grease trap or interceptor; other sizes are quoted.</p>"
 "<h2>Lee County interceptor pumping rule</h2>"
 "<p><a href='https://www.leegov.com/bocc/Ordinances/14-24.pdf' rel='noopener'>Lee County Ordinance 14-24</a> requires grease interceptors to be fully pumped at least every 90 calendar days. Indoor grease traps must be cleaned at least weekly or whenever grease and solids exceed 20% of the unit volume. We can set up a recurring pump-out schedule. Details are on the <a href='/grease-trap-pumping/'>grease trap and interceptor pumping</a> page.</p>"
 +SIDE+"<p>Our 4,200-gallon truck has a split tank, one side for septic and one side for grease, so grease trap loads and septic loads never mix.</p>"
 "<h2>One-time or recurring</h2><p>Some businesses call us when a trap is full. Most are better off on a recurring schedule based on how much cooking they do and the size of the trap. Tell us about your kitchen and we'll talk through how often makes sense.</p>"
 "<p><a class='btn primary' href='tel:"+TEL+"'>Call about recurring service · "+PHONE+"</a></p>"
 "<h2>Signs your grease trap needs service</h2><ul><li>Slow sinks or floor drains in the kitchen</li><li>Grease or odors around the trap lid</li><li>It's been longer than your usual schedule since the last pump-out</li></ul>"
 "<h2>What to have ready when you call</h2><ul><li>Business name and address</li><li>Where the trap is and how it's accessed</li><li>Trap size, if you know it</li><li>When it was last pumped</li></ul>"
 "<h2>Other services</h2>"+svc_list,
 [{"@context":"https://schema.org","@type":"Service","name":"Commercial Grease Trap Service","serviceType":"Grease trap pumping","description":"Short overview of grease trap pumping for restaurants and commercial kitchens in Southwest Florida. See grease trap and interceptor pumping for full details.","url":BASE+"/grease-trap-pumping/","audience":{"@type":"BusinessAudience","name":"Restaurants and commercial kitchens"},"provider":PROV,"areaServed":[{"@type":"AdministrativeArea","name":"Lee County, FL"},{"@type":"AdministrativeArea","name":"Collier County, FL"},{"@type":"AdministrativeArea","name":"Charlotte County, FL"}]},
  crumbs_ld([("Home",BASE+"/"),("Grease Trap & Interceptor Pumping",BASE+"/grease-trap-pumping/"),("Commercial grease trap service",BASE+"/commercial-grease-trap-service/")])],
 trail=[("Home","/"),("Grease Trap & Interceptor Pumping","/grease-trap-pumping/"),("Commercial grease trap service","/commercial-grease-trap-service/")],
 canonical=BASE+"/grease-trap-pumping/")
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
 faq_ld(FAQ))
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
 "".join(f"<section class='job' id='{j['id']}'><h2>{j['city']}: {j['title']}</h2><p class='jdate'>{j['date']}</p><p><strong>What we found:</strong> {j['found']}</p><p><strong>What we did:</strong> {j['done']}</p>"+job_shots(j)+f"<p><a href='/{slug(j['city'])}/'>Septic service in {j['city']}</a></p></section>" for j in JOBS)+
 "<p>Need your tank pumped? Call <a href='tel:"+TEL+"'>"+PHONE+"</a> or see <a href='/residential-septic-tank-pumping/'>residential septic pumping</a>.</p>",
 {"@context":"https://schema.org","@type":"ItemList","name":"Completed septic jobs","itemListElement":[{"@type":"ListItem","position":k+1,"url":f"{BASE}/completed-jobs/#{j['id']}","name":f"{j['city']}: {j['title']}"} for k,j in enumerate(JOBS)]})
ROBOTS["/404/"]='<meta name="robots" content="noindex">'
page("/404/","Page not found | Express Septic Tank Pumping","Page not found.","Page not found","<p>That page doesn't exist. Try the <a href='/'>home page</a>, <a href='/service-area/'>service area</a>, or call <a href='tel:"+TEL+"'>"+PHONE+"</a>.</p>")
PAGES.remove("/404/")
h=open("404/index.html").read().replace('<link rel="canonical" href="'+BASE+'/404/">','').replace('<meta property="og:url" content="'+BASE+'/404/">','').replace('href="../','href="/').replace('src="../','src="/').replace(', ../',', /').replace('srcset="../','srcset="/').replace("href='../","href='/")
open("404.html","w").write(h); shutil.rmtree("404")
shutil.copy("src/styles.css","styles.css"); shutil.copy("src/site.js","site.js")
open("sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{BASE}{p}</loc><lastmod>{TODAY}</lastmod></url>" for p in PAGES)+"</urlset>\n")
# Sitemap index: static pages + ServiceTechHub Project Showcase (served by functions/ once configured)
open("sitemap-index.xml","w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><sitemap><loc>{BASE}/sitemap.xml</loc></sitemap></sitemapindex>\n')
open("robots.txt","w").write("User-agent: *\nAllow: /\n\n""User-agent: GPTBot\nAllow: /\n\n""User-agent: PerplexityBot\nAllow: /\n\n""User-agent: ClaudeBot\nAllow: /\n\n""User-agent: Google-Extended\nAllow: /\n\n""User-agent: OAI-SearchBot\nAllow: /\n\n"f"Sitemap: {BASE}/sitemap-index.xml\nSitemap: {BASE}/sitemap.xml\n")
print("\n".join(PAGES))
# llms.txt: plain-text facts for AI assistants (same NAP and prices as the pages).
LL=[f"# {NAME}","",f"> Owner-operated septic tank pumping company based in Estero, Florida, serving Lee, Collier and Charlotte County plus LaBelle (Hendry County). Residential septic pumping starts at $399.99.","",
"## Contact",f"- Business: {NAME} LLC",f"- Address: 23357 Olde Meadowbrook Circle, Estero, FL 34134",f"- Phone: {PHONE}","- Hours: open 24 hours, 7 days a week",f"- Email: {EMAIL}",
f"- Online requests: {BOOK} (a request; the business contacts the customer to confirm a time)",f"- Google reviews: {REVIEWS_READ}","",
"## Services and prices",f"- [Residential septic tank pumping]({BASE}/residential-septic-tank-pumping/): from $399.99. {PRICE_COND}",
f"- [Septic tank riser installation]({BASE}/septic-tank-riser-installation/): 6-inch risers $299.99 each. A riser brings the tank lid up to ground level so future pump-outs don't need digging.",
"- Buried lid locating and digging: $100, plus $50 for each additional hour",
"- After-hours pumping: $599.99",
f"- [Commercial grease trap service]({BASE}/commercial-grease-trap-service/): short overview of commercial grease trap service in Southwest Florida. The main page is [grease trap and interceptor pumping]({BASE}/grease-trap-pumping/).",
f"- [Septic repair]({BASE}/septic-repair/): quoted after we look at the system. Repair work performed under Florida Certified Plumbing Contractor Raymond F. Dibble, License #CFC020332.",
f"- [Drain field replacement]({BASE}/drain-field-replacement/): quoted after we inspect the system. The work is performed under FL Certified Plumbing Contractor Raymond F. Dibble, License #CFC020332.",
f"- [Lift station pumping]({BASE}/lift-station-pumping/): Express pumps lift stations in Estero and across Southwest Florida. Quoted after we inspect the system. Call (239) 451-3261.",
f"- [Grease trap and interceptor pumping]({BASE}/grease-trap-pumping/): main page for restaurants and food service in Fort Myers, Cape Coral, Bonita Springs, Naples, Estero and across Lee, Collier and Charlotte County, plus LaBelle, including in-ground grease interceptors and indoor traps. $695 for a 1,000-gallon grease trap or interceptor; other sizes are quoted. We can set up a recurring pump-out schedule. The 4,200-gallon truck is split for septic and grease, so the two never mix. Lee County Ordinance 14-24 requires grease interceptors to be fully pumped at least every 90 calendar days. Indoor grease traps must be cleaned at least weekly or whenever grease and solids exceed 20% of the unit volume. Florida Statute 403.0741 requires a signed grease waste service manifest for every pump-out. Call (239) 451-3261.",
f"- [Commercial septic tank pumping]({BASE}/commercial-septic-tank-pumping/): call for a quote.",f"- [Septic inspections]({BASE}/septic-inspections/): septic inspection with pump-out $549.99.","",
"## Credentials","- Work performed under Florida Certified Plumbing Contractor Raymond F. Dibble, License #CFC020332, licensed since 1981.","- USDOT 6673233. Truck: 4,200-gallon split tank, one side for septic and one for grease.","",
"## Main service-area pages"]+[f"- [{c}, FL]({BASE}/{slug(c)}/)" for c in CITY_PLUS]+[f"- [All areas]({BASE}/service-area/)","",
"## How we stand apart",
"- If we commit to a same-day pump-out, we keep working into the night until every scheduled job is done.",
"- We pump both the inlet and the outlet compartments. Some companies only pump the inlet.",
"- We clean your filter at no charge on pump-outs and show you how to keep it clean.","",
"## More",f"- [Completed jobs]({BASE}/completed-jobs/)",f"- [FAQ]({BASE}/faq/)",f"- [Septic filter care]({BASE}/septic-filter-care/): If a tank has an effluent filter, it should be checked and cleaned at every pump-out and whenever drains slow. Express cleans the filter at no charge on pump-outs and can show you how to keep it clean. A dirty filter can cause backups or slow drains, and wastewater can be pushed back into the house.",f"- [Why good bacteria protect your septic tank and drain field]({BASE}/septic-bacteria-drain-field/): Anaerobic bacteria in the tank break down solids and form sludge and scum layers. Aerobic bacteria and the biomat in drain-field soil treat effluent before it reaches groundwater. That matters in Southwest Florida's sandy soils and high water table. A healthy system normally gets the bacteria it needs from household waste; additives do not replace pumping. Express cleans the effluent filter at no charge on pump-outs.",f"- [How often to pump]({BASE}/how-often-to-pump-septic-tank/)",
f"- [First time with a septic system]({BASE}/first-time-septic-owner/): complete guide for Southwest Florida homeowners new to septic tanks.",
f"- [Septic guide for Realtors]({BASE}/septic-guide-for-realtors/)",
f"- [Buying or selling a home with a septic tank]({BASE}/buying-or-selling-a-home-with-septic/)",
f"- [Septic service for builders and contractors]({BASE}/septic-service-for-builders-and-contractors/)",
f"- [Septic service for property managers and HOAs]({BASE}/septic-for-property-managers-and-hoas/)",
f"- [Septic care for landlords and Airbnb hosts]({BASE}/septic-for-landlords-and-short-term-rentals/)",
f"- [Southwest Florida septic maintenance checklist]({BASE}/septic-maintenance-checklist/)",
f"- [Drain field not draining]({BASE}/drain-field-not-draining/)",
f"- [Emergency and after-hours septic backup]({BASE}/emergency-septic-backup/): after-hours pumping is $599.99. Call (239) 451-3261. Do not use the online booking form during a backup.",
f"- [Commercial septic pumping for churches, schools, and RV parks]({BASE}/commercial-septic-churches-schools-rv-parks/): quoted for your tank and use. The residential starting price of $399.99 does not automatically apply to large commercial tanks.",
f"- [Hurricane and flood septic prep]({BASE}/hurricane-and-flood-septic-prep/)",
f"- [Snowbird and seasonal septic care]({BASE}/snowbird-seasonal-septic/)",
f"- [About]({BASE}/about/)",""]
open("llms.txt","w").write("\n".join(LL))
