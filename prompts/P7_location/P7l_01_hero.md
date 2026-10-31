# P7 Location — Section 01: Hero
# Flash Engine — Location Page | Atomic Mini-Prompt
# Model: Gemini Flash 3.8
# Write ONLY this section. Nothing else.

## VARIABLES — fill ALL before submitting
PRIMARY_SERVICE  = [fill in]
LOCATION_CITY    = [fill in — the TARGET city for this page]
HUB_CITY         = [fill in — your main operating city]
STATE            = [fill in]
PHONE            = [fill in]
LOCAL_LANDMARKS  = [fill in — real verifiable landmarks in LOCATION_CITY]
LOCAL_CLIMATE    = [fill in — climate/geographic factor relevant to service]
LOCAL_PERMIT     = [fill in — any permit note for LOCATION_CITY, or leave blank]
LOCAL_NEIGHBORHOODS = [fill in — neighborhoods/zips in LOCATION_CITY]

## SECTION RULES — Hero (Section 1 of 7)
Word budget: HARD LIMIT ≤120 words total

Write in this order:

1. H1: {PRIMARY_SERVICE} in {LOCATION_CITY}, {STATE}

2. SNIPPET ZONE (40-60 words, standalone paragraph):
   - What service, who it is for, in {LOCATION_CITY} specifically
   - Mention {LOCATION_CITY} — NOT {HUB_CITY}
   - Self-contained for AI Overview extraction

3. SUBHEADLINE (≤50 words):
   - Reference {LOCATION_CITY} specifically, not the hub city
   - Mention {LOCAL_CLIMATE} if relevant

4. CTA: "Call {PHONE}" + "Get a Free Estimate"

SELF-CHECK:
- [ ] H1 = {PRIMARY_SERVICE} in {LOCATION_CITY}, {STATE}
- [ ] Snippet zone is 40-60 words, mentions {LOCATION_CITY}
- [ ] Total ≤ 120 words
- [ ] No pricing

## GOLDEN EXAMPLE
<!-- PASTE YOUR CLAUDE/PRO OUTPUT FOR THIS SECTION HERE -->
<!-- Until filled: Flash will follow the rules above without an example -->

## OUTPUT RULES
- Output ONLY the section content in Markdown
- Start directly with the content — no intro, no preamble
- No pricing, no em-dashes (—), no separator lines (---)
- Bold ONE key phrase per paragraph
- Short paragraphs: 2-3 sentences max
