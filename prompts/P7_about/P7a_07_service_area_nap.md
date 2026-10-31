# P7 About — Section 07: Service Area + NAP
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

## SECTION RULES — Service Area + NAP (Section 7 of 8)
Word budget: 80-120 words (text only)

H2: Serving {CITY} and Surrounding Communities

Write two columns:

LEFT COLUMN — NAP block (must match Google Business Profile VERBATIM):
{COMPANY_NAME}
{ADDRESS}
{PHONE} (click-to-call link)
Hours: [from master_brief]
Service Area: {SERVICE_AREA}
(hyperlink only cities live in phase1_registry.json — plain text otherwise)

RIGHT COLUMN note: "[GOOGLE MAPS IFRAME centered on {ADDRESS}]"

ENTITY TRIANGULATION LINKS (2026 — mandatory):
"Find us on: [Google Business Profile] | [Facebook] | [BBB] | [Yelp]"
Use URLs from {SOCIAL_PROFILES}

SELF-CHECK:
- [ ] H2 = "Serving {CITY} and Surrounding Communities"
- [ ] NAP matches master_brief exactly
- [ ] Map iframe note present
- [ ] Entity triangulation links present with {SOCIAL_PROFILES} URLs
- [ ] 80-120 words

## GOLDEN EXAMPLE
<!-- PASTE YOUR CLAUDE/PRO OUTPUT FOR THIS SECTION HERE -->
<!-- Until filled: Flash will follow the rules above without an example -->

## OUTPUT RULES
- Output ONLY the section content in Markdown
- Start directly with the content — no intro, no preamble
- No pricing, no em-dashes (—), no separator lines (---)
- Bold ONE key phrase per paragraph
- Short paragraphs: 2-3 sentences max
