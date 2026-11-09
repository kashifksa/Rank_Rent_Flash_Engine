#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
orchestrator.py — Rank & Rent Flash Engine (Whole-Website Orchestrator)
=======================================================================
Coordinates atomic section generation, stitching, validation, builder data
compilation, and 1-command whole-website HTML generation across any template.

Usage:
  python scripts/orchestrator.py --status
  python scripts/orchestrator.py --prep-phase1
  python scripts/orchestrator.py --prep --page commercial-hvac-duct-cleaning --type service
  python scripts/orchestrator.py --stitch --page commercial-hvac-duct-cleaning --type service
  python scripts/orchestrator.py --validate --page commercial-hvac-duct-cleaning
  python scripts/orchestrator.py --compile
  python scripts/orchestrator.py --build-site --template stitch_modern_industrial
  python scripts/orchestrator.py --build-site --template cornerstone --out dist
"""

import os
import sys
import json
import shutil
import argparse
import subprocess
from pathlib import Path

# Force UTF-8 on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT_DIR / "scripts"
PROMPTS_DIR = ROOT_DIR / "prompts"
EXAMPLES_DIR = ROOT_DIR / "examples"
WIP_DIR = ROOT_DIR / "work_in_progress"
STATE_FILE = ROOT_DIR / "pipeline_state.json"
BRIEF_FILE = ROOT_DIR / "master_brief.json"
TOPICAL_FILE = ROOT_DIR / "topical_authority.json"

PAGE_TYPES = {
    "service": {
        "prompt_folder": "P7_service",
        "prefix": "P7s_",
        "structure_file": "SERVICE_PAGE_STRUCTURE.md",
        "example_file": "service_page_example.md",
        "sections": [
            "01_hero",
            "02_trust_bar",
            "03_services_grid",
            "04_why_us",
            "05_process",
            "06_local_proof",
            "07_service_area",
            "08_mid_cta",
            "09_faq",
            "10_bottom_cta",
        ],
    },
    "location": {
        "prompt_folder": "P7_location",
        "prefix": "P7l_",
        "structure_file": "LOCATION_PAGE_STRUCTURE.md",
        "example_file": "location_page_example.md",
        "sections": [
            "01_hero",
            "02_localized_intro",
            "03_services_overview",
            "04_local_proof",
            "05_local_faq",
            "06_service_area",
            "07_bottom_cta",
        ],
    },
    "blog": {
        "prompt_folder": "P7_blog",
        "prefix": "P7b_",
        "structure_file": "BLOG_POST_STRUCTURE.md",
        "example_file": "blog_post_example.md",
        "sections": [
            "01_header",
            "02_cause_context",
            "03_diy_vs_pro",
            "04_structured_data",
            "05_how_it_works",
            "06_local_considerations",
            "07_faq",
            "08_conclusion_cta",
        ],
    },
    "about": {
        "prompt_folder": "P7_about",
        "prefix": "P7a_",
        "structure_file": "ABOUT_PAGE_STRUCTURE.md",
        "example_file": "about_page_example.md",
        "sections": [
            "01_identity_hook",
            "02_origin_story",
            "03_team_credentials",
            "04_credentials_display",
            "05_community_proof",
            "06_trust_signals",
            "07_service_area_nap",
            "08_bottom_cta",
        ],
    },
    "contact": {
        "prompt_folder": "P7_about",
        "prefix": "P7a_",
        "structure_file": "ABOUT_PAGE_STRUCTURE.md",
        "example_file": "about_page_example.md",
        "sections": [
            "01_contact_hero",
            "02_contact_form",
            "03_nap_block",
            "04_trust_bar",
        ],
    },
}

AVAILABLE_TEMPLATES = {
    "cornerstone": "Cornerstone ProFlow (Full-bleed authority)",
    "keystone": "Keystone Classic (Kadence split + info topbar)",
    "industrial": "Modern Industrial (Dark header + blueprint)",
    "bold": "Bold Trade (Rugged dark + amber skin)",
    "clean": "Clean Local (Friendly teal + rounded skin)",
    "authority": "Executive Contractor (Double-decker nav + dispatch card)",
    "emergency": "Rapid Dispatch (Docked trust bar + stripe cards)",
    "bento": "Modern Bento (Floating pill nav + warm stone Bento grid)",
    "atelier": "Swiss Editorial Atelier (Architectural magazine grid + warm paper)",
}


def load_json(path: Path):
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def load_state():
    state = load_json(STATE_FILE)
    if not state:
        return {
            "project": "Rank & Rent Flash Engine",
            "current_page": None,
            "completed_pages": [],
            "completed_sections": {},
            "golden_examples_completed": [],
        }
    return state


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def get_status():
    state = load_state()
    brief = load_json(BRIEF_FILE)
    topical = load_json(TOPICAL_FILE)
    nap = brief.get("nap", {})

    print("=" * 72)
    print("  RANK & RENT FLASH ENGINE — WHOLE-WEBSITE ORCHESTRATOR STATUS")
    print("=" * 72)
    print(f"Project Company    : {nap.get('company_name', brief.get('project_name', 'Unknown'))}")
    print(f"Niche & Location   : {brief.get('niche', 'N/A')} in {brief.get('city', 'N/A')}, {brief.get('state', 'N/A')}")
    print(f"Dispatch Phone     : {nap.get('phone', 'N/A')}")

    print("\nAvailable Website Templates:")
    for tid, tname in AVAILABLE_TEMPLATES.items():
        print(f"  • {tid:<26} -> {tname}")

    # Audit Phase 1 Pages
    md_files = sorted(ROOT_DIR.glob("page_content_*.md"))
    print(f"\nValidated Content Pages Ready ({len(md_files)}):")
    for mf in md_files:
        slug = mf.stem.replace("page_content_", "")
        if slug == "residential-air-duct-cleaning":
            continue  # FIX 32
        words = len(mf.read_text(encoding="utf-8", errors="ignore").split())
        print(f"  ✓ {slug:<42} ({words:,} words)")

    print("\nPipeline Page Structures & Golden Examples:")
    for ptype, cfg in PAGE_TYPES.items():
        if ptype == "contact":
            continue
        ex_path = EXAMPLES_DIR / cfg["example_file"]
        is_ready = ex_path.exists() and len(ex_path.read_text(encoding="utf-8", errors="ignore").strip()) > 300
        status_str = "READY" if is_ready else "PENDING"
        print(f"  • {ptype.upper():<10} ({cfg['structure_file']:<28}) : {status_str} ({len(cfg['sections'])} sections)")

    print("\nQuick Whole-Website Commands:")
    print("  1. Prep all Phase 1 pages : python scripts/orchestrator.py --prep-phase1")
    print("  2. Compile to Builder     : python scripts/orchestrator.py --compile")
    print("  3. Build Stitch Website   : python scripts/orchestrator.py --build-site --template stitch_modern_industrial")
    print("  4. Build Cornerstone Site : python scripts/orchestrator.py --build-site --template cornerstone")
    print("=" * 72)


def prep_page(page_slug, page_type):
    if page_type not in PAGE_TYPES:
        print(f"ERROR: Unknown page type '{page_type}'. Choose from: {list(PAGE_TYPES.keys())}")
        sys.exit(1)

    cfg = PAGE_TYPES[page_type]
    target_dir = WIP_DIR / f"{page_type}_{page_slug}"
    target_dir.mkdir(parents=True, exist_ok=True)

    state = load_state()
    state["current_page"] = page_slug
    state["current_type"] = page_type
    save_state(state)

    print(f"Preparing {page_type.upper()} page: '{page_slug}' ({cfg['structure_file']})")
    for idx, sec in enumerate(cfg["sections"], 1):
        sec_file = target_dir / f"section_{sec}.md"
        if not sec_file.exists():
            header = f"# Section {idx:02d}: {sec}\n# Page: {page_slug}\n\n"
            sec_file.write_text(header, encoding="utf-8")
        print(f"  [{idx:02d}/{len(cfg['sections'])}] {sec_file.name}")


def prep_phase1_all():
    topical = load_json(TOPICAL_FILE)
    pages = topical.get("pages", [])
    prepped = 0
    for p in pages:
        if p.get("phase") != 1:
            continue
        pid = p.get("page_id")
        ptype = p.get("page_type")
        if not pid or pid in ("homepage", "residential-air-duct-cleaning") or ptype not in PAGE_TYPES:
            continue
        md_file = ROOT_DIR / f"page_content_{pid}.md"
        if md_file.exists():
            print(f"  ✓ Skipping {pid} (page_content_{pid}.md already exists)")
            continue
        prep_page(pid, ptype)
        prepped += 1
    print(f"\nPhase 1 prep complete ({prepped} new page folders created in work_in_progress/).")


def stitch_page(page_slug, page_type):
    if page_type not in PAGE_TYPES:
        print(f"ERROR: Unknown page type '{page_type}'.")
        sys.exit(1)

    cfg = PAGE_TYPES[page_type]
    target_dir = WIP_DIR / f"{page_type}_{page_slug}"
    if not target_dir.exists():
        print(f"ERROR: Work in progress directory not found: {target_dir}")
        sys.exit(1)

    brief = load_json(BRIEF_FILE)
    company = brief.get("nap", {}).get("company_name", brief.get("project_name", ""))
    niche = brief.get("niche", "")
    city = brief.get("city", "")
    state_code = brief.get("state", "")

    output_file = ROOT_DIR / f"page_content_{page_slug}.md"
    frontmatter = f"""---
title: "{page_slug.replace('-', ' ').title()} | {company}"
slug: "{page_slug}"
page_type: "{page_type}"
niche: "{niche}"
city: "{city}"
state: "{state_code}"
published: false
---

"""
    stitched_blocks = [frontmatter]
    missing = []

    for sec in cfg["sections"]:
        sec_file = target_dir / f"section_{sec}.md"
        if not sec_file.exists():
            missing.append(sec)
            continue
        text = sec_file.read_text(encoding="utf-8", errors="ignore").strip()
        lines = text.splitlines()
        content_lines = [l for l in lines if not l.startswith("# Section ") and not l.startswith("# Page: ")]
        cleaned_sec = "\n".join(content_lines).strip()
        if cleaned_sec:
            stitched_blocks.append(f"<!-- SECTION: {sec} -->\n" + cleaned_sec + "\n")

    if missing:
        print(f"WARNING: {len(missing)} section(s) missing for {page_slug}: {', '.join(missing)}")

    full_content = "\n".join(stitched_blocks)
    output_file.write_text(full_content, encoding="utf-8")
    print(f"✓ Stitched {output_file.name} ({len(full_content.split())} words)")
    validate_page(page_slug)
    run_gate(page_slug)


def run_gate(page_slug=None):
    """pipeline_gate.py: page_meta generation + section validation + SEO checks. Returns True when nothing blocks."""
    import subprocess
    cmd = [sys.executable, str(SCRIPTS_DIR / "pipeline_gate.py")] + ([page_slug] if page_slug else [])
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(ROOT_DIR))
    print(r.stdout[-6000:])
    return r.returncode == 0


def validate_page(page_slug):
    content_file = ROOT_DIR / f"page_content_{page_slug}.md"
    if not content_file.exists():
        print(f"ERROR: {content_file} does not exist.")
        sys.exit(1)

    filter_script = SCRIPTS_DIR / "pre_publish_filter.py"
    if filter_script.exists():
        print(f"Running pre_publish_filter.py on {content_file.name}...")
        cmd = [sys.executable, str(filter_script), str(content_file)]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if res.stdout.strip():
            print(res.stdout.strip())
        if res.stderr.strip():
            print(res.stderr.strip())


def save_as_golden(page_slug, page_type):
    if page_type not in PAGE_TYPES:
        print(f"ERROR: Unknown page type '{page_type}'.")
        sys.exit(1)

    cfg = PAGE_TYPES[page_type]
    content_file = ROOT_DIR / f"page_content_{page_slug}.md"
    if not content_file.exists():
        print(f"ERROR: {content_file} does not exist. Stitch the page first.")
        sys.exit(1)

    target_example = EXAMPLES_DIR / cfg["example_file"]
    target_example.write_text(content_file.read_text(encoding="utf-8", errors="ignore"), encoding="utf-8")

    state = load_state()
    if page_type not in state.get("golden_examples_completed", []):
        state.setdefault("golden_examples_completed", []).append(page_type)
    save_state(state)
    print(f"✓ Saved {content_file.name} as GOLDEN EXAMPLE -> {target_example}")


def run_compile():
    compiler_script = SCRIPTS_DIR / "compile_builder_data.py"
    cmd = [sys.executable, str(compiler_script)]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(res.stdout.strip())
    if res.stderr.strip():
        print(res.stderr.strip())


def build_full_website(template_id="stitch_modern_industrial", out_folder=None):
    """
    Compiles all pipeline pages into Studio Builder, renders every page using
    the chosen template (cornerstone OR stitch_modern_industrial OR any future
    Stitch template), and writes the standalone HTML site + images to disk.
    """
    print("=" * 72)
    print(f"  BUILDING FULL WEBSITE — TEMPLATE: {template_id}")
    print("=" * 72)

    # Step 1: Compile latest markdown content & metadata into Builder
    run_compile()

    if not out_folder:
        if template_id.startswith("stitch"):
            out_folder = "dist_stitch"
        elif template_id == "keystone":
            out_folder = "dist_keystone"
        else:
            out_folder = "build_site"
    out_dir = ROOT_DIR / out_folder
    out_dir.mkdir(parents=True, exist_ok=True)

    builder_url = f"file:///{str(ROOT_DIR / 'studio_builder.html').replace(chr(92), '/')}"

    from playwright.sync_api import sync_playwright

    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    ]
    exec_path = next((cp for cp in chrome_paths if os.path.exists(cp)), None)

    with sync_playwright() as p:
        launch_kwargs = {"headless": True}
        if exec_path:
            launch_kwargs["executable_path"] = exec_path
        else:
            launch_kwargs["channel"] = "msedge"

        browser = p.chromium.launch(**launch_kwargs)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(builder_url)
        page.wait_for_timeout(600)

        # Select the requested template in the Builder
        page.evaluate(f"selectWebsiteTemplate('{template_id}', 'homepage', true)")
        page.wait_for_timeout(500)

        pages = page.evaluate("Object.keys(window.BUILDER_PAGES_DATA)")
        tpl_type = page.evaluate(f"(window.BUILDER_TEMPLATES['{template_id}'] || {{}}).type || 'native'")
        print(f"Exporting {len(pages)} pages using '{template_id}' ({tpl_type}) -> {out_dir} ...")

        for pid in pages:
            filename = "index.html" if pid in ("homepage", "home") else f"{pid}.html"
            if tpl_type == "stitch":
                doc_html = page.evaluate(f"window.getActiveStitchDocumentHTML('{pid}')")
            else:
                doc_html = page.evaluate(f"generateProductionDocument('{pid}')")

            if doc_html:
                out_path = out_dir / filename
                out_path.write_text(doc_html, encoding="utf-8")
                print(f"  ✓ {filename:<46} ({len(doc_html) // 1024} KB)")

        browser.close()

    # Copy geotagged WebP images folder into output directory
    src_images = ROOT_DIR / "images"
    dst_images = out_dir / "images"
    if src_images.exists():
        if dst_images.exists():
            shutil.rmtree(dst_images)
        shutil.copytree(src_images, dst_images)
        print(f"✓ Synced geotagged WebP images -> {dst_images}")

    print("=" * 72)
    print(f"SUCCESS: Complete {len(pages)}-page website generated in: {out_dir}")
    print("=" * 72)


FORCE_BUILD = False


def build_site_v5(template_id="cornerstone", out_folder=None):
    """
    Whole-site export with the section-registry builder (builder/index.html).
    Templates: cornerstone, keystone, industrial. Sections come from sections_schema.json.
    If builder_state.json exists in the project root it is used as the saved project state.
    """
    print("=" * 72)
    print(f"  BUILDING FULL WEBSITE (builder v5) - TEMPLATE: {template_id}")
    print("=" * 72)

    # 1. sections must match the schema before anything is built
    import subprocess
    val = subprocess.run([sys.executable, str(ROOT_DIR / "validate_sections.py")], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if val.returncode != 0:
        print(val.stdout)
        print("ABORTED: fix the section errors above first (python validate_sections.py).")
        return
    print("OK sections match sections_schema.json")

    # 1b. the pipeline gate: generate page_meta from content + brief, then run every SEO/quality check.
    #     Any FAIL blocks the export (use --force only for a deliberate draft build).
    if not run_gate():
        if FORCE_BUILD:
            print("WARNING: gate failed but --force was given, building anyway (do NOT publish this build).")
        else:
            print("ABORTED: fix the blocking issues listed by the gate (python scripts/pipeline_gate.py), or build a draft with --force.")
            return

    # 2. compile md -> builder/js/data.js
    run_compile()

    out_dir = ROOT_DIR / (out_folder or f"dist_{template_id}")
    out_dir.mkdir(parents=True, exist_ok=True)
    url = f"file:///{str(ROOT_DIR / 'builder' / 'index.html').replace(chr(92), '/')}"

    from playwright.sync_api import sync_playwright
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    ]
    exec_path = next((cp for cp in chrome_paths if os.path.exists(cp)), None)
    with sync_playwright() as p:
        kw = {"headless": True}
        if exec_path:
            kw["executable_path"] = exec_path
        else:
            kw["channel"] = "msedge"
        browser = p.chromium.launch(**kw)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        errs = []
        page.on("pageerror", lambda e: errs.append(str(e)))
        page.goto(url)
        page.wait_for_timeout(500)
        # always start from the file state (builder_state.json), never from a browser profile
        page.evaluate("localStorage.clear()")
        page.reload()
        page.wait_for_timeout(500)
        ok = page.evaluate(f"!!Builder.TEMPLATES['{template_id}']")
        if not ok:
            print("Unknown template. Available:", page.evaluate("Object.keys(Builder.TEMPLATES)"))
            browser.close()
            return
        page.evaluate(f"Builder.state.template = '{template_id}'")
        files = page.evaluate("Builder.exportAll()")
        browser.close()
    if errs:
        print("Builder errors:", errs)

    for fname, html in files.items():
        (out_dir / fname).write_text(html, encoding="utf-8")
        print(f"  OK {fname:<48} ({len(html) // 1024} KB)")

    src_images = ROOT_DIR / "images"
    dst_images = out_dir / "images"
    if src_images.exists():
        if dst_images.exists():
            shutil.rmtree(dst_images)
        shutil.copytree(src_images, dst_images)
        print(f"OK Synced geotagged WebP images -> {dst_images}")
    print("=" * 72)
    print(f"SUCCESS: {len(files)}-page website generated in: {out_dir}")
    print("=" * 72)


def main():
    parser = argparse.ArgumentParser(description="Rank & Rent Flash Engine Orchestrator")
    parser.add_argument("--status", action="store_true", help="Show pipeline, templates, and page progress")
    parser.add_argument("--prep-phase1", action="store_true", help="Prepare all Phase 1 pages from topical_authority.json")
    parser.add_argument("--prep", action="store_true", help="Prepare sections for a single page in work_in_progress")
    parser.add_argument("--stitch", action="store_true", help="Stitch sections into page_content_[slug].md")
    parser.add_argument("--validate", action="store_true", help="Validate page with pre_publish_filter")
    parser.add_argument("--save-golden", action="store_true", help="Save stitched page as a golden example")
    parser.add_argument("--compile", action="store_true", help="Compile all page_content_*.md files into Studio Builder")
    parser.add_argument("--build-site", action="store_true", help="Generate complete multi-page website using chosen template")
    parser.add_argument("--template", default="stitch_modern_industrial", help="Template ID (cornerstone or stitch_modern_industrial)")
    parser.add_argument("--engine", choices=["legacy", "v5"], default="legacy", help="v5 = new section-registry builder (builder/index.html); templates: cornerstone, keystone, industrial")
    parser.add_argument("--out", default=None, help="Output directory for --build-site (e.g. dist_stitch)")
    parser.add_argument("--force", action="store_true", help="Build even if the pipeline gate has blocking issues (draft builds only)")
    parser.add_argument("--page", help="Page slug (e.g. commercial-hvac-duct-cleaning)")
    parser.add_argument("--type", choices=["service", "location", "blog", "about", "contact"], help="Page type")

    args = parser.parse_args()

    if args.status or not any([
        args.prep_phase1, args.prep, args.stitch, args.validate,
        args.save_golden, args.compile, args.build_site
    ]):
        get_status()
        return

    if args.prep_phase1:
        prep_phase1_all()
    elif args.prep:
        if not args.page or not args.type:
            print("ERROR: --prep requires --page <slug> and --type <service|location|blog|about|contact>")
            sys.exit(1)
        prep_page(args.page, args.type)
    elif args.stitch:
        if not args.page or not args.type:
            print("ERROR: --stitch requires --page <slug> and --type <service|location|blog|about|contact>")
            sys.exit(1)
        stitch_page(args.page, args.type)
    elif args.validate:
        if not args.page:
            print("ERROR: --validate requires --page <slug>")
            sys.exit(1)
        validate_page(args.page)
    elif args.save_golden:
        if not args.page or not args.type:
            print("ERROR: --save-golden requires --page <slug> and --type <service|location|blog|about>")
            sys.exit(1)
        save_as_golden(args.page, args.type)
    elif args.compile:
        run_compile()
    elif args.build_site:
        global FORCE_BUILD
        FORCE_BUILD = args.force
        if args.engine == "v5" or not (ROOT_DIR / "studio_builder.html").exists():
            build_site_v5(template_id=args.template if args.template in ("cornerstone", "keystone", "industrial", "bold", "clean", "authority", "emergency", "bento", "atelier") else "cornerstone", out_folder=args.out)
        else:
            build_full_website(template_id=args.template, out_folder=args.out)


if __name__ == "__main__":
    main()
