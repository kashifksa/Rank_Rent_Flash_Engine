# P7 Blog — Section 01: Post Header + Answer Block
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

## PRE-CHECK (run before writing this section)
Confirm: python scripts/check_blog_cannibalization.py --new-keyword "{POST_KEYWORD}"
returned PASS. If FAIL — do not write. Update keyword in topical_authority.json first.

## SECTION RULES — Post Header (Section 1 of 8)
Word budget: 80-120 words

Write in this order:

1. H1: {POST_TITLE}
   Use EXACTLY as set in topical_authority.json — do NOT rewrite it.

2. IMMEDIATE ANSWER BLOCK (40-60 words, mandatory for Featured Snippet / AI Overview):
   - Directly answer the core question in {POST_KEYWORD}
   - Standalone paragraph — no "In this article..." opener
   - Short sentences, mobile-first

3. AUTHOR ATTRIBUTION LINE (E-E-A-T — 2026 required):
   "By {AUTHOR_NAME} | {AUTHOR_TITLE}"
   Link {AUTHOR_NAME} to About page if live in phase1_registry.json.

SELF-CHECK:
- [ ] H1 matches {POST_TITLE} exactly
- [ ] Immediate answer is 40-60 words, standalone
- [ ] Author attribution line present
- [ ] No "In this article" opener
- [ ] 80-120 words total

## GOLDEN EXAMPLE
<!-- Golden example generated from: blog_page_example.md -->
<!-- Section 01 — injected by inject_golden_examples.py -->

# How to Spot Air Duct Cleaning Scams Before They Waste Your Money

The most reliable way to spot an air duct cleaning scam is to ask for NADCA certification before anyone enters your home. **NADCA-certified technicians** must pass the ASCS examination and use commercial-grade source removal equipment. The low-price coupon operations that dominate Facebook groups have neither. If the company cannot produce a NADCA membership number, treat that as the first red flag.

By the Rockford Air Duct Pros Team | NADCA ASCS Certified, Serving Rockford, IL Since 2014

## OUTPUT RULES
- Output ONLY the section content in Markdown
- Start directly with the content — no intro, no preamble
- No pricing, no em-dashes (—), no separator lines (---)
- Bold ONE key phrase per paragraph
- Short paragraphs: 2-3 sentences max
