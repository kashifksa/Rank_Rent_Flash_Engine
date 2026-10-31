#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pre_brief_check.py — Rank & Rent Pipeline (FIX 2)
==================================================
Validates all input files before running Prompt 4 (master_brief.json).

Run AFTER clean_research.py, BEFORE submitting Prompt 4.
Usage: python pre_brief_check.py

Checks performed:
  1. data.txt exists and is non-empty
  2. data.txt contains the required pipeline section headers
  3. data.txt has no raw HTML artifacts from the scraper
  4. data.txt has sufficient content (minimum line count)
  5. No obvious encoding errors
  6. Warns if data.txt appears to contain raw, uncleaned content
"""

import os
import re
import sys

DATA_FILE = "data.txt"

# ---------------------------------------------------------------------------
# Required section headers that data.txt must contain
# (clean_research.py must have produced a file with these present)
# ---------------------------------------------------------------------------
REQUIRED_SECTIONS = [
    "[Primary Keyword]",
    "[City]",
    "[Niche]",
    "[NAP]",
]

# Sections that are strongly recommended (warn if missing, don't fail)
RECOMMENDED_SECTIONS = [
    "[Competitors]",
    "[Customer Pain Points]",
    "[Services Offered]",
    "[Expansion Cities Identified]",
]

# Signs of uncleaned raw scrape data
RAW_SCRAPE_PATTERNS = [
    r"<html",
    r"<div",
    r"<span",
    r"<script",
    r"Posted by u/",
    r"View all comments",
    r"\[deleted\]",
    r"^\s*https?://\S{20,}",   # bare long URLs
]
RAW_RE = re.compile("|".join(RAW_SCRAPE_PATTERNS), re.IGNORECASE | re.MULTILINE)

MIN_LINES = 50   # minimum meaningful lines expected after cleaning

# ---------------------------------------------------------------------------

def check(label: str, passed: bool, detail: str = "", fatal: bool = True):
    """Print result line. Returns True if passed."""
    status = "PASS" if passed else ("FAIL" if fatal else "WARN")
    icon   = "[PASS]" if passed else ("[FAIL]" if fatal else "[WARN]")
    print(f"  {icon} {label}")
    if detail:
        print(f"         {detail}")
    return passed


def run():
    print("=" * 60)
    print("  pre_brief_check.py — Input Validation for Prompt 4")
    print("=" * 60)
    print()

    failures = 0

    # ------------------------------------------------------------------
    # CHECK 1: data.txt exists
    # ------------------------------------------------------------------
    exists = os.path.exists(DATA_FILE)
    if not check("data.txt exists", exists,
                 detail="" if exists else f"Expected at: {os.path.abspath(DATA_FILE)}"):
        print()
        print("FATAL: data.txt missing. Run research_scraper.py then clean_research.py.")
        sys.exit(1)

    with open(DATA_FILE, "r", encoding="utf-8", errors="replace") as f:
        raw = f.read()

    lines = [l for l in raw.splitlines() if l.strip()]

    # ------------------------------------------------------------------
    # CHECK 2: Non-empty
    # ------------------------------------------------------------------
    if not check("data.txt is non-empty", len(lines) > 0,
                 detail=f"Found {len(lines)} non-empty lines"):
        failures += 1

    # ------------------------------------------------------------------
    # CHECK 3: Minimum line count
    # ------------------------------------------------------------------
    sufficient = len(lines) >= MIN_LINES
    if not check(
        f"data.txt has sufficient content (>= {MIN_LINES} lines)",
        sufficient,
        detail=f"Found {len(lines)} lines. Run clean_research.py if count is too low.",
        fatal=False
    ):
        pass  # warn only

    # ------------------------------------------------------------------
    # CHECK 4: Required section headers present
    # ------------------------------------------------------------------
    for section in REQUIRED_SECTIONS:
        found = section in raw
        if not check(f"Required section present: {section}", found,
                     detail="" if found else f"Add '{section}' section to data.txt"):
            failures += 1

    # ------------------------------------------------------------------
    # CHECK 5: Recommended section headers (warn only)
    # ------------------------------------------------------------------
    for section in RECOMMENDED_SECTIONS:
        found = section in raw
        check(f"Recommended section present: {section}", found,
              detail="" if found else f"Consider adding '{section}' for richer output",
              fatal=False)

    # ------------------------------------------------------------------
    # CHECK 6: No raw HTML / scraper artifacts
    # ------------------------------------------------------------------
    raw_match = RAW_RE.search(raw)
    no_raw = raw_match is None
    if not check(
        "No raw HTML or scraper artifacts in data.txt",
        no_raw,
        detail="" if no_raw else f"Found artifact near: {repr(raw_match.group(0)[:60])}. Run clean_research.py.",
    ):
        failures += 1

    # ------------------------------------------------------------------
    # CHECK 7: No encoding errors (replacement chars)
    # ------------------------------------------------------------------
    no_replacement = "\ufffd" not in raw
    check("No encoding errors (replacement chars)", no_replacement,
          detail="" if no_replacement else "File contains replacement chars — re-save as UTF-8",
          fatal=False)

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print()
    print("-" * 60)
    if failures == 0:
        print("ALL REQUIRED CHECKS PASSED")
        print("data.txt is ready. Proceed to Prompt 4 (master_brief.json).")
    else:
        print(f"{failures} REQUIRED CHECK(S) FAILED")
        print("Fix the issues above before running Prompt 4.")
        print("Common fix: re-run clean_research.py after editing data.txt.")
        sys.exit(1)
    print("-" * 60)


if __name__ == "__main__":
    run()

