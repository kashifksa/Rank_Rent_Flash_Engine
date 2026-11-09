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
                   cases: (key.match(/class="ba-case"/g) || []).length, anim: /data-anim="rise"/.test(home), fx: /data-fx="airflow"/.test(home),
                   caseStudies: home.includes('id="sec-case-studies"') };
        }""")
        check("every template x page renders (%d combos)" % r["combos"], not r["bad"], r["bad"])
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
        pg.screenshot(path=str(SHOTS / "builder_home.png"))
        b.close()
    check("no console / page errors", not errors, errors[:4])
    print("\nscreenshot: " + str(SHOTS / "builder_home.png"))
    print("RESULT: " + ("ALL PASSED" if not fails else f"{len(fails)} FAILED: " + "; ".join(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

