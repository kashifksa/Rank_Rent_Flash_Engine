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
<!-- PASTE YOUR CLAUDE/PRO OUTPUT FOR THIS SECTION HERE -->
<!-- Until filled: Flash will follow the rules above without an example -->
<!-- Priority: fill this before Nov 2 while Claude access is available -->

## OUTPUT RULES
- Output ONLY the section content in Markdown
- Start directly with the content — no intro, no "Here is the section:" preamble
- No pricing, no em-dashes (—), no separator lines (---)
- Bold ONE key phrase per paragraph
