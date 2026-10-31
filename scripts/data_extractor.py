"""
data_extractor.py — Rank & Rent Flash Engine
Converts raw data.txt into a compact data_brief.txt (~500-800 words)
that P4 can reliably process on Gemini Flash 3.8.

Usage:
    python scripts/data_extractor.py
    python scripts/data_extractor.py --input path/to/data.txt --output path/to/data_brief.txt

Input:  data.txt (raw scraped research — can be very large)
Output: data_brief.txt (structured key:value brief for P4)

How it works:
    1. Reads data.txt
    2. Uses rule-based extraction to find values for each required P4 field
    3. Truncates all values to safe lengths
    4. Writes compact data_brief.txt
    5. Reports word count — warns if still > 1000 words
"""

import os
import re
import sys
import argparse


# ─────────────────────────────────────────────────────────────────────────────
# CONFIG — adjust extraction patterns per your data.txt format
# ─────────────────────────────────────────────────────────────────────────────

# Labels that signal a field value in data.txt
# Add more patterns here if your data.txt uses different labels
FIELD_PATTERNS = {
    "niche":               [r"(?i)niche[:\s]+(.+)", r"(?i)primary service[:\s]+(.+)"],
    "primary_service":     [r"(?i)primary service[:\s]+(.+)", r"(?i)main service[:\s]+(.+)"],
    "city":                [r"(?i)^city[:\s]+(.+)", r"(?i)target city[:\s]+(.+)"],
    "state":               [r"(?i)^state[:\s]+(.+)"],
    "company_name":        [r"(?i)company name[:\s]+(.+)", r"(?i)business name[:\s]+(.+)"],
    "phone":               [r"(?i)phone[:\s]+(.+)", r"(?i)telephone[:\s]+(.+)"],
    "address":             [r"(?i)^address[:\s]+(.+)", r"(?i)street address[:\s]+(.+)"],
    "email":               [r"(?i)^email[:\s]+(.+)"],
    "website":             [r"(?i)^website[:\s]+(.+)", r"(?i)^url[:\s]+(.+)"],
    "founded_year":        [r"(?i)founded[:\s]+(\d{4})", r"(?i)established[:\s]+(\d{4})", r"(?i)in business since[:\s]+(\d{4})"],
    "primary_keyword":     [r"(?i)primary keyword[:\s]+(.+)", r"(?i)main keyword[:\s]+(.+)"],
    "secondary_keywords":  [r"(?i)secondary keywords[:\s]+(.+)", r"(?i)keywords[:\s]+(.+)"],
    "services":            [r"(?i)^services[:\s]+(.+)", r"(?i)service list[:\s]+(.+)"],
    "sub_services":        [r"(?i)sub.?services[:\s]+(.+)", r"(?i)service types[:\s]+(.+)"],
    "neighborhoods":       [r"(?i)neighborhoods[:\s]+(.+)", r"(?i)areas served[:\s]+(.+)"],
    "expansion_cities":    [r"(?i)expansion cities[:\s]+(.+)", r"(?i)service area cities[:\s]+(.+)"],
    "local_challenge":     [r"(?i)local challenge[:\s]+(.+)", r"(?i)regional challenge[:\s]+(.+)", r"(?i)climate[:\s]+(.+)"],
    "local_landmarks":     [r"(?i)landmarks[:\s]+(.+)", r"(?i)local landmarks[:\s]+(.+)"],
    "credentials":         [r"(?i)credentials[:\s]+(.+)", r"(?i)licenses[:\s]+(.+)", r"(?i)certifications[:\s]+(.+)"],
    "community_ties":      [r"(?i)community ties[:\s]+(.+)", r"(?i)memberships[:\s]+(.+)", r"(?i)sponsorships[:\s]+(.+)"],
    "tone_voice":          [r"(?i)tone[:\s]+(.+)", r"(?i)voice[:\s]+(.+)", r"(?i)writing style[:\s]+(.+)"],
    "pain_points":         [r"(?i)pain points[:\s]+(.+)", r"(?i)customer problems[:\s]+(.+)"],
    "monetization_model":  [r"(?i)monetization[:\s]+(.+)", r"(?i)business model[:\s]+(.+)"],
}

# Max characters to keep per field value (prevents bloat)
MAX_FIELD_LENGTH = 200

# Fields that are always set to a fixed value for this kit
FIXED_FIELDS = {
    "monetization_model": "rank_and_rent",
    "no_pricing_rule": "NEVER include pricing on any page",
}


def extract_field(text, patterns):
    """Try each pattern in order, return first match (stripped, truncated)."""
    for pattern in patterns:
        matches = re.findall(pattern, text, re.MULTILINE)
        if matches:
            value = matches[0].strip()
            if value and len(value) > 2:
                return value[:MAX_FIELD_LENGTH]
    return ""


def extract_list_field(text, patterns, max_items=10):
    """Extract a comma-separated or newline-separated list field."""
    raw = extract_field(text, patterns)
    if not raw:
        return []
    # Split on commas, semicolons, or newlines
    items = re.split(r"[,;\n]+", raw)
    items = [i.strip().strip('"').strip("'") for i in items if i.strip()]
    return items[:max_items]


def extract_pain_points(text, max_items=5):
    """Find pain points from research content."""
    patterns = [
        r"(?i)pain points?[:\s]+(.+?)(?=\n\n|\Z)",
        r"(?i)customer problems?[:\s]+(.+?)(?=\n\n|\Z)",
        r"(?i)common complaints?[:\s]+(.+?)(?=\n\n|\Z)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            raw = match.group(1).strip()[:500]
            items = re.split(r"[,;\n•\-]+", raw)
            items = [i.strip() for i in items if len(i.strip()) > 5]
            if items:
                return items[:max_items]
    return []


def summarize_research(text, max_words=100):
    """Extract a brief research summary from the text body."""
    # Take first 500 chars of non-header, non-empty text
    lines = [l.strip() for l in text.split("\n") if l.strip() and not l.startswith("#") and len(l.strip()) > 30]
    summary = " ".join(lines[:3])
    words = summary.split()
    return " ".join(words[:max_words])


def word_count(text):
    return len(text.split())


def main():
    parser = argparse.ArgumentParser(description="Extract structured brief from data.txt for P4")
    parser.add_argument("--input",  default="data.txt",       help="Input file (default: data.txt)")
    parser.add_argument("--output", default="data_brief.txt", help="Output file (default: data_brief.txt)")
    args = parser.parse_args()

    # Find input file
    input_path = args.input
    if not os.path.exists(input_path):
        # Try scripts/ subdirectory
        alt = os.path.join("scripts", args.input)
        if os.path.exists(alt):
            input_path = alt
        else:
            print(f"ERROR: Cannot find input file: {args.input}")
            sys.exit(1)

    print(f"Reading: {input_path}")
    with open(input_path, "r", encoding="utf-8", errors="replace") as f:
        raw = f.read()

    print(f"Input size: {word_count(raw):,} words — compressing...")

    # ── Extract all fields ──────────────────────────────────────────────────

    fields = {}

    # Simple string fields
    simple = [
        "niche", "primary_service", "city", "state", "company_name",
        "phone", "address", "email", "website", "founded_year",
        "primary_keyword", "local_challenge", "tone_voice", "monetization_model",
    ]
    for field in simple:
        if field in FIELD_PATTERNS:
            fields[field] = extract_field(raw, FIELD_PATTERNS[field])

    # List fields
    list_fields = [
        ("secondary_keywords", 8),
        ("services", 6),
        ("sub_services", 8),
        ("neighborhoods", 12),
        ("expansion_cities", 8),
        ("local_landmarks", 5),
        ("credentials", 6),
        ("community_ties", 5),
    ]
    for field, max_items in list_fields:
        if field in FIELD_PATTERNS:
            fields[field] = extract_list_field(raw, FIELD_PATTERNS[field], max_items)

    # Pain points
    fields["pain_points"] = extract_pain_points(raw)

    # Research summary (from body of data.txt, not headers)
    fields["research_summary"] = summarize_research(raw)

    # Fixed fields
    fields["monetization_model"] = "rank_and_rent"

    # ── Build data_brief.txt ────────────────────────────────────────────────

    lines = [
        "=" * 60,
        "DATA BRIEF — Rank & Rent Flash Engine",
        "Generated by: data_extractor.py",
        "Source: " + input_path,
        "Paste this file into P4 prompt (not the raw data.txt)",
        "=" * 60,
        "",
        "# PROJECT IDENTITY",
        f"NICHE:              {fields.get('niche', '[fill in]')}",
        f"PRIMARY_SERVICE:    {fields.get('primary_service', '[fill in]')}",
        f"CITY:               {fields.get('city', '[fill in]')}",
        f"STATE:              {fields.get('state', '[fill in]')}",
        "",
        "# NAP (Name, Address, Phone)",
        f"COMPANY_NAME:       {fields.get('company_name', '[fill in]')}",
        f"ADDRESS:            {fields.get('address', '[fill in]')}",
        f"PHONE:              {fields.get('phone', '[fill in]')}",
        f"EMAIL:              {fields.get('email', '[fill in]')}",
        f"WEBSITE:            {fields.get('website', '[fill in]')}",
        f"FOUNDED_YEAR:       {fields.get('founded_year', '[fill in]')}",
        "",
        "# KEYWORDS",
        f"PRIMARY_KEYWORD:    {fields.get('primary_keyword', '[fill in]')}",
        f"SECONDARY_KEYWORDS: {', '.join(fields['secondary_keywords']) if fields.get('secondary_keywords') else '[fill in]'}",
        "",
        "# SERVICES",
        f"SERVICES:           {', '.join(fields['services']) if fields.get('services') else '[fill in]'}",
        f"SUB_SERVICES:       {', '.join(fields['sub_services']) if fields.get('sub_services') else '[fill in]'}",
        "",
        "# GEOGRAPHY",
        f"NEIGHBORHOODS:      {', '.join(fields['neighborhoods']) if fields.get('neighborhoods') else '[fill in]'}",
        f"EXPANSION_CITIES:   {', '.join(fields['expansion_cities']) if fields.get('expansion_cities') else '[fill in]'}",
        f"LOCAL_LANDMARKS:    {', '.join(fields['local_landmarks']) if fields.get('local_landmarks') else '[fill in]'}",
        f"LOCAL_CHALLENGE:    {fields.get('local_challenge', '[fill in]')}",
        "",
        "# TRUST & CREDENTIALS",
        f"CREDENTIALS:        {', '.join(fields['credentials']) if fields.get('credentials') else '[fill in]'}",
        f"COMMUNITY_TIES:     {', '.join(fields['community_ties']) if fields.get('community_ties') else '[fill in]'}",
        "",
        "# CONTENT STRATEGY",
        f"PAIN_POINTS:        {', '.join(fields['pain_points']) if fields.get('pain_points') else '[fill in]'}",
        f"TONE:               {fields.get('tone_voice', 'professional, trustworthy, local')}",
        "",
        "# BUSINESS MODEL",
        f"MONETIZATION:       rank_and_rent",
        f"PRICING_RULE:       NEVER include pricing on any page",
        "",
        "# RESEARCH SUMMARY (from data.txt)",
        fields.get("research_summary", "[no summary extracted — check data.txt]"),
        "",
        "=" * 60,
        "END OF DATA BRIEF",
        "=" * 60,
        "",
        "INSTRUCTIONS FOR P4:",
        "1. Review all [fill in] fields above and complete them manually",
        "2. Paste this entire file into the P4 prompt where indicated",
        "3. P4 will generate master_brief.json from this brief",
        "4. Do NOT paste raw data.txt into P4 — it will overwhelm Flash 3.8",
    ]

    brief_text = "\n".join(lines)

    # ── Write output ────────────────────────────────────────────────────────

    output_path = args.output
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(brief_text)

    wc = word_count(brief_text)
    print(f"Output: {output_path}")
    print(f"Output size: {wc} words (from {word_count(raw):,})")

    # Quality checks
    missing = []
    required = ["niche", "city", "state", "company_name", "phone", "primary_keyword"]
    for field in required:
        val = fields.get(field, "")
        if not val or "[fill in]" in str(val):
            missing.append(field)

    if missing:
        print(f"\nWARNING: These required fields were not found in data.txt:")
        for m in missing:
            print(f"  - {m} → fill in manually in {output_path}")

    if wc > 1200:
        print(f"\nWARNING: Output is {wc} words — still large for Flash 3.8.")
        print("Consider reducing the RESEARCH SUMMARY section manually.")
    elif wc <= 800:
        print(f"\nPASS: Output is {wc} words — safe for Flash 3.8.")
    else:
        print(f"\nOK: Output is {wc} words — acceptable for Flash 3.8.")

    print("\nNext step: Review data_brief.txt, fill any [fill in] fields, then run P4.")


if __name__ == "__main__":
    main()

