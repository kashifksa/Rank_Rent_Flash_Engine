# P7 Blog — Section 02: Cause or Context
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

## SECTION RULES — Cause or Context (Section 2 of 8)
Word budget: 150-250 words

H2 (question-based): What Causes [Core Problem Related to {POST_KEYWORD}]?

Answer-first: First sentence directly answers the H2 question.

Write 2-3 short paragraphs (2-3 sentences each).

Include a cause list: 3-5 bullets with bolded cause labels.

Then add ONE H3 for a local/seasonal factor:
H3 formula: "How [Local Condition] in {CITY} Makes [Issue] Worse"

In this H3: embed at least one local entity — city code, regional weather,
local infrastructure, or specific neighborhood.

SELF-CHECK:
- [ ] H2 is a question, answer-first opening
- [ ] 3-5 cause bullets with bolded labels
- [ ] H3 with local/seasonal angle present, includes local entity
- [ ] 150-250 words

## GOLDEN EXAMPLE
<!-- Golden example generated from: blog_page_example.md -->
<!-- Section 02 — injected by inject_golden_examples.py -->

## What Makes Air Duct Cleaning Scams So Common?

Air duct cleaning scams are common because the service is invisible. Homeowners cannot see inside their duct system, which makes it nearly impossible to verify whether any work was actually performed or performed correctly. Unscrupulous operators exploit this information gap.

The economics make it attractive for bad actors. A van, a shop vac, and a door-hanger printer are the only startup costs required for a fraudulent operation. **No license, no certification, and no actual equipment** are needed to collect payment from homeowners who do not know what legitimate duct cleaning looks like.

Several recurring tactics drive the majority of consumer complaints:

- **The whole-house coupon** - advertised at suspiciously low prices in Facebook groups and on door hangers; the low price is a door-opener, not a real quote
- **Fake mold discovery** - technician "finds" black mold without any laboratory testing and upsells a high-margin treatment
- **Scope inflation** - arrives to do one area, then claims the entire system needs cleaning and presents a dramatically higher invoice
- **Unverifiable credentials** - claims NADCA certification or "EPA certification" that does not exist under that name

### How the Rockford, IL Market Creates Extra Risk

**Rockford's buy-sell-trade Facebook groups and Nextdoor communities** surface consumer scam complaints about duct cleaning more frequently than most comparable Midwest markets. The city's large inventory of pre-1985 homes creates a ready pool of homeowners anxious about decades of dust in original galvanized ductwork, which is exactly the customer profile these operations target. Out-of-market vans frequently canvass Winnebago County neighborhoods after home improvement trade shows and spring advertising pushes.

## OUTPUT RULES
- Output ONLY the section content in Markdown
- Start directly with the content — no intro, no preamble
- No pricing, no em-dashes (—), no separator lines (---)
- Bold ONE key phrase per paragraph
- Short paragraphs: 2-3 sentences max
