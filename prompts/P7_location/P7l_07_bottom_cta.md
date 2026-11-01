# P7 Location — Section 07: Bottom CTA
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

## SECTION RULES — Bottom CTA (Section 7 of 7)
Word budget: ≤60 words HARD LIMIT

H2: Serving {LOCATION_CITY} — Call for a Free Estimate Today

Write:
1. Availability statement (20-30 words) mentioning {LOCATION_CITY}
2. CTA: "Call {PHONE}"
3. Trust micro-copy: "Licensed • Insured • Serving {LOCATION_CITY} and Surrounding Areas"

SELF-CHECK:
- [ ] H2 = "Serving {LOCATION_CITY} — Call for a Free Estimate Today"
- [ ] {LOCATION_CITY} mentioned in body
- [ ] Total ≤ 60 words
- [ ] No pricing

## GOLDEN EXAMPLE
<!-- Golden example generated from: location_page_example.md -->
<!-- Section 07 — injected by inject_golden_examples.py -->

## Serving Loves Park - Call for a Free Estimate Today

**NADCA-certified air duct cleaning is available throughout Loves Park** with the same team and equipment that Rockford homeowners have trusted since 2014.

**Call (815) 555-0142**

Licensed * Insured * Serving Loves Park and Surrounding Areas

## OUTPUT RULES
- Output ONLY the section content in Markdown
- Start directly with the content — no intro, no preamble
- No pricing, no em-dashes (—), no separator lines (---)
- Bold ONE key phrase per paragraph
- Short paragraphs: 2-3 sentences max
