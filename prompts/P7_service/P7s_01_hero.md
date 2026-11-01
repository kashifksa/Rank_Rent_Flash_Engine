# P7 Service — Section 01: Hero
# Flash Engine — Service Page | Atomic Mini-Prompt
# Model: Gemini Flash 3.8
# Write ONLY this section. Nothing else.

## VARIABLES — fill ALL before submitting
PRIMARY_SERVICE = [fill in]
CITY            = [fill in]
STATE           = [fill in]
COMPANY_NAME    = [fill in]
PHONE           = [fill in]
LOCAL_CHALLENGE = [fill in — e.g. "Austin's intense hail storms"]

## SECTION RULES — Hero (Section 1 of 10)
Word budget: HARD LIMIT ≤120 words total (H1 + snippet zone + subheadline + CTA text)

Write in this exact order:

1. H1: {PRIMARY_SERVICE} in {CITY}, {STATE}

2. SNIPPET ZONE (40-60 words, standalone paragraph):
   - Directly answer: what is this service, who is it for, what area does it cover
   - Self-contained — no "We offer..." opener
   - This is the Featured Snippet / AI Overview capture target

3. SUBHEADLINE (≤50 words):
   - One sentence benefit statement referencing {LOCAL_CHALLENGE}
   - Must mention {CITY}

4. CTA TEXT (≤15 words):
   - Click-to-call: "Call {PHONE}"
   - Secondary anchor: "Get a Free Quote"

SELF-CHECK before outputting:
- [ ] H1 contains PRIMARY_SERVICE + CITY + STATE
- [ ] Snippet zone is 40-60 words, standalone paragraph
- [ ] Total word count ≤ 120
- [ ] No pricing anywhere
- [ ] No em-dashes

## GOLDEN EXAMPLE
<!-- Golden example generated from: service_page_example.md -->
<!-- Section 01 — injected by inject_golden_examples.py -->

# Residential Air Duct Cleaning in Rockford, IL

**Professional air duct cleaning in Rockford, IL** removes accumulated dust, allergens, and contaminants from your home's supply and return ductwork using NADCA-certified technicians and commercial-grade negative air pressure equipment. This service is designed for Rockford homeowners in single-family homes, condos, and multi-family units across Winnebago County.

Rockford's predominantly pre-1985 housing stock means most local homes have original galvanized sheet metal ducts that have never been professionally cleaned. Our NADCA-certified team brings the right equipment and training to restore airflow and indoor air quality in older Rockford homes.

**Call (815) 555-0142**
[Get a Free Quote](#mid-cta)

## OUTPUT RULES
- Output ONLY the section content in Markdown
- Start directly with the content — no intro, no "Here is the section:" preamble
- No pricing, no em-dashes (—), no separator lines (---)
- Bold ONE key phrase per paragraph
