# P4 — Generate master_brief.json
# Flash Engine | Output: master_brief.json (SINGLE SOURCE OF TRUTH)
# IMPORTANT: Use json.dumps() style output — no Python f-strings

## TASK
Using data.txt and the market/competitor reports, generate the complete
master_brief.json. This file drives every subsequent step in the pipeline.

## INPUTS REQUIRED
Paste the following before submitting:
=== DATA.TXT CONTENT ===
[paste full data.txt here]

=== MARKET INTELLIGENCE ===
[paste market_intelligence.json here]

=== COMPETITOR INTELLIGENCE ===
[paste competitor_intelligence.json here]

## OUTPUT FORMAT
Output ONLY valid JSON. No markdown fences, no explanation.
Structure must include ALL of these top-level keys:

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
  "social_profiles": {},
  "tone": {
    "voice": "",
    "style": "",
    "avoid": []
  },
  "monetization_model": "rank_and_rent",
  "phase": 1
}

## SELF-CHECK before outputting
- [ ] Output is valid JSON — test mentally for syntax errors
- [ ] No pricing in any field
- [ ] nap block is complete — all 5 fields filled
- [ ] services and sub_services arrays are non-empty
- [ ] tone block is complete
