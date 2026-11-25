/* ToiletCall.ca - shared script
   Fill in CONFIG when the owner confirms each detail. Anything left empty
   keeps its visible "[OWNER TO CONFIRM]" placeholder on the page. */
var CONFIG = {
  phone: "(431) 340-5777",          // shown text, e.g. "204 555 0123"
  phoneTel: "+14313405777",       // dialling number, e.g. "+12045550123"
  email: "hello@toiletcall.example",
  hours: "10 am - 6 pm. Emergencies 24/7.",
  area: "Winnipeg and surrounding area",
  response: "",       // response-time wording used on confirmations
  etUser: "payments",         // e-Transfer address, part before the @
  etHost: "toiletcall.example",         // e-Transfer address, part after the @
  stripeLink: "",     // Stripe Payment Link (https://buy.stripe.com/...)
  web3formsKey: ""    // Web3Forms access key
};

(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---------- tracking: none (no analytics) ---------- */
  function track() {}

  /* ---------- owner details ---------- */
  $$("[data-fill]").forEach(function (el) {
    var v = CONFIG[el.getAttribute("data-fill")];
    if (v) { el.textContent = v; el.classList.remove("tbc"); }
  });
  if (CONFIG.phoneTel) $$("[data-tel]").forEach(function (a) { a.setAttribute("href", "tel:" + CONFIG.phoneTel); });
  $$("[data-tel],a[href^='tel:']").forEach(function (a) {
    a.addEventListener("click", function () { track("click_to_call", { page: location.pathname }); });
  });
  if (CONFIG.email) $$("[data-mail]").forEach(function (a) { a.setAttribute("href", "mailto:" + CONFIG.email); });

  /* ---------- mobile menu ---------- */
  var burger = $("#burger"), menu = $("#menu"), scrim = $("#scrim");
  function setMenu(open) {
    if (!burger) return;
    menu.classList.toggle("open", open);
    scrim.classList.toggle("on", open);
    burger.setAttribute("aria-expanded", open);
    burger.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    if (open) menu.removeAttribute("inert"); else menu.setAttribute("inert", "");
  }
  if (burger) {
    burger.addEventListener("click", function () { setMenu(burger.getAttribute("aria-expanded") !== "true"); });
    scrim.addEventListener("click", function () { setMenu(false); });
    menu.addEventListener("click", function (e) { if (e.target.closest("a")) setMenu(false); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && menu.classList.contains("open")) { setMenu(false); burger.focus(); }
    });
    window.matchMedia("(min-width:1200px)").addEventListener("change", function (m) { if (m.matches) setMenu(false); });
  }

  /* ---------- reveal on scroll ---------- */
  var els = $$(".rv");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { threshold: 0.12 });
    els.forEach(function (el) { io.observe(el); });
  } else els.forEach(function (el) { el.classList.add("in"); });

  var yr = $("#yr"); if (yr) yr.textContent = new Date().getFullYear();

  /* ---------- payments ---------- */
  var pb = $("#payBtn");
  if (pb) { if (CONFIG.stripeLink) pb.href = CONFIG.stripeLink; else pb.removeAttribute("target"); }
  var eb = $("#etBtn");
  if (eb) {
    var box = $("#etBox"), em = $("#etEmail"), pm = $("#payMsg");
    eb.addEventListener("click", function () {
      var open = eb.getAttribute("aria-expanded") === "true";
      if (!open) {
        if (CONFIG.etUser && CONFIG.etHost) { em.textContent = CONFIG.etUser + "@" + CONFIG.etHost; em.classList.remove("tbc"); }
        else { em.textContent = "[e-Transfer email: OWNER TO CONFIRM]"; em.classList.add("tbc"); }
      }
      box.hidden = open; eb.setAttribute("aria-expanded", !open);
    });
    var cp = $("#etCopy");
    if (cp) cp.addEventListener("click", function () {
      if (!(CONFIG.etUser && CONFIG.etHost)) { pm.textContent = "The e-Transfer address has not been added yet."; return; }
      var addr = CONFIG.etUser + "@" + CONFIG.etHost;
      try { navigator.clipboard.writeText(addr).then(function () { pm.textContent = "Email copied."; }, function () { pm.textContent = "Please copy the email above."; }); }
      catch (e) { pm.textContent = "Please copy the email above."; }
    });
  }

  /* ---------- forms ---------- */
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  $$("form.js-form").forEach(function (form) {
    var kind = form.getAttribute("data-kind");
    var submit = $("button[type=submit]", form);
    var statusEl = $(".form-status", form);
    var refMsg = $(".referral-msg", form);
    var triage = $$("input[name=triage]", form);
    var isReferral = false;

    triage.forEach(function (r) {
      r.addEventListener("change", function () {
        isReferral = r.checked && r.value === "Yes";
        if (refMsg) refMsg.hidden = !isReferral;
        if (submit) submit.textContent = isReferral ? "Ask for a licensed referral" : submit.getAttribute("data-label");
      });
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var data = new FormData(form);
      var name = (data.get("name") || data.get("contact_name") || "").toString().trim();
      var subject = "ToiletCall.ca: " + (isReferral ? "Licensed referral request" : kind);
      var panel = form.parentNode.querySelector(".confirm");

      function done(sent) {
        track("form_submit", { form: kind, referral: isReferral });
        var resp = CONFIG.response || "We reply during opening hours (10 am - 6 pm), and emergencies are answered 24/7. For the fastest help, call us.";
        var html;
        if (isReferral) {
          html = "<h3>Referral request received</h3><p>Thank you" + (name ? ", " + esc(name) : "") + ". ToiletCall is a cleaning service, so we do not do pipe work ourselves. We will connect you with a licensed plumber from our partner network.</p>" +
                 "<p><strong>What happens next:</strong> we contact you to confirm the details and pass them on. " + resp + "</p>";
        } else if (kind === "Emergency booking") {
          html = "<h3>Your toilet rescue request is in</h3><p>Thank you" + (name ? ", " + esc(name) : "") + ". We have your request for a toilet cleaning and rescue visit. ToiletCall is a cleaning service, not a plumbing company.</p>" +
                 "<p><strong>What happens next:</strong> we contact you to confirm the visit, then attend, clean, sanitize and restock. " + resp + "</p>";
        } else {
          html = "<h3>Enquiry received</h3><p>Thank you" + (name ? ", " + esc(name) : "") + ". We have your " + esc(kind.toLowerCase()) + " and will be in touch to talk it through.</p><p>" + resp + "</p>";
        }
        if (!sent) html += '<p class="demo">Demo form: it is not connected yet, so nothing was sent.</p>';
        panel.innerHTML = html; panel.hidden = false; form.hidden = true;
        panel.setAttribute("tabindex", "-1"); panel.focus();
      }

      if (!CONFIG.web3formsKey) { done(false); return; }
      data.append("access_key", CONFIG.web3formsKey);
      data.append("subject", subject);
      if (submit) { submit.disabled = true; }
      if (statusEl) statusEl.textContent = "Sending...";
      fetch("https://api.web3forms.com/submit", { method: "POST", body: data })
        .then(function (r) { return r.json(); })
        .then(function (j) { if (j && j.success) done(true); else throw new Error("fail"); })
        .catch(function () {
          if (submit) submit.disabled = false;
          if (statusEl) statusEl.textContent = "Sorry, that did not send. Please call us instead.";
        });
    });
  });
})();
