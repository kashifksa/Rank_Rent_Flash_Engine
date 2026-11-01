# P7 Blog — Section 06: Local Considerations
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

## SECTION RULES — Local Considerations (Section 6 of 8)
Word budget: 120-180 words

H2 (question-based): What Should {CITY} Homeowners Know About [Topic]?

Answer-first: First sentence states the most important local consideration.

Write 2-3 paragraphs (2-3 sentences each):
- Reference at least one: local building code, regional climate,
  municipal rule, local geography, utility company, or city ordinance
- Bold the most important local fact in each paragraph
- Mention {CITY} naturally — 1-2 times per paragraph max
- Example: "**{CITY}'s [local condition]** means [specific implication]"

Do NOT stuff the city name. Natural mentions only.

SELF-CHECK:
- [ ] H2 is question-based: "What Should {CITY} Homeowners Know..."
- [ ] Answer-first opening
- [ ] At least 1 local entity embedded (code, climate, utility, ordinance)
- [ ] Bold key local fact per paragraph
- [ ] City name: 1-2 mentions per paragraph max
- [ ] 120-180 words

## GOLDEN EXAMPLE
<!-- Golden example generated from: blog_page_example.md -->
<!-- Section 06 — injected by inject_golden_examples.py -->

## What Should Rockford Homeowners Know About Duct Cleaning Scams?

**Rockford's older housing stock makes local homeowners a more frequent target** than homeowners in newer construction markets. A 1960s or 1970s ranch home with original galvanized supply trunks is genuinely overdue for cleaning in many cases, and homeowners in these homes are more likely to respond to low-price advertising because they know the concern is real.

Winnebago County has no specific consumer protection ordinance targeting duct cleaning fraud, so the practical recourse after being scammed is limited to filing a complaint with the Illinois Attorney General's Consumer Protection Division and disputing the charge with your credit card company if you paid by card. **Paying by credit card** is your best protection against bait-and-switch billing because it gives you a chargeback path.

The Illinois EPA does not regulate duct cleaning companies, and there is no state licensing requirement for residential HVAC duct cleaning technicians in Illinois. This means **NADCA certification is the only meaningful third-party credential** that verifies training and equipment standards. Verify NADCA membership at nadca.com before any technician arrives.

## OUTPUT RULES
- Output ONLY the section content in Markdown
- Start directly with the content — no intro, no preamble
- No pricing, no em-dashes (—), no separator lines (---)
- Bold ONE key phrase per paragraph
- Short paragraphs: 2-3 sentences max
