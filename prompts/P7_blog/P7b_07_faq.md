# P7 Blog — Section 07: FAQ
# Flash Engine — Blog Post | Atomic Mini-Prompt
# Model: Gemini Flash 3.8
# Write ONLY this section. Nothing else.

## VARIABLES — fill ALL before submitting
POST_TITLE       = [fill in — exact title from topical_authority.json, do not rewrite]
POST_KEYWORD     = [fill in — primary informational keyword]
CITY             = [fill in]
STATE            = [fill in]
PRIMARY_SERVICE  = [fill in — parent service this post supports]
PHONE            = [fill in]
RELATED_SERVICE_PAGE = [fill in — slug of live service page from phase1_registry.json]
AUTHOR_NAME      = [fill in — from master_brief.json]
AUTHOR_TITLE     = [fill in — e.g. "Master Roofer, 15 years serving Austin"]

## SECTION RULES — FAQ (Section 7 of 8)
Word budget: 150-350 words

H2: Frequently Asked Questions About [Topic of {POST_KEYWORD}] in {CITY}

Write 3-5 questions in natural language format (voice search + AI Overview).

Required question types — include at least one of each:
- LONG-TAIL: variation of {POST_KEYWORD}
- LOCAL REGULATORY: "Do I need a permit for [action] in {CITY}?" (high AI value)
- PROCESS/TIMELINE: framed without pricing
- VOICE SEARCH: "Can I..." or "Should I..." or "Is it safe to..."

Per answer:
- Open with direct 1-sentence reply (answer-first)
- Then elaborate: 40-80 words total
- No pricing — "Contact us for a free estimate" for cost questions

IMPORTANT: Do NOT repeat questions already in {RELATED_SERVICE_PAGE} FAQ.
Check the service page FAQ before writing.

SELF-CHECK:
- [ ] H2 mentions topic and {CITY}
- [ ] 3-5 questions, all natural language format
- [ ] Local regulatory question included
- [ ] Each answer opens with direct reply
- [ ] No pricing
- [ ] No duplicate questions from service page FAQ
- [ ] 150-350 words

## GOLDEN EXAMPLE
<!-- PASTE YOUR CLAUDE/PRO OUTPUT FOR THIS SECTION HERE -->
<!-- Until filled: Flash will follow the rules above without an example -->

## OUTPUT RULES
- Output ONLY the section content in Markdown
- Start directly with the content — no intro, no preamble
- No pricing, no em-dashes (—), no separator lines (---)
- Bold ONE key phrase per paragraph
- Short paragraphs: 2-3 sentences max
