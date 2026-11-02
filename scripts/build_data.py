"""
build_data.py — Rank & Rent Flash Engine (Adaptive / Smart Ingestion)
=====================================================================
Merges ALL research sources into a single structured data.txt file.

SMART FILE DETECTION:
You do NOT need to rename your downloaded files to rigid names!
build_data.py automatically scans raw_research/ and matches files using
flexible pattern matching for:
  - AlsoAsked / PAA files (CSV or TXT)
  - SEMrush / Keyword Magic tables (CSV or TXT)
  - AnswerThePublic exports (CSV or TXT)
  - SERP / Competitor snippets (CSV or TXT)
  - TopicalRelevance exports (TXT)
  - YouTube transcripts or video URLs (TXT)
  - ahrefs_keywords.csv in root or raw_research/

Usage:
    python scripts/build_data.py
"""

import os
import re
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

# Force UTF-8 on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = Path(__file__).parent.parent          # D:\Projects\Rank_Rent_Flash_Engine
RAW  = BASE / "raw_research"
OUT  = BASE / "data.txt"


# =============================================================================
# SMART FILE MATCHING HELPERS
# =============================================================================

def find_file(patterns, exts=None):
    """Scan raw_research/ for first file matching any pattern substring."""
    if not RAW.exists():
        return None
    for p in RAW.iterdir():
        if p.is_file():
            nl = p.name.lower()
            if exts and not any(nl.endswith(e.lower()) for e in exts):
                continue
            if any(pat.lower() in nl for pat in patterns):
                return p
    return None


def read_txt(filepath, max_chars=30000):
    """Read a text file, return string truncated to max_chars."""
    if not filepath or not filepath.exists():
        return ""
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore").strip()
        return content[:max_chars]
    except Exception as e:
        print(f"  [WARN] Could not read {filepath.name}: {e}")
        return ""


def read_json(filepath):
    """Read a JSON file, return dict or empty dict."""
    if not filepath or not filepath.exists():
        return {}
    try:
        return json.loads(filepath.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"  [WARN] Could not read {filepath.name}: {e}")
        return {}


def section(title, lines):
    """Format a named section for data.txt output."""
    border = "=" * 70
    out = [border, f"  {title}", border, ""]
    if not lines:
        out.append("  [No data available for this section]")
    else:
        for line in lines:
            if line and str(line).strip():
                clean = str(line).replace("\n", " ").strip()
                out.append(f"  {clean}")
    out.append("")
    return "\n".join(out) + "\n"


def parse_csv_smart(filepath, prefer_keywords=None, max_rows=300):
    """
    Intelligently find the primary text/question/keyword column from a CSV.
    """
    if not filepath or not filepath.exists():
        return []

    lines = []
    try:
        with open(filepath, encoding="utf-8", errors="ignore") as f:
            reader = csv.reader(f)
            header = next(reader, [])
            col_idx = 0

            # Detect matching column by header names
            if prefer_keywords and header:
                for idx, h in enumerate(header):
                    hl = h.lower()
                    if any(pk.lower() in hl for pk in prefer_keywords):
                        col_idx = idx
                        break
            elif header:
                # Common defaults: 'keyword', 'question', 'query'
                for idx, h in enumerate(header):
                    hl = h.lower()
                    if any(k in hl for k in ["keyword", "question", "query", "term"]):
                        col_idx = idx
                        break

            for i, row in enumerate(reader):
                if i >= max_rows:
                    break
                if len(row) > col_idx and row[col_idx].strip():
                    val = row[col_idx].strip()
                    # Skip common CSV noise or headers repeated
                    if val.lower() not in ["select all keywords", "keyword", "question"]:
                        lines.append(val)
    except Exception as e:
        print(f"  [WARN] Could not parse CSV {filepath.name}: {e}")
    return lines


def parse_semrush_table(filepath, max_rows=500):
    """
    Extracts both questions and high-volume keywords from SEMrush Keyword Magic CSV.
    Returns (keywords_list, questions_list).
    """
    if not filepath or not filepath.exists():
        return [], []

    kws = []
    questions = []
    QUESTION_STARTERS = ("how", "what", "why", "where", "when", "can", "is", "does", "do", "should", "will", "are")
    NICHE_TERMS = {"duct", "vent", "air", "hvac", "heat", "ac", "furnace", "plenum", "clean", "dryer", "filter", "blower", "pipe", "odor", "mold", "dust", "allergy", "stanley"}

    try:
        with open(filepath, encoding="utf-8", errors="ignore") as f:
            reader = csv.reader(f)
            header = next(reader, [])
            kw_col = vol_col = kd_col = intent_col = None

            for i, h in enumerate(header):
                hl = h.lower()
                if "keyword" in hl and kw_col is None:
                    kw_col = i
                elif "volume" in hl or "vol" in hl:
                    vol_col = i
                elif "kd" in hl or "difficulty" in hl:
                    kd_col = i
                elif "intent" in hl:
                    intent_col = i

            kw_col = kw_col if kw_col is not None else 1 if len(header) > 1 else 0

            for i, row in enumerate(reader):
                if i >= max_rows:
                    break
                if len(row) > kw_col:
                    kw = row[kw_col].strip()
                    if not kw or kw.lower() == "keyword":
                        continue

                    kw_l = kw.lower()
                    # Filter out unrelated queries that don't match the niche
                    if not any(term in kw_l for term in NICHE_TERMS):
                        continue

                    vol = row[vol_col].strip() if vol_col is not None and len(row) > vol_col else ""
                    kd  = row[kd_col].strip() if kd_col is not None and len(row) > kd_col else ""
                    intent = row[intent_col].strip() if intent_col is not None and len(row) > intent_col else ""

                    entry = f"{kw}" + (f" (Vol: {vol}, KD: {kd})" if vol else "")

                    # Check if question
                    if "i" in intent.lower() or any(kw_l.startswith(s + " ") for s in QUESTION_STARTERS) or "?" in kw:
                        questions.append(entry)
                    else:
                        kws.append(entry)
    except Exception as e:
        print(f"  [WARN] SEMrush table error: {e}")

    return kws, questions


def parse_answerthepublic(filepath):
    """
    Extract queries from AnswerThePublic CSV or raw TXT dump.
    """
    if not filepath or not filepath.exists():
        return []

    if filepath.suffix.lower() == ".csv":
        return parse_csv_smart(filepath, prefer_keywords=["keyword", "query", "question"])

    # If TXT dump
    content = read_txt(filepath, max_chars=50000)
    lines = []
    # Ignore UI navigation noise
    UI_NOISE = {
        "answerthepublic", "search keywords", "pricing", "upgrade", "log in", "logout",
        "content studio", "dashboard", "suggested for you", "track changes", "top ideas",
        "export", "start a free trial", "generate content", "copy", "get ai response",
        "sentiment", "brands", "chatgpt", "gemini", "prompt", "intent", "overview",
        "keywords lists", "use cases", "create project", "keyword coverage", "content schedule",
        "all content", "settings", "hide menu", "increase daily limits", "unlock all",
        "watch tutorial", "send feedback", "community", "ai models", "search engines",
        "social media", "shopping", "united states", "search all", "neil:", "50% off",
        "view message", "access to", "showing", "alphabeticals", "organic searches",
        "trending keywords", "see what's breaking", "search interest", "search modifiers",
        "available searches", "fullscreen", "no results found", "instagram", "available on the",
        "products ranked for", "start free trial", "view 10 results", "view 1 results", "view 2 results",
        "view up to", "start a 7-day"
    }

    for raw_line in content.split("\n"):
        line = raw_line.strip()
        if len(line) < 8 or len(line) > 120:
            continue
        ll = line.lower()
        if any(noise in ll for noise in UI_NOISE):
            continue
        if re.match(r"^search volume\s+\d+", ll) or re.match(r"^cpc\s+", ll) or re.match(r"^updated\s+", ll):
            continue
        lines.append(line)

    # Deduplicate preserving order
    return list(dict.fromkeys(lines))


def parse_serp_data(filepath):
    """
    Extract competitor domains and snippets from SERP export or TXT dump.
    Returns (domains_list, snippets_list).
    """
    if not filepath or not filepath.exists():
        return [], []

    content = read_txt(filepath, max_chars=30000)
    # Extract domains
    raw_domains = re.findall(r"(?:https?://)?(?:www\.)?([a-z0-9\-]+\.(?:com|net|org|us|biz|co))", content, re.IGNORECASE)
    # Filter out common analytics or non-competitor domains
    EXCLUDE = {"google.com", "sbmm.com", "schema.org", "w3.org", "youtube.com", "notegpt.io", "semrush.com"}
    domains = [d.lower() for d in raw_domains if d.lower() not in EXCLUDE and len(d) > 6]
    domains = list(dict.fromkeys(domains))

    # Extract snippets / lines of substance
    snippets = []
    for line in content.split("\n"):
        clean = line.strip()
        if len(clean) > 25 and not clean.startswith("#") and not clean.startswith("http"):
            snippets.append(clean)

    return domains[:20], snippets[:30]


def categorize_research(raw_text):
    """
    Parse compiled_research.txt or research_data.txt and split into
    pain_points, forum_questions, trust_signals, objections.
    """
    buckets = {
        "pain_points": [],
        "forum_questions": [],
        "trust_signals": [],
        "objections": [],
        "uncategorized": [],
    }

    PAIN_WORDS  = {"scam","avoid","broken","issue","frustrat","terrible","never use",
                   "rip off","problem","complaint","horrible","worst","damage","leak",
                   "dirty","mold","dust","clog","smell","odor","allerg"}
    TRUST_WORDS = {"recommend","honest","reliable","professional","license","insured",
                   "certified","nadca","bbb","review","on time","trustworthy","verified"}
    OBJ_WORDS   = {"too expensive","diy","do it myself","worth it","wait","delay",
                   "not sure","skeptical","hesitant","unnecessary","overpriced"}

    blocks = re.split(r"\n{2,}|\[Source:", raw_text)
    seen = set()

    for block in blocks:
        text = block.strip()
        if len(text) < 40:
            continue
        key = text[:60]
        if key in seen:
            continue
        seen.add(key)

        text_l = text.lower()
        matched = False

        if "?" in text:
            q = re.search(r"([A-Z][^.?!]{10,}?\?)", text)
            if q:
                buckets["forum_questions"].append(q.group(1).strip())
                matched = True

        if any(w in text_l for w in PAIN_WORDS):
            buckets["pain_points"].append(text[:500])
            matched = True

        if any(w in text_l for w in TRUST_WORDS):
            buckets["trust_signals"].append(text[:500])
            matched = True

        if any(w in text_l for w in OBJ_WORDS):
            buckets["objections"].append(text[:500])
            matched = True

        if not matched:
            buckets["uncategorized"].append(text[:300])

    return buckets


# =============================================================================
# LOAD MASTER BRIEF (for project identity)
# =============================================================================

brief = read_json(BASE / "master_brief.json")
niche   = brief.get("niche", "Air Duct Cleaning")
city    = brief.get("city", "Rockford")
state   = brief.get("state", "IL")
company = brief.get("nap", {}).get("company_name", "Rockford Air Duct Pros")
phone   = brief.get("nap", {}).get("phone", "(815) 555-0142")
address = brief.get("nap", {}).get("address", "1111 S Alpine Rd, Rockford, IL 61108")
email   = brief.get("nap", {}).get("email", "service@rockfordairductpros.com")
website = brief.get("nap", {}).get("website", "https://rockfordairductpros.com")
founded = brief.get("founded_year", "2014")
primary_kw = brief.get("primary_keyword", "air duct cleaning rockford il")
secondary_kws = brief.get("secondary_keywords", [])
services_list = brief.get("services", [])
sub_services  = brief.get("sub_services", [])
expansion_cities = brief.get("expansion_cities", [])
neighborhoods    = brief.get("neighborhoods", [])
competitors_brief = brief.get("differentiation_angles", [])
pain_brief = brief.get("pain_points", [])
credentials = brief.get("credentials", [])
local_challenge = brief.get("local_challenge", "")
local_landmarks = brief.get("local_landmarks", [])

print("=" * 70)
print("  BUILD_DATA.PY — ADAPTIVE RESEARCH COMPILER")
print(f"  Niche  : {niche}")
print(f"  City   : {city}, {state}")
print(f"  Output : {OUT}")
print("=" * 70)


# =============================================================================
# DETECT RESEARCH FILES IN raw_research/
# =============================================================================

alsoasked_file = find_file(["alsoasked", "paa", "people_also_ask"], exts=[".csv", ".txt"])
semrush_table  = find_file(["table", "semrush", "magic", "questions"], exts=[".csv"])
answerthepublic_file = find_file(["answerthepublic", "atp"], exts=[".csv", ".txt"])
serp_file      = find_file(["serp", "snippet", "sbmm"], exts=[".csv", ".txt"])
topical_file   = find_file(["topical", "relevance"], exts=[".txt", ".csv"])
youtube_file   = find_file(["youtube", "transcript"], exts=[".txt"])
forum_file     = find_file(["compiled", "research", "forum"], exts=[".txt"])

print("\n  [SCANNING raw_research/ — Detected Files]:")
print(f"  ✓ PAA / AlsoAsked    : {alsoasked_file.name if alsoasked_file else '[None found]'}")
print(f"  ✓ SEMrush Table      : {semrush_table.name if semrush_table else '[None found]'}")
print(f"  ✓ AnswerThePublic    : {answerthepublic_file.name if answerthepublic_file else '[None found]'}")
print(f"  ✓ SERP / Competitors : {serp_file.name if serp_file else '[None found]'}")
print(f"  ✓ Topical Relevance  : {topical_file.name if topical_file else '[None found]'}")
print(f"  ✓ YouTube File       : {youtube_file.name if youtube_file else '[None found]'}")
print()


# =============================================================================
# SECTION 1 — PROJECT INFO
# =============================================================================

project_info = [
    f"Niche           : {niche}",
    f"Primary Service : {brief.get('primary_service', niche)}",
    f"City            : {city}",
    f"State           : {state}",
    f"Company Name    : {company}",
    f"Address         : {address}",
    f"Phone           : {phone}",
    f"Email           : {email}",
    f"Website         : {website}",
    f"Founded Year    : {founded}",
    f"Date Compiled   : {datetime.now().strftime('%Y-%m-%d')}",
    f"Primary Keyword : {primary_kw}",
]


# =============================================================================
# SECTION 2 — TARGET KEYWORDS
# =============================================================================

ahrefs_kws = []
ahrefs_path = BASE / "ahrefs_keywords.csv"
if ahrefs_path.exists():
    try:
        with open(ahrefs_path, encoding="utf-8", errors="ignore") as f:
            reader = csv.reader(f)
            header = next(reader, [])
            kw_col = vol_col = kd_col = 0
            for i, h in enumerate(header):
                hl = h.lower()
                if "keyword" in hl: kw_col = i
                if "volume" in hl or "vol" in hl: vol_col = i
                if "difficulty" in hl or "kd" in hl: kd_col = i
            for row in reader:
                if len(row) > max(kw_col, vol_col):
                    kw = row[kw_col].strip()
                    if not kw or kw.lower() == "keyword":
                        continue
                    vol = row[vol_col].strip() if vol_col < len(row) else "?"
                    kd = row[kd_col].strip() if kd_col < len(row) else "?"
                    ahrefs_kws.append(f"{kw} — Vol:{vol}/mo KD:{kd}")
    except Exception as e:
        print(f"  [WARN] ahrefs_keywords.csv parse error: {e}")

semrush_kws, semrush_table_questions = parse_semrush_table(semrush_table, max_rows=500)
all_keywords = list(dict.fromkeys(ahrefs_kws[:40] + semrush_kws[:40] + [primary_kw] + secondary_kws))
print(f"  [S2] Keywords — {len(all_keywords)} total loaded")


# =============================================================================
# SECTION 3 — PEOPLE ALSO ASK (PAA)
# =============================================================================

paa_items = []
if alsoasked_file:
    paa_items.extend(parse_csv_smart(alsoasked_file, prefer_keywords=["question"]))

# Combine with SEMrush questions
paa_combined = list(dict.fromkeys([q.strip() for q in (paa_items + semrush_table_questions) if len(q.strip()) > 8]))
print(f"  [S3] PAA & Questions — {len(paa_combined)} questions loaded")


# =============================================================================
# SECTION 4 & 16 — CONTENT IDEAS (AnswerThePublic)
# =============================================================================

atp_rows = parse_answerthepublic(answerthepublic_file)
print(f"  [S4/S16] AnswerThePublic Content Ideas — {len(atp_rows)} items loaded")


# =============================================================================
# SECTION 5, 6, 7, 11, 12, 15 — Forum Research
# =============================================================================

compiled_text = read_txt(forum_file) or read_txt(BASE / "research_data.txt")
buckets = categorize_research(compiled_text)
all_pain_points = list(dict.fromkeys(pain_brief + buckets["pain_points"]))
print(f"  [S5-S15] Forum & Sentiment — {len(all_pain_points)} pain points, {len(buckets['trust_signals'])} trust signals")


# =============================================================================
# SECTION 8 & 13 — SERP SNIPPETS & COMPETITORS
# =============================================================================

serp_domains, serp_snippets = parse_serp_data(serp_file)
all_competitors = list(dict.fromkeys(serp_domains + [f"From brief: {a}" for a in competitors_brief[:5]]))
print(f"  [S8/S13] Competitors & SERP — {len(all_competitors)} competitors, {len(serp_snippets)} SERP snippets")


# =============================================================================
# SECTION 17 — TOPICAL RELEVANCE
# =============================================================================

topical_raw = read_txt(topical_file)
topical_frequency = topical_relevance = topical_schema = ""
if topical_raw:
    freq_m = re.search(r"Frequency\s*\n(.+?)(?:\n\n|\Z)", topical_raw, re.DOTALL)
    rel_m  = re.search(r"Relevance\s*\n(.+?)(?:\n\n|\Z)", topical_raw, re.DOTALL)
    schema_m = re.search(r'(<script type="application/ld\+json">.*?</script>)', topical_raw, re.DOTALL)
    if freq_m:   topical_frequency = freq_m.group(1).strip()
    if rel_m:    topical_relevance  = rel_m.group(1).strip()
    if schema_m: topical_schema     = schema_m.group(1).strip()
print(f"  [S17] Topical Relevance — {'Found' if topical_raw else 'None'}")


# =============================================================================
# SECTION 18 — YOUTUBE TRANSCRIPT OR URLS
# =============================================================================

youtube_content = read_txt(youtube_file)
print(f"  [S18] YouTube Content — {'Found (' + str(len(youtube_content)) + ' chars)' if youtube_content else 'None'}")


# =============================================================================
# ASSEMBLE data.txt
# =============================================================================

output_parts = [
    "=" * 70,
    "  RANK & RENT RESEARCH DATA — MASTER FILE",
    f"  Niche   : {niche}",
    f"  City    : {city}, {state}",
    f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
    "=" * 70,
    "",
]

output_parts.append(section("SECTION 1 — PROJECT INFO", project_info))
output_parts.append(section("SECTION 2 — TARGET KEYWORDS (Ahrefs + SEMrush)", all_keywords or [f"primary keyword: {primary_kw}"]))
output_parts.append(section("SECTION 3 — PEOPLE ALSO ASK (PAA QUESTIONS)", paa_combined[:150]))
output_parts.append(section("SECTION 4 — CONTENT IDEAS (AnswerThePublic)", atp_rows[:80]))
output_parts.append(section("SECTION 5 — CUSTOMER PAIN POINTS", all_pain_points[:30]))
output_parts.append(section("SECTION 6 — CUSTOMER QUESTIONS FROM FORUMS", (buckets["forum_questions"] + paa_combined[:20])[:30]))
output_parts.append(section("SECTION 7 — PRICING SIGNALS (note: no pricing on site)", [
    "NOTE: Captured competitor pricing signals for research only.",
    "RULE: Never include pricing on any page of this Rank & Rent site.",
]))
output_parts.append(section("SECTION 8 — COMPETITOR NAMES & DOMAINS", all_competitors))
output_parts.append(section("SECTION 9 — SERVICES IN THIS NICHE", services_list + sub_services))
output_parts.append(section("SECTION 10 — LOCAL CONTEXT", [
    f"City: {city}, {state}",
    f"Local challenge: {local_challenge}",
] + [f"Landmark: {lm}" for lm in local_landmarks]
  + [f"Neighborhood: {n}" for n in neighborhoods]
  + [f"Expansion city: {ec}" for ec in expansion_cities]))
output_parts.append(section("SECTION 11 — TRUST SIGNALS & DECISION FACTORS",
    buckets["trust_signals"][:20] + [f"Credential: {c}" for c in credentials]))
output_parts.append(section("SECTION 12 — OBJECTIONS", buckets["objections"][:15]))
output_parts.append(section("SECTION 13 — GOOGLE SERP SNIPPETS", serp_snippets))
output_parts.append(section("SECTION 14 — YOUTUBE TRANSCRIPT NOTES", [
    f"Video Source: {line.strip()}" if line.strip().startswith("http") else line.strip()
    for line in youtube_content.split("\n") if len(line.strip()) > 10
][:20] if youtube_content else ["[No transcript notes]"]))
output_parts.append(section("SECTION 15 — UNCATEGORIZED FORUM DATA", buckets["uncategorized"][:20]))
output_parts.append(section("SECTION 16 — ANSWERTHEPUBLIC KEYWORD VARIATIONS", atp_rows[:150]))

# Section 17
output_parts += [
    "=" * 70,
    "  SECTION 17 — TOPICAL RELEVANCE (Semantic Keywords & Schema)",
    "=" * 70,
    "",
    "  FREQUENCY ENTITIES:",
    f"  {topical_frequency or '[None]'}",
    "",
    "  RELEVANCE ENTITIES:",
    f"  {topical_relevance or '[None]'}",
    "",
    "  SCHEMA MARKUP:",
    topical_schema or "  [None]",
    "\n",
]

# Section 18
formatted_yt = "\n".join(
    f"Video Reference: {l.strip()}" if l.strip().startswith("http") else l
    for l in (youtube_content or "[No transcript]").split("\n")
)
output_parts += [
    "=" * 70,
    "  SECTION 18 — FULL YOUTUBE COMPETITOR TRANSCRIPT / NOTES",
    "=" * 70,
    "",
    formatted_yt,
    "\n",
    "=" * 70 + "\n  END OF DATA FILE\n" + "=" * 70
]

final = "\n".join(output_parts)
OUT.write_text(final, encoding="utf-8")

word_count = len(final.split())
print("=" * 70)
print(f"  SUCCESS: data.txt written ({len(final):,} chars / ~{word_count:,} words)")
print(f"  Path: {OUT}")
print("=" * 70)
