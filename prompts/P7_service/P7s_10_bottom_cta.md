# P7 Service — Section 10: Bottom CTA
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

## SECTION RULES — Bottom CTA (Section 10 of 10)
Word budget: ≤60 words HARD LIMIT

H2: Ready for Professional {PRIMARY_SERVICE} in {CITY}?

Write:
1. Value recap (15-25 words): One sentence summarizing core value. Bold the key term.
2. CTA button text: "Call {PHONE}"
3. Trust micro-copy (≤10 words): "Licensed • Insured • {CITY}'s Trusted {PRIMARY_SERVICE} Team"

SELF-CHECK before outputting:
- [ ] H2 matches: "Ready for Professional {PRIMARY_SERVICE} in {CITY}?"
- [ ] Total ≤ 60 words
- [ ] One bolded key term in value recap
- [ ] Trust micro-copy uses bullet separators (•)
- [ ] No pricing

## GOLDEN EXAMPLE
<!-- Golden example generated from: service_page_example.md -->
<!-- Section 10 — injected by inject_golden_examples.py -->

## Ready for Professional Air Duct Cleaning in Rockford?

**NADCA-certified technicians** with camera documentation on every job, serving Rockford and Winnebago County since 2014.

**Call (815) 555-0142**

Licensed * Insured * Rockford's Trusted Air Duct Cleaning Team

## OUTPUT RULES
- Output ONLY the section content in Markdown
- Start directly with the content — no intro, no "Here is the section:" preamble
- No pricing, no em-dashes (—), no separator lines (---)
- Bold ONE key phrase per paragraph
