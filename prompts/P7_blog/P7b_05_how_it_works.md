# P7 Blog — Section 05: How It Works (Bridge Section)
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

## SECTION RULES — How It Works (Section 5 of 8)
Word budget: 150-200 words

H2 (question-based): How Does Professional [Service/Process] Work?

Answer-first: First sentence states what the professional process involves.

Write 3-5 numbered steps. Bold each step title.

INTERNAL LINK PLACEMENT (mandatory):
Add 1 contextual link to {RELATED_SERVICE_PAGE} within this section.
Example: "Our [service name] team starts with..." linked to the service page.
Only link if {RELATED_SERVICE_PAGE} is live in phase1_registry.json.
If not live — plain text, log in pending_links.json.

Educational framing — not a sales pitch. This bridges informational → commercial.

SELF-CHECK:
- [ ] H2 is question-based: "How Does Professional..."
- [ ] Answer-first opening
- [ ] 3-5 steps, all bolded titles
- [ ] Internal link to {RELATED_SERVICE_PAGE} present (or deferred)
- [ ] No sales pitch tone
- [ ] 150-200 words

## GOLDEN EXAMPLE
<!-- PASTE YOUR CLAUDE/PRO OUTPUT FOR THIS SECTION HERE -->
<!-- Until filled: Flash will follow the rules above without an example -->

## OUTPUT RULES
- Output ONLY the section content in Markdown
- Start directly with the content — no intro, no preamble
- No pricing, no em-dashes (—), no separator lines (---)
- Bold ONE key phrase per paragraph
- Short paragraphs: 2-3 sentences max
