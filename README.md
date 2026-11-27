# ToiletCall.ca

Static website for ToiletCall.ca, a toilet cleaning and rescue service in Winnipeg (not a plumbing company). Plain HTML, CSS and JavaScript on the server, no build step needed to host it.

**Start with `_source/FILL-IN.md`**: it lists everything that needs filling in. All values live in `_source/site-config.json`; run `python3 _source/build.py` to regenerate the pages.

## Hosting (Hostinger)
Upload every file in the repo root (including the hidden `.htaccess`) into `public_html`, enable the free SSL certificate, then visit the site. You do not need to upload `_source`. `.htaccess` forces HTTPS, gives clean URLs (`/contact` instead of `contact.html`), adds security headers and a custom 404.

## SEO
Unique titles and descriptions, canonical and hreflang tags, Open Graph and Twitter cards, JSON-LD (LocalBusiness, WebSite, WebPage, BreadcrumbList, Service, FAQPage), `sitemap.xml`, `robots.txt` (search and AI crawlers allowed), `llms.txt` and `llms-full.txt`, web manifest, custom 404, IndexNow key file.
