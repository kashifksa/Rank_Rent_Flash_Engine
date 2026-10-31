import os
import re
import csv
import zipfile

# ── Paths ──
DIR = r"C:\xampp\htdocs\ccbismarck\SprinklerRepairDenton"
COMPILED_RESEARCH = r"C:\xampp\htdocs\ccbismarck\compiled_research_data.txt"
DATA_TXT = r"C:\xampp\htdocs\ccbismarck\data.txt"

# ── Helpers ──
def read_csv_col(filepath, col_index=0, skip_header=True):
    lines = []
    if not os.path.exists(filepath): return lines
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        if skip_header:
            next(reader, None)
        for row in reader:
            if len(row) > col_index:
                lines.append(row[col_index].strip())
    return [l for l in lines if l]

def extract_excel_strings(filepath):
    if not os.path.exists(filepath): return []
    try:
        with zipfile.ZipFile(filepath, 'r') as z:
            if 'xl/sharedStrings.xml' in z.namelist():
                xml = z.read('xl/sharedStrings.xml').decode('utf-8')
                return re.findall(r'<t.*?>(.*?)</t>', xml)
    except Exception:
        pass
    return []

# ── Data Extraction ──

# S1: Info
project_info = [
    "Niche          : Sprinkler Repair",
    "City           : Denton",
    "State          : TX",
    "Full Keyword   : Sprinkler Repair Denton TX",
    "Website URL    : [To Be Determined]",
    "Date Researched: 2026-07-22"
]

# S2: Target Keywords (from Semrush)
kws = read_csv_col(os.path.join(DIR, "sprinkler repair denton-semrush.csv"), col_index=1)
vols = read_csv_col(os.path.join(DIR, "sprinkler repair denton-semrush.csv"), col_index=5)
target_keywords = [f"{k} — {v}/mo" for k, v in zip(kws, vols)][:25]

# S3: PAA Questions — All 413 from Semrush + PAA export
paa_semrush = read_csv_col(os.path.join(DIR, "sprinkler repair-semrushquestions-413.csv"), col_index=1)
paa_export = read_csv_col(os.path.join(DIR, "paas_export_sprinkler repair denton.csv"), col_index=0, skip_header=False)
paa = list(dict.fromkeys([q.strip() for q in paa_semrush + paa_export if len(q.strip()) > 10]))  # deduplicated

# S4: Content Ideas / S8: Competitors (from Topic Research Excel)
excel_strings = extract_excel_strings(os.path.join(DIR, "topic-research-semrush.xls"))
competitors = set()
content_ideas = set()
for s in excel_strings:
    if '.com' in s or '.net' in s or '.org' in s:
        domain = re.sub(r'https?://(www\.)?', '', s).split('/')[0]
        competitors.add(domain)
    elif len(s) > 15 and ('How' in s or 'What' in s or 'Best' in s or 'Top' in s or 'Repair' in s):
        content_ideas.add(s)

competitors = list(competitors)
content_ideas = list(content_ideas)

# S13: SERP Snippets
serp = read_csv_col(os.path.join(DIR, "SERP_Results.csv"), col_index=3)
if not serp: serp = read_csv_col(os.path.join(DIR, "SERP_Results.csv"), col_index=2)
serp = list(set([s for s in serp if len(s) > 40]))

# S16: AnswerThePublic — all_categories CSV (2,890 keyword variations)
atp_rows = []
atp_path = os.path.join(DIR, "all_categories-sprinkler_repair-en-us-19-07-2026.csv")
if os.path.exists(atp_path):
    with open(atp_path, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header
        for row in reader:
            if len(row) >= 9 and row[5].strip():  # col 5 = Keyword, col 8 = Search Vol
                kw = row[5].strip()
                vol = row[8].strip()
                mod_type = row[3].strip()  # col 3 = Modifier Type
                atp_rows.append(f"{kw} [{mod_type}] — {vol}/mo")
atp_keywords = list(dict.fromkeys(atp_rows))  # deduplicated

# S17: Topical Relevance data
topical_frequency = ""
topical_relevance = ""
topical_schema = ""
topical_path = os.path.join(DIR, "topicalrelvance.txt")
if os.path.exists(topical_path):
    with open(topical_path, 'r', encoding='utf-8', errors='ignore') as f:
        topical_raw = f.read()
    freq_match = re.search(r'Frequency\n(.+?)\n', topical_raw)
    rel_match = re.search(r'Relevance\n(.+?)\n', topical_raw)
    schema_match = re.search(r'(<script type="application/ld\+json">.*?</script>)', topical_raw, re.DOTALL)
    if freq_match: topical_frequency = freq_match.group(1).strip()
    if rel_match: topical_relevance = rel_match.group(1).strip()
    if schema_match: topical_schema = schema_match.group(1).strip()

# S18: Full YouTube Transcript
youtube_transcript = ""
t_path2 = os.path.join(DIR, "NoteGPT_Transcript_The Best Sprinkler Repair in DFW - Sprinkler Repair of Texas.txt")
if os.path.exists(t_path2):
    with open(t_path2, 'r', encoding='utf-8', errors='ignore') as f:
        youtube_transcript = f.read().strip()

# Process Compiled Research (S5, S6, S7, S11, S12)
pain_points = []
forum_qs = []
pricing = []
trust = []
objections = []
uncategorized = []

with open(COMPILED_RESEARCH, 'r', encoding='utf-8') as f:
    compiled_text = f.read()

blocks = compiled_text.split('--- [Source:')
for b in blocks[1:]:
    text = b.split('] ---')[-1].strip()
    text_lower = text.lower()
    
    matched = False
    
    # Heuristics
    if '$' in text or 'cost' in text_lower or 'price' in text_lower or 'pay' in text_lower or 'quote' in text_lower:
        pricing.append(text.replace('\n', '  '))
        matched = True
    
    if '?' in text:
        q_match = re.search(r'([A-Z][^.?!]*\?)', text)
        if q_match:
            forum_qs.append(q_match.group(1))
            matched = True
            
    if 'scam' in text_lower or 'avoid' in text_lower or 'broken' in text_lower or 'leak' in text_lower or 'issue' in text_lower or 'frustrat' in text_lower or 'terrible' in text_lower or 'never use' in text_lower or 'rip off' in text_lower:
        pain_points.append(text.replace('\n', '  '))
        matched = True
        
    if 'recommend' in text_lower or 'honest' in text_lower or 'reliable' in text_lower or 'professional' in text_lower or 'license' in text_lower or 'insured' in text_lower or 'reviews' in text_lower or 'on time' in text_lower:
        trust.append(text.replace('\n', '  '))
        matched = True
        
    if 'too expensive' in text_lower or 'diy' in text_lower or 'do it myself' in text_lower or 'worth it' in text_lower or 'wait' in text_lower or 'delay' in text_lower:
        objections.append(text.replace('\n', '  '))
        matched = True
        
    if not matched:
        uncategorized.append(text.replace('\n', '  '))

# Filter & sample
import random
random.shuffle(pain_points)
random.shuffle(pricing)
random.shuffle(trust)
random.shuffle(objections)
random.shuffle(uncategorized)

pain_points = list(set(pain_points))
forum_qs = list(set(forum_qs))
pricing = list(set(pricing))
trust = list(set(trust))
objections = list(set(objections))
uncategorized = list(set(uncategorized))

# S9 & S14: Transcript processing
services = [
    "Sprinkler Head Replacement & Adjustment",
    "Leak Detection and Pipe Repair",
    "Zone Valve Repair and Replacement",
    "Controller / Timer Programming & Replacement",
    "System Diagnostics and Tune-ups",
    "Wire Tracking and Electrical Troubleshooting",
    "Rain Sensor Installation",
    "Drip Irrigation Repair"
]

transcript_notes = []
t_path = os.path.join(DIR, "NoteGPT_Transcript_The Best Sprinkler Repair in DFW - Sprinkler Repair of Texas.txt")
if os.path.exists(t_path):
    with open(t_path, 'r', encoding='utf-8', errors='ignore') as f:
        t_text = f.read()
        sentences = re.split(r'(?<=[.!?]) +', t_text)
        for s in sentences:
            if 'we do' in s.lower() or 'offer' in s.lower() or 'specialize' in s.lower() or 'call us' in s.lower():
                transcript_notes.append(s.strip())
transcript_notes = list(set(transcript_notes))[:10]

local_context = [
    "Denton TX has hot dry summers — high demand June through September",
    "Texas requires backflow preventer testing annually by a licensed plumber",
    "Clay soil in Denton area causes more pipe shifting and breaks",
    "Many homes in Denton built in the 1990s and 2000s have aging sprinkler systems now needing repair",
    "Water conservation restrictions in Denton require efficient systems and smart controllers"
]

# ── Generate Output ──
def format_section(title, lines):
    border = "=" * 70
    out = [border, f"  {title}", border, ""]
    if not lines:
        out.append("  [No data available]")
    else:
        for l in lines:
            out.append(f"  {l}")
    out.append("\n")
    return "\n".join(out)

output = [
    "=" * 70,
    "  RANK & RENT RESEARCH DATA — MASTER FILE",
    "  Generated from all Scraper & Semrush sources",
    "=" * 70,
    ""
]

output.append(format_section("SECTION 1 — PROJECT INFO", project_info))
output.append(format_section("SECTION 2 — TARGET KEYWORDS", target_keywords))
output.append(format_section("SECTION 3 — PEOPLE ALSO ASK (PAA QUESTIONS)", paa))
output.append(format_section("SECTION 4 — CONTENT IDEAS", content_ideas))
output.append(format_section("SECTION 5 — CUSTOMER PAIN POINTS", pain_points))
output.append(format_section("SECTION 6 — CUSTOMER QUESTIONS FROM FORUMS", forum_qs))
output.append(format_section("SECTION 7 — PRICING DATA", pricing))
output.append(format_section("SECTION 8 — COMPETITOR NAMES", competitors))
output.append(format_section("SECTION 9 — SERVICES IN THIS NICHE", services))
output.append(format_section("SECTION 10 — LOCAL CONTEXT", local_context))
output.append(format_section("SECTION 11 — TRUST SIGNALS & DECISION FACTORS", trust))
output.append(format_section("SECTION 12 — OBJECTIONS", objections))
output.append(format_section("SECTION 13 — GOOGLE SERP SNIPPETS", serp))
output.append(format_section("SECTION 14 — ADDITIONAL NOTES (From YouTube Transcript)", transcript_notes))
output.append(format_section("SECTION 15 — UNCATEGORIZED FORUM DATA", uncategorized))
output.append(format_section("SECTION 16 — ANSWERTHEPUBLIC KEYWORD VARIATIONS (2890 rows)", atp_keywords))

# Section 17 — Topical Relevance
output.append("=" * 70)
output.append("  SECTION 17 — TOPICAL RELEVANCE (Semantic Keywords & Schema)")
output.append("=" * 70)
output.append("")
output.append("  Recommended Word Count: ~1156 words")
output.append("")
output.append("  FREQUENCY ENTITIES (use often throughout the page):")
output.append(f"  {topical_frequency}")
output.append("")
output.append("  RELEVANCE ENTITIES (confidence score — more specific):")
output.append(f"  {topical_relevance}")
output.append("")
output.append("  SCHEMA MARKUP (ready to paste — replace headline and URL):")
output.append(topical_schema)
output.append("\n")

# Section 18 — Full YouTube Transcript
output.append("=" * 70)
output.append("  SECTION 18 — FULL YOUTUBE COMPETITOR TRANSCRIPT")
output.append("  Source: NoteGPT — The Best Sprinkler Repair in DFW")
output.append("=" * 70)
output.append("")
output.append(youtube_transcript)
output.append("\n")

output.append("=" * 70 + "\n  END OF DATA FILE\n" + "=" * 70)

with open(DATA_TXT, 'w', encoding='utf-8') as f:
    f.write("\n".join(output))

print("data.txt has been generated successfully!")
