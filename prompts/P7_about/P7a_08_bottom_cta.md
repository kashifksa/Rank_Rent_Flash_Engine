# P7 About — Section 08: Bottom CTA
# Flash Engine — About Page | Atomic Mini-Prompt
# Model: Gemini Flash 3.8
# Write ONLY this section. Nothing else.

## VARIABLES — fill ALL before submitting
COMPANY_NAME     = [fill in]
CITY             = [fill in]
STATE            = [fill in]
PHONE            = [fill in]
ADDRESS          = [fill in — full address from NAP]
FOUNDED_YEAR     = [fill in]
PRIMARY_SERVICE  = [fill in]
SERVICE_AREA     = [fill in — list of cities served]
CREDENTIALS      = [fill in — licenses, certs from master_brief.json]
COMMUNITY_TIES   = [fill in — memberships, sponsorships]
SOCIAL_PROFILES  = [fill in — GBP URL, Facebook, BBB, Yelp]

## SECTION RULES — Bottom CTA (Section 8 of 8)
Word budget: ≤60 words HARD LIMIT

H2: Ready to Work with {CITY}'s Trusted {PRIMARY_SERVICE} Team?

Write:
1. Trust recap + action statement (25-40 words). Bold the key term.
2. CTA: "Call {PHONE}"
3. Form note: "[CONTACT FORM — Name, Phone, Message]"
4. Trust micro-copy: "Licensed • Insured • Proudly Serving {CITY} Since {FOUNDED_YEAR}"

SELF-CHECK:
- [ ] H2 = "Ready to Work with {CITY}'s Trusted {PRIMARY_SERVICE} Team?"
- [ ] Total ≤ 60 words
- [ ] Trust micro-copy uses bullet separators (•)
- [ ] No pricing

## GOLDEN EXAMPLE
<!-- Golden example generated from: about_page_example.md -->
<!-- Section 08 — injected by inject_golden_examples.py -->

## Ready to Schedule? We Are Ready to Help.

**Rockford Air Duct Pros** is available for scheduling throughout Winnebago County. Call us directly to speak with our team, verify our credentials, and book your appointment without going through an online form.

**Call (815) 555-0142**

Licensed * Insured * NADCA Certified * Serving Rockford, IL Since 2014

## OUTPUT RULES
- Output ONLY the section content in Markdown
- Start directly with the content — no intro, no preamble
- No pricing, no em-dashes (—), no separator lines (---)
- Bold ONE key phrase per paragraph
- Short paragraphs: 2-3 sentences max
