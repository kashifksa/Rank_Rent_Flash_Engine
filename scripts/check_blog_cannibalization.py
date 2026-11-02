#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_blog_cannibalization.py - Rank & Rent Pipeline (FIX 31)
=============================================================
Detects keyword cannibalization between blog posts, and between
blog posts and service/location pages.

Run BEFORE writing any Phase 5 blog post (before Prompt 7).
Usage:
  python check_blog_cannibalization.py
      (audits ALL blog posts in topical_authority.json against each other
       and against all service/location pages)

  python check_blog_cannibalization.py --new-keyword "how to fix a sprinkler head"
      (checks a proposed new keyword against everything already registered)

Exit code 0 = PASS (safe to proceed)
Exit code 1 = FAIL (conflicts found - fix before writing)
"""

import json
import os
import re
import sys
import argparse

TOPICAL_FILE = "topical_authority.json"

# Page types treated as "blog / informational"
BLOG_TYPES = {"blog", "blog_post", "informational", "how_to", "guide",
              "faq_post", "seasonal", "case_study"}

# Page types treated as "money pages" (service/location)
MONEY_TYPES = {"service", "service_page", "primary_service", "secondary_service",
               "location", "location_hub", "zip_code_page", "neighborhood_page",
               "homepage", "about", "contact"}

# Stop words to strip before comparing keyword tokens
STOP_WORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "can", "could", "should", "may", "might", "must", "shall", "your",
    "my", "our", "its", "this", "that", "these", "those", "how", "what",
    "when", "where", "why", "which", "who", "if", "so", "as", "than",
    "then", "just", "more", "most", "also", "not", "no", "any", "all",
}

# Similarity threshold - keyword pairs above this are flagged
# 0.5 = 50% of meaningful tokens overlap
SIMILARITY_THRESHOLD = 0.50


# ─── Helpers ──────────────────────────────────────────────────────────────────

def tokenise(keyword: str) -> set:
    """Lowercase, remove punctuation, remove stop words → set of meaningful tokens."""
    tokens = re.findall(r"[a-z]+", keyword.lower())
    return {t for t in tokens if t not in STOP_WORDS and len(t) > 2}


def similarity(kw_a: str, kw_b: str) -> float:
    """Jaccard similarity between two keyword token sets."""
    a, b = tokenise(kw_a), tokenise(kw_b)
    if not a or not b:
        return 0.0
    intersection = a & b
    union = a | b
    return len(intersection) / len(union)


def get_page_id(page: dict) -> str:
    return str(page.get("page_id") or page.get("id") or page.get("slug") or "?")


def get_keyword(page: dict) -> str:
    return str(
        page.get("primary_keyword") or
        page.get("keyword") or
        page.get("target_keyword") or
        ""
    ).strip()


def get_type(page: dict) -> str:
    return str(page.get("page_type") or page.get("type") or "").lower().replace(" ", "_")


def load_pages(topical: dict | list) -> list[dict]:
    if isinstance(topical, list):
        return topical
    if isinstance(topical, dict):
        pages = (topical.get("pages") or topical.get("content_map") or
                 topical.get("topical_map") or [])
        for key, val in topical.items():
            if isinstance(val, list) and key.lower().startswith("phase"):
                pages = pages + val
        return pages
    return []


# ─── Core audit ───────────────────────────────────────────────────────────────

def audit(new_keyword: str | None = None) -> bool:
    """
    Run the cannibalization audit.
    Returns True if clean (no conflicts), False if conflicts found.
    """
    if not os.path.exists(TOPICAL_FILE):
        print(f"ERROR: {TOPICAL_FILE} not found. Run Prompt 5 first.")
        sys.exit(1)

    with open(TOPICAL_FILE, "r", encoding="utf-8") as f:
        topical = json.load(f)

    all_pages = load_pages(topical)

    blog_pages  = [p for p in all_pages if get_type(p) in BLOG_TYPES and get_keyword(p)]
    money_pages = [p for p in all_pages if get_type(p) in MONEY_TYPES and get_keyword(p)]

    print("=" * 60)
    print("  check_blog_cannibalization.py - Blog Keyword Audit")
    print("=" * 60)
    print(f"\n  Blog posts found   : {len(blog_pages)}")
    print(f"  Money pages found  : {len(money_pages)}")
    if new_keyword:
        print(f"  New keyword check  : \"{new_keyword}\"")
    print()

    conflicts = []

    # ── If checking a new proposed keyword ────────────────────────────────────
    if new_keyword:
        # vs existing blog posts
        for bp in blog_pages:
            kw = get_keyword(bp)
            sim = similarity(new_keyword, kw)
            if sim >= SIMILARITY_THRESHOLD:
                conflicts.append({
                    "type": "blog-vs-blog (proposed)",
                    "a": f'NEW: "{new_keyword}"',
                    "b": f'{get_page_id(bp)}: "{kw}"',
                    "similarity": round(sim * 100),
                })
        # vs money pages
        for mp in money_pages:
            kw = get_keyword(mp)
            sim = similarity(new_keyword, kw)
            if sim >= SIMILARITY_THRESHOLD:
                conflicts.append({
                    "type": "blog-vs-service (proposed)",
                    "a": f'NEW: "{new_keyword}"',
                    "b": f'{get_page_id(mp)} [{get_type(mp)}]: "{kw}"',
                    "similarity": round(sim * 100),
                })

    # ── Blog-vs-blog full audit ────────────────────────────────────────────────
    for i, bp_a in enumerate(blog_pages):
        for bp_b in blog_pages[i + 1:]:
            kw_a, kw_b = get_keyword(bp_a), get_keyword(bp_b)
            sim = similarity(kw_a, kw_b)
            if sim >= SIMILARITY_THRESHOLD:
                conflicts.append({
                    "type": "blog-vs-blog",
                    "a": f'{get_page_id(bp_a)}: "{kw_a}"',
                    "b": f'{get_page_id(bp_b)}: "{kw_b}"',
                    "similarity": round(sim * 100),
                })

    # ── Blog-vs-money-page audit ───────────────────────────────────────────────
    if not new_keyword:  # already checked above when new_keyword provided
        for bp in blog_pages:
            kw_b = get_keyword(bp)
            for mp in money_pages:
                kw_m = get_keyword(mp)
                sim = similarity(kw_b, kw_m)
                if sim >= SIMILARITY_THRESHOLD:
                    conflicts.append({
                        "type": "blog-vs-service",
                        "a": f'{get_page_id(bp)}: "{kw_b}"',
                        "b": f'{get_page_id(mp)} [{get_type(mp)}]: "{kw_m}"',
                        "similarity": round(sim * 100),
                    })

    # ── Report ────────────────────────────────────────────────────────────────
    if not conflicts:
        print("  [PASS] No keyword cannibalization detected.")
        if new_keyword:
            print(f"  Safe to proceed with: \"{new_keyword}\"")
        else:
            print("  All blog post keywords are semantically distinct.")
        print()
        print("-" * 60)
        print("CLEAN - Proceed to Prompt 7.")
        print("-" * 60)
        return True

    print(f"  [FAIL] {len(conflicts)} cannibalization conflict(s) found:\n")
    for i, c in enumerate(conflicts, 1):
        print(f"  {i}. [{c['type']}] - {c['similarity']}% similarity")
        print(f"       A: {c['a']}")
        print(f"       B: {c['b']}")
        print()

    print("-" * 60)
    print("HOW TO FIX:")
    print("  blog-vs-blog    → Reframe one post with a different angle/intent")
    print("                    e.g. DIY fix vs cost guide vs diagnosis signs")
    print("  blog-vs-service → Change the blog to informational intent only")
    print("                    e.g. 'how to tell if...' not 'sprinkler repair in city'")
    print("  Update topical_authority.json with the corrected keyword,")
    print("  then re-run this script before proceeding to Prompt 7.")
    print("-" * 60)
    return False


# ─── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check blog post keyword cannibalization before writing."
    )
    parser.add_argument(
        "--new-keyword", "-k",
        type=str,
        default=None,
        help="Proposed new blog post keyword to check before writing"
    )
    args = parser.parse_args()

    clean = audit(new_keyword=args.new_keyword)
    sys.exit(0 if clean else 1)

