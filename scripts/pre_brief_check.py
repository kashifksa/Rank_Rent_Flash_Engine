#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pre_brief_check.py — Rank & Rent Pipeline (Adaptive Input Validation)
=====================================================================
Validates all input files before running Prompt 4 (master_brief.json).

Checks performed:
  1. data.txt exists and is non-empty
  2. data.txt contains the required pipeline fields (Primary Keyword, City, Niche, NAP)
  3. data.txt has no raw HTML artifacts from the scraper
  4. data.txt has sufficient content (minimum line count)
  5. No obvious encoding errors
"""

import os
import re
import sys
from pathlib import Path

# Force UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data.txt" if (BASE_DIR / "data.txt").exists() else Path("data.txt")

# Required fields/sections (any match counts as pass)
REQUIRED_CHECKS = [
    ("Primary Keyword", [r"\[Primary Keyword\]", r"Primary Keyword\s*:", r"SECTION 2"]),
    ("City",            [r"\[City\]", r"City\s*:", r"SECTION 10"]),
    ("Niche",           [r"\[Niche\]", r"Niche\s*:", r"SECTION 1"]),
    ("NAP / Company",   [r"\[NAP\]", r"Company Name\s*:", r"Phone\s*:"]),
]

RECOMMENDED_CHECKS = [
    ("Competitors",         [r"\[Competitors\]", r"SECTION 8", r"competitor"]),
    ("Customer Pain Points",[r"\[Customer Pain Points\]", r"SECTION 5", r"pain points"]),
    ("Services Offered",    [r"\[Services Offered\]", r"SECTION 9", r"services in this niche"]),
    ("Expansion Cities",    [r"\[Expansion Cities Identified\]", r"Expansion city\s*:", r"SECTION 10"]),
]

RAW_SCRAPE_PATTERNS = [
    r"<html",
    r"<div",
    r"<span",
    r"<script(?!\s+type=[\"']application/ld\+json[\"'])",  # Allow JSON-LD schema
    r"Posted by u/",
    r"View all comments",
    r"\[deleted\]",
    r"^\s*https?://\S{40,}",   # bare long tracking URLs
]
RAW_RE = re.compile("|".join(RAW_SCRAPE_PATTERNS), re.IGNORECASE | re.MULTILINE)

MIN_LINES = 50


def check(label: str, passed: bool, detail: str = "", fatal: bool = True):
    icon = "[PASS]" if passed else ("[FAIL]" if fatal else "[WARN]")
    print(f"  {icon} {label}")
    if detail:
        print(f"         {detail}")
    return passed


def run():
    print("=" * 60)
    print("  pre_brief_check.py — Input Validation for Prompt 4")
    print("=" * 60)
    print(f"  Target: {DATA_FILE}")
    print()

    failures = 0

    exists = DATA_FILE.exists()
    if not check("data.txt exists", exists, detail="" if exists else f"Expected at: {DATA_FILE.resolve()}"):
        print("\nFATAL: data.txt missing. Run python scripts/build_data.py first.")
        sys.exit(1)

    raw = DATA_FILE.read_text(encoding="utf-8", errors="replace")
    lines = [l for l in raw.splitlines() if l.strip()]

    if not check("data.txt is non-empty", len(lines) > 0, detail=f"Found {len(lines)} non-empty lines"):
        failures += 1

    sufficient = len(lines) >= MIN_LINES
    check(f"data.txt has sufficient content (>= {MIN_LINES} lines)", sufficient,
          detail=f"Found {len(lines)} lines.", fatal=False)

    for name, patterns in REQUIRED_CHECKS:
        found = any(re.search(pat, raw, re.IGNORECASE) for pat in patterns)
        if not check(f"Required field present: {name}", found,
                     detail="" if found else f"Add {name} to data.txt"):
            failures += 1

    for name, patterns in RECOMMENDED_CHECKS:
        found = any(re.search(pat, raw, re.IGNORECASE) for pat in patterns)
        check(f"Recommended section present: {name}", found,
              detail="" if found else f"Consider adding {name}", fatal=False)

    raw_match = RAW_RE.search(raw)
    no_raw = raw_match is None
    if not check("No raw HTML or scraper artifacts in data.txt", no_raw,
                 detail="" if no_raw else f"Found artifact near: {repr(raw_match.group(0)[:60])}"):
        failures += 1

    no_replacement = "\ufffd" not in raw
    check("No encoding errors (replacement chars)", no_replacement,
          detail="" if no_replacement else "File contains replacement chars", fatal=False)

    print()
    print("-" * 60)
    if failures == 0:
        print("ALL REQUIRED CHECKS PASSED")
        print("data.txt is ready. Proceed to Prompt 4 (master_brief.json).")
    else:
        print(f"{failures} REQUIRED CHECK(S) FAILED")
        sys.exit(1)
    print("-" * 60)


if __name__ == "__main__":
    run()
