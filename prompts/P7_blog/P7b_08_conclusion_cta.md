# P7 Blog — Section 08: Conclusion CTA
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

## SECTION RULES — Conclusion CTA (Section 8 of 8)
Word budget: 60-100 words

H2: Get Expert {PRIMARY_SERVICE} Help in {CITY}

Write:
1. Key takeaway (25-40 words): 1-2 sentences summarizing the post's main point.
   Bold the most important term.
2. Low-friction local CTA: "If you're dealing with [issue] in the greater
   {CITY} area..." + action statement.
3. Click-to-call: {PHONE} (formatted as clickable link)
4. 2 related links (blog post or service page — live in phase1_registry.json only)

SELF-CHECK:
- [ ] H2 = "Get Expert {PRIMARY_SERVICE} Help in {CITY}"
- [ ] Key takeaway 25-40 words
- [ ] {CITY} mentioned in CTA
- [ ] Phone link formatted correctly
- [ ] 2 internal links, both confirmed live
- [ ] 60-100 words

## GOLDEN EXAMPLE
<!-- Golden example generated from: blog_page_example.md -->
<!-- Section 08 — injected by inject_golden_examples.py -->

## Get Expert Air Duct Cleaning Help in Rockford

Spotting a scam is the first step. Finding a verified, trustworthy alternative is the second. If you are in the greater Rockford area and want NADCA-certified service with camera documentation on every job, our team is available for scheduling throughout Winnebago County.

**Call (815) 555-0142** to speak directly with our team and verify credentials before any appointment is made.

Related reading: What Is NADCA Certification and Why Does It Matter for Duct Cleaning | How Often Should You Clean Air Ducts

## OUTPUT RULES
- Output ONLY the section content in Markdown
- Start directly with the content — no intro, no preamble
- No pricing, no em-dashes (—), no separator lines (---)
- Bold ONE key phrase per paragraph
- Short paragraphs: 2-3 sentences max
