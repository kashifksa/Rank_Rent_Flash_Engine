#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
clean_research.py — Rank & Rent Pipeline (FIX 3)
================================================
Filters raw research_data.txt into a curated data.txt.

Run AFTER research_scraper.py, BEFORE build_data.py.
Usage: python clean_research.py

What it removes:
  - HTML tags and entities
  - Bare URLs and http/https lines
  - Duplicate lines (keeps first occurrence)
  - Lines shorter than 40 chars (noise / navigation fragments)
  - Lines that are purely numeric or punctuation
  - Reddit/Quora boilerplate ("Posted by u/", "View all comments", etc.)
  - Lines with excessive caps (>60% uppercase = scraper artifact)
  - Empty lines clusters (collapses 2+ blank lines into 1)

What it keeps:
  - All substantive sentences (40+ chars, mixed case)
  - Lines containing [Section Headers] used by the pipeline
  - Lines with keyword/niche data signals
"""

import re
import os
import sys

INPUT_FILE  = "research_data.txt"
OUTPUT_FILE = "data.txt"

# ---------------------------------------------------------------------------
# Boilerplate patterns to strip (case-insensitive)
# ---------------------------------------------------------------------------
BOILERPLATE_PATTERNS = [
    r"^posted by u/",
    r"^view all comments",
    r"^share\s*$",
    r"^save\s*$",
    r"^report\s*$",
    r"^reply\s*$",
    r"^upvote\s*$",
    r"^downvote\s*$",
    r"^collapsed\s*$",
    r"^continue this thread",
    r"^load more comments",
    r"^\d+ (point|points|comment|comments|vote|votes|hour|hours|day|days|month|months) ago",
    r"^(quora|reddit)\s*[-|]\s*",
    r"^advertisement\s*$",
    r"^sponsored\s*$",
    r"^cookie policy",
    r"^privacy policy",
    r"^terms of service",
    r"^all rights reserved",
    r"^copyright \d{4}",
    r"^\[deleted\]\s*$",
    r"^\[removed\]\s*$",
    r"^answer requested by",
    r"^originally answered",
    r"^related questions?:",
]

BOILERPLATE_RE = re.compile(
    "|".join(BOILERPLATE_PATTERNS), re.IGNORECASE
)

# HTML tag / entity pattern
HTML_RE = re.compile(r"<[^>]+>|&[a-z]{2,6};|&#\d+;", re.IGNORECASE)

# Bare URL pattern (lines that are ONLY a URL)
URL_ONLY_RE = re.compile(r"^\s*https?://\S+\s*$", re.IGNORECASE)

# Excessive caps check
def is_excessive_caps(line: str) -> bool:
    letters = [c for c in line if c.isalpha()]
    if len(letters) < 10:
        return False
    caps_ratio = sum(1 for c in letters if c.isupper()) / len(letters)
    return caps_ratio > 0.60

# Section header pattern — always keep these
SECTION_HEADER_RE = re.compile(r"^\[.+\]\s*$")

def clean_line(line: str) -> str | None:
    """Return cleaned line or None if the line should be dropped."""
    stripped = line.strip()

    # Always keep section headers
    if SECTION_HEADER_RE.match(stripped):
        return stripped

    # Drop empty lines (handled separately for collapsing)
    if not stripped:
        return ""

    # Drop bare URLs
    if URL_ONLY_RE.match(stripped):
        return None

    # Strip inline HTML; if the result is empty, drop
    cleaned = HTML_RE.sub("", stripped).strip()
    if not cleaned:
        return None

    # Drop boilerplate
    if BOILERPLATE_RE.match(cleaned):
        return None

    # Drop lines shorter than 40 chars (noise)
    if len(cleaned) < 40 and not SECTION_HEADER_RE.match(cleaned):
        return None

    # Drop lines that are purely punctuation or numbers
    if re.match(r"^[\W\d]+$", cleaned):
        return None

    # Drop excessive caps lines (scraper nav artifacts)
    if is_excessive_caps(cleaned):
        return None

    return cleaned


def run():
    if not os.path.exists(INPUT_FILE):
        print(f"ERROR: {INPUT_FILE} not found. Run research_scraper.py first.")
        sys.exit(1)

    with open(INPUT_FILE, "r", encoding="utf-8", errors="replace") as f:
        raw_lines = f.readlines()

    print(f"Input:  {len(raw_lines)} lines from {INPUT_FILE}")

    seen = set()
    output_lines = []
    blank_streak = 0

    for raw in raw_lines:
        result = clean_line(raw)

        if result is None:
            continue  # drop

        if result == "":
            blank_streak += 1
            if blank_streak <= 1:
                output_lines.append("")
            continue

        blank_streak = 0

        # Deduplicate (normalised)
        key = result.lower().strip()
        if key in seen:
            continue
        seen.add(key)

        output_lines.append(result)

    # Remove leading/trailing blank lines
    while output_lines and output_lines[0] == "":
        output_lines.pop(0)
    while output_lines and output_lines[-1] == "":
        output_lines.pop()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines) + "\n")

    kept = len([l for l in output_lines if l])
    dropped = len(raw_lines) - kept
    print(f"Output: {kept} lines written to {OUTPUT_FILE}")
    print(f"Dropped {dropped} lines (noise, duplicates, boilerplate, HTML, URLs)")
    print("clean_research.py complete. Run pre_brief_check.py next.")


if __name__ == "__main__":
    run()

