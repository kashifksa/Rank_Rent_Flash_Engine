# P4 — Generate master_brief.json
# Flash Engine | Output: master_brief.json (SINGLE SOURCE OF TRUTH)
# Input: data.txt (Argon Browser Bridge) OR data_brief.txt (Small Context Fallback)

## WORKFLOW MODES:

### Option A: Gemini Browser Bridge (Argon / Gemini Advanced) — RECOMMENDED
Gemini Argon in Chrome has a 1M+ token context window. It accepts the FULL, rich 18-section `data.txt` directly without losing any research data!
Run:
  python scripts/gemini_browser_bridge.py --task brief
It feeds `data.txt` directly into Argon, extracts everything into `master_brief.json`, and saves it automatically.

### Option B: Small-Context Fallback (Flash 3.8)
If pasting manually into a small-context window:
  python scripts/data_extractor.py
Paste `data_brief.txt` into the input block below.

## INPUT DATA
=== RESEARCH DATA ===
[paste full data.txt OR data_brief.txt content here]
=== END ===

## TASK
Convert the structured brief above into master_brief.json.
Do NOT invent values not present in the brief.
For any missing field: use an empty string "" or empty array [].

## OUTPUT FORMAT
Output ONLY valid JSON. No markdown fences. No explanation.

{
  "project_name": "",
  "niche": "",
  "primary_service": "",
  "city": "",
  "state": "",
  "nap": {
    "company_name": "",
    "address": "",
    "phone": "",
    "email": "",
    "website": ""
  },
  "founded_year": "",
  "primary_keyword": "",
  "secondary_keywords": [],
  "services": [],
  "sub_services": [],
  "expansion_cities": [],
  "neighborhoods": [],
  "local_challenge": "",
  "local_landmarks": [],
  "credentials": [],
  "community_ties": [],
  "social_profiles": {
    "google_business_profile": "",
    "facebook": "",
    "bbb": "",
    "yelp": ""
  },
  "tone": {
    "voice": "",
    "style": "",
    "avoid": ["em-dashes", "pricing", "superlatives without evidence"]
  },
  "pain_points": [],
  "monetization_model": "rank_and_rent",
  "phase": 1
}

## SELF-CHECK before outputting
- [ ] Output is valid JSON — no trailing commas, all strings quoted
- [ ] No pricing in any field
- [ ] nap block complete — all 5 fields present (empty string if unknown)
- [ ] services and sub_services arrays populated from brief
- [ ] tone block complete
- [ ] monetization_model = "rank_and_rent" (always)
- [ ] No invented data — only what was in data_brief.txt
