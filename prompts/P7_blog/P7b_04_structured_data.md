# P7 Blog — Section 04: Structured Data Element (REQUIRED)
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

## SECTION RULES — Structured Data Element (Section 4 of 8)
Word budget: 60-120 words
MANDATORY — every blog post must have at least one table or structured list

H2: [Quick Reference: choose a title relevant to {POST_KEYWORD}]
Examples: "Quick Reference: Types of [Issue] and What to Do"
          "At a Glance: [Topic] Facts for {CITY} Homeowners"

Choose the format that fits best:

OPTION A — Comparison table:
| [Column 1] | [Column 2] | [Column 3] |
|---|---|---|
| Row 1 | ... | ... |

OPTION B — Numbered process list:
1. **Step one bold title** — brief description
2. **Step two bold title** — brief description

OPTION C — Quick-reference bullet list with bolded facts

Do NOT add pricing columns. No dollar amounts anywhere.
Localize at least one row/item to {CITY} where possible.

SELF-CHECK:
- [ ] Structured element present (table OR numbered list OR bullet list)
- [ ] No pricing in any column or row
- [ ] At least one {CITY} reference in the data
- [ ] 60-120 words

## GOLDEN EXAMPLE
<!-- Golden example generated from: blog_page_example.md -->
<!-- Section 04 — injected by inject_golden_examples.py -->

## Quick Reference: Air Duct Cleaning Scam Warning Signs

Use this table to evaluate any duct cleaning company before you schedule an appointment or let anyone into your home.

| Warning Sign | What It Means | What to Do |
|---|---|---|
| Cannot provide NADCA membership number | Not NADCA certified | Do not schedule |
| Advertises unusually low whole-house pricing | Classic bait-and-switch entry tactic | Get written scope and price before agreeing |
| Claims to find mold without lab test | High-pressure upsell tactic | Ask for laboratory identification; decline on-the-spot treatment |
| Uses only a shop vac or compressed air | Not source removal; does not meet NADCA standard | Decline service |
| Refuses to provide before-and-after camera footage | Cannot verify work was performed | Do not pay until documentation is provided |
| Pressures you to decide immediately | High-pressure sales tactic | Take time; legitimate companies do not pressure immediate decisions |
| No verifiable local reviews or BBB listing | Likely a traveling operation | Search company name plus city; check BBB before booking |

## OUTPUT RULES
- Output ONLY the section content in Markdown
- Start directly with the content — no intro, no preamble
- No pricing, no em-dashes (—), no separator lines (---)
- Bold ONE key phrase per paragraph
- Short paragraphs: 2-3 sentences max
