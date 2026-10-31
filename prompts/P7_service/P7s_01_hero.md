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
<!-- PASTE YOUR CLAUDE/PRO OUTPUT FOR THIS SECTION HERE -->
<!-- Until filled: Flash will follow the rules above without an example -->
<!-- Priority: fill this before Nov 2 while Claude access is available -->

## OUTPUT RULES
- Output ONLY the section content in Markdown
- Start directly with the content — no intro, no "Here is the section:" preamble
- No pricing, no em-dashes (—), no separator lines (---)
- Bold ONE key phrase per paragraph
