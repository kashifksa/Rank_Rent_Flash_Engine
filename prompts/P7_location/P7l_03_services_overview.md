# P7 Location — Section 03: Services Overview
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

## SECTION RULES — Services Overview (Section 3 of 7)
Word budget: 120-200 words

H2: Our {PRIMARY_SERVICE} Services in {LOCATION_CITY}

Answer-first: First sentence states what services are available in {LOCATION_CITY}.

Write 2-4 service cards:
### [Sub-service Name]
[30-50 word description mentioning {LOCATION_CITY}]
Bold the key term.

Section parity: all card descriptions within ±2% word count.

End with: "See our full {PRIMARY_SERVICE} services →" [link to hub service page]
(Only link if hub service page is live in phase1_registry.json)

SELF-CHECK:
- [ ] H2 = "Our {PRIMARY_SERVICE} Services in {LOCATION_CITY}"
- [ ] 2-4 cards, all mention {LOCATION_CITY}
- [ ] Card descriptions within ±2% word count
- [ ] Internal link to hub service page (if live)
- [ ] 120-200 words

## GOLDEN EXAMPLE
<!-- Golden example generated from: location_page_example.md -->
<!-- Section 03 — injected by inject_golden_examples.py -->

## Our Air Duct Cleaning Services in Loves Park

Loves Park homeowners have access to the full range of residential air duct cleaning services that Rockford Air Duct Pros provides across Winnebago County.

### Residential Duct Cleaning

**Full residential duct cleaning in Loves Park** covers every supply register, return air boot, main trunk line, and plenum using the NADCA source removal method. Our technicians arrive with commercial-grade negative air equipment sized for the duct configurations typical of Loves Park's mid-century split-levels and ranch homes.

### Dryer Vent Cleaning

**Dryer vent lint removal** is recommended annually for Loves Park homes with dryer vent runs exceeding 15 feet or routed through exterior walls with multiple bends. Long vent runs are common in Loves Park's ranch-style floor plans and represent a genuine fire risk when clogged with compacted lint.

### Video Camera Inspection

**Before-and-after camera documentation** is included on every job in Loves Park. Our technicians pass a flexible camera through your supply and return trunks prior to cleaning and again after completion, giving you verifiable proof of what the service achieved inside the ductwork you cannot see.

### Sanitization Treatment

**Post-cleaning antimicrobial fogging** applies an EPA-registered agent to duct surfaces after mechanical cleaning. This service is recommended for Loves Park homes with documented moisture in basement plenums or for households where occupants have respiratory sensitivities.

## OUTPUT RULES
- Output ONLY the section content in Markdown
- Start directly with the content — no intro, no preamble
- No pricing, no em-dashes (—), no separator lines (---)
- Bold ONE key phrase per paragraph
- Short paragraphs: 2-3 sentences max
