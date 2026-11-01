#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
orchestrator.py — Rank & Rent Flash Engine
==========================================
Coordinates atomic section generation, stitching, validation, and golden example tracking.

Usage:
  python scripts/orchestrator.py --status
  python scripts/orchestrator.py --prep --page residential-air-duct-cleaning --type service
  python scripts/orchestrator.py --stitch --page residential-air-duct-cleaning --type service
  python scripts/orchestrator.py --validate --page residential-air-duct-cleaning
  python scripts/orchestrator.py --save-golden --type service --page residential-air-duct-cleaning
"""

import os
import sys
import json
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
DATA_BRIEF = ROOT_DIR / "data_brief.txt"
DATA_TXT = ROOT_DIR / "data.txt"

PAGE_TYPES = {
    "service": {
        "prompt_folder": "P7_service",
        "prefix": "P7s_",
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
}


def load_state():
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "project": "Rank & Rent Flash Engine",
        "current_page": None,
        "completed_pages": [],
        "completed_sections": {},
        "golden_examples_completed": [],
    }


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def get_status():
    state = load_state()
    print("=" * 65)
    print("  RANK & RENT FLASH ENGINE — ORCHESTRATOR STATUS")
    print("=" * 65)
    print(f"Current Page       : {state.get('current_page', 'None')}")
    print(f"Completed Pages    : {len(state.get('completed_pages', []))}")
    for p in state.get("completed_pages", []):
        print(f"  ✓ {p}")

    print("\nGolden Examples Status:")
    for ptype, cfg in PAGE_TYPES.items():
        ex_path = EXAMPLES_DIR / cfg["example_file"]
        is_ready = False
        if ex_path.exists():
            text = ex_path.read_text(encoding="utf-8", errors="ignore")
            if "PENDING" not in text and len(text.strip()) > 300:
                is_ready = True
        status_str = "READY (Golden Example Active)" if is_ready else "PENDING generation"
        print(f"  {ptype.upper():<10}: {status_str}")

    print("\nWork In Progress:")
    if WIP_DIR.exists():
        subdirs = [d for d in WIP_DIR.iterdir() if d.is_dir()]
        if not subdirs:
            print("  (No active work-in-progress directories)")
        for sd in subdirs:
            sec_files = list(sd.glob("section_*.md"))
            print(f"  Page: {sd.name} ({len(sec_files)} sections in progress)")
    else:
        print("  (No work-in-progress directory)")
    print("=" * 65)


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

    print(f"Preparing {page_type.upper()} page: '{page_slug}'")
    print(f"Target directory: {target_dir}")
    print(f"Sections to generate: {len(cfg['sections'])}")

    for idx, sec in enumerate(cfg["sections"], 1):
        sec_file = target_dir / f"section_{sec}.md"
        if not sec_file.exists():
            # Create template with header
            header = f"# Section {idx:02d}: {sec}\n# Page: {page_slug}\n\n"
            sec_file.write_text(header, encoding="utf-8")
        print(f"  [{idx:02d}/{len(cfg['sections'])}] {sec_file.name}")

    print("\nPage prep complete. You can now write or generate individual sections.")


def stitch_page(page_slug, page_type):
    if page_type not in PAGE_TYPES:
        print(f"ERROR: Unknown page type '{page_type}'.")
        sys.exit(1)

    cfg = PAGE_TYPES[page_type]
    target_dir = WIP_DIR / f"{page_type}_{page_slug}"
    if not target_dir.exists():
        print(f"ERROR: Work in progress directory not found: {target_dir}")
        sys.exit(1)

    output_file = ROOT_DIR / f"page_content_{page_slug}.md"
    stitched_blocks = []

    # YAML Frontmatter
    frontmatter = f"""---
title: "{page_slug.replace('-', ' ').title()} | Rockford Air Duct Pros"
slug: "{page_slug}"
page_type: "{page_type}"
niche: "Air Duct Cleaning"
city: "Rockford"
state: "IL"
published: false
---

"""
    stitched_blocks.append(frontmatter)

    missing = []
    for sec in cfg["sections"]:
        sec_file = target_dir / f"section_{sec}.md"
        if not sec_file.exists():
            missing.append(sec)
            continue
        text = sec_file.read_text(encoding="utf-8", errors="ignore").strip()
        # Clean section header comment if present
        lines = text.splitlines()
        content_lines = [l for l in lines if not l.startswith("# Section ") and not l.startswith("# Page: ")]
        cleaned_sec = "\n".join(content_lines).strip()
        if cleaned_sec:
            stitched_blocks.append(f"<!-- SECTION: {sec} -->\n" + cleaned_sec + "\n")

    if missing:
        print(f"WARNING: The following {len(missing)} section(s) are missing:")
        for m in missing:
            print(f"  - section_{m}.md")

    full_content = "\n".join(stitched_blocks)
    output_file.write_text(full_content, encoding="utf-8")
    print(f"\nStitched page saved to: {output_file}")
    print(f"Total word count: {len(full_content.split())} words")

    # Run pre_publish_filter.py validation
    validate_page(page_slug)


def validate_page(page_slug):
    content_file = ROOT_DIR / f"page_content_{page_slug}.md"
    if not content_file.exists():
        print(f"ERROR: {content_file} does not exist.")
        sys.exit(1)

    filter_script = SCRIPTS_DIR / "pre_publish_filter.py"
    if filter_script.exists():
        print("\nRunning pre_publish_filter.py validation...")
        try:
            cmd = [sys.executable, str(filter_script), str(content_file)]
            res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
            print(res.stdout)
            if res.stderr:
                print(res.stderr)
        except Exception as e:
            print(f"Validation execution error: {e}")


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
    content = content_file.read_text(encoding="utf-8", errors="ignore")
    target_example.write_text(content, encoding="utf-8")

    state = load_state()
    if page_type not in state.get("golden_examples_completed", []):
        state.setdefault("golden_examples_completed", []).append(page_type)
    save_state(state)

    print(f"SUCCESS: Saved {content_file.name} as GOLDEN EXAMPLE -> {target_example}")


def main():
    parser = argparse.ArgumentParser(description="Rank & Rent Flash Engine Orchestrator")
    parser.add_argument("--status", action="store_true", help="Show pipeline and page progress")
    parser.add_argument("--prep", action="store_true", help="Prepare sections for a page in work_in_progress")
    parser.add_argument("--stitch", action="store_true", help="Stitch sections into page_content_[slug].md")
    parser.add_argument("--validate", action="store_true", help="Validate page with pre_publish_filter")
    parser.add_argument("--save-golden", action="store_true", help="Save stitched page as a golden example")
    parser.add_argument("--page", help="Page slug (e.g. residential-air-duct-cleaning)")
    parser.add_argument("--type", choices=["service", "location", "blog", "about"], help="Page type")

    args = parser.parse_args()

    if args.status or (not any([args.prep, args.stitch, args.validate, args.save_golden])):
        get_status()
        return

    if args.prep:
        if not args.page or not args.type:
            print("ERROR: --prep requires --page <slug> and --type <service|location|blog|about>")
            sys.exit(1)
        prep_page(args.page, args.type)

    elif args.stitch:
        if not args.page or not args.type:
            print("ERROR: --stitch requires --page <slug> and --type <service|location|blog|about>")
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


if __name__ == "__main__":
    main()

