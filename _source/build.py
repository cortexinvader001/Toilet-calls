import re, json, pathlib, html

import os, sys
HERE = pathlib.Path(__file__).resolve().parent
CFG = json.loads((HERE / "site-config.json").read_text())
ICON = pathlib.Path(os.environ.get("ICON_DIR", HERE / "icons"))
OUT = pathlib.Path(os.environ.get("OUT_DIR", HERE.parent))
CLEAN = "--html" not in sys.argv          # clean URLs (/contact) unless --html is given
DOMAIN = CFG["domain"].rstrip("/")
TOK = {"@@PHONE@@": CFG["phone"], "@@PHONE_TEL@@": CFG["phone_tel"], "@@PHONE_INTL@@": CFG["phone_intl"], "@@EMAIL@@": CFG["email"],
       "@@STREET@@": CFG["street"], "@@CITY@@": CFG["city"], "@@REGION@@": CFG["region"], "@@HOURS@@": CFG["hours"], "@@AREA@@": CFG["area"]}


def fill(t):
    for k, v in TOK.items():
        t = t.replace(k, v)
    return t


def link(h):
    """Turn page.html links into clean URLs in production."""
    if not CLEAN:
        return h
    def r(m):
        name, frag = m.group(1), m.group(2) or ""
        return 'href="' + ("/" if name == "index" else "/" + name) + frag + '"'
    return re.sub(r'href="(?!https?:)([a-z0-9-]+)\.html(#[^"]*)?"', r, h)


USED = set()


def ic(name, cls=""):
    weight = "bold" if name.endswith("-bold") else "duotone"
    fname = name if name.endswith("-bold") else name + "-duotone"
    USED.add((weight, fname))
    svg = (ICON / weight / f"{fname}.svg").read_text()
    return svg.replace("<svg", f'<svg class="{("ic " + cls).strip()}" aria-hidden="true" focusable="false"', 1)


def A(x):
    """Marks wording that is allowed to use the banned words (disclaimers, referral, guide FAQ)."""
    return f"<!--A-->{x}<!--/A-->"


VALS = {"phone": "@@PHONE@@", "email": "@@EMAIL@@", "hours": "@@HOURS@@", "area": "@@AREA@@"}
def tbc(key, label):
    if key:
        return f'<span data-fill="{key}">{VALS[key]}</span>'
    return TXT[label]
TXT = {"Hygiene statement": CFG["hygiene_statement"], "Reviews": CFG["reviews_text"], "Credentials": CFG["credentials_text"]}


DISC_FULL = ("ToiletCall is a toilet cleaning and rescue service, not a plumbing company. We clean, sanitize, "
             "unclog simple blockages, remove odours and restock restrooms. For pipe repairs, leaks or installation, "
             "we connect you with a licensed plumber.")
DISC_SHORT = ("ToiletCall is a cleaning and rescue service, not a plumbing company. For pipe repairs, leaks or "
              "installation, we connect you with a licensed plumber.")
SCOPE = ("If a job needs pipe work, leak repair or a new toilet installed, that is plumbing. We will not attempt it - "
         "we will refer you to a licensed plumber.")


def disclaimer_box():
    return f'<aside class="disclaimer">{ic("shield-check")}<p>{A(DISC_FULL)}</p></aside>'


def referral():
    return f'''<aside class="referral rv"><h3>{A("Need an actual plumber?")}</h3>
<p>{A("Leaks, pipe repairs and toilet installation are plumbing jobs, and we do not do them. If your job needs one, we will tell you straight away and connect you with a licensed plumber from our partner network - so you still solve the problem with one call.")}</p></aside>'''


NAV = [
    ("index.html", "Home", "Home"),
    ("services.html", "Services", "Services"),
    ("for-businesses.html", "Businesses", "For Businesses"),
    ("for-property-managers.html", "Property Managers", "For Property Managers"),
    ("pricing.html", "Pricing", "Pricing"),
    ("about.html", "About", "About"),
    ("faq.html", "FAQ", "FAQ"),
    ("contact.html", "Book", "Contact / Book"),
]


def header(active):
    def cur(f): return ' aria-current="page"' if f == active else ""
    links = "".join(f'<li><a href="{f}"{cur(f)}>{s}</a></li>' for f, s, _ in NAV)
    dd = "".join(f'<li><a href="{f}"{cur(f)}>{l} {ic("caret-right-bold")}</a></li>' for f, _, l in NAV)
    return f'''<div class="topstrip">{"Fast Toilet Cleaning, Unclogging &amp; Sanitizing"}</div>
<header class="site-header" id="top">
  <div class="wrap bar">
    <a class="brand" href="index.html" aria-label="ToiletCall.ca home"><img src="icon.png" alt="" width="40" height="44"><span>ToiletCall<small>.ca</small></span></a>
    <nav aria-label="Main"><ul class="nav-links">{links}</ul></nav>
    <div class="bar-actions">
      <a class="btn btn-cta btn-sm call-pill" data-tel href="contact.html#book">{ic("phone-call")}<span>Call now</span></a>
      <button class="burger" id="burger" type="button" aria-expanded="false" aria-controls="menu" aria-label="Open menu">{ic("list-bold", "i-open")}{ic("x-bold", "i-close")}</button>
    </div>
  </div>
  <div class="dropdown" id="menu" inert>
    <div class="dropdown-inner"><div class="dropdown-card">
      <ul>{dd}</ul>
      <a class="btn btn-cta" href="contact.html#book">Book a Rescue</a>
    </div></div>
  </div>
  <div class="scrim" id="scrim"></div>
</header>'''


SERVICES = [
    ("s1", "spray-bottle", "Emergency toilet cleaning and sanitizing"),
    ("s2", "drop", "Unclogging - no plumbing repair"),
    ("s3", "wind", "Odour removal and deodorizing"),
    ("s4", "package", "Restroom restocking"),
    ("s5", "clipboard-text", "Scheduled restroom inspections"),
    ("s6", "key", "Move-in / move-out deep cleaning"),
    ("s7", "house-line", "Help for seniors, landlords and Airbnb hosts"),
]


def footer():
    sv = "".join(f'<li><a href="{SVC_PAGES[i][0]}">{A(t) if "plumbing" in t else t}</a></li>' for i, _, t in SERVICES)
    return f'''<footer>
  <div class="wrap">
    <div class="foot">
      <div class="foot-brand"><img src="logo-full.png" alt="ToiletCall logo" width="80" height="110">
        <p class="foot-disc">{A(DISC_FULL)}</p></div>
      <div><h4>Services</h4><ul>{sv}</ul></div>
      <div><h4>Contact</h4><ul class="foot-contact">
        <li>@@STREET@@</li>
        <li>Phone: {tbc("phone", "Phone")}</li>
        <li>Email: {tbc("email", "Email")}</li>
        <li><strong>Hours:</strong> {tbc("hours", "Hours")}</li></ul>
        <h4>More</h4><ul>
        <li><a href="for-businesses.html">For Businesses</a></li><li><a href="for-property-managers.html">For Property Managers</a></li>
        <li><a href="pricing.html">Pricing</a></li><li><a href="faq.html">FAQ</a></li>
        <li><a href="contact.html#pay">Pay online</a></li><li><a href="privacy.html">Privacy</a></li></ul></div>
    </div>
    <p class="foot-ref">{A("Need a plumber? We will connect you with a licensed plumber from our partner network.")}</p>
    <p class="foot-copy">&copy; <span id="yr">2026</span> ToiletCall.ca</p>
  </div>
</footer>
<div class="callbar"><a class="btn btn-ghost" data-tel href="contact.html#book">{ic("phone-call")}Call now</a><a class="btn btn-cta" href="contact.html#book">Book a Rescue</a></div>'''


LD_EXTRA = {}   # fname -> list of extra JSON-LD nodes
PAGE_NAMES = {"index.html": "Home", "services.html": "Services", "for-businesses.html": "For Businesses",
              "for-property-managers.html": "For Property Managers", "pricing.html": "Pricing", "about.html": "About",
              "faq.html": "FAQ", "contact.html": "Contact / Book", "privacy.html": "Privacy"}
TODAY = "2026-11-27"


def business_node():
    return {"@type": ["LocalBusiness", "ProfessionalService"], "@id": DOMAIN + "/#business", "name": "ToiletCall",
            "alternateName": "ToiletCall.ca", "url": DOMAIN + "/", "logo": DOMAIN + "/logo-full.png", "image": DOMAIN + "/og-image.png",
            "description": "Toilet cleaning and rescue service in Winnipeg: emergency toilet cleaning, sanitizing, unclogging of simple blockages, odour removal and restroom restocking. Not a plumbing company.",
            "telephone": "@@PHONE_INTL@@", "email": "@@EMAIL@@", "currenciesAccepted": "CAD", "paymentAccepted": "Credit card, Interac e-Transfer",
            "address": {"@type": "PostalAddress", "streetAddress": "@@STREET@@", "addressLocality": "@@CITY@@", "addressRegion": "@@REGION@@", "addressCountry": "CA"},
            "areaServed": [{"@type": "City", "name": "Winnipeg"}, {"@type": "AdministrativeArea", "name": "Manitoba"}],
            "contactPoint": [{"@type": "ContactPoint", "telephone": "@@PHONE_INTL@@", "contactType": "customer service", "email": "@@EMAIL@@", "areaServed": "CA", "availableLanguage": "English"}],
            "knowsAbout": ["Toilet cleaning", "Toilet unclogging", "Restroom sanitizing", "Odour removal", "Restroom restocking"]}


def seo_extra(fname, title, desc):
    url = DOMAIN + ("/" if fname == "index.html" else "/" + fname.replace(".html", ""))
    clean_title = re.sub(r"&amp;", "&", title)
    graph = [business_node(),
             {"@type": "WebSite", "@id": DOMAIN + "/#website", "url": DOMAIN + "/", "name": "ToiletCall.ca", "inLanguage": "en-CA", "publisher": {"@id": DOMAIN + "/#business"}},
             {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": clean_title, "isPartOf": {"@id": DOMAIN + "/#website"},
              "about": {"@id": DOMAIN + "/#business"}, "inLanguage": "en-CA", "dateModified": TODAY, "primaryImageOfPage": DOMAIN + "/og-image.png"}]
    crumbs = [("Home", DOMAIN + "/")]
    if fname in SVC_FILES:
        crumbs += [("Services", DOMAIN + "/services"), (SVC_FILES[fname], url)]
    elif fname != "index.html":
        crumbs += [(PAGE_NAMES.get(fname, fname), url)]
    if len(crumbs) > 1:
        graph.append({"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": n, "name": nm, "item": u} for n, (nm, u) in enumerate(crumbs, 1)]})
    graph += LD_EXTRA.get(fname, [])
    ld = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False) + "</script>"
    head = f'''<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<link rel="alternate" hreflang="en-CA" href="{url}">
<link rel="alternate" hreflang="x-default" href="{url}">
<meta name="author" content="ToiletCall">
<meta name="geo.region" content="CA-MB"><meta name="geo.placename" content="Winnipeg">
<meta name="format-detection" content="telephone=yes">
<meta name="apple-mobile-web-app-title" content="ToiletCall">
<meta name="application-name" content="ToiletCall">
<link rel="manifest" href="site.webmanifest">
<link rel="alternate" type="text/plain" href="{DOMAIN}/llms.txt" title="LLM-readable site summary">'''
    if fname == "index.html":
        head += '\n<link rel="preload" as="image" href="hero-v2.webp" type="image/webp" fetchpriority="high">'
    return head + "\n" + ld


def page(fname, title, desc, body, extra=""):
    url = DOMAIN + ("/" if fname == "index.html" else "/" + fname.replace(".html", ""))
    h = f'''<!DOCTYPE html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self' https://api.web3forms.com; form-action 'self' https://api.web3forms.com; base-uri 'self'; object-src 'none'">
<meta name="referrer" content="strict-origin-when-cross-origin">

<!--A--><meta name="description" content="{desc}"><!--/A-->
<link rel="canonical" href="{url}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="favicon-192.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta name="theme-color" content="#0E2A47">
<meta property="og:type" content="website">
<meta property="og:site_name" content="ToiletCall.ca">
<meta property="og:title" content="{title}">
<!--A--><meta property="og:description" content="{desc}"><!--/A-->
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{DOMAIN}/og-image.png">
<link rel="stylesheet" href="style.css">
{seo_extra(fname, title, desc)}
{extra}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header(fname)}
<main id="main">
{body}
</main>
{footer()}
<script src="config.js"></script>
<script src="script.js"></script>
</body>
</html>'''
    (OUT / fname).write_text(fill(link(h)))


def pagehead(kicker, h1, lede, icon):
    return f'''<section class="pagehead"><div class="wrap"><div class="ph-panel">
<p class="kicker">{kicker}</p><h1>{h1}</h1><p class="lede">{lede}</p>
<span class="ph-icon" aria-hidden="true">{ic(icon)}</span></div></div></section>'''


def final_cta():
    return f'''<section class="final"><div class="wrap"><div class="cta-band rv">
<div><h2>{A("Do not live with it. Do not pay a plumber to clean it.")}</h2>
<p>Book a toilet rescue today. {tbc("phone", "Phone")}</p></div>
<div class="acts"><a class="btn btn-cta" href="contact.html#book">Book a Rescue</a><a class="btn btn-ghost" data-tel href="contact.html#book">Call now</a></div>
</div></div></section>'''


FAQ = [
    ("Are you a plumbing company?", A("No. ToiletCall is a toilet cleaning and rescue service, not a plumbing company. We clean, sanitize, unclog simple blockages, remove odours and restock restrooms. For pipe repairs, leaks or installation, we connect you with a licensed plumber.")),
    ("Can you unclog a toilet?", A("Yes, when the blockage is caused by waste or paper and no repairs are needed. If the blockage is in the pipes, we will say so and refer you to a licensed plumber.")),
    ("Do you install toilets?", A("No. Installing or replacing a toilet is plumbing work. We will refer you to a licensed plumber.")),
    ("Do you offer monthly plans for businesses?", 'Yes. Our restroom-care subscription covers scheduled inspections, cleaning and sanitizing, restocking and emergency call-outs. See <a href="for-businesses.html">For Businesses</a>.'),
    ("What if water is leaking from a pipe?", A("That is a plumbing job, and we do not do it. We will tell you straight away and connect you with a licensed plumber from our partner network.")),
    ("Can you help seniors, landlords and Airbnb hosts?", "Yes. We offer respectful in-home help for seniors, and fast turnarounds for landlords and hosts between tenants and guests."),
    ("How do I pay?", 'By card through Stripe&rsquo;s secure payment page, or by Interac e-Transfer. See the <a href="contact.html#pay">payment options</a>.'),
    ("Where do you work, and when?", f'Service area: {tbc("area", "Service area")} Hours: {tbc("hours", "Hours")}'),
]


def faq_list(items):
    return '<div class="faq">' + "".join(f'<details class="rv"><summary>{q}</summary><p>{a}</p></details>' for q, a in items) + "</div>"


# ---------------------------------------------------------------- HOME
def home():
    minis = {
        "s1": "Dirty, soiled or unusable right now? Fully cleaned and sanitized.",
        "s2": "Waste or paper blockages cleared, with no pipe work needed.",
        "s3": "Persistent smells removed with a deep clean and deodorizing.",
        "s4": "Tissue, soap and paper towels checked and refilled.",
        "s5": "Regular checks for businesses, with a simple report after each visit.",
        "s6": "Toilet deep cleaning before keys change hands or guests arrive.",
        "s7": "Respectful in-home help for seniors; quick turnarounds for landlords and hosts.",
    }
    minis_html = "".join(
        f'<a class="mini rv" href="{SVC_PAGES[i][0]}"><span class="tile" aria-hidden="true">{ic(icn)}</span><span><strong>{A(t) if "plumbing" in t else t}</strong><small>{minis[i]}</small></span></a>'
        for i, icn, t in SERVICES)
    aud = [
        ("Homeowners and renters", "Fast help with a dirty, clogged, overflowing or smelly toilet.", "contact.html#book", "Book a one-time rescue"),
        ("Seniors and families helping seniors", "Safe, respectful toilet assistance at home.", "contact.html#book", "Book a visit or call"),
        ("Landlords and Airbnb hosts", "Turnover cleaning and emergency help between guests.", "move-in-move-out-toilet-cleaning.html", "Deep clean and concierge"),
        ("Restaurants, gas stations, offices, churches, small businesses", "Clean, stocked, inspected restrooms without hiring cleaners.", "for-businesses.html", "Commercial subscription"),
        ("Property managers", "One contact for tenant restroom emergencies and turnover sanitation.", "for-property-managers.html", "Toilet concierge"),
    ]
    aud_html = "".join(f'<a class="aud rv" href="{h}"><span><strong>{t}</strong><small>{d}</small></span><span class="go">{l} {ic("caret-right-bold")}</span></a>' for t, d, h, l in aud)
    body = f'''
<section class="hero"><div class="wrap"><div class="hero-panel">
  <div class="hero-copy">
    <span class="eyebrow"><svg class="arcs" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" aria-hidden="true"><path d="M4 12a8 8 0 0 1 8-8"/><path d="M4 20a16 16 0 0 1 16-16"/></svg>Toilet Cleaning &amp; Unclogging Specialists</span>
    <h1>Toilet trouble? <em>We rescue toilets.</em></h1>
    <p>{A("Fast toilet cleaning, unclogging, sanitizing and restroom support - without the plumber's price. Dirty, clogged, overflowing, smelly or simply unusable? One call and we will clean it, clear it, sanitize it and get it back in service.")}</p>
    <div class="hero-cta"><a class="btn btn-cta" href="contact.html#book">Book a Rescue</a><a class="btn btn-ghost" href="for-businesses.html">For Businesses</a></div>
    <p class="hero-disc">{A(DISC_SHORT)}</p>
  </div>
  <div class="hero-art"><img src="hero-v2.webp" fetchpriority="high" decoding="async" width="928" height="1152" alt="Two cleaning team members in matching blue uniforms standing back to back, smiling"></div>
</div></div></section>

<section class="strip"><div class="wrap"><p class="rv">Dirty? <span>Clogged by waste or paper?</span> Overflowing? Smelly? Guests arriving? <strong>That is exactly what we are for.</strong></p></div></section>

<section id="services"><div class="wrap">
  <p class="kicker rv">What we do</p><h2 class="rv">Seven ways we rescue a toilet.</h2>
  <div class="minis">{minis_html}</div>
  <div class="more rv"><a class="btn btn-ghost" href="services.html">See what is included</a></div>
</div></section>

<section class="how"><div class="wrap">
  <p class="kicker rv">How it works</p><h2 class="rv">Three steps back to a clean toilet.</h2>
  <ol class="steps">
    <li class="rv"><span class="n">1</span><h3>Call or book online.</h3><p>Tell us what is wrong and where.</p></li>
    <li class="rv"><span class="n">2</span><h3>We attend and rescue.</h3><p>We clean, unclog simple blockages, sanitize and deodorize.</p></li>
    <li class="rv"><span class="n">3</span><h3>Back in service.</h3><p>{A("Clean, fresh, restocked - and if it turns out to need a plumber, we will tell you honestly and arrange a referral.")}</p></li>
  </ol>
</div></section>

<section class="who"><div class="wrap">
  <p class="kicker rv">Who we help</p><h2 class="rv">Homes, hosts, businesses and buildings.</h2>
  <div class="auds">{aud_html}</div>
</div></section>

<section class="teaser"><div class="wrap"><div class="teaser-card rv">
  <div><p class="kicker">For businesses</p><h2>Clean, stocked restrooms - on a schedule, not on your staff.</h2>
  <p>Monthly restroom care for businesses: inspections, sanitizing, restocking and emergency service, handled by ToiletCall.</p></div>
  <a class="btn btn-cta" href="for-businesses.html">Request a subscription quote</a>
</div></div></section>

<section class="refsec"><div class="wrap">{referral()}</div></section>

<section class="faqsec"><div class="wrap">
  <p class="kicker rv">Quick answers</p><h2 class="rv">Questions people ask first.</h2>
  {faq_list(FAQ[:5])}
  <div class="more rv"><a class="btn btn-ghost" href="faq.html">All questions</a></div>
</div></section>
{final_cta()}'''
    page("index.html", "Toilet Cleaning &amp; Rescue Service in Winnipeg | ToiletCall.ca",
         "ToiletCall.ca is a toilet cleaning and rescue service in Winnipeg, not a plumbing company. Emergency cleaning, unclogging and sanitizing. Call @@PHONE@@.",
         body)


# ---------------------------------------------------------------- SERVICES
def services():
    global SVC_DET
    det = SVC_DET = {
        "s1": ("For toilets that are dirty, soiled or unusable right now. Full clean and sanitize of bowl, seat, exterior, base and surrounding floor area.",
               "Call when the toilet is dirty, soiled or unusable right now.", "Bowl, seat, exterior, base and surrounding floor area, cleaned and sanitized."),
        "s2": (A("For blockages caused by waste or paper. Cleared without plumbing repairs. If the blockage is in the pipes, we say so and refer a licensed plumber."),
               "Call when the toilet is blocked by waste or paper.", "Clearing of waste or paper blockages, with cleaning and sanitizing around the toilet."),
        "s3": (A("For persistent smells. Deep clean, sanitize and deodorize, including the base seal area and surrounding surfaces we can reach without repairs."),
               "Call when a smell keeps coming back.", "Deep clean, sanitizing and deodorizing, including the base seal area and reachable surrounding surfaces."),
        "s4": ("Tissue, soap and paper towels checked and refilled. Can be a one-off visit or part of a business subscription.",
               "Call when supplies run low, or ask about a business subscription.", "Tissue, soap and paper towels checked and refilled."),
        "s5": ("Regular checks for businesses: cleanliness, odours, supplies and issues spotted early, with a simple report after each visit.",
               "Call to set up regular checks for your business.", "Checks of cleanliness, odours and supplies, with a simple report after each visit."),
        "s6": ("Toilet deep cleaning for empty or newly occupied homes, rentals and listings - before keys change hands or guests arrive.",
               "Call before a move-in, a move-out or a guest arrival.", "Toilet deep cleaning for empty or newly occupied homes, rentals and listings."),
        "s7": ("Respectful in-home assistance for seniors; fast turnarounds for landlords and hosts between tenants and guests.",
               "Call when you or a family member needs toilet help at home, or between tenants and guests.", "Respectful in-home assistance, and fast turnarounds for landlords and hosts."),
    }
    blocks = ""
    for n, (i, icn, t) in enumerate(SERVICES, 1):
        what, when, inc = det[i]
        title = A(t) if "plumbing" in t else t
        blocks += f'''<article class="sv rv" id="{i}"><div class="sv-head"><span class="tile" aria-hidden="true">{ic(icn)}</span><span class="num">{n:02d}</span></div>
<div class="sv-body"><h2>{title}</h2><p class="what">{what}</p>
<dl class="facts"><div><dt>When to call</dt><dd>{when}</dd></div><div><dt>What is included</dt><dd>{inc}</dd></div>
<div><dt>Out of scope</dt><dd>Pipe or fixture work. See the referral note below.</dd></div></dl>
<a class="btn btn-cta btn-sm" href="contact.html#book">Book a visit</a> <a class="btn btn-ghost btn-sm" href="{SVC_PAGES[i][0]}">Details and price</a></div></article>'''
    body = f'''{pagehead("Services", "Toilet cleaning, unclogging and sanitizing services", "Seven services, each one about getting a toilet clean, fresh and back in use.", "spray-bottle")}
<section><div class="wrap">
  {disclaimer_box()}
  <div class="svlist">{blocks}</div>
  <aside class="scope rv"><strong>Scope line.</strong> {A(SCOPE)}</aside>
  {referral()}
</div></section>
{final_cta()}'''
    page("services.html", "Toilet Cleaning, Unclogging &amp; Sanitizing Services | ToiletCall.ca",
         "Toilet cleaning, unclogging of simple blockages, sanitizing, odour removal and restocking in Winnipeg. Cleaning, not plumbing.", body)


# ---------------------------------------------------------------- FORMS
def f_input(label, name, typ="text", req=False, auto="", extra=""):
    r = " required" if req else ""
    a = f' autocomplete="{auto}"' if auto else ""
    return f'<label>{label}{" *" if req else ""}<input type="{typ}" name="{name}"{r}{a} {extra}></label>'


def booking_form():
    checks = ["Dirty", "Clogged by waste or paper", "Overflowing", "Smelly", "Needs restocking", "Move-in or move-out clean", "Other"]
    ck = "".join(f'<label class="opt"><input type="checkbox" name="whats_wrong" value="{c}"> {c}</label>' for c in checks)
    return f'''<div class="formcard" id="book">
<form class="js-form" data-kind="Emergency booking" aria-labelledby="bk-h">
<h2 id="bk-h">Book a toilet rescue</h2>
<p class="fnote">Phone is fastest. This form is the backup.</p>
{f_input("Name", "name", "text", True, "name")}
{f_input("Phone", "phone", "tel", True, "tel")}
{f_input("Email", "email", "email", False, "email")}
{f_input("Address or area", "address", "text", False, "street-address")}
<label>Property type<select name="property_type"><option>Home</option><option>Rental</option><option>Airbnb</option><option>Business</option><option>Managed building</option></select></label>
<fieldset><legend>What is wrong? (tick all that apply)</legend><div class="opts">{ck}</div></fieldset>
<fieldset><legend>{A("Is water leaking from a pipe, or does anything appear broken or in need of installation?")} *</legend>
<div class="opts"><label class="opt"><input type="radio" name="triage" value="No" required> No</label><label class="opt"><input type="radio" name="triage" value="Yes" required> Yes</label></div></fieldset>
<div class="referral-msg" hidden role="status"><p>{A("This may need a licensed plumber. We do not do plumbing work, but we can connect you with a licensed plumber from our partner network. Use the button below to ask for that referral instead of a cleaning booking.")}</p></div>
<label>Urgency<select name="urgency"><option>Emergency today</option><option>This week</option><option>Scheduled or recurring</option></select></label>
{f_input("Number of toilets or restrooms", "toilets", "number", False, "", 'min="1"')}
{f_input("Preferred date and time", "preferred_time", "datetime-local")}
<label>Notes<textarea name="notes"></textarea></label>
<label>Photo (optional)<input type="file" name="photo" accept="image/*"></label>
<label class="opt consent"><input type="checkbox" name="consent" required> I agree to be contacted about this request. *</label>
<button class="btn btn-cta" type="submit" data-label="Book a Rescue">Book a Rescue</button>
<div class="hp" aria-hidden="true"><label>Leave this empty<input type="checkbox" name="botcheck" tabindex="-1" autocomplete="off"></label></div>
<p class="form-status" role="status"></p>
<p class="fnote">We use your details only to reply to your request. See our <a href="privacy.html">privacy notice</a>.</p>
</form><div class="confirm" hidden></div></div>'''


def biz_form():
    return f'''<div class="formcard" id="enquiry">
<form class="js-form" data-kind="Business subscription enquiry" aria-labelledby="bz-h">
<h2 id="bz-h">Request a subscription quote</h2>
{f_input("Business name", "business_name", "text", True, "organization")}
{f_input("Type of business", "business_type", "text", True)}
{f_input("Number of restrooms", "restrooms", "number", True, "", 'min="1"')}
{f_input("Address", "address", "text", True, "street-address")}
{f_input("Contact name", "contact_name", "text", True, "name")}
{f_input("Phone", "phone", "tel", True, "tel")}
{f_input("Email", "email", "email", True, "email")}
<label>Current problem (if any)<textarea name="current_problem"></textarea></label>
<label class="opt consent"><input type="checkbox" name="consent" required> I agree to be contacted about this enquiry. *</label>
<button class="btn btn-cta" type="submit" data-label="Request a quote">Request a quote</button>
<div class="hp" aria-hidden="true"><label>Leave this empty<input type="checkbox" name="botcheck" tabindex="-1" autocomplete="off"></label></div>
<p class="form-status" role="status"></p>
<p class="fnote">We use your details only to reply to your enquiry. See our <a href="privacy.html">privacy notice</a>.</p>
</form><div class="confirm" hidden></div></div>'''


def pm_form():
    return f'''<div class="formcard" id="enquiry">
<form class="js-form" data-kind="Property manager concierge enquiry" aria-labelledby="pm-h">
<h2 id="pm-h">Talk to us about your buildings</h2>
{f_input("Company", "company", "text", True, "organization")}
{f_input("Contact name", "contact_name", "text", True, "name")}
{f_input("Phone", "phone", "tel", True, "tel")}
{f_input("Email", "email", "email", True, "email")}
{f_input("Number of units or buildings", "units", "text", True)}
{f_input("Areas covered", "areas", "text", True)}
<label>Current needs<textarea name="current_needs"></textarea></label>
<label class="opt consent"><input type="checkbox" name="consent" required> I agree to be contacted about this enquiry. *</label>
<button class="btn btn-cta" type="submit" data-label="Talk to us">Talk to us</button>
<div class="hp" aria-hidden="true"><label>Leave this empty<input type="checkbox" name="botcheck" tabindex="-1" autocomplete="off"></label></div>
<p class="form-status" role="status"></p>
<p class="fnote">We use your details only to reply to your enquiry. See our <a href="privacy.html">privacy notice</a>.</p>
</form><div class="confirm" hidden></div></div>'''


# ---------------------------------------------------------------- BUSINESSES
def businesses():
    plan = ""
    for lab, vals in [("Price", ["$149/month", "$249/month", "$399/month"]),
                      ("Restrooms", ["1 restroom", "Up to 3 restrooms", "High-traffic restrooms"]),
                      ("Visits", ["Weekly", "Weekly", "Twice weekly"]),
                      ("Included", ["Inspections, cleaning and sanitizing, restocking, emergency call-outs"] * 3),
                      ("Emergency call-outs", ["Standard $89 rate or better"] * 3)]:
        plan += f'<tr><th scope="row">{lab}</th>' + "".join(f"<td>{v}</td>" for v in vals) + "</tr>"
    body = f'''{pagehead("For Businesses", "Clean, stocked restrooms - on a schedule, not on your staff.", "Monthly restroom care for businesses: inspections, sanitizing, restocking and emergency service, handled by ToiletCall.", "storefront")}
<section><div class="wrap two">
  <div>
    <h2 class="rv">What is included</h2>
    <ul class="ticks rv"><li>Scheduled restroom inspections</li><li>Cleaning and sanitizing</li><li>Restocking of tissue, soap and paper towels</li><li>Odour control</li><li>Emergency call-outs for subscription customers</li></ul>
    <h2 class="rv">Why it matters</h2>
    <p class="rv">Customers judge a business by its restrooms. Your staff should not be pulled off their jobs to deal with a toilet emergency. We are built for restaurants, gas stations, offices, churches and small businesses.</p>
    <h2 class="rv">How it starts</h2>
    <ol class="plain rv"><li>You send the enquiry form.</li><li>We do a walk-through or a call to assess the restrooms.</li><li>You get a monthly plan.</li></ol>
  </div>
  {biz_form()}
</div></section>
<section class="plansec" id="plans"><div class="wrap">
  <h2 class="rv">Plans</h2>
  <p class="lede rv">Restroom-only care, so it costs far less than full janitorial service. Prices in CAD, before tax. Restocking can be added to any plan.</p>
  <div class="tablewrap rv"><table class="plans"><thead><tr><th></th><th>Essential</th><th>Standard</th><th>High-traffic</th></tr></thead><tbody>{plan}</tbody></table></div>
</div></section>
<section><div class="wrap">{referral()}</div></section>'''
    page("for-businesses.html", "Commercial Restroom Cleaning &amp; Care Subscriptions | ToiletCall.ca",
         "Monthly commercial restroom cleaning and care for businesses: inspections, sanitizing, restocking and emergency service. Cleaning, not plumbing.", body)


def property_managers():
    body = f'''{pagehead("For Property Managers", A("One call for every tenant toilet emergency."), A("Emergency cleaning, tenant turnover sanitation, supply delivery and plumber coordination for the buildings you manage."), "buildings")}
<section><div class="wrap two">
  <div>
    <h2 class="rv">The toilet concierge</h2>
    <ul class="ticks rv">
      <li><strong>Emergency cleaning</strong> when a tenant reports a dirty, clogged or overflowing toilet.</li>
      <li><strong>Tenant turnover sanitation</strong> - deep toilet cleaning between tenancies, alongside move-in and move-out cleans.</li>
      <li><strong>Supply delivery</strong> - tissue, soap and paper towels delivered and stocked.</li>
      <li><strong>{A("Plumber coordination")}</strong> - {A("when a repair is genuinely required, ToiletCall coordinates with a licensed plumber so the manager makes one call, not three.")}</li>
    </ul>
  </div>
  {pm_form()}
</div></section>
<section class="plansec" id="rates"><div class="wrap">
  <h2 class="rv">Rate card</h2>
  <p class="lede rv">For account holders. Prices in CAD, before tax.</p>
  <div class="tablewrap rv"><table class="plans"><thead><tr><th>Service</th><th>Rate</th></tr></thead><tbody>
  <tr><th scope="row">Emergency cleaning call-out</th><td>$79 &middot; $59 for account holders on a monthly plan</td></tr>
  <tr><th scope="row">Tenant-turnover sanitation</th><td>$59 per bathroom</td></tr>
  <tr><th scope="row">Supply delivery</th><td>$25 plus supplies</td></tr>
  <tr><th scope="row">Optional retainer</th><td>$99/month per property, call-outs at $59</td></tr>
  </tbody></table></div>
</div></section>
<section><div class="wrap">{referral()}</div></section>'''
    page("for-property-managers.html", "Toilet Concierge for Property Managers | ToiletCall.ca",
         "A toilet concierge for property managers: emergency cleaning, tenant turnover sanitation and supply delivery. Cleaning, not plumbing.", body)


# ---------------------------------------------------------------- PRICING
def pricing():
    items = [("One-time toilet rescue", "$89 - one visit: cleaning, sanitizing, simple unclogging and deodorizing. After-hours and emergency call-outs: $129.", "$89", "per visit &middot; emergency $129"),
             ("Move-in / move-out toilet deep cleaning", "$69 for the first bathroom, $39 for each additional bathroom - deep cleaning and sanitizing for empty or newly occupied homes, rentals and listings.", "$69", "first bathroom &middot; +$39 each extra"),
             ("Restroom restocking", "$39 per visit - tissue, soap and paper towels checked and refilled. Supplies billed at cost, or we restock with yours.", "$39", "per visit &middot; supplies at cost"),
             ("Business restroom-care subscription", "From $149/month - scheduled inspections, cleaning and sanitizing, restocking and emergency call-outs for your business restroom.", "From $149", "per month"),
             ("Property-manager toilet concierge", "From $59 per visit for account holders - emergency cleaning, tenant-turnover sanitation and supply delivery for your rental properties.", "From $59", "per visit &middot; account holders")]
    rows = "".join(f'<div class="price rv"><div><strong>{t}</strong><small>{d}</small></div><div class="amt"><b>{p}</b><small>{u}</small></div></div>' for t, d, p, u in items)
    body = f'''{pagehead("Pricing", "Pricing for toilet cleaning and rescue", "Clear prices for cleaning, sanitizing and restroom care. All prices are in Canadian dollars, before tax.", "credit-card")}
<section><div class="wrap">
  <div class="prices">{rows}</div>
  <p class="fnote rv" style="margin-top:18px">Prices in CAD, before tax. Business plans and the property-manager rate card are on the <a href="for-businesses.html#plans">For Businesses</a> and <a href="for-property-managers.html#rates">For Property Managers</a> pages.</p>
  {disclaimer_box()}
  <div class="more rv"><a class="btn btn-cta" href="contact.html#book">Book a Rescue</a> <a class="btn btn-ghost" href="for-businesses.html#enquiry">Request a quote</a></div>
</div></section>'''
    page("pricing.html", "Toilet Cleaning Prices in Winnipeg | ToiletCall.ca",
         "Pricing for ToiletCall.ca toilet cleaning, rescue and restroom-care services, in Canadian dollars. Cleaning, not plumbing.", body)


# ---------------------------------------------------------------- ABOUT
def about():
    alts = ["Team member in a blue uniform talking with a homeowner at the front door",
            "Team member in a blue uniform going through a visit checklist with a homeowner in a bright bathroom",
            "Cleaner in a blue cap and light blue gloves wiping a toilet in a spotless bathroom"]
    imgs = ["about-1-v2.webp", "about-2-v2.webp", "about-3.webp"]
    rows = [
        ("Cleaning only, on purpose", "ToiletCall is a cleaning and rescue service. Staying out of pipe work lets us focus on what matters in the moment: a clean, sanitized, usable toilet."),
        ("Honest about what we do", A("If a job needs pipe work, a leak fixed or a new toilet installed, we tell you straight away and connect you with a licensed plumber from our partner network.")),
        ("Clean, sanitized, restocked", f'Every visit ends with a toilet that is clean, fresh and back in service. Hygiene and products statement: {tbc("", "Hygiene statement")}'),
    ]
    zig = ""
    for n, ((t, p), im, al) in enumerate(zip(rows, imgs, alts), 1):
        tilt = -3 if n % 2 else 3
        zig += f'''<div class="row rv"><figure class="photo" style="--tilt:{tilt}deg"><div class="photo-frame"><img src="{im}" width="900" height="672" loading="lazy" alt="{al}"></div></figure>
<div class="row-text"><span class="idx">{n:02d}</span><h3>{t}</h3><p>{p}</p></div></div>'''
    body = f'''{pagehead("About us", "About ToiletCall", "A cleaning-only toilet rescue service, built for the moment a toilet becomes a problem.", "heart")}
<section class="about" style="border-radius:var(--radius)"><div class="wrap"><div class="zig">{zig}</div></div></section>
<section><div class="wrap">
  <h2 class="rv">Trust details</h2>
  <ul class="slots rv"><li><strong>Reviews:</strong> {tbc("", "Reviews")}</li><li><strong>Registration and insurance:</strong> {tbc("", "Credentials")}</li>
  <li><strong>Hours:</strong> {tbc("hours", "Hours")}</li><li><strong>Service area:</strong> {tbc("area", "Service area")}</li></ul>
</div></section>
{final_cta()}'''
    page("about.html", "About ToiletCall | Toilet Cleaning in Winnipeg",
         "About ToiletCall.ca: a cleaning-only toilet rescue service, not a plumbing company, with honest referrals when a job needs pipe work.", body)


def faq():
    LD_EXTRA["faq.html"] = [{"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in FAQ]}]
    body = f'''{pagehead("FAQ", "Questions about toilet cleaning and rescue", "Straight answers, starting with the one we hear most.", "chats-circle")}
<section><div class="wrap">{faq_list(FAQ)}{referral()}</div></section>
{final_cta()}'''
    page("faq.html", "Toilet Cleaning &amp; Unclogging FAQ | ToiletCall.ca",
         "Answers to common questions about ToiletCall.ca: cleaning, not plumbing, unclogging simple blockages, referrals and payment.", body)


# ---------------------------------------------------------------- CONTACT
def contact():
    body = f'''{pagehead("Contact / Book", "Book a toilet rescue", "Phone first. The form below is the backup, not the gate.", "phone-call")}
<section><div class="wrap two">
  <div class="info">
    <ul class="infolist">
      <li>{ic("phone-call")}<span><strong>Phone</strong><a class="bigtel" data-tel href="#book">{tbc("phone", "Phone")}</a></span></li>
      <li>{ic("map-pin")}<span><strong>Address</strong>@@STREET@@</span></li>
      <li>{ic("clock")}<span><strong>Hours</strong>{tbc("hours", "Hours")}</span></li>
      <li>{ic("map-pin")}<span><strong>Service area</strong>{tbc("area", "Service area")}</span></li>
      <li>{ic("chats-circle")}<span><strong>Email</strong>{tbc("email", "Email")}</span></li>
    </ul>
    {disclaimer_box()}
    <div class="paycard" id="pay">
      <h2>Pay online</h2>
      <p>Already had your visit or quote? Choose how you would like to pay.</p>
      <div class="pay-opts">
        <a class="btn btn-cta" id="payBtn" href="#pay" target="_blank" rel="noopener noreferrer">{ic("credit-card")}Pay by card</a>
        <button class="btn btn-ghost" id="etBtn" type="button" aria-expanded="false" aria-controls="etBox">{ic("bank")}Pay by e-Transfer</button>
      </div>
      <div class="etbox" id="etBox" hidden>
        <p>Send an Interac e-Transfer to:</p>
        <p class="etmail" id="etEmail"></p>
        <button class="btn btn-cta btn-sm" id="etCopy" type="button">Copy email</button>
        <p class="etnote">Please add your name and job address in the message.</p>
        <p class="paymsg" id="payMsg" role="status"></p>
      </div>
    </div>
  </div>
  {booking_form()}
</div></section>'''
    page("contact.html", "Book a Toilet Rescue in Winnipeg | ToiletCall.ca",
         "Book a toilet cleaning and rescue visit in Winnipeg, or call @@PHONE@@. Emergencies 24/7. Cleaning, not plumbing.", body)


def privacy():
    body = f'''{pagehead("Privacy", "Privacy notice", "How ToiletCall.ca uses the details you send us.", "shield-check")}
<section><div class="wrap prose">
  <h2>What we collect</h2><p>The details you type into our forms: name, phone, email, address or area, property type, what is wrong, notes and an optional photo. Business and property-manager forms also ask for company details. We do not use analytics or tracking tools on this site.</p>
  <h2>Why</h2><p>Only to reply to your request, book and carry out a visit, and arrange a referral when a job needs one.</p>
  <h2>Who sees it</h2><p>The ToiletCall owner receives form submissions by email through our form service. Card payments are taken on Stripe&rsquo;s own page, and we never see your card details.</p>
  <h2>Keeping and removing your details</h2>
  <p>We keep your details only as long as we need them to reply to you, carry out your visit or subscription, arrange a referral, and meet any record-keeping the law requires (for example, accounting records). After that we delete them.</p>
  <p>You can ask us at any time to see, correct or delete the details we hold about you. Email us at {tbc("email", "Email")} or call {tbc("phone", "Phone")}, and we will deal with your request promptly.</p>
</div></section>'''
    page("privacy.html", "Privacy | ToiletCall.ca", "Privacy notice for ToiletCall.ca: what details we collect through our booking and enquiry forms, why, and how to have them deleted.", body)


# ---------------------------------------------------------------- SERVICE PAGES
SVC_PAGES = {
 "s1": ("emergency-toilet-cleaning.html", "Emergency Toilet Cleaning &amp; Sanitizing | ToiletCall.ca",
        "Emergency toilet cleaning and sanitizing for dirty, soiled or unusable toilets. Fast help from ToiletCall.ca. Cleaning, not plumbing.",
        "Emergency toilet cleaning and sanitizing", "Dirty, soiled or unusable right now? One call and we clean and sanitize it.",
        "$89 per visit. After-hours and emergency call-outs: $129. Prices in CAD, before tax."),
 "s2": ("toilet-unclogging.html", "Toilet Unclogging for Waste &amp; Paper Blockages | ToiletCall.ca",
        "Toilet unclogging for simple waste or paper blockages, with cleaning and sanitizing included. No pipe repairs. ToiletCall.ca.",
        "Unclogging a toilet - no plumbing repair", "Blocked by waste or paper? We clear it and clean up.",
        "Included in the $89 one-time toilet rescue visit ($129 after hours or in an emergency). Prices in CAD, before tax."),
 "s3": ("toilet-odour-removal.html", "Toilet Odour Removal &amp; Deodorizing | ToiletCall.ca",
        "Toilet odour removal and deodorizing: deep cleaning and sanitizing for smells that keep coming back. ToiletCall.ca.",
        "Odour removal and deodorizing", "A smell that keeps coming back? We deep clean, sanitize and deodorize.",
        "Included in the $89 one-time toilet rescue visit ($129 after hours or in an emergency). Prices in CAD, before tax."),
 "s4": ("restroom-restocking.html", "Restroom Restocking: Tissue, Soap &amp; Paper Towels | ToiletCall.ca",
        "Restroom restocking for homes and businesses: tissue, soap and paper towels checked and refilled. ToiletCall.ca.",
        "Restroom restocking", "Tissue, soap and paper towels checked and refilled.",
        "$39 per visit. Supplies billed at cost, or we restock with yours. Best added to a business subscription. Prices in CAD, before tax."),
 "s5": ("restroom-inspections.html", "Scheduled Restroom Inspections for Businesses | ToiletCall.ca",
        "Scheduled restroom inspections for businesses: cleanliness, odours and supplies checked, with a simple report after each visit.",
        "Scheduled restroom inspections", "Regular checks so small problems are caught early.",
        "Part of the business restroom-care subscription, from $149/month. Prices in CAD, before tax."),
 "s6": ("move-in-move-out-toilet-cleaning.html", "Move-In / Move-Out Toilet Deep Cleaning | ToiletCall.ca",
        "Move-in and move-out toilet deep cleaning for empty or newly occupied homes, rentals and listings. ToiletCall.ca.",
        "Move-in / move-out deep cleaning", "Deep-cleaned toilets before keys change hands or guests arrive.",
        "$69 for the first bathroom, $39 for each additional bathroom. Prices in CAD, before tax."),
 "s7": ("seniors-landlords-airbnb-toilet-help.html", "Toilet Help for Seniors, Landlords &amp; Airbnb Hosts | ToiletCall.ca",
        "Respectful in-home toilet help for seniors, and fast toilet cleaning turnarounds for landlords and Airbnb hosts. ToiletCall.ca.",
        "Help for seniors, landlords and Airbnb hosts", "Respectful help at home, and quick turnarounds between tenants and guests.",
        "Visits start at $89 (one-time rescue). Property managers: see the rate card. Prices in CAD, before tax."),
}
ICONS = {i: icn for i, icn, _ in SERVICES}
TITLES = {i: t for i, _, t in SERVICES}
SVC_FILES = {v[0]: TITLES[k] for k, v in SVC_PAGES.items()}
PRICE_NUM = {"s1": ("89", "CAD"), "s2": ("89", "CAD"), "s3": ("89", "CAD"), "s4": ("39", "CAD"), "s5": ("149", "CAD"), "s6": ("69", "CAD"), "s7": ("89", "CAD")}

def plain(x):
    x = re.sub(r"<!--.*?-->", "", x, flags=re.S)
    x = re.sub(r"<[^>]+>", "", x)
    return html.unescape(re.sub(r"\s+", " ", x)).strip()


def service_pages():
    for i, (fname, title, desc, h1, lede, price) in SVC_PAGES.items():
        what, when, inc = SVC_DET[i]
        related = "".join(f'<a class="mini" href="{SVC_PAGES[k][0]}"><span class="tile" aria-hidden="true">{ic(ICONS[k])}</span><span><strong>{A(TITLES[k]) if "plumbing" in TITLES[k] else TITLES[k]}</strong></span></a>' for k in SVC_PAGES if k != i)
        h1h = A(h1) if "plumbing" in h1 else h1
        url_ = DOMAIN + "/" + fname.replace(".html", "")
        LD_EXTRA[fname] = [{"@type": "Service", "@id": url_ + "#service", "name": plain(h1), "serviceType": plain(h1), "description": plain(what),
                            "url": url_, "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "City", "name": "Winnipeg"},
                            "offers": {"@type": "Offer", "priceCurrency": "CAD", "price": PRICE_NUM[i][0], "priceSpecification": {"@type": "PriceSpecification", "priceCurrency": "CAD", "price": PRICE_NUM[i][0], "valueAddedTaxIncluded": False}, "url": url_}}]
        body = f'''<section class="pagehead"><div class="wrap"><div class="ph-panel">
<p class="kicker"><a href="services.html" style="text-decoration:none">Services</a> / {h1h}</p><h1>{h1h}</h1><p class="lede">{lede}</p>
<span class="ph-icon" aria-hidden="true">{ic(ICONS[i])}</span></div></div></section>
<section><div class="wrap two">
  <div>
    <h2 class="rv">What it is</h2><p class="rv">{what}</p>
    <h2 class="rv">When to call</h2><p class="rv">{when}</p>
    <h2 class="rv">What is included</h2><p class="rv">{inc}</p>
    <h2 class="rv">Price</h2><p class="rv"><strong>{price}</strong> See the full <a href="pricing.html">pricing page</a>.</p>
    <h2 class="rv">What we do not do</h2><p class="rv">{A(SCOPE)}</p>
    <div class="more rv"><a class="btn btn-cta" href="contact.html#book">Book a Rescue</a> <a class="btn btn-ghost" data-tel href="contact.html#book">Call now</a></div>
  </div>
  <aside>{disclaimer_box()}{referral()}</aside>
</div></section>
<section class="plansec"><div class="wrap"><h2 class="rv">Other services</h2><div class="minis">{related}</div></div></section>
{final_cta()}'''
        page(fname, title, desc, body)


home(); services(); service_pages(); businesses(); property_managers(); pricing(); about(); faq(); contact(); privacy()

pages = ["index.html", "services.html"] + [v[0] for v in SVC_PAGES.values()] + [ "for-businesses.html", "for-property-managers.html", "pricing.html", "about.html", "faq.html", "contact.html", "privacy.html"]

import secrets
PRIO = {"index.html": "1.0", "services.html": "0.9", "contact.html": "0.9", "pricing.html": "0.8", "for-businesses.html": "0.8", "for-property-managers.html": "0.8", "faq.html": "0.7", "about.html": "0.6", "privacy.html": "0.3"}
def u(p): return DOMAIN + "/" + ("" if p == "index.html" else p.replace(".html", ""))
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
for p in pages:
    sm += f"  <url>\n    <loc>{u(p)}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>{'weekly' if p in ('index.html','pricing.html') else 'monthly'}</changefreq>\n    <priority>{PRIO.get(p, '0.7')}</priority>\n"
    sm += f'    <xhtml:link rel="alternate" hreflang="en-CA" href="{u(p)}"/>\n'
    if p == "index.html": sm += f"    <image:image><image:loc>{DOMAIN}/og-image.png</image:loc><image:title>ToiletCall toilet cleaning and rescue</image:title></image:image>\n"
    sm += "  </url>\n"
(OUT / "sitemap.xml").write_text(sm + "</urlset>\n")

bots = ["Googlebot", "Bingbot", "Applebot", "Applebot-Extended", "DuckDuckBot", "YandexBot", "Baiduspider", "GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-User", "Claude-SearchBot", "anthropic-ai", "PerplexityBot", "Perplexity-User", "Google-Extended", "Meta-ExternalAgent", "CCBot", "Amazonbot", "cohere-ai", "Bytespider", "MistralAI-User"]
rb = "# ToiletCall.ca - all search engines and AI assistants are welcome\nUser-agent: *\nAllow: /\nDisallow: /404.html\n\n"
rb += "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots)
rb += f"Sitemap: {DOMAIN}/sitemap.xml\n"
(OUT / "robots.txt").write_text(rb)

# llms.txt
svc_lines = "\n".join(f"- [{plain(TITLES[k])}]({u(v[0])}): {plain(SVC_DET[k][0])}" for k, v in SVC_PAGES.items())
llms = f"""# ToiletCall.ca

> ToiletCall is a toilet cleaning and rescue service in Winnipeg, Manitoba, Canada. We clean, sanitize, unclog simple waste or paper blockages, remove odours and restock restrooms. ToiletCall is NOT a plumbing company: for pipe repairs, leaks or toilet installation we refer customers to a licensed plumber.

Phone: @@PHONE@@ | Email: @@EMAIL@@ | Address: @@STREET@@, Winnipeg, MB | Hours: @@HOURS@@ | Prices in CAD, before tax.

## Services
{svc_lines}

## Customers
- [For Businesses]({u("for-businesses.html")}): monthly restroom-care subscriptions from $149/month (restaurants, gas stations, offices, churches, small businesses).
- [For Property Managers]({u("for-property-managers.html")}): toilet concierge for rental properties, emergency call-out $79 ($59 for account holders).

## Key facts
- [Pricing]({u("pricing.html")}): one-time toilet rescue $89 per visit, $129 after hours or emergency; move-in/move-out deep clean $69 first bathroom, $39 each additional; restocking $39 per visit.
- [FAQ]({u("faq.html")}): answers on scope, unclogging, plans and payment.
- [About]({u("about.html")}): cleaning-only by design, honest referrals to licensed plumbers when needed.
- [Book or contact]({u("contact.html")}): booking form, phone, card and Interac e-Transfer payment.

## Optional
- [Full text version]({DOMAIN}/llms-full.txt)
- [Privacy]({u("privacy.html")})
"""
(OUT / "llms.txt").write_text(fill(llms))
faq_txt = "\n\n".join(f"### {q}\n{plain(a)}" for q, a in FAQ)
full = llms.split("## Services")[0] + "## Services\n\n" + "\n\n".join(f"### {plain(TITLES[k])}\nURL: {u(v[0])}\n{plain(SVC_DET[k][0])}\nWhen to call: {plain(SVC_DET[k][1])}\nIncluded: {plain(SVC_DET[k][2])}\nPrice: {v[5]}" for k, v in SVC_PAGES.items()) + f"\n\n## Business subscription plans (CAD/month, before tax)\n- Essential $149: 1 restroom, weekly visit\n- Standard $249: up to 3 restrooms, weekly visits\n- High-traffic $399: high-traffic restrooms, twice-weekly visits\nEmergency call-outs for subscribers at the standard $89 rate or better.\n\n## Property-manager rate card (CAD, before tax)\n- Emergency cleaning call-out $79 ($59 for account holders on a monthly plan)\n- Tenant-turnover sanitation $59 per bathroom\n- Supply delivery $25 plus supplies\n- Optional retainer $99/month per property, call-outs at $59\n\n## Frequently asked questions\n\n{faq_txt}\n"
(OUT / "llms-full.txt").write_text(fill(full))

(OUT / "site.webmanifest").write_text(json.dumps({"name": "ToiletCall.ca", "short_name": "ToiletCall", "description": "Toilet cleaning and rescue service in Winnipeg",
    "start_url": "/", "display": "browser", "background_color": "#FFFFFF", "theme_color": "#0E2A47", "lang": "en-CA",
    "icons": [{"src": "favicon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "apple-touch-icon.png", "sizes": "180x180", "type": "image/png"}]}, indent=2))

# 404
body404 = f'''<section class="pagehead"><div class="wrap"><div class="ph-panel"><p class="kicker">Error 404</p><h1>That page is not here.</h1>
<p class="lede">The page may have moved. Head back to the home page, or call us and we will help.</p>
<div class="more"><a class="btn btn-cta" href="index.html">Go to the home page</a> <a class="btn btn-ghost" href="services.html">See services</a></div>
<span class="ph-icon" aria-hidden="true">{ic("question")}</span></div></div></section>'''
page("404.html", "Page not found | ToiletCall.ca", "Page not found.", body404)
t = (OUT / "404.html").read_text().replace('content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"', 'content="noindex, follow"')
t = re.sub(r'<link rel="canonical"[^>]*>\n', "", t)
# 404 must work from any folder depth: absolute asset paths
t = re.sub(r'(href|src)="(?!https?:|#|mailto:|tel:|/)([^"]+)"', r'\1="/\2"', t)
(OUT / "404.html").write_text(t)

# IndexNow key (Bing, Yandex etc.)
keyfile = HERE / "indexnow-key.txt"
key = keyfile.read_text().strip() if keyfile.exists() else secrets.token_hex(16)
keyfile.write_text(key)
(OUT / f"{key}.txt").write_text(key)
print("built", len(pages), "pages; indexnow key", key)

cfgjs = {"phone": CFG["phone"], "phoneTel": CFG["phone_tel"], "email": CFG["email"], "hours": CFG["hours"], "area": CFG["area"], "response": CFG["response"],
         "etUser": CFG["etransfer_email"].split("@")[0] if "@" in CFG["etransfer_email"] else "", "etHost": CFG["etransfer_email"].split("@")[1] if "@" in CFG["etransfer_email"] else "",
         "stripeLink": CFG["stripe_link"], "web3formsKey": CFG["web3forms_key"]}
(OUT / "config.js").write_text("/* GENERATED from site-config.json by _source/build.py - edit site-config.json, not this file. */\nvar CONFIG = " + json.dumps(cfgjs, indent=2) + ";\n")
(OUT / "robots.txt").write_text(fill((OUT / "robots.txt").read_text()))
if os.environ.get("LIST_ICONS"): print("\n".join(f"{w}/{n}" for w, n in sorted(USED)))
