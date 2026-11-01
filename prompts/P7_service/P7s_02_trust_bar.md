# P7 Service — Section 02: Trust Bar
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

## SECTION RULES — Trust Bar (Section 2 of 10)
Word budget: ≤40 words total across all badges
NO H2 — this is a decorative trust bar only

Write exactly 4 trust badges as a simple list:
- [Star rating] e.g. "4.9★ Rated on Google"
- [Licensed & Insured] e.g. "Licensed & Insured in {STATE}"
- [Years in business] e.g. "Serving {CITY} Since [Year from master_brief]"
- [Guarantee] e.g. "100% Satisfaction Guarantee"

Each badge: 4-7 words. No sentences. No punctuation at end.

SELF-CHECK before outputting:
- [ ] Exactly 4 badges
- [ ] Total ≤ 40 words
- [ ] No H2 heading
- [ ] No pricing

## GOLDEN EXAMPLE
<!-- Golden example generated from: service_page_example.md -->
<!-- Section 02 — injected by inject_golden_examples.py -->

- **4.9 Stars** Rated on Google
- **Licensed and Insured** in Illinois
- **Serving Rockford Since 2014**
- **100% Satisfaction Guarantee**

## OUTPUT RULES
- Output ONLY the section content in Markdown
- Start directly with the content — no intro, no "Here is the section:" preamble
- No pricing, no em-dashes (—), no separator lines (---)
- Bold ONE key phrase per paragraph
