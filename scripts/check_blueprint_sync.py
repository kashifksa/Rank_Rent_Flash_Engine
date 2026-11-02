#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_blueprint_sync.py — Rank & Rent Pipeline (FIX 19)
=======================================================
Compares the homepage service card count in master_site_blueprint.json
against the Phase 1 service pages in topical_authority.json.

Run AFTER any homepage edit that adds or removes a service card.
Usage: python check_blueprint_sync.py

What it checks:
  1. topical_authority.json exists and is valid JSON
  2. master_site_blueprint.json exists and is valid JSON
  3. Count of Phase 1 service pages in topical_authority.json
  4. Count of service cards in the homepage section of master_site_blueprint.json
  5. Flags a mismatch (blueprint drift) if counts differ
  6. Lists any service card destinations not registered in topical_authority.json
  7. Lists any Phase 1 service pages that have no matching homepage service card
"""

import json
import os
import sys

TOPICAL_FILE    = "topical_authority.json"
BLUEPRINT_FILE  = "master_site_blueprint.json"

# Keys used to identify page type in topical_authority.json
SERVICE_PAGE_TYPES = {"service", "service_page", "primary_service", "secondary_service"}

# Phase identifiers for Phase 1
PHASE1_IDENTIFIERS = {"phase_1", "phase1", "1", 1}

# Keys in master_site_blueprint.json that represent the homepage service cards section
HOMEPAGE_SECTION_KEYS = {"service_cards", "services_grid", "services", "service_grid_cards"}

# ---------------------------------------------------------------------------

def load_json(filepath: str) -> dict | list | None:
    if not os.path.exists(filepath):
        print(f"  [FAIL] File not found: {filepath}")
        return None
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"  [FAIL] JSON parse error in {filepath}: {e}")
        return None


def get_phase1_service_pages(topical: dict | list) -> list[dict]:
    """Extract all Phase 1 service pages from topical_authority.json."""
    pages = []

    # Support both list-of-pages and dict-with-phases formats
    if isinstance(topical, list):
        all_pages = topical
    elif isinstance(topical, dict):
        # Try common keys
        all_pages = (
            topical.get("pages") or
            topical.get("content_map") or
            topical.get("topical_map") or
            []
        )
        # Also flatten phase-keyed structures
        for key, val in topical.items():
            if isinstance(val, list) and key.lower().startswith("phase"):
                all_pages.extend(val)
    else:
        all_pages = []

    for page in all_pages:
        if not isinstance(page, dict):
            continue
        phase = str(page.get("phase", page.get("publishing_phase", ""))).lower().replace(" ", "_")
        ptype = str(page.get("page_type", page.get("type", ""))).lower().replace(" ", "_")
        if phase in {str(p) for p in PHASE1_IDENTIFIERS} and ptype in SERVICE_PAGE_TYPES:
            pages.append(page)

    return pages


def get_homepage_service_cards(blueprint: dict | list) -> list[dict]:
    """Extract service cards from the homepage section of master_site_blueprint.json."""
    cards = []

    # Navigate to homepage
    if isinstance(blueprint, dict):
        pages_field = blueprint.get("pages")
        if isinstance(pages_field, dict):
            homepage = pages_field.get("homepage") or {}
        elif isinstance(pages_field, list):
            homepage = next(
                (p for p in pages_field if isinstance(p, dict) and
                 str(p.get("page_id", p.get("id", ""))).lower() in {"homepage", "home", "home_page"}),
                {}
            )
        else:
            homepage = blueprint.get("homepage") or {}
        
        # Also check if blueprint IS the homepage object
        if not homepage and "sections" in blueprint:
            homepage = blueprint

    elif isinstance(blueprint, list):
        # List of pages — find homepage
        homepage = next(
            (p for p in blueprint if isinstance(p, dict) and
             str(p.get("page_id", p.get("id", ""))).lower() in {"homepage", "home", "home_page"}),
            {}
        )
    else:
        homepage = {}

    # Look for sections containing service cards
    sections = homepage.get("sections", [])
    for section in sections:
        if not isinstance(section, dict):
            continue
        section_type = str(section.get("type", section.get("section_type", ""))).lower()
        if any(k in section_type for k in ("service", "grid", "card")):
            # Found service section — extract cards
            raw_cards = (
                section.get("cards") or
                section.get("service_cards") or
                section.get("items") or
                section.get("services") or
                []
            )
            cards.extend(raw_cards)

    # Fallback: check top-level homepage keys
    if not cards:
        for key in HOMEPAGE_SECTION_KEYS:
            if key in homepage:
                val = homepage[key]
                if isinstance(val, list):
                    cards.extend(val)
                    break

    return cards


def get_page_id(page: dict) -> str:
    return str(page.get("page_id") or page.get("id") or page.get("slug") or "unknown")


def get_card_target(card: dict) -> str:
    return str(card.get("link_to") or card.get("page_id") or card.get("target_page_id") or
               card.get("url") or card.get("slug") or "unknown")


def run():
    print("=" * 60)
    print("  check_blueprint_sync.py — Homepage Service Card Audit")
    print("=" * 60)
    print()

    failures = 0
    warnings = 0

    # ------------------------------------------------------------------
    # Load files
    # ------------------------------------------------------------------
    print("Loading files...")
    topical   = load_json(TOPICAL_FILE)
    blueprint = load_json(BLUEPRINT_FILE)

    if topical is None:
        print(f"FATAL: Cannot load {TOPICAL_FILE}. Run Prompt 5 first.")
        sys.exit(1)
    if blueprint is None:
        print(f"FATAL: Cannot load {BLUEPRINT_FILE}. Run Prompt 6 first.")
        sys.exit(1)

    print(f"  [OK] {TOPICAL_FILE} loaded")
    print(f"  [OK] {BLUEPRINT_FILE} loaded")
    print()

    # ------------------------------------------------------------------
    # Extract data
    # ------------------------------------------------------------------
    phase1_service_pages = get_phase1_service_pages(topical)
    homepage_cards       = get_homepage_service_cards(blueprint)

    phase1_ids = {get_page_id(p) for p in phase1_service_pages}
    card_targets = {get_card_target(c) for c in homepage_cards}

    print(f"Phase 1 service pages in topical_authority.json : {len(phase1_service_pages)}")
    for p in phase1_service_pages:
        print(f"    - {get_page_id(p)} ({p.get('primary_keyword', p.get('keyword', 'no keyword'))})")

    print()
    print(f"Homepage service cards in master_site_blueprint.json: {len(homepage_cards)}")
    for c in homepage_cards:
        print(f"    - {get_card_target(c)} ({c.get('title', c.get('heading', 'no title'))})")

    print()

    # ------------------------------------------------------------------
    # CHECK 1: Counts match
    # ------------------------------------------------------------------
    counts_match = len(phase1_service_pages) == len(homepage_cards)
    status = "[PASS]" if counts_match else "[FAIL]"
    print(f"  {status} Service card count matches Phase 1 count: "
          f"{len(homepage_cards)} cards vs {len(phase1_service_pages)} Phase 1 pages")
    if not counts_match:
        failures += 1
        if len(homepage_cards) > len(phase1_service_pages):
            print("         Homepage has MORE cards than Phase 1 service pages.")
            print("         Remove extra cards OR register the missing pages in topical_authority.json.")
        else:
            print("         Phase 1 has MORE pages than homepage cards.")
            print("         Add missing service cards to homepage OR move pages to a later phase.")

    print()

    # ------------------------------------------------------------------
    # CHECK 2: Cards without a registered Phase 1 target
    # ------------------------------------------------------------------
    orphaned_cards = card_targets - phase1_ids - {"unknown"}
    if orphaned_cards:
        print(f"  [FAIL] {len(orphaned_cards)} card(s) link to pages NOT in Phase 1 topical_authority.json:")
        for target in sorted(orphaned_cards):
            print(f"         - {target}")
        print("         Fix: register each page in topical_authority.json (correct phase, keyword, priority)")
        print("              AND add a pending_links.json entry for each.")
        failures += 1
    else:
        print("  [PASS] All homepage card targets are registered in topical_authority.json")

    # ------------------------------------------------------------------
    # CHECK 3: Phase 1 pages with no homepage card
    # ------------------------------------------------------------------
    unlinked_pages = phase1_ids - card_targets - {"unknown"}
    if unlinked_pages:
        print(f"  [WARN] {len(unlinked_pages)} Phase 1 service page(s) have no homepage service card:")
        for pid in sorted(unlinked_pages):
            print(f"         - {pid}")
        print("         Consider adding a service card for each, or move to a later phase.")
        warnings += 1
    else:
        print("  [PASS] All Phase 1 service pages have a matching homepage card")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print()
    print("-" * 60)
    if failures == 0 and warnings == 0:
        print("SYNC VERIFIED -- Homepage cards match Phase 1 service pages exactly.")
    elif failures == 0:
        print(f"SYNC OK with {warnings} warning(s). Review warnings above.")
    else:
        print(f"SYNC FAILED -- {failures} error(s), {warnings} warning(s).")
        print("Fix blueprint drift before publishing the homepage.")
        print("Reference: AGENTS.md > Blueprint Drift Prevention (FIX 19)")
        sys.exit(1)
    print("-" * 60)


if __name__ == "__main__":
    run()

