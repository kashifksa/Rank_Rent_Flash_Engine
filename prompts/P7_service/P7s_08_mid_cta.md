# P7 Service — Section 08: Mid CTA
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

## SECTION RULES — Mid CTA (Section 8 of 10)
Word budget: 30-50 words

H2: Get Your Free {PRIMARY_SERVICE} Estimate in {CITY}

Write:
1. Urgency statement (20-30 words): Reference {LOCAL_CHALLENGE} naturally.
   No pricing. No "limited time" clichés.

2. CTA button text: "Call {PHONE}"

3. Form note: "[SHORT CONTACT FORM — Name, Phone, Message]"

SELF-CHECK before outputting:
- [ ] H2 matches: "Get Your Free {PRIMARY_SERVICE} Estimate in {CITY}"
- [ ] No pricing or dollar amounts
- [ ] {LOCAL_CHALLENGE} referenced in urgency statement
- [ ] Total 30-50 words (button and form note excluded from count)

## GOLDEN EXAMPLE
<!-- Golden example generated from: service_page_example.md -->
<!-- Section 08 — injected by inject_golden_examples.py -->

## Get Your Free Air Duct Cleaning Estimate in Rockford

**Rockford's sub-zero winters** push forced-air systems to run continuously from October through April, accelerating allergen and debris buildup inside ductwork that compounds year after year in older homes.

**Call (815) 555-0142**

[SHORT CONTACT FORM - Name, Phone, Message]

## OUTPUT RULES
- Output ONLY the section content in Markdown
- Start directly with the content — no intro, no "Here is the section:" preamble
- No pricing, no em-dashes (—), no separator lines (---)
- Bold ONE key phrase per paragraph
