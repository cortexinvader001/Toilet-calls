# ToiletCall.ca

Static website for ToiletCall.ca, a toilet cleaning and rescue service (not a plumbing company). Plain HTML, CSS and JavaScript, no build step.

Pages: Home, Services, For Businesses, For Property Managers, Pricing, About, FAQ, Contact/Book, Privacy.

## Run locally
Open `index.html` in a browser.

## Before launch
All settings are in the `CONFIG` block at the top of `script.js`:
- Replace the dummy phone, email and hours; fill in the service area.
- `stripeLink`: paste the Stripe Payment Link. `etUser` / `etHost`: the e-Transfer email.
- `web3formsKey`: Web3Forms access key (forms are in demo mode until set).
- Fill every remaining `[OWNER TO CONFIRM]` placeholder (prices, reviews, credentials, hygiene statement, privacy details).
- Replace the hero and About photos with cleaning-focused ones.

## Hosting (Hostinger)
Upload every file (including `.htaccess`) into `public_html`, enable the free SSL certificate, then visit the site. `.htaccess` forces HTTPS and adds security headers. Note that `.htaccess` is a hidden file: make sure hidden files are shown when uploading.
