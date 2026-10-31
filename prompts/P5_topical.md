# P5 — Generate topical_authority.json
# Flash Engine | Output: topical_authority.json
# Read master_brief.json before running this prompt

## TASK
Using master_brief.json, generate the complete topical authority map.
This file defines every page to be built, in priority order.

## INPUT REQUIRED
Paste before submitting:
=== MASTER_BRIEF.JSON ===
[paste full master_brief.json here]

## RULES
- Phase 1: homepage + primary service page + about + contact + primary city location page
- Phase 2: secondary service pages
- Phase 3: expansion city location pages (one per expansion_cities entry)
- Phase 4: comparison, how-to, problem, glossary pages
- Phase 5: blog posts (informational intent ONLY — how to, signs of, guide to, what is)
- Blog post keywords must NOT overlap with service or location page keywords
- No two blog posts may share the same intent angle

## OUTPUT FORMAT
Output ONLY valid JSON. No markdown fences, no explanation.

{
  "pages": [
    {
      "page_id": "unique-slug",
      "page_type": "service | location | blog | about | contact | homepage",
      "phase": 1,
      "priority": 1,
      "target_keyword": "",
      "h1_title": "",
      "parent_service": "",
      "city": "",
      "status": "planned"
    }
  ]
}

## SELF-CHECK before outputting
- [ ] Phase 1 contains: homepage, primary service, about, contact, primary location
- [ ] All blog post keywords are informational intent (how to / signs of / guide to)
- [ ] No blog keyword overlaps with any service or location page keyword
- [ ] Output is valid JSON
