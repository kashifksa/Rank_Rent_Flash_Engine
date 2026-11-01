# P7 Service — Section 06: Local Proof
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

## SECTION RULES — Local Proof (Section 6 of 10)
Word budget: 130-170 words

H2: What {CITY} Customers Say About Our {PRIMARY_SERVICE}

Write 2-3 review excerpts. Each review MUST reference {CITY} or a specific
neighborhood in {CITY} — this is required for AI citation / GEO validation.

Format per review:
> "[30-50 word quote that mentions {CITY} or a specific neighborhood]"
> — [First name], [Neighborhood], {CITY}

Then add 1 stats sentence (20-30 words):
"Our team has completed [number]+ {PRIMARY_SERVICE} projects across {CITY}
with an average [X.X]★ rating."

IMPORTANT:
- Quotes must sound real and natural — not marketing speak
- Location-rich language in quotes: "right here in [neighborhood]" or
  "in our [neighborhood] home" — AI engines use this to validate local authority
- CSS text stars only — note "★★★★★" in text, never render star images

SELF-CHECK before outputting:
- [ ] H2 matches: "What {CITY} Customers Say About Our {PRIMARY_SERVICE}"
- [ ] 2-3 reviews written, each names {CITY} or a neighborhood
- [ ] Stats sentence included
- [ ] Total 130-170 words

## GOLDEN EXAMPLE
<!-- Golden example generated from: service_page_example.md -->
<!-- Section 06 — injected by inject_golden_examples.py -->

## What Rockford Customers Say About Our Air Duct Cleaning

> "We moved into a 1968 ranch on the Rolling Green side of Rockford and the ducts had clearly never been touched. The before-and-after camera footage was shocking. The team was thorough, professional, and done in under three hours. **Best home improvement decision** we made that year."
> -- Karen M., Rolling Green, Rockford
> *****

> "I was skeptical after getting burned by a low-price coupon outfit last winter. These technicians actually showed me the camera footage before they started and explained every step. My wife has asthma and she noticed a difference within a week. **Completely different experience** from the bait-and-switch outfits."
> -- Dave T., Edgewater, Rockford
> *****

> "Our HVAC contractor recommended them after finding heavy debris in our plenum during a tune-up. They cleaned the full trunk line system in our 1972 home in Highland Park. Detailed, professional, and they actually cleaned up after themselves. **Highly recommend for any older Rockford home.**"
> -- Sandra W., Highland Park, Rockford
> *****

Our team has completed 400+ residential air duct cleaning projects across Rockford and Winnebago County with an average 4.9-star rating from verified customers.

## OUTPUT RULES
- Output ONLY the section content in Markdown
- Start directly with the content — no intro, no "Here is the section:" preamble
- No pricing, no em-dashes (—), no separator lines (---)
- Bold ONE key phrase per paragraph
