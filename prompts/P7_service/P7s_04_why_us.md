# P7 Service — Section 04: Why Choose Us
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

## SECTION RULES — Why Choose Us (Section 4 of 10)
Word budget: 120-180 words

H2: Why {CITY} Homeowners Choose Us for {PRIMARY_SERVICE}

First sentence (answer-first rule): State the core differentiator in 1-2 sentences.

Then 4-6 bullet points with icons:
**[Bold Label 3-5 words]** — one sentence explanation (15-25 words)

Requirements:
- At least 2 bullets must reference LOCAL advantages:
  response time to {CITY}, local knowledge of {LOCAL_CHALLENGE},
  community ties, neighborhood familiarity
- Mention {CITY} at least once in the body text
- Each bullet explanation: 15-25 words exactly

SELF-CHECK before outputting:
- [ ] H2 matches exactly: "Why {CITY} Homeowners Choose Us for {PRIMARY_SERVICE}"
- [ ] Answer-first: first sentence states the differentiator
- [ ] 4-6 bullets written
- [ ] At least 2 bullets reference local advantages with {CITY} name
- [ ] Each bullet label is bolded
- [ ] Total 120-180 words

## GOLDEN EXAMPLE
<!-- Golden example generated from: service_page_example.md -->
<!-- Section 04 — injected by inject_golden_examples.py -->

## Why Rockford Homeowners Choose Us for Air Duct Cleaning

We are the only dedicated air duct cleaning company in the Rockford area with NADCA certification, EPA Lead-Safe credentials, and a documented before-and-after camera inspection on every job.

- **NADCA Certified Technicians** - Our team holds active ASCS certification from the National Air Duct Cleaners Association, the industry's highest credential standard.
- **Camera Documentation on Every Job** - You receive photographic proof of conditions before and after cleaning, not just a verbal assurance that the work was done.
- **Trained for Rockford's Older Homes** - We know pre-1985 galvanized sheet metal ductwork. Our equipment reaches trunk lines and plenums that consumer-grade shop vacs cannot access.
- **Rockford-Based Response Time** - Our team operates out of the Rockford area and can schedule residential appointments within Winnebago County without the dispatch delays of out-of-market contractors.
- **No Bait-and-Switch Tactics** - We do not advertise low-price coupons and upsell on arrival. Every scope of work is documented before we begin.
- **BBB Accredited, A+ Rated** - Our standing with the Better Business Bureau reflects a zero-complaint record since our founding in 2014.

## OUTPUT RULES
- Output ONLY the section content in Markdown
- Start directly with the content — no intro, no "Here is the section:" preamble
- No pricing, no em-dashes (—), no separator lines (---)
- Bold ONE key phrase per paragraph
