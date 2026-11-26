"""Shared 10DLC legal pages + quote form for Express Septic Tank Pumping LLC brand sites.
Copied section for section from the APPROVED reference (xpressseptictankpumpinglehighacres.com
/privacy-policy/ and /terms/, campaign CB9XKZB approved 2026-11-17), with brand details swapped.
Plain static HTML only (carrier reviewers must see it without JS)."""
import html as H

LAST_UPDATED = "November 26, 2026"   # one consistent date across all rebuilt sites
EFFECTIVE = "November 26, 2026"
LLC = "Express Septic Tank Pumping LLC"

def _e(s): return H.escape(s, True)

class Brand:
  def __init__(self, name, phone, tel, email, street, city, region, zip, base,
               service="septic tank pumping and related local services",
               appt="septic pumping", svc_info="property details, septic system details",
               form_where="the quote/request form", form_tech=None, hosting="Cloudflare Pages",
               book_reply="to request service", is_llc=False, emerg="Septic backing up right now?", quote_paths=("/", "/contact/")):
    self.__dict__.update(locals()); del self.__dict__["self"]
    self.base = base.rstrip("/")
    self.aka = "" if is_llc else f" (also operating as {name})"
    self.prog = f"{name} Customer Notifications" if is_llc else f"Express Septic Tank Pumping / {name} Customer Notifications"
  @property
  def ph(self): return f'<a href="tel:{self.tel}">{_e(self.phone)}</a>'
  @property
  def mail(self): return f'<a href="mailto:{self.email}">{self.email}</a>'
  def url(self, p=""): u = self.base + p; return f'<a href="{u}">{u}</a>'

def operated_line(b):
  return (f'<p class="express-operator">Operated by {LLC} · Call <a href="tel:{b.tel}" style="display:inline">{_e(b.phone)}</a>'
          f' · <a href="sms:{b.tel}?&amp;body=BOOK" style="display:inline">Text BOOK</a></p>')

def sms_optin_html(b):
  """Text BOOK CTA, same structure as the approved Xpress 'Book by text' block."""
  sender = LLC if b.is_llc else f"{_e(b.name)}, operated by {LLC},"
  return ('<div class="sms-optin-block">'
    + operated_line(b) +
    f'<p class="sms-optin"><strong><a href="sms:{b.tel}?&amp;body=BOOK" style="display:inline">Text BOOK to {_e(b.phone)}</a></strong> {b.book_reply}. '
    'If BOOK doesn&rsquo;t fill in automatically, type BOOK in the message. '
    f'By texting BOOK, you agree to receive text messages from {sender} about your booking request. '
    'Msg &amp; data rates may apply. Msg frequency varies. Reply HELP for help, STOP to opt out. '
    'Consent is not a condition of purchase. See our <a href="/privacy-policy/" style="display:inline">Privacy Policy</a> and <a href="/terms/" style="display:inline">SMS Terms</a>.</p>'
    '</div>')

def consent_text(b):
  sender = LLC if b.is_llc else f"{_e(b.name)}, operated by {LLC},"
  return (f'I agree to receive text messages from {sender} at the number provided about my quote, appointment scheduling, '
          'arrival times and service updates. Msg frequency varies. Msg &amp; data rates may apply. Reply HELP for help, STOP to opt out. '
          'Consent is not a condition of purchase. See our <a href="/privacy-policy/">Privacy Policy</a> and <a href="/terms/">SMS Terms</a>.')

def consent_box(b):
  """Unchecked, optional SMS consent checkbox: same markup and wording as the live Xpress form."""
  return ('<div class="sms-consent" id="sms-consent"><label for="sms-consent-checkbox">'
          '<input type="checkbox" id="sms-consent-checkbox" name="sms_consent" value="yes">'
          f'<span>{consent_text(b)}</span></label></div>')

def quote_form_html(b, services):
  return "<style>" + FORM_CSS + "</style>" + _quote_form_html(b, services)
def _quote_form_html(b, services):
  """Native quote/request form. No server backend: submitting opens the visitor's email app
  addressed to the brand inbox (mailto), with the SMS consent answer written into the email."""
  opts = "".join(f'<option>{_e(s)}</option>' for s in services)
  return f'''<div class="quote-wrap" id="quote"><div class="form-card request-card">
<h2>Request service or a quote</h2>
<p class="form-intro">Send us your request and we'll confirm your appointment.</p>
<form class="quote-form" id="quote-form" action="mailto:{b.email}" method="post" enctype="text/plain" data-to="{b.email}" data-brand="{_e(b.name)}">
<div class="qf-row"><label for="qf-name">Name</label><input id="qf-name" name="name" autocomplete="name" required></div>
<div class="qf-row"><label for="qf-phone">Mobile phone</label><input id="qf-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required></div>
<div class="qf-row"><label for="qf-email">Email <span class="opt">(optional)</span></label><input id="qf-email" name="email" type="email" autocomplete="email"></div>
<div class="qf-row"><label for="qf-addr">Service address</label><input id="qf-addr" name="address" autocomplete="street-address" required></div>
<div class="qf-row"><label for="qf-svc">What do you need?</label><select id="qf-svc" name="service">{opts}</select></div>
<div class="qf-row"><label for="qf-msg">Details <span class="opt">(optional)</span></label><textarea id="qf-msg" name="details" rows="4"></textarea></div>
{consent_box(b)}
<button class="btn solid qf-submit" type="submit">Send request</button>
</form>
<p class="form-note">Sending opens your email app with your request addressed to {b.mail}. {b.emerg} Please call {b.ph} instead. See our <a href="/privacy-policy/">privacy policy</a> and <a href="/terms/">SMS terms</a>.</p>
</div></div>
<script>
(function(){{var f=document.getElementById('quote-form');if(!f)return;f.addEventListener('submit',function(ev){{
if(!f.reportValidity||f.reportValidity()){{ev.preventDefault();var g=function(n){{var el=f.elements[n];return el?el.value.trim():''}};
var c=document.getElementById('sms-consent-checkbox').checked;
var lines=['Name: '+g('name'),'Mobile phone: '+g('phone'),'Email: '+g('email'),'Service address: '+g('address'),'Service: '+g('service'),'Details: '+g('details'),'',
'SMS consent checkbox: '+(c?'CHECKED (agreed to receive text messages)':'not checked (no text messages)'),
'Consent wording shown: '+document.querySelector('#sms-consent span').textContent.trim(),'Submitted from: '+location.href+' on '+new Date().toString()];
location.href='mailto:'+f.dataset.to+'?subject='+encodeURIComponent('Quote request - '+g('name')+' - '+f.dataset.brand)+'&body='+encodeURIComponent(lines.join('\\n'));}}}});}})();
</script>'''

def privacy_body(b):
  """Approved reference /privacy-policy/ sections 1-12, brand-swapped."""
  return f'''<div class="prose legal-doc">
<p><strong>EXPRESS SEPTIC TANK PUMPING LLC</strong>{_e(b.aka)}<br>
Effective Date: {EFFECTIVE}<br>
Last Updated: {LAST_UPDATED}</p>
<p>Website: {b.url("/")}<br>
SMS Terms &amp; Conditions: {b.url("/terms")}</p>

<h2>1. Who We Are</h2>
<p>This Privacy Policy describes how {LLC} ("{_e(b.name)}," "we," "us," or "our") collects, uses, and protects personal information when you visit our website at {b.url("/")}, call us, text us, submit a form, or otherwise use our services.</p>
<p>{LLC} is a Florida limited liability company providing {b.service}. {"This policy covers " + LLC + "." if b.is_llc else "This policy covers " + LLC + ", including the " + _e(b.name) + " brand used on this site."}</p>
<ul>
<li>Business address: {_e(b.street)}, {_e(b.city)}, {b.region} {b.zip}</li>
<li>Phone: {_e(b.phone)}</li>
<li>Email: {b.mail}</li>
</ul>

<h2>2. Information We Collect</h2>
<p>We may collect the following categories of information:</p>
<ul>
<li><strong>Contact information:</strong> name, mobile and other phone numbers, email address, and service or billing address.</li>
<li><strong>Service information:</strong> {b.svc_info}, service requests, appointment dates and times, job notes, and service history.</li>
<li><strong>Communications:</strong> records of phone calls, text messages, emails, and website form submissions you send to us, including your SMS opt-in and opt-out status.</li>
<li><strong>Payment information:</strong> information needed to invoice and collect payment. Card payments are processed by third-party payment processors; we do not store full card numbers.</li>
<li><strong>Website information:</strong> basic technical data such as IP address, browser type, pages visited, and referring pages, collected through standard server logs and cookies.</li>
</ul>
<p>We collect this information directly from you (by phone, text, email, or our website contact form) and automatically when you use our website.</p>

<h2>3. How We Use Your Information</h2>
<p>We use personal information to:</p>
<ul>
<li>Respond to inquiries and provide quotes;</li>
<li>Schedule, confirm, and remind you of service appointments;</li>
<li>Follow up on missed calls and service requests;</li>
<li>Provide customer service and answer your questions;</li>
<li>Perform, invoice, and collect payment for services;</li>
<li>Send service-related text messages to customers who have opted in (see Section 5);</li>
<li>Maintain business records, comply with legal obligations, and protect against fraud or misuse; and</li>
<li>Improve our website and services.</li>
</ul>
<p>We do not sell your personal information.</p>

<h2>4. How We Share Your Information</h2>
<p>We share personal information only as needed to run our business, and only with:</p>
<ul>
<li><strong>Service providers</strong> that perform services on our behalf, such as our telephone and messaging provider, scheduling/invoicing software, payment processors, email providers, and website hosting. These providers may use your information only to provide services to us.</li>
<li><strong>Legal and safety purposes:</strong> when required by law, subpoena, or court order, or to protect our rights, property, or safety, or that of our customers or others.</li>
<li><strong>Business transfers:</strong> in connection with a merger, sale, or transfer of all or part of our business, subject to this Privacy Policy.</li>
</ul>
<p><strong>SMS consent is not shared with third parties. No mobile information will be shared with third parties or affiliates for marketing or promotional purposes. Mobile opt-in data and consent will not be shared with any third parties.</strong> Information sharing with subcontractors in support of services, such as customer service and message delivery, is permitted, but all of the above categories exclude text messaging originator opt-in data and consent; this information will not be shared with any third parties.</p>

<h2>5. Text Messaging (SMS)</h2>
<p><strong>{LLC}</strong> is the business that sends text messages under this program{_e(b.aka)}. Messages about booking and service are sent from {b.ph}.</p>
<p><strong>Information collected in connection with SMS:</strong> name, mobile phone number, email address, service or billing address, and service details needed to respond to your booking or service request.</p>
<p><strong>Message types:</strong> booking replies when you text BOOK, appointment reminders, scheduling confirmations, missed-call follow-ups, and customer service replies related to {b.service}.</p>
<p><strong>How you opt in:</strong> You may opt in by (a) texting <strong>BOOK</strong> to <strong>{_e(b.phone)}</strong> {b.book_reply} and receive related booking messages; (b) verbally agreeing to receive text messages during a phone call with us when you provide your mobile number or request to be contacted by text; or (c) checking the optional SMS consent box (unchecked by default) on {b.form_where} on our website, agreeing to receive text messages from {LLC} at the number provided about your quote, appointment scheduling, arrival times, and service updates. Consent to receive text messages is not a condition of purchasing any goods or services.</p>
<p><strong>Key terms:</strong></p>
<ul>
<li>Message frequency varies.</li>
<li>Message and data rates may apply.</li>
<li>To opt out at any time, reply <strong>STOP</strong>. You will receive one confirmation message and no further messages unless you opt in again.</li>
<li>For help, reply <strong>HELP</strong> or call {b.ph}.</li>
<li>Carriers are not liable for delayed or undelivered messages.</li>
</ul>
<p><strong>Mobile numbers and SMS opt-in consent are never shared with or sold to third parties or affiliates for marketing or promotional purposes.</strong> Text messaging originator opt-in data and consent will not be shared with any third parties. Service providers that deliver messages on our behalf may process that data only to send those messages for us.</p>
<p>Full SMS Terms &amp; Conditions: {b.url("/terms")}</p>

<h2>6. Cookies</h2>
<p>Our website may use cookies and similar technologies to keep the site working and to understand how it is used. You can control cookies through your browser settings. Disabling cookies may affect some website features. {b.form_tech} This website is hosted on {b.hosting}.</p>

<h2>7. Data Retention and Security</h2>
<p>We keep personal information only as long as needed for the purposes described in this policy, including to provide services, maintain business and tax records, and comply with legal obligations. We use reasonable administrative, technical, and physical safeguards to protect personal information. No method of transmission or storage is 100% secure, and we cannot guarantee absolute security.</p>

<h2>8. Your Choices and Rights</h2>
<ul>
<li><strong>Text messages:</strong> Reply STOP to any message to opt out. Reply HELP for help.</li>
<li><strong>Email:</strong> Ask us to stop emailing you at any time.</li>
<li><strong>Access, correction, deletion:</strong> You may request access to, correction of, or deletion of your personal information by contacting us using the information below. We may need to keep certain information to comply with legal obligations or complete transactions.</li>
</ul>
<p>We will not discriminate against you for exercising any of these choices.</p>

<h2>9. Children's Privacy</h2>
<p>Our services are intended for adults. We do not knowingly collect personal information from children under 13. If you believe a child has provided us information, contact us and we will delete it.</p>

<h2>10. Florida and U.S. Users</h2>
<p>We are based in Florida and our services are provided in the United States. This policy is intended to comply with applicable U.S. federal law, including the Telephone Consumer Protection Act (TCPA) and CAN-SPAM Act, and applicable Florida law, including the Florida Telephone Solicitation Act. Information is stored and processed in the United States.</p>

<h2>11. Changes to This Policy</h2>
<p>We may update this Privacy Policy from time to time. The "Last Updated" date above shows when it was last revised. Changes are effective when posted on this page.</p>

<h2>12. Contact Us</h2>
<p>EXPRESS SEPTIC TANK PUMPING LLC{"" if b.is_llc else " (" + _e(b.name) + ")"}<br>
{_e(b.street)}<br>
{_e(b.city)}, {b.region} {b.zip}<br>
Phone: {_e(b.phone)}<br>
Email: {b.mail}<br>
Website: {b.url("/")}</p>
<p class="updated">Last updated: {LAST_UPDATED}</p>
</div>'''

def terms_body(b):
  """Approved reference /terms/ (SMS Terms & Conditions) sections 1-11, brand-swapped."""
  qlinks = " or ".join(b.url(p) for p in b.quote_paths)
  return f'''<div class="prose legal-doc">
<p><strong>EXPRESS SEPTIC TANK PUMPING LLC</strong>{_e(b.aka)}<br>
Effective Date: {EFFECTIVE}<br>
Last Updated: {LAST_UPDATED}</p>
<p>Website: {b.url("/")}<br>
Privacy Policy: {b.url("/privacy-policy")}<br>
SMS Terms &amp; Conditions: {b.url("/terms")}</p>

<h2>1. Program Name and Description</h2>
<p><strong>Program name:</strong> {_e(b.prog)}</p>
<p>{LLC} ("we," "us," "our"){"" if b.is_llc else ", also operating as " + _e(b.name) + ","} sends text messages to customers who have opted in, about {b.service}. Messages are sent from our business number, {_e(b.phone)}.</p>

<h2>2. Types of Messages</h2>
<p>By opting in, you may receive the following types of text messages:</p>
<ul>
<li><strong>Appointment reminders</strong> (for example, a reminder of your scheduled {b.appt} date and time);</li>
<li><strong>Scheduling confirmations</strong> (confirming, rescheduling, or updating a service appointment, including technician arrival updates);</li>
<li><strong>Missed-call follow-ups</strong> (a text after we miss your call, so we can help with your request); and</li>
<li><strong>Customer service replies</strong> (answers to your questions about quotes, service, invoices, and your account).</li>
</ul>
<p>Sample message: "{_e(b.name)}: Your {b.appt} appointment is confirmed for Tue 10/13 between 8-10 AM. Reply C to confirm or call {_e(b.phone)}. Msg &amp; data rates may apply. Reply STOP to opt out, HELP for help."</p>

<h2>3. How You Opt In</h2>
<p>You may opt in to receive text messages by:</p>
<ul>
<li><strong>Text BOOK:</strong> texting BOOK to {_e(b.phone)} {b.book_reply}, as shown on our website;</li>
<li><strong>Phone call:</strong> verbally agreeing, during a phone call with us, to receive text messages when you provide your mobile number or ask us to text you; or</li>
<li><strong>Website form:</strong> checking the optional SMS consent box (unchecked by default) on {b.form_where} at {qlinks}, agreeing to receive text messages from {LLC} at the number you provide about your quote, appointment scheduling, arrival times, and service updates.</li>
</ul>
<p>Consent to receive text messages is not a condition of purchase. You may also contact us by phone at {_e(b.phone)} or by email at {b.mail} instead.</p>

<h2>4. Message Frequency and Cost</h2>
<p>Message frequency may vary. Frequency depends on your service activity, such as appointments and service requests.</p>
<p>Message and data rates may apply. Check your mobile plan for details.</p>

<h2>5. Opting Out (STOP)</h2>
<p>To opt out at any time, text STOP. You may also reply END, CANCEL, UNSUBSCRIBE, QUIT, or STOPALL. After you text STOP, you will receive one final message confirming that you have been unsubscribed, and you will no longer receive text messages from us unless you opt in again. To rejoin, text START or tell us you would like to receive texts again.</p>

<h2>6. Help (HELP)</h2>
<p>For assistance, text HELP or visit {b.url("/")} / call {_e(b.phone)}. You may also email {b.mail}.</p>

<h2>7. Privacy and Data Sharing</h2>
<p><strong>SMS consent is not shared with third parties. Mobile opt-in data will not be shared with third parties. No mobile information will be shared with third parties or affiliates for marketing or promotional purposes.</strong></p>
<p>See our Privacy Policy for more information: {b.url("/privacy-policy")}</p>

<h2>8. Supported Carriers and Delivery</h2>
<p>Our program works with major U.S. wireless carriers. Carriers are not liable for delayed or undelivered messages. Delivery of messages is subject to effective transmission by your wireless carrier and is not guaranteed.</p>

<h2>9. Your Responsibilities</h2>
<p>You confirm that you are the account holder or authorized user of the mobile number you provide. If you change or give up your mobile number, please text STOP from that number or tell us so we can update our records.</p>

<h2>10. Changes to These Terms</h2>
<p>We may update these SMS Terms &amp; Conditions from time to time. Changes are effective when posted on this page. Continuing to receive messages after changes are posted means you accept the updated terms. You may opt out at any time by texting STOP.</p>

<h2>11. Contact Us</h2>
<p>EXPRESS SEPTIC TANK PUMPING LLC{"" if b.is_llc else " (" + _e(b.name) + ")"}<br>
{_e(b.street)}<br>
{_e(b.city)}, {b.region} {b.zip}<br>
Phone: {_e(b.phone)}<br>
Email: {b.mail}<br>
Website: {b.url("/")}</p>
<p class="updated">Last updated: {LAST_UPDATED}</p>
</div>'''

def privacy_stub_body():
  return '''<div class="prose"><h2>Privacy Policy moved</h2>
<p>Our full Privacy Policy (including SMS consent language) is at <a href="/privacy-policy/">/privacy-policy/</a>.</p>
<p><a href="/privacy-policy/">View Privacy Policy</a> · <a href="/terms/">SMS Terms</a></p></div>'''

FORM_CSS = '''
/* ---- quote form + SMS consent (10DLC) ---- */
.quote-wrap{max-width:720px;margin:0 auto}
.request-card{background:#fff;border:1px solid rgba(0,0,0,.12);border-radius:14px;padding:28px;color:#1a1a1a}
.request-card h2{margin-top:0}
.quote-form{display:grid;gap:14px;margin-top:12px}
.qf-row{display:grid;gap:6px}
.qf-row label{font-weight:600;font-size:.95rem}
.qf-row .opt{font-weight:400;opacity:.7}
.quote-form input,.quote-form select,.quote-form textarea{font:inherit;padding:11px 12px;border:1px solid rgba(0,0,0,.25);border-radius:8px;background:#fff;color:#1a1a1a;width:100%;box-sizing:border-box}
.sms-consent{background:rgba(0,0,0,.035);border-radius:10px;padding:12px 14px}
.sms-consent label{display:flex;gap:10px;align-items:flex-start;font-size:.88rem;line-height:1.45;font-weight:400}
.sms-consent input{margin-top:3px;width:18px;height:18px;flex:0 0 auto}
.qf-submit{justify-self:start}
.form-note{font-size:.85rem;margin-top:14px;opacity:.85}
.express-operator{font-size:.85rem;margin:0 0 6px}
.legal-doc h2{margin-top:1.6em}
.legal-doc .updated{margin-top:2em;font-size:.9rem;opacity:.75}
'''
