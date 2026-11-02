"""
data_extractor.py — Rank & Rent Flash Engine
Converts raw data.txt into a compact data_brief.txt (~500-800 words)
that P4 can reliably process on Gemini Flash 3.8.

Usage:
    python scripts/data_extractor.py
"""

import os
import re
import sys
import argparse
from pathlib import Path

# Force UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

MAX_FIELD_LENGTH = 200


def word_count(text):
    return len(text.split())


def extract_field(text, patterns):
    for pattern in patterns:
        matches = re.findall(pattern, text, re.MULTILINE)
        if matches:
            val = matches[0].strip()
            if val and len(val) >= 2:
                return val[:MAX_FIELD_LENGTH]
    return ""


def extract_section_lines(text, section_num):
    """Extract non-empty item lines from a specific SECTION header."""
    pattern = rf"SECTION\s+{section_num}\b.*?\n=+\n(.*?)(?=\n=|\Z)"
    m = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if not m:
        return []
    lines = []
    for raw in m.group(1).split("\n"):
        clean = raw.strip()
        if clean and not clean.startswith("[") and not clean.startswith("="):
            lines.append(clean)
    return lines


def main():
    parser = argparse.ArgumentParser(description="Extract structured brief from data.txt for P4")
    parser.add_argument("--input",  default="data.txt",       help="Input file (default: data.txt)")
    parser.add_argument("--output", default="data_brief.txt", help="Output file (default: data_brief.txt)")
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent.parent

    input_path = args.input
    if not os.path.exists(input_path):
        if (base_dir / args.input).exists():
            input_path = str(base_dir / args.input)
        else:
            print(f"ERROR: Cannot find input file: {args.input}")
            sys.exit(1)

    output_path = str(base_dir / args.output) if args.output == "data_brief.txt" else args.output

    print(f"Reading: {input_path}")
    raw = Path(input_path).read_text(encoding="utf-8", errors="replace")
    print(f"Input size: {word_count(raw):,} words — compressing...")

    fields = {}

    # Extract primary identity
    fields["niche"]           = extract_field(raw, [r"(?i)^\s*niche[:\s]+(.+)", r"(?i)primary service[:\s]+(.+)"])
    fields["primary_service"] = extract_field(raw, [r"(?i)^\s*primary service[:\s]+(.+)", r"(?i)main service[:\s]+(.+)"])
    fields["city"]            = extract_field(raw, [r"(?i)^\s*city[:\s]+(.+)", r"(?i)target city[:\s]+(.+)"])
    fields["state"]           = extract_field(raw, [r"(?i)^\s*state[:\s]+(.+)"])
    fields["company_name"]    = extract_field(raw, [r"(?i)^\s*company name[:\s]+(.+)", r"(?i)business name[:\s]+(.+)"])
    fields["phone"]           = extract_field(raw, [r"(?i)^\s*phone[:\s]+(.+)", r"(?i)telephone[:\s]+(.+)"])
    fields["address"]         = extract_field(raw, [r"(?i)^\s*address[:\s]+(.+)", r"(?i)street address[:\s]+(.+)"])
    fields["email"]           = extract_field(raw, [r"(?i)^\s*email[:\s]+(.+)"])
    fields["website"]         = extract_field(raw, [r"(?i)^\s*website[:\s]+(.+)", r"(?i)^\s*url[:\s]+(.+)"])
    fields["founded_year"]    = extract_field(raw, [r"(?i)^\s*founded year[:\s]+(\d{4})", r"(?i)^\s*founded[:\s]+(\d{4})"])
    fields["primary_keyword"] = extract_field(raw, [r"(?i)^\s*primary keyword[:\s]+(.+)"])

    # Keywords from Section 2
    sec2 = extract_section_lines(raw, 2)
    clean_kws = [k.split("—")[0].strip() for k in sec2 if k][:8]
    fields["secondary_keywords"] = clean_kws[1:] if len(clean_kws) > 1 else clean_kws

    # Services from Section 9
    sec9 = extract_section_lines(raw, 9)
    fields["services"] = sec9[:6]
    fields["sub_services"] = sec9[6:14]

    # Geography from Section 10
    sec10 = extract_section_lines(raw, 10)
    neighborhoods = []
    expansion_cities = []
    landmarks = []
    local_challenge = ""

    for line in sec10:
        if line.lower().startswith("neighborhood:"):
            neighborhoods.append(line.split(":", 1)[1].strip())
        elif line.lower().startswith("expansion city:"):
            expansion_cities.append(line.split(":", 1)[1].strip())
        elif line.lower().startswith("landmark:"):
            landmarks.append(line.split(":", 1)[1].strip())
        elif line.lower().startswith("local challenge:"):
            local_challenge = line.split(":", 1)[1].strip()

    fields["neighborhoods"] = neighborhoods[:10]
    fields["expansion_cities"] = expansion_cities[:8]
    fields["local_landmarks"] = landmarks[:6]
    fields["local_challenge"] = local_challenge

    # Pain points from Section 5
    sec5 = extract_section_lines(raw, 5)
    fields["pain_points"] = sec5[:6]

    # Credentials & trust from Section 11
    sec11 = extract_section_lines(raw, 11)
    fields["credentials"] = [c.replace("Credential:", "").strip() for c in sec11 if "Credential:" in c][:6]

    # PAA questions summary from Section 3
    sec3 = extract_section_lines(raw, 3)
    sample_paa = sec3[:10]

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
        "",
        "# CUSTOMER PAIN POINTS",
        f"PAIN_POINTS:        {'; '.join(fields['pain_points']) if fields.get('pain_points') else '[fill in]'}",
        "",
        "# TOP CUSTOMER QUESTIONS (PAA)",
        f"QUESTIONS:          {'; '.join(sample_paa) if sample_paa else '[fill in]'}",
        "",
        "# BUSINESS MODEL",
        "MONETIZATION:       rank_and_rent",
        "PRICING_RULE:       NEVER include pricing on any page",
        "",
        "=" * 60,
        "END OF DATA BRIEF",
        "=" * 60,
    ]

    brief_text = "\n".join(lines)
    Path(output_path).write_text(brief_text, encoding="utf-8")

    wc = word_count(brief_text)
    print(f"Output: {output_path}")
    print(f"Output size: {wc} words (from {word_count(raw):,})")
    print("\nPASS: Output is structured and ready for P4.")


if __name__ == "__main__":
    main()
