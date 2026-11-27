# ToiletCall.ca - things to fill in

Everything the owner needs to fill in lives in **one file: `_source/site-config.json`**.
After editing it, run `python3 _source/build.py` (Python 3, no packages needed) and upload the changed files.
It rebuilds all pages, the sitemap, `llms.txt`, structured data and `config.js` so every place stays in sync.

## In `site-config.json`
| Setting | What it is | Status |
|---|---|---|
| `phone`, `phone_tel`, `phone_intl` | Booking phone: shown text, dialling number, international format | Set (431) 340-5777 |
| `email` | Booking and contact email (footer, contact page, privacy page, search data) | Set admin@toiletcall.ca |
| `street`, `city`, `region` | Business address for the footer, contact page and Google | Street set; city/region assumed Winnipeg, MB - **confirm** |
| `hours` | Opening hours wording | Set |
| `area` | Service area wording | Set to "Winnipeg and surrounding area" - **confirm** |
| `response` | Response-time sentence shown after a form is sent | Draft - **confirm** |
| `etransfer_email` | Interac e-Transfer address shown after "Pay by e-Transfer" | Set to admin@toiletcall.ca - **confirm** |
| `stripe_link` | Stripe Payment Link (let customers choose the amount). Empty = card button is inactive | **Needed** |
| `web3forms_key` | Access key from web3forms.com, created with the inbox that should get bookings. Empty = forms run in demo mode and send nothing | **Needed** |
| `hygiene_statement` | About page: products and hygiene wording | Draft - **confirm** |
| `reviews_text` | About page reviews line. Replace with real reviews when there are some | Placeholder |
| `credentials_text` | Registration and insurance wording. Only claim what is true | Draft - **confirm** |
| `google_site_verification` | Search Console HTML-tag method: paste ONLY the `content` value (the long code) from the tag Google gives you | Needed after launch |
| `bing_site_verification` | Bing Webmaster Tools meta-tag code (`msvalidate.01` content value) | Optional |
| `domain` | Site address used in canonical links, sitemap and search data | https://toiletcall.ca |

## Not in the config file (edit `_source/build.py`)
- **Prices**: the `pricing()`, `businesses()` and `property_managers()` functions, plus the `SVC_PAGES` prices and `PRICE_NUM` for search data.
- **Page copy and FAQ**: the `FAQ` list and each page function.
- **Hero and About photos**: replace `hero-v2.webp`, `about-1-v2.webp`, `about-2-v2.webp`, `about-3.webp` with cleaning-focused photos (gloves, spray, cloths, tidy restrooms; no wrenches, pipes or tool belts), same filenames.
- **Logo**: `logo-full.png`, `icon.png`, favicons and `og-image.png` use the current artwork. Swap if the client supplies a final "ToiletCall" logo.

## After launch (outside the code)
1. Google Search Console: add the site, verify, submit `https://toiletcall.ca/sitemap.xml`.
2. Bing Webmaster Tools: add the site (import from Search Console is fastest).
3. Google Business Profile: create and verify; use the exact name, address and phone as on the site.
4. Hostinger: switch on the free SSL certificate before uploading `.htaccess`.
5. Privacy page: have the wording reviewed.
