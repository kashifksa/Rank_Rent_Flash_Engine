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
<!-- PASTE YOUR CLAUDE/PRO OUTPUT FOR THIS SECTION HERE -->
<!-- Until filled: Flash will follow the rules above without an example -->
<!-- Priority: fill this before Nov 2 while Claude access is available -->

## OUTPUT RULES
- Output ONLY the section content in Markdown
- Start directly with the content — no intro, no "Here is the section:" preamble
- No pricing, no em-dashes (—), no separator lines (---)
- Bold ONE key phrase per paragraph
