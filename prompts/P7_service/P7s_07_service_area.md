# P7 Service — Section 07: Service Area
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

## SECTION RULES — Service Area (Section 7 of 10)
Word budget: 80-150 words (text only, map is separate)

H2: Proudly Serving {CITY} and Surrounding Areas

First sentence (answer-first): State the service radius in one sentence.

Then write:
"Our {PRIMARY_SERVICE} team covers {CITY} and the following
neighborhoods and communities:"

Bulleted list of neighborhoods and zip codes
(use neighborhoods from master_brief.json)

Then 1-2 sentences for expansion cities:
- If expansion city is live in phase1_registry.json → hyperlink it
- If NOT live → plain text only (no hyperlink)

Note at end: "[GOOGLE MAPS IFRAME — do not generate AI map image]"

SELF-CHECK before outputting:
- [ ] H2 matches: "Proudly Serving {CITY} and Surrounding Areas"
- [ ] Answer-first opening sentence states radius
- [ ] Neighborhood bullet list present
- [ ] Map iframe note included (not an actual image)
- [ ] Deferred city links are plain text only
- [ ] Total 80-150 words

## GOLDEN EXAMPLE
<!-- Golden example generated from: service_page_example.md -->
<!-- Section 07 — injected by inject_golden_examples.py -->

## Proudly Serving Rockford and Surrounding Areas

Our air duct cleaning team covers the full Rockford metro area and surrounding Winnebago County communities within approximately 30 miles of our service center at 1111 S Alpine Rd.

Our residential air duct cleaning team covers Rockford and the following neighborhoods and communities:

- Churchill's Grove
- Edgewater
- Rolling Green
- Highland Park
- Signal Hill
- Midtown
- Zip codes: 61101, 61102, 61103, 61104, 61107, 61108, 61109, 61114, 61115

We also serve homeowners in Loves Park, Machesney Park, Belvidere, Roscoe, Rockton, Cherry Valley, Winnebago, and Pecatonica. Scheduling availability in outlying communities may vary by day of week.

[GOOGLE MAPS IFRAME - do not generate AI map image]

## OUTPUT RULES
- Output ONLY the section content in Markdown
- Start directly with the content — no intro, no "Here is the section:" preamble
- No pricing, no em-dashes (—), no separator lines (---)
- Bold ONE key phrase per paragraph
