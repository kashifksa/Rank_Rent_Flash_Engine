#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_builder.py - one-command smoke test for the Site Builder (builder/index.html).

    python scripts/test_builder.py

Checks: sections match schema, builder loads with no console errors, every template x page renders,
Before/After cards + slider exist, animation/option attributes export, edits reach the export,
logo upload reaches the export, and (optionally) screenshots are saved to scratch/test_shots/.
Exit code 1 if anything fails.
"""
import os, sys, subprocess
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
SHOTS = ROOT / "scratch" / "test_shots"
fails = []


def check(name, ok, extra=""):
    print(("PASS  " if ok else "FAIL  ") + name + (("  -> " + str(extra)) if extra and not ok else ""))
    if not ok:
        fails.append(name)


def main():
    # 1. sections vs schema
    v = subprocess.run([sys.executable, str(ROOT / "validate_sections.py")], capture_output=True, text=True, encoding="utf-8", errors="replace")
    check("sections match sections_schema.json (validate_sections.py)", v.returncode == 0, v.stdout[-400:])
    # 2. fresh data
    c = subprocess.run([sys.executable, str(ROOT / "scripts" / "compile_builder_data.py")], capture_output=True, text=True, encoding="utf-8", errors="replace")
    check("compile_builder_data.py runs", c.returncode == 0, c.stderr[-300:])

    from playwright.sync_api import sync_playwright
    cp = next((x for x in (r"C:\Program Files\Google\Chrome\Application\chrome.exe", r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe") if os.path.exists(x)), None)
    SHOTS.mkdir(parents=True, exist_ok=True)
    errors = []
    with sync_playwright() as p:
        kw = {"headless": True}
        if cp:
            kw["executable_path"] = cp
        else:
            kw["channel"] = "msedge"
        b = p.chromium.launch(**kw)
        pg = b.new_page(viewport={"width": 1700, "height": 980})
        pg.on("pageerror", lambda e: errors.append("PAGEERROR " + str(e)))
        pg.on("console", lambda m: errors.append("CONSOLE " + m.text) if m.type == "error" else None)
        pg.goto("file:///" + str(ROOT / "builder" / "index.html").replace("\\", "/"))
        pg.wait_for_timeout(1000)
        pg.evaluate("localStorage.clear()"); pg.reload(); pg.wait_for_timeout(800)

        r = pg.evaluate("""() => {
          const B = window.Builder, bad = [], rows = [];
          for (const t of Object.keys(B.TEMPLATES)) {
            B.setTemplate(t);
            for (const pid of B.pageIds()) {
              const h = B.exportPage(pid);
              const n = (h.match(/<section class="sec /g) || []).length;
              if (h.includes('Render error') || n !== B.sectionList(pid).length) bad.push(t + '/' + pid);
              rows.push(n);
            }
          }
          B.setTemplate('cornerstone');
          const home = B.exportPage('homepage');
          B.setTemplate('keystone');
          const key = B.exportPage('homepage');
          B.setTemplate('cornerstone');
          return { bad, combos: rows.length, cards: (home.match(/class="dba-card"/g) || []).length,
                   revs: (home.match(/class="card rev/g) || []).length, areaTags: (home.match(/class="tag"/g) || []).length,
                   cases: (key.match(/class="ba-case"/g) || []).length, anim: /data-anim="rise"/.test(home), fx: /data-fx="airflow"/.test(home),
                   caseStudies: home.includes('id="sec-case-studies"') };
        }""")
        check("every template x page renders (%d combos)" % r["combos"], not r["bad"], r["bad"])
        # templates: each skin must exist, headers valid, and the primary button must be readable (WCAG AA 4.5:1)
        tc = pg.evaluate("""() => { const B = Builder, lum = h => { h = h.replace('#',''); if (h.length === 3) h = h.split('').map(c => c + c).join('');
            const c = [0,2,4].map(i => parseInt(h.substr(i,2),16)/255).map(v => v <= .03928 ? v/12.92 : Math.pow((v+.055)/1.055, 2.4)); return .2126*c[0]+.7152*c[1]+.0722*c[2]; };
          const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x,y)+.05)/(Math.min(x,y)+.05); };
          const out = {}; Object.keys(B.TEMPLATES).forEach(k => { B.setTemplate(k); const t = B.TEMPLATES[k], css = (B.SKINS || {})[t.skin] || '', vars = B.cssVars();
            const mv = vars.match(/--btn-fg:(#[0-9a-fA-F]{3,6})/), ms = css.match(/\.btn-primary\{color:(#[0-9a-fA-F]{3,6})/), txt = ms ? ms[1] : (mv ? mv[1] : '#ffffff');
            out[k] = { skin: t.skin, header: t.header, skinOk: !t.skin || css.length > 50, hdrOk: ['classic','topbar','dark','decker','floating','gridline','console'].indexOf(t.header || 'classic') > -1, ratio: +ratio(t.theme.accent, txt).toFixed(2) }; });
          B.setTemplate('cornerstone'); return out; }""")
        bad_t = [k for k, v in tc.items() if not v["skinOk"] or not v["hdrOk"]]
        check("every template has a valid skin and header variant", not bad_t, bad_t)
        low = {k: v["ratio"] for k, v in tc.items() if v["ratio"] < 4.5}
        check("every template keeps the primary button readable (>= 4.5:1)", not low, tc)
        check("Homepage customer reviews render (>= 3 review cards)", r["revs"] >= 3, r["revs"])
        check("Homepage service area tags render (>= 3 tags)", r["areaTags"] >= 3, r["areaTags"])
        check("Before/After: 3 comparison cards (Cornerstone)", r["cards"] == 3, r["cards"])
        check("Before/After: wipe slider cases (Keystone)", r["cases"] >= 1, r["cases"])
        check("animation attribute exported (Cornerstone = rise)", r["anim"])
        check("hero effect exported (Cornerstone = airflow)", r["fx"])
        check("Case Studies section present on homepage", r["caseStudies"])

        # SEO: JS panel must agree with scripts/seo_audit.py (same thresholds, same math)
        sys.path.insert(0, str(ROOT / "scripts"))
        import seo_audit
        js = pg.evaluate("() => { const o = {}; Builder.pageIds().forEach(id => { const r = Builder.seoAudit(id); o[id] = r && r.density ? [r.density.combinedPct, r.score] : null; }); return o; }")
        drift, nopy = [], 0
        for pid_, val in js.items():
            py = seo_audit.audit_page(pid_)
            if not py or "density" not in py or not val:
                nopy += 1
                continue
            if abs(py["density"]["combined_pct"] - val[0]) > 0.15:
                drift.append((pid_, py["density"]["combined_pct"], val[0]))
        check("SEO panel (JS) density matches seo_audit.py (+-0.15)", not drift, drift)
        check("SEO audit covers every page with a keyword", len(js) - nopy >= 8, f"{len(js) - nopy}/{len(js)}")
        # location page: the single SEO panel must also run the doorway / local-proof checks and agree with seo_local.py
        loc_js = pg.evaluate("() => { const r = Builder.seoAudit('air-duct-cleaning-loves-park-il'); return r.checks.map(c => [c.id, c.status]); }")
        loc_js = dict(loc_js)
        import seo_local
        hub, state, company = seo_local.brief_info()
        texts = {}
        for pid_ in seo_audit.all_page_ids():
            fm_, body_ = seo_audit.split_front_matter((ROOT / f"page_content_{pid_}.md").read_text(encoding="utf-8", errors="ignore"))
            texts[pid_] = seo_audit.clean_text(body_)
        loc_py = {c["id"]: c["status"] for c in seo_local.audit_location("air-duct-cleaning-loves-park-il", texts, hub, state, company)["checks"]}
        mism = {k: (loc_py[k], loc_js.get(k)) for k in loc_py if loc_js.get(k) != loc_py[k]}
        check("SEO panel runs location checks and matches seo_local.py", "similarity" in loc_js and not mism, mism)
        # Phase 3 structure / schema / NAP checks: JS panel must give the same verdicts as seo_audit.py on every page
        P3 = ["word_total", "word_sections", "answer_first", "headings", "parseable", "faq", "schema_types", "schema_faq_match", "nap"]
        js3 = pg.evaluate("() => { const o = {}; Builder.pageIds().forEach(id => { const r = Builder.seoAudit(id); o[id] = r ? Object.fromEntries(r.checks.map(c => [c.id, c.status])) : {}; }); return o; }")
        diff3 = []
        for pid_ in js3:
            py = seo_audit.audit_page(pid_)
            if not py:
                continue
            pys = {c["id"]: c["status"] for c in py["checks"]}
            for k in P3:
                if k in pys and js3[pid_].get(k) != pys[k]:
                    diff3.append((pid_, k, pys[k], js3[pid_].get(k)))
        check("Phase 3 checks (JS) match seo_audit.py on every page", not diff3, diff3[:4])
        check("Phase 3 checks exist in the panel", all(k in js3["commercial-hvac-duct-cleaning"] for k in ["word_total", "answer_first", "schema_types", "nap"]))
        # Phase 4 link / cannibalization checks: same verdicts in the panel and in seo_audit.py
        P4 = ["links_planned", "links_broken", "links_contextual", "links_self", "anchors", "cannibal", "blog_intent", "location_hub"]
        diff4 = []
        for pid_ in js3:
            py = seo_audit.audit_page(pid_)
            if not py:
                continue
            pys = {c["id"]: c["status"] for c in py["checks"]}
            js_now = pg.evaluate("(id) => Object.fromEntries(Builder.seoAudit(id).checks.map(c => [c.id, c.status]))", pid_)
            for k in P4:
                if k in pys and js_now.get(k) != pys[k]:
                    diff4.append((pid_, k, pys[k], js_now.get(k)))
        check("Phase 4 link checks (JS) match seo_audit.py on every page", not diff4, diff4[:4])
        # a link to an unbuilt page must FAIL, a link to a live page must pass
        r4 = pg.evaluate("""() => { const B = Builder, m = B.editModel('commercial-hvac-duct-cleaning', '09_faq');
          m.paras = (m.paras || []).concat(['See [air duct cleaning in Belvidere](air-duct-cleaning-belvidere-il.html) and [dryer vents](dryer-vent-cleaning-and-lint-removal.html).']);
          const r = Builder.seoAudit('commercial-hvac-duct-cleaning'); const o = Object.fromEntries(r.checks.map(c => [c.id, c.status]));
          B.resetSection('commercial-hvac-duct-cleaning', '09_faq'); return o; }""")
        check("link to an unbuilt page fails (planned-link rule)", r4.get("links_planned") == "fail", r4)
        # Phase 5 E-E-A-T / rules / image QA / reviews: same verdicts in the panel and in seo_audit.py
        P5 = ["experience", "credentials", "filler", "superlatives", "repetition", "rules", "images", "reviews"]
        diff5 = []
        for pid_ in js3:
            py = seo_audit.audit_page(pid_)
            if not py:
                continue
            pys = {c["id"]: c["status"] for c in py["checks"]}
            js_now = pg.evaluate("(id) => Object.fromEntries(Builder.seoAudit(id).checks.map(c => [c.id, c.status]))", pid_)
            for k in P5:
                if k in pys and js_now.get(k) != pys[k]:
                    diff5.append((pid_, k, pys[k], js_now.get(k)))
        check("Phase 5 checks (JS) match seo_audit.py on every page", not diff5, diff5[:5])
        r5 = pg.evaluate("""() => { const B = Builder, m = B.editModel('commercial-hvac-duct-cleaning', '09_faq');
          m.paras = (m.paras || []).concat(['We are the best \\u2014 only $99 flat-rate, look no further.']);
          const r = Builder.seoAudit('commercial-hvac-duct-cleaning'); const o = Object.fromEntries(r.checks.map(c => [c.id, c.status]));
          B.resetSection('commercial-hvac-duct-cleaning', '09_faq'); return o; }""")
        check("hard-rule violations (em dash, price) FAIL; filler/superlatives WARN", r5.get("rules") == "fail" and r5.get("filler") == "warn" and r5.get("superlatives") == "warn", r5)
        check("non-location pages do not get location checks", "similarity" not in dict(pg.evaluate("() => Builder.seoAudit('commercial-hvac-duct-cleaning').checks.map(c => [c.id, c.status])")))
        before = pg.evaluate("Builder.seoAudit('homepage').density.combinedPct")
        pg.evaluate("""() => { const B = Builder, m = B.editModel('homepage', 'intro');
          m.paras = (m.paras || []).concat(['We provide air duct cleaning in Rockford. '.repeat(30)]); }""")
        after = pg.evaluate("Builder.seoAudit('homepage').density.combinedPct")
        check("SEO density reacts live to text edits", after > before, (before, after))
        pg.evaluate("() => { Builder.resetSection('homepage', 'intro'); }")
        pg.click("#seoBtn"); pg.wait_for_timeout(300)
        check("SEO button opens the audit panel", pg.is_visible("#seoPop") and "Primary keyword" in pg.inner_text("#seoPop"))
        pg.click("#seoBtn")
        hh = pg.evaluate("Builder.exportPage('homepage')")
        hdr, ftr = hh.split("</header>")[0], hh.split("<footer")[1]
        check("logo auto-detected in header (images/*logo*.webp)", "logo.webp" in hdr)
        check("light logo variant used in footer", "logo-light.webp" in ftr)
        check("logo is never used as a content image", "logo" not in "".join(pg.evaluate("Builder.imageOptions('homepage').map(i => i.file)")))

        # edit -> export
        pg.select_option("#tplSel", "keystone"); pg.wait_for_timeout(400)
        pg.click("#seclist .row:nth-child(3)"); pg.wait_for_timeout(400)
        el = pg.query_selector('#editor input[data-f="h2"]') or pg.query_selector('#editor input[data-f="h1"]')
        el.fill("TEST EDIT 123"); pg.wait_for_timeout(300)
        check("text edit reaches export", "TEST EDIT 123" in pg.evaluate("Builder.exportPage('homepage')"))
        pg.select_option('#editor select[data-o="anim"]', "zoom"); pg.wait_for_timeout(200)
        check("animation option reaches export", 'data-anim="zoom"' in pg.evaluate("Builder.exportPage('homepage')"))
        pg.evaluate("""() => { const c=document.createElement('canvas'); c.width=200; c.height=60; const x=c.getContext('2d'); x.fillStyle='#09f'; x.fillRect(0,0,200,60);
          Builder.state.brand={logoSrc:'upload',logoData:c.toDataURL('image/webp'),mode:'logo',height:44,favicon:true,footer:true}; }""")
        check("logo reaches export", '<img src="data:image/' in pg.evaluate("Builder.exportPage('homepage')"))
        check("saved edit dropped when its source text changes (no drift)", pg.evaluate("""() => { const B=Builder; const sid='services-grid'; B.editModel('homepage',sid);
          B.ps('homepage').srcHash[sid]='x'; return B.reconcile() >= 1; }"""))
        pg.reload(); pg.wait_for_timeout(800)
        fl = pg.frame_locator("#frame")
        fl.locator("a[href^='#']").first.click()
        pg.wait_for_timeout(300)
        nested_builder = fl.locator("#tplSel").count()
        check("clicking #hash link in preview never loads builder inside #frame", nested_builder == 0, nested_builder)
        pg.screenshot(path=str(SHOTS / "builder_home.png"))
        b.close()
    check("no console / page errors", not errors, errors[:4])
    print("\nscreenshot: " + str(SHOTS / "builder_home.png"))
    print("RESULT: " + ("ALL PASSED" if not fails else f"{len(fails)} FAILED: " + "; ".join(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

