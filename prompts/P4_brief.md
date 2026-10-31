# P4 — Generate master_brief.json
# Flash Engine | Output: master_brief.json (SINGLE SOURCE OF TRUTH)
# Input: data_brief.txt (NOT raw data.txt — run data_extractor.py first)

## WHY data_brief.txt (NOT data.txt)
Raw data.txt is 5,000-15,000 words of scraped content.
Flash 3.8 cannot reliably process it. Even Gemini Pro sometimes fails.
data_extractor.py compresses it to ~500-800 words of structured key:value pairs.
Flash converts a 500-word brief into JSON perfectly.

## PRE-CHECK (run before submitting this prompt)
  python scripts/data_extractor.py
  → Review data_brief.txt
  → Fill any [fill in] fields manually
  → THEN paste data_brief.txt below

## INPUT — paste data_brief.txt content here
=== DATA_BRIEF.TXT ===
[paste full data_brief.txt content here]
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
