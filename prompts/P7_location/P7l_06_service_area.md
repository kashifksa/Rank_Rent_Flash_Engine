# P7 Location — Section 06: Service Area Detail
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

## SECTION RULES — Service Area Detail (Section 6 of 7)
Word budget: 60-100 words (text only, map is separate)

H2: Areas We Serve in and Around {LOCATION_CITY}

Write:
"Our team covers {LOCATION_CITY} and these surrounding neighborhoods:"

Bulleted list: neighborhoods and zip codes from {LOCAL_NEIGHBORHOODS}

1 sentence for adjacent towns (plain text, no hyperlink unless live in phase1_registry.json)

Note: "[GOOGLE MAPS IFRAME centered on {LOCATION_CITY} — no AI map image]"

SELF-CHECK:
- [ ] H2 = "Areas We Serve in and Around {LOCATION_CITY}"
- [ ] Neighborhood bullet list present
- [ ] Map iframe note included
- [ ] Adjacent towns: plain text if not live
- [ ] 60-100 words

## GOLDEN EXAMPLE
<!-- Golden example generated from: location_page_example.md -->
<!-- Section 06 — injected by inject_golden_examples.py -->

## Areas We Serve in and Around Loves Park

Our team covers all of Loves Park and adjacent communities within the North Rockford corridor, serving residential properties throughout this area without additional travel fees.

Our air duct cleaning team covers Loves Park and the following neighborhoods and zip codes:

- North Loves Park residential corridor
- Colonial Village
- Machesney Park Road area
- Loves Park zip code: 61111
- Adjacent North Rockford zip codes: 61115, 61114

We also serve homeowners in Machesney Park, Roscoe, and Rockton. Scheduling for adjacent communities may vary by day of week.

[GOOGLE MAPS IFRAME - do not generate AI map image]

## OUTPUT RULES
- Output ONLY the section content in Markdown
- Start directly with the content — no intro, no preamble
- No pricing, no em-dashes (—), no separator lines (---)
- Bold ONE key phrase per paragraph
- Short paragraphs: 2-3 sentences max
