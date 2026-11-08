#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compile_builder_data.py — Dynamic Pipeline-to-Builder Compiler
==============================================================
Reads master_brief.json + topical_authority.json + all page_content_[slug].md files
AND all templates/*.html files, compiles them into scripts/builder_data.js, and
syncs window.BUILDER_PAGES_DATA + window.STITCH_TEMPLATES_HTML inside studio_builder.html.
"""

import os
import re
import sys
import json
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent


def load_json_safe(path: Path):
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  [WARN] Could not parse {path.name}: {e}")
    return {}


SCHEMA = load_json_safe(BASE_DIR / "sections_schema.json").get("page_types", {})


def normalize_sections(sections_dict: dict, page_type: str, pid: str):
    """Rename section keys to the canonical LIVE-site ids from sections_schema.json,
    drop sections the live site does not render separately, and return them in live order."""
    spec = SCHEMA.get(page_type)
    if not spec:
        return sections_dict, []
    aliases = spec.get("aliases", {})
    canon = {s["id"]: s for s in spec["sections"]}

    renamed = {}
    for key, content in sections_dict.items():
        renamed[aliases.get(key, key)] = content

    ordered, warnings = {}, []
    for s in spec["sections"]:
        sid = s["id"]
        if sid in renamed:
            if s.get("live", True):
                ordered[sid] = renamed[sid]
        elif s.get("live", True):
            warnings.append(f"missing live section '{sid}'")
    for key, content in renamed.items():
        if key not in canon:
            ordered[key] = content
            warnings.append(f"extra non-schema section '{key}'")
    return ordered, warnings


def parse_markdown_sections(md_text: str):
    yaml_match = re.search(r"^---\s*\r?\n([\s\S]*?)\r?\n---\s*\r?\n?", md_text)
    body_str = md_text[yaml_match.end():].strip() if yaml_match else md_text.strip()

    pattern = r"(?:<!--\s*=+\s*-->\s*)?<!--\s*SECTION:\s*([a-zA-Z0-9_-]+)(?:\s*\|\s*BLOCK:[^>]*)?\s*-->(?:\s*<!--\s*=+\s*-->)?"
    parts = re.split(pattern, body_str)

    sections_dict = {}
    if len(parts) > 1:
        for i in range(1, len(parts), 2):
            sec_name = parts[i].strip()
            sec_content = parts[i + 1].strip() if (i + 1) < len(parts) else ""
            sec_content = re.sub(r"<!--\s*=+\s*-->\s*$", "", sec_content).strip()
            sections_dict[sec_name] = sec_content
    else:
        sections_dict["main"] = body_str

    return sections_dict


def discover_project_pages():
    brief = load_json_safe(BASE_DIR / "master_brief.json")
    topical = load_json_safe(BASE_DIR / "topical_authority.json")
    nap = brief.get("nap", {})
    company_name = nap.get("company_name", brief.get("project_name", "Rockford Air Duct Pros"))
    phone = nap.get("phone", "(815) 555-0142")
    default_city = brief.get("city", "Rockford")

    default_pages = [
        {"id": "homepage", "title": f"Homepage ({default_city} Primary Hub)", "slug": "/", "type": "homepage"},
        {"id": "about", "title": "About Us", "slug": "about", "type": "about"},
        {"id": "contact", "title": "Contact Us", "slug": "contact", "type": "contact"},
        {"id": "air-duct-cleaning-loves-park-il", "title": "Loves Park Location Page", "slug": "air-duct-cleaning-loves-park-il", "type": "location"},
        {"id": "commercial-hvac-duct-cleaning", "title": "Commercial HVAC Duct Cleaning", "slug": "commercial-hvac-duct-cleaning", "type": "service"},
        {"id": "dryer-vent-cleaning-and-lint-removal", "title": "Dryer Vent Cleaning & Lint Removal", "slug": "dryer-vent-cleaning-and-lint-removal", "type": "service"},
        {"id": "negative-air-vacuum-trunk-line-cleaning", "title": "Negative Air Vacuum Trunk Line Cleaning", "slug": "negative-air-vacuum-trunk-line-cleaning", "type": "service"},
        {"id": "sanitization-and-antimicrobial-fogging", "title": "Air Duct Sanitization & Antimicrobial Fogging", "slug": "sanitization-and-antimicrobial-fogging", "type": "service"},
        {"id": "video-camera-ductwork-inspection", "title": "Video Camera Ductwork Inspection", "slug": "video-camera-ductwork-inspection", "type": "service"},
        {"id": "how-to-spot-air-duct-cleaning-scams", "title": "Blog: How to Spot Air Duct Cleaning Scams", "slug": "how-to-spot-air-duct-cleaning-scams", "type": "blog"},
    ]

    pages_by_id = {p["id"]: p for p in default_pages}

    for tp in topical.get("pages", []):
        pid = tp.get("page_id")
        if not pid or pid == "residential-air-duct-cleaning":
            continue  # FIX 32
        md_file = BASE_DIR / f"page_content_{pid}.md"
        if md_file.exists() and pid not in pages_by_id:
            pages_by_id[pid] = {
                "id": pid,
                "title": tp.get("parent_service") or tp.get("h1_title") or pid.replace("-", " ").title(),
                "slug": "/" if pid == "homepage" else pid,
                "type": tp.get("page_type", "service"),
                "city": tp.get("city", default_city),
                "keyword": tp.get("target_keyword", ""),
            }

    return list(pages_by_id.values()), company_name, phone, default_city


def discover_stitch_templates():
    templates_dir = BASE_DIR / "templates"
    templates_html = {}
    if templates_dir.exists():
        for html_file in sorted(templates_dir.glob("*.html")):
            rel_key = f"templates/{html_file.name}"
            raw_html = html_file.read_text(encoding="utf-8", errors="ignore")
            templates_html[rel_key] = raw_html
    return templates_html


def sanitize_for_script_tag(json_str: str) -> str:
    # Escape closing </script> tags inside JSON strings so inline HTML <script> block never breaks
    return json_str.replace("</script>", "<\\/script>").replace("</SCRIPT>", "<\\/SCRIPT>")


def compile_all_pages(sync_builder_html=True):
    pages_config, company_name, phone, default_city = discover_project_pages()
    compiled = {}

    for p in pages_config:
        pid = p["id"]
        md_path = BASE_DIR / f"page_content_{pid}.md"
        if not md_path.exists():
            continue

        meta_path = BASE_DIR / f"page_meta_{pid}.json"
        plan_path = BASE_DIR / f"image_plan_{pid}.json"

        md_text = md_path.read_text(encoding="utf-8", errors="ignore")
        sections_dict = parse_markdown_sections(md_text)
        sections_dict, sec_warnings = normalize_sections(sections_dict, p["type"], pid)
        for w in sec_warnings:
            print(f"  [SECTIONS] {pid}: {w}")
        meta_data = load_json_safe(meta_path)
        plan_data = load_json_safe(plan_path)
        images_list = plan_data.get("images", [])

        img_dir = f"images/{pid}" if (BASE_DIR / "images" / pid).exists() else "images/homepage"

        compiled[pid] = {
            "id": pid,
            "title": p["title"],
            "slug": p["slug"],
            "type": p["type"],
            "company_name": company_name,
            "phone": phone,
            "city": p.get("city", meta_data.get("city", default_city)),
            "sections": sections_dict,
            "meta": meta_data,
            "images": images_list,
            "img_dir": img_dir,
        }

    templates_html = discover_stitch_templates()

    pages_js = "window.BUILDER_PAGES_DATA = " + sanitize_for_script_tag(json.dumps(compiled, indent=2)) + ";"
    templates_js = "window.STITCH_TEMPLATES_HTML = " + sanitize_for_script_tag(json.dumps(templates_html, indent=2)) + ";"
    combined_js = pages_js + "\n" + templates_js

    out_path = BASE_DIR / "scripts" / "builder_data.js"
    out_path.write_text(combined_js, encoding="utf-8")
    print(f"✓ Compiled {len(compiled)} pipeline pages + {len(templates_html)} Stitch archetype files -> {out_path}")

    if sync_builder_html:
        builder_path = BASE_DIR / "studio_builder.html"
        if builder_path.exists():
            html_text = builder_path.read_text(encoding="utf-8")
            pattern = r"window\.BUILDER_PAGES_DATA\s*=\s*\{[\s\S]*?</script>"
            replacement = f"{combined_js}\n  </script>"
            if re.search(pattern, html_text):
                new_html = re.sub(pattern, lambda _: replacement, html_text, count=1)
                builder_path.write_text(new_html, encoding="utf-8")
                print(f"✓ Synced window.BUILDER_PAGES_DATA & window.STITCH_TEMPLATES_HTML inside studio_builder.html")

    return compiled


if __name__ == "__main__":
    compile_all_pages(sync_builder_html=True)
