# P7 Location — Section 05: Local FAQ (MUST BE 100% UNIQUE)
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

## SECTION RULES — Local FAQ (Section 5 of 7)
Word budget: 150-280 words
THIS SECTION MUST BE 100% UNIQUE — questions must be specific to {LOCATION_CITY}

H2: {PRIMARY_SERVICE} FAQs for {LOCATION_CITY} Homeowners

Write 3-5 questions UNIQUE to {LOCATION_CITY}. Format as natural language questions.

REQUIRED question types (must include all three):
1. PERMIT: "Does {LOCATION_CITY} require a permit for {PRIMARY_SERVICE}?"
   Answer: use {LOCAL_PERMIT} if set, otherwise give general guidance.
2. RESPONSE TIME: "How quickly can you reach [Neighborhood] in {LOCATION_CITY}?"
3. LOCAL CONDITION: "How does {LOCAL_CLIMATE} affect {PRIMARY_SERVICE} in {LOCATION_CITY}?"

Per answer: open with direct 1-sentence reply, then elaborate. 40-70 words each.

Do NOT reuse questions from:
- The hub service page FAQ
- Any other location page FAQ

SELF-CHECK:
- [ ] H2 = "{PRIMARY_SERVICE} FAQs for {LOCATION_CITY} Homeowners"
- [ ] 3-5 questions, all unique to {LOCATION_CITY}
- [ ] All 3 required question types present
- [ ] Each answer opens with direct reply
- [ ] 150-280 words

## GOLDEN EXAMPLE
<!-- PASTE YOUR CLAUDE/PRO OUTPUT FOR THIS SECTION HERE -->
<!-- Until filled: Flash will follow the rules above without an example -->

## OUTPUT RULES
- Output ONLY the section content in Markdown
- Start directly with the content — no intro, no preamble
- No pricing, no em-dashes (—), no separator lines (---)
- Bold ONE key phrase per paragraph
- Short paragraphs: 2-3 sentences max
