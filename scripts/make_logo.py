#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_logo.py - builds a niche-specific logo (icon + wordmark) as SVG source + transparent WebP (<100 KB).
Reads company name / niche / colors from master_brief.json. Output goes to images/homepage/.

    python scripts/make_logo.py                      # uses brief + builder default accent
    python scripts/make_logo.py --accent "#fd761a" --dark "#121315"
"""
import sys, os, json, re, argparse, io
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent

# niche -> icon glyph (64x64 viewBox, drawn white on the accent tile). Add a niche = add one entry.
ICONS = {
    "air duct": '<rect x="12" y="18" width="40" height="28" rx="6" fill="none" stroke="#fff" stroke-width="4"/>'
                '<path d="M18 28c5-4 7 4 12 0s7 4 12 0" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/>'
                '<path d="M18 37c5-4 7 4 12 0s7 4 12 0" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/>',
    "roof": '<path d="M10 34 32 14l22 20" fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M18 31v18h28V31" fill="none" stroke="#fff" stroke-width="4" stroke-linejoin="round"/>',
    "plumb": '<path d="M32 12c8 10 13 17 13 24a13 13 0 0 1-26 0c0-7 5-14 13-24z" fill="none" stroke="#fff" stroke-width="4" stroke-linejoin="round"/>',
    "default": '<path d="M32 14 50 24v16L32 50 14 40V24z" fill="none" stroke="#fff" stroke-width="4" stroke-linejoin="round"/>',
}


def pick_icon(niche: str) -> str:
    n = (niche or "").lower()
    for k, v in ICONS.items():
        if k != "default" and k in n:
            return v
    if "hvac" in n or "duct" in n or "vent" in n:
        return ICONS["air duct"]
    return ICONS["default"]


def split_name(company: str, city: str):
    """'Rockford Air Duct Pros' -> ('ROCKFORD', 'AIR DUCT PROS')."""
    words = company.upper().split()
    if city and words and words[0] == city.upper():
        return words[0], " ".join(words[1:]) or company.upper()
    if len(words) >= 3:
        return words[0], " ".join(words[1:])
    return company.upper(), ""


def logo_html(line1, line2, icon, accent, text_color, font_q):
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?{font_q}&display=swap" rel="stylesheet">
<style>
html,body{{margin:0;background:transparent}}
#logo{{display:inline-flex;align-items:center;gap:14px;padding:8px;font-family:'Montserrat','Segoe UI',Arial,sans-serif}}
#logo svg{{width:72px;height:72px;display:block}}
.t1{{font-weight:800;font-size:34px;letter-spacing:.5px;color:{text_color};line-height:1}}
.t2{{font-weight:700;font-size:15.5px;letter-spacing:4.2px;color:{accent};margin-top:7px;line-height:1}}
</style></head><body>
<div id="logo"><svg viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="{accent}"/>{icon}</svg>
<div><div class="t1">{line1}</div><div class="t2">{line2}</div></div></div></body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--accent", default="#fd761a")
    ap.add_argument("--dark", default="#121315")
    ap.add_argument("--out", default=str(ROOT / "images" / "homepage"))
    a = ap.parse_args()

    brief = json.loads((ROOT / "master_brief.json").read_text(encoding="utf-8"))
    company = brief.get("nap", {}).get("company_name") or brief.get("project_name", "Company")
    line1, line2 = split_name(company, brief.get("city", ""))
    icon = pick_icon(brief.get("niche", ""))
    slug = re.sub(r"[^a-z]+", "-", company.lower()).strip("-")
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    font_q = "family=Montserrat:wght@700;800"

    from playwright.sync_api import sync_playwright
    from PIL import Image
    cp = next((x for x in (r"C:\Program Files\Google\Chrome\Application\chrome.exe", r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe") if os.path.exists(x)), None)

    results = []
    with sync_playwright() as p:
        kw = {"headless": True}
        if cp:
            kw["executable_path"] = cp
        else:
            kw["channel"] = "msedge"
        b = p.chromium.launch(**kw)
        for variant, text_color in (("logo", a.dark), ("logo-light", "#ffffff")):
            pg = b.new_page(device_scale_factor=3, viewport={"width": 700, "height": 200})
            pg.set_content(logo_html(line1, line2, icon, a.accent, text_color, font_q))
            try:
                pg.wait_for_load_state("networkidle", timeout=6000)
            except Exception:
                pass
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(400)
            png = pg.locator("#logo").screenshot(omit_background=True)
            img = Image.open(io.BytesIO(png)).convert("RGBA")
            path = out / f"{slug}-{variant}.webp"
            for q in (92, 85, 75, 65, 50):
                img.save(path, "WEBP", quality=q, method=6)
                if path.stat().st_size <= 100 * 1024:
                    break
            # editable vector source (icon only) for future edits
            if variant == "logo":
                svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="{a.accent}"/>{icon}</svg>'
                (out / f"{slug}-logo-icon.svg").write_text(svg, encoding="utf-8")
            results.append((path.name, img.size, round(path.stat().st_size / 1024, 1)))
            pg.close()
        b.close()
    for name, size, kb in results:
        print(f"OK {name}  {size[0]}x{size[1]}px  {kb} KB")
    print(f"icon source: {slug}-logo-icon.svg  | text: '{line1}' / '{line2}'")


if __name__ == "__main__":
    main()

